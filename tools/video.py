#!/usr/bin/env python3
"""Local review helpers. No network requests; never overwrites an output."""
import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def probe(source):
    raw = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(source)]))
    # Deliberately omit original filename, location tags and arbitrary metadata.
    streams = [{k: s[k] for k in ('codec_type','codec_name','width','height','r_frame_rate','avg_frame_rate','duration','color_transfer','color_space','color_primaries','sample_aspect_ratio','sample_rate','channels') if k in s} | {'rotation': next((x.get('rotation', 0) for x in s.get('side_data_list', []) if 'rotation' in x), 0)} for s in raw['streams']]
    return {'duration': float(raw['format']['duration']), 'streams': streams}


def number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def plan_load(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or not isinstance(data.get('source'), str):
        raise ValueError('Plan needs source and segments.')
    source = (path.parent / data['source']).resolve()
    if not source.is_file():
        raise ValueError('Source file is missing.')
    info = probe(source)
    segments = data.get('segments')
    if not isinstance(segments, list) or not 1 <= len(segments) <= 100:
        raise ValueError('Use 1-100 segments in playback order.')
    spans = []
    for s in segments:
        if not isinstance(s, dict) or not number(s.get('start')) or not number(s.get('end')):
            raise ValueError('Every range needs finite numeric start/end seconds.')
        if not 0 <= s['start'] < s['end'] <= info['duration'] + 0.001:
            raise ValueError('Range is reversed, empty or outside the source.')
        spans.append((s['start'], s['end']))
    return source, info, spans


def new_output(path, source=None):
    if path.exists() or (source and path.resolve() == source.resolve()):
        raise ValueError('Output exists or is the source. Choose a new filename.')
    path.parent.mkdir(parents=True, exist_ok=True)


def rough_cut(plan, output):
    source, info, spans = plan_load(plan)
    video = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    audio = any(s['codec_type'] == 'audio' for s in info['streams'])
    if not video or not audio:
        raise ValueError('Rough cut requires a video and an audio stream.')
    if video.get('color_transfer') != 'bt709' or video.get('color_primaries') != 'bt709':
        raise ValueError('Requires reviewed SDR BT.709 source. Convert HDR/unknown color properly first; do not relabel metadata.')
    if video.get('sample_aspect_ratio', '1:1') not in ('1:1', 'N/A'):
        raise ValueError('Convert non-square-pixel footage to square pixels before using this helper.')
    new_output(output, source)
    filters, labels = [], []
    for i, (start,end) in enumerate(spans):
        filters += [f'[0:v:0]trim=start={start}:end={end},setpts=PTS-STARTPTS,fps=30,setsar=1[v{i}]', f'[0:a:0]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,aresample=48000[a{i}]']
        labels += [f'[v{i}][a{i}]']
    filters.append(''.join(labels)+f'concat=n={len(spans)}:v=1:a=1[v][a]')
    cmd = ['ffmpeg','-v','error','-n','-i',str(source),'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-map_metadata','-1','-c:v','libx264','-x264-params','colorprim=bt709:transfer=bt709:colormatrix=bt709','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)]
    run(cmd)
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    result = probe(output)
    expected = sum(end-start for start,end in spans)
    if abs(result['duration'] - expected) > max(.2, len(spans)/30+.05):
        raise ValueError('Output duration mismatch. Inspect the intermediate; do not use as final.')
    return {'status':'review intermediate only','expected_duration':expected,'actual_duration':result['duration'],'segments':len(spans)}


def remap(plan, words_path, output):
    _, info, spans = plan_load(plan)
    words = json.loads(words_path.read_text())
    if not isinstance(words,list):
        raise ValueError('Word data must be a list.')
    previous = -1
    for w in words:
        if not isinstance(w,dict) or not isinstance(w.get('text'),str) or not number(w.get('start')) or not number(w.get('end')) or not 0 <= w['start'] < w['end'] <= info['duration']+.001 or w['start'] < previous:
            raise ValueError('Invalid or unordered word timestamps.')
        previous = w['start']
    result, offset = [], 0.0
    for start,end in spans:
        for w in words:
            if w['end'] <= start or w['start'] >= end:
                continue
            if w['start'] < start-.001 or w['end'] > end+.001:
                raise ValueError('A cut crosses a spoken word. Move the cut to a clean boundary.')
            result.append({'start':round(offset+w['start']-start,4),'end':round(offset+w['end']-start,4),'text':w['text']})
        offset += end-start
    new_output(output)
    output.write_text(json.dumps(result, indent=2)+'\n')
    return {'words':len(result),'duration':offset}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    p=sub.add_parser('probe');p.add_argument('source',type=Path)
    p=sub.add_parser('validate');p.add_argument('plan',type=Path)
    p=sub.add_parser('rough-cut');p.add_argument('plan',type=Path);p.add_argument('output',type=Path)
    p=sub.add_parser('remap');p.add_argument('plan',type=Path);p.add_argument('words',type=Path);p.add_argument('output',type=Path)
    a=parser.parse_args()
    if a.command=='doctor':
        result={'python_ok':sys.version_info >= (3,10), 'ffmpeg':bool(shutil.which('ffmpeg')), 'ffprobe':bool(shutil.which('ffprobe')), 'note':'Transcriber, coding agent and HyperFrames must be checked separately.'}
    elif a.command=='probe': result=probe(a.source)
    elif a.command=='validate':
        _,_,spans=plan_load(a.plan);result={'valid':True,'segments':len(spans),'duration':sum(e-s for s,e in spans)}
    elif a.command=='rough-cut': result=rough_cut(a.plan,a.output)
    else: result=remap(a.plan,a.words,a.output)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try: main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as e:
        # Avoid echoing media metadata or a subprocess's possibly private stderr.
        print('Error: '+(str(e) if not isinstance(e,subprocess.CalledProcessError) else 'Media tool failed. Check the source and installed codecs locally.'),file=sys.stderr)
        sys.exit(1)
