# Talking Head Video Agent

By [TheVibeFounder](https://github.com/thevibefounder).

[Download the latest ZIP](https://github.com/thevibefounder/talking-head-video-agent/releases/latest/download/talking-head-video-agent.zip)
· [Release notes](https://github.com/thevibefounder/talking-head-video-agent/releases)
· [Chicago workshop](https://thevibefounder.com/chicago/ai-forge/)

Chicago workshop edition · v1.0.1

Turn your own recorded take into a reviewed vertical edit, a post caption,
and three distinct hook tests. This is an agent workspace: instructions,
templates and local helpers for a coding agent. It is not a standalone app
or a promise of one-click editing.

## Start here
1. Unzip this folder and open it as a project in Codex or Claude Code.
2. Put one clip you own in `input/`. A short, clear recording is best for a first run.
3. Paste the contents of `START-HERE.txt` into the agent.
4. Review the proposed story and preview. Give timestamped corrections.
5. Approve the edit before final export. Check the three hook versions yourself.

The agent reads `AGENTS.md` (also pointed to by `CLAUDE.md`). If your tool
ignores these files, explicitly ask it to read them. Setup is in `SETUP.md`.
No footage, transcript, account login or API key is included.

## What you receive
- An exact source transcript, edit plan and editable project.
- A review preview with captions and your natural voice.
- After approval: three hook variants, a post caption, hooks.md and QA notes.
- A record of what you learned, so your own future edits improve.

The bundled Python helper inspects footage, validates edit ranges, builds a
rough cut and remaps word timestamps. Final captioned composition and export
are driven by your coding agent with HyperFrames. Transcription needs a local
transcriber or a provider you separately approve. A coding-agent subscription
and optional provider charges are your own.

## Workshop links
- Resources and downloads: https://thevibefounder.com/chicago/ai-forge/
- Nine-slide walkthrough: https://thevibefounder.com/chicago/ai-forge/talking-head-how-to.html
- HyperFrames setup: https://hyperframes.heygen.com/quickstart
- FFmpeg: https://ffmpeg.org/download.html
- Python: https://www.python.org/downloads/

## Working folders
`input/` keeps originals. `work/` holds transcripts, plans, previews and rough
cuts. `final/` is only for approved deliverables. Start from `templates/`.
Never overwrite the original clip.

## Caption edition
This portable edition uses the bundled open-source Anton font. It preserves
the single-word, uppercase, white, centered caption approach, but is not the
private workspace's exact custom-font preset. See `caption-style/README.md`.

## Privacy
Local helper scripts make no network requests. Your coding agent may send
prompts, transcript text or media to its provider. Use material you are allowed
to share and check your provider settings. Never paste secrets into the agent
or the project. See `PRIVACY.md` before sharing your own version.

## Support and updates

If this helps your work, star the repository and
[follow TheVibeFounder](https://github.com/thevibefounder) for more builds.
Stars and follows are optional. Report reproducible problems through GitHub
Issues without sharing private files. See CONTRIBUTING.md before submitting a fix.

## License

Copyright (c) 2026 TheVibeFounder. Original instructions, templates and helper
code are released under the [MIT License](LICENSE). The bundled Anton font
retains its SIL Open Font License in assets/fonts/OFL.txt. This license does
not grant rights to anyone else's footage, likeness or account.
