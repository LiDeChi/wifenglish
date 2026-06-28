#!/usr/bin/env python3
"""
Re-generate lesson audios with reference audio for consistent voices.
Uses Boson ref_audio + ref_text for stable speaker voice.
"""

import base64
import json
import os
from pathlib import Path

import requests

KEY = os.environ.get(
    "BOSON_API_KEY", "bai-MvuD-6LzgliIUQAxQ007pRyOfVPBfuM6qymny_nKlsE1sPNF"
)
API_URL = "https://api.boson.ai/v1/audio/speech"
MODEL = "higgs-audio-v3-tts"

# Speaker to ref mapping
REFS = {
    "sales": {
        "audio": "audio/ref_liwei.mp3",
        "text": "Hello, welcome to our showroom. My name is Li Wei. Please take your time.",
    },
    "customer": {
        "audio": "audio/ref_zhang.mp3",
        "text": "Hi, I'm looking for a sofa set for my new apartment.",
    },
}


def clean_text(t):
    import re

    t = re.sub(r"<\|.*?\|>", "", t)
    return " ".join(t.split()).strip()


def b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def synthesize(text, out_path, ref_audio_path=None, ref_text=None):
    key = KEY
    headers = {"Authorization": f"Bearer {key}"}

    data = {"model": MODEL, "input": text, "response_format": "mp3"}

    if ref_audio_path and ref_text:
        # Use multipart to send ref_audio as file
        files = {"ref_audio": open(ref_audio_path, "rb")}
        data["ref_text"] = ref_text
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {key}"},
            data=data,
            files=files,
            timeout=90,
        )
    else:
        headers["Content-Type"] = "application/json"
        resp = requests.post(API_URL, headers=headers, json=data, timeout=90)

    resp.raise_for_status()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved: {out_path} ({len(resp.content)} bytes)")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate lesson audios with reference voices.")
    parser.add_argument("--input", default="lesson-data.json", help="Input lesson JSON file")
    parser.add_argument("--output-dir", default="audio/lesson01", help="Output audio directory")
    args = parser.parse_args()

    data = json.load(open(args.input))
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for scene in data["scenes"]:
        sid = scene["id"]
        print(f"Scene {sid}")
        for idx, line in enumerate(scene["lines"]):
            role = line.get("role", "customer")
            ref = REFS.get(role)
            clean = clean_text(line["en"])

            fname = f"scene{sid:02d}_line{idx:02d}.mp3"
            out = str(out_dir / fname)

            if ref:
                synthesize(clean, out, ref["audio"], ref["text"])
            else:
                synthesize(clean, out)

    print(f"Done. Output: {out_dir}")


if __name__ == "__main__":
    main()
