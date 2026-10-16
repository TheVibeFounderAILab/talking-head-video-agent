# Setup

Open the unzipped folder in a coding agent that can read files and run local
commands. A chat-only browser session cannot run the bundled helpers by itself.

## Ask the agent to check first
Run `python3 tools/video.py doctor` (Windows: `py -3 tools/video.py doctor`).
The helpers need Python 3.10+ and FFmpeg/ffprobe on PATH. They use only Python's
standard library. Official installation links:
- https://www.python.org/downloads/
- https://ffmpeg.org/download.html

HyperFrames supplies the editable composition, preview and final renderer.
Use an already installed plugin when available. Otherwise follow
https://hyperframes.heygen.com/quickstart and install the official skills from
https://github.com/heygen-com/hyperframes. The documented standalone command is
`npx skills add heygen-com/hyperframes`; choose Core Skills and restart your agent.
Node.js LTS: https://nodejs.org/en/download
Do not run installations silently or copy account settings from another computer.

## Transcription
Use an existing local word-timestamp transcriber. The kit does not bundle a
speech model or claim transcription works without one. Examples include
whisper.cpp or faster-whisper; ask the agent to check your machine before
installing. Hosted transcription is optional and requires your approval.
Convert output into the JSON schema shown in templates/words.example.json.

## Local helper commands
```sh
python3 tools/video.py probe input/clip.mp4
python3 tools/video.py validate work/plan.json
python3 tools/video.py rough-cut work/plan.json work/rough-cut.mp4
python3 tools/video.py remap work/plan.json work/words.json work/cut-words.json
```
Plan paths resolve relative to the plan file. Inspect templates/plan.example.json.
The rough-cut helper produces a review intermediate only. It does not crop,
add captions, normalize loudness or produce a final posting package. It accepts
SDR BT.709 video with audio and rejects HDR/unknown color for a reviewed conversion.
Convert/review other inputs first; do not merely relabel their color metadata.
Existing outputs are never overwritten. Subprocesses use argument lists, not a shell.

## First run
Use a short clip. Approve the story, watch the preview with sound, then approve
export. If a tool cannot run, ask the agent to state the missing dependency,
what is already complete and the exact next step. No guaranteed editing time.
