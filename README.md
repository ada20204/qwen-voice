# qwen-voice (Clawdbot Skill)

Goal: Add **voice understanding + voice reply** to Clawdbot chats.

What it does:
- ASR: voice → text (optional coarse timestamps via chunking)
- TTS: text → voice (default voice: Cherry)
- Voice Clone: one sample voice → your custom voice → voice replies

## Requirements

System:
- ffmpeg
- curl

Python:
- Python 3.10+
- Recommended: `uv` (or any venv + pip)

## Env vars

Required:
- `DASHSCOPE_API_KEY`

### Where the code reads env from

The scripts support **both**:
1) **User-level** (recommended): `~/.config/qwen-voice/.env`
2) **Project-level** (dev/testing): `./.qwen-voice/.env`

Precedence: user-level first, then project-level.

### Setup (recommended)

Copy the template dir into your user config:

```bash
cp -r .qwen-voice ~/.config/qwen-voice
cp ~/.config/qwen-voice/.env.example ~/.config/qwen-voice/.env
# edit ~/.config/qwen-voice/.env
```

### Setup (project-local, optional)

```bash
cp .qwen-voice/.env.example .qwen-voice/.env
# edit .qwen-voice/.env
```

## Quick commands

ASR (no timestamps):
```bash
python3 skill/scripts/qwen_asr.py --in /path/to/audio.ogg
```

ASR (with coarse timestamps):
```bash
python3 skill/scripts/qwen_asr.py --in /path/to/audio.ogg --timestamps --chunk-sec 3
```

TTS (preset voice):
```bash
python3 skill/scripts/qwen_tts.py --text '你好，我是 Pi。' --voice Cherry --out /tmp/out.ogg
```

Voice clone (create profile once, reuse):
```bash
python3 skill/scripts/qwen_voice_clone.py --in ./sample.ogg --name george --out ./george.voice.json
python3 skill/scripts/qwen_tts.py --text '你好，我是 George。' --voice-profile ./george.voice.json --out /tmp/out.ogg
```

## Notes / pitfalls

- Timestamps are **chunk-based**, not word-level alignment.
- Inputs are converted to **mono 16k WAV** before ASR.
- `.ogg` output is Opus (Telegram voice-note friendly).

## Repo layout

- `skill/`  Clawdbot skill (scripts + SKILL.md)
- `.qwen-voice/`  env template directory (copy to `~/.config/qwen-voice/`)
- `requirements.in / requirements.txt`  dependency list (uv generated)
