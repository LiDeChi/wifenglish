#!/usr/bin/env python3
"""
Clean TTS generation for the lesson.
- No emotion tags in spoken text
- Different voice per role
"""

import json
import os
from pathlib import Path

import requests

from env_utils import load_local_env

load_local_env()

KEY = os.environ.get("BOSON_API_KEY")
URL = "https://api.boson.ai/v1/audio/speech"
MODEL = "higgs-audio-v3-tts"

VOICE_MAP = {"sales": "warm_female", "customer": "jake"}


def clean_text(text: str) -> str:
    """Remove any control tags so they are never spoken."""
    import re

    text = re.sub(r"<\|.*?\|>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def synthesize(text: str, voice: str, out_path: str):
    if not KEY:
        raise RuntimeError("BOSON_API_KEY is not set")

    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "input": text, "voice": voice, "response_format": "mp3"}
    resp = requests.post(URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"  Saved {out_path} ({len(resp.content)} bytes)")


def main():
    data = json.load(open("lesson-data.json"))
    out_dir = Path("audio/lesson01")
    out_dir.mkdir(parents=True, exist_ok=True)

    for scene in data["scenes"]:
        sid = scene["id"]
        print(f"Scene {sid}: {scene['title_en']}")
        for idx, line in enumerate(scene["lines"]):
            role = line.get("role", "customer")
            voice = VOICE_MAP.get(role, "jake")
            clean = clean_text(line["en"])
            fname = f"scene{sid:02d}_line{idx:02d}.mp3"
            out = out_dir / fname
            synthesize(clean, voice, str(out))
    print("\nAll clean lesson audios generated.")


if __name__ == "__main__":
    main()
