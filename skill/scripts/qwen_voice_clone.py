#!/usr/bin/env python3
import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

from qwen_common import get_dashscope_key, ensure_dir

CUSTOMIZE_URL = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
ENROLL_MODEL = "qwen-voice-enrollment"  # fixed
DEFAULT_TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def to_data_uri(audio_path: Path, mime: str) -> str:
    b64 = base64.b64encode(audio_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def create_voice(sample_path: Path, preferred_name: str, target_model: str, mime: str, key: str, work_dir: Path) -> str:
    data_uri = to_data_uri(sample_path, mime)
    payload = {
        "model": ENROLL_MODEL,
        "input": {
            "action": "create",
            "target_model": target_model,
            "preferred_name": preferred_name,
            "audio": {"data": data_uri},
        },
    }
    payload_path = work_dir / "voice_enroll_payload.json"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    proc = subprocess.run(
        [
            "curl",
            "-sS",
            "-X",
            "POST",
            CUSTOMIZE_URL,
            "-H",
            f"Authorization: Bearer {key}",
            "-H",
            "Content-Type: application/json",
            "--data-binary",
            f"@{payload_path}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    j = json.loads(proc.stdout)
    try:
        return j["output"]["voice"]
    except Exception as e:
        raise RuntimeError(f"unexpected response: {e} {j}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="sample audio file path")
    ap.add_argument("--name", default="george", help="preferred_name")
    ap.add_argument("--mime", default="audio/wav", help="MIME type for the sample audio")
    ap.add_argument("--target-model", default=DEFAULT_TARGET_MODEL)
    ap.add_argument("--out", required=True, help="output JSON file to store the voice parameter")
    ap.add_argument("--work-dir", default="work/qwen-voice", help="scratch dir")
    args = ap.parse_args()

    key = get_dashscope_key()

    inp = Path(args.inp)
    if not inp.exists():
        raise FileNotFoundError(str(inp))

    work = Path(args.work_dir)
    ensure_dir(work)

    # Convert to a stable format (wav 24k mono) to improve enrollment reliability
    sample_wav = work / (inp.stem + "_enroll_24k.wav")
    run(["ffmpeg", "-y", "-i", str(inp), "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(sample_wav)])

    voice = create_voice(sample_wav, args.name, args.target_model, "audio/wav", key, work)

    outp = Path(args.out)
    ensure_dir(outp.parent)
    outp.write_text(
        json.dumps(
            {
                "preferred_name": args.name,
                "target_model": args.target_model,
                "voice": voice,
                "sample": str(inp),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(str(outp))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed: {e}", file=sys.stderr)
        sys.exit(2)
