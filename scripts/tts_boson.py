#!/usr/bin/env python3
"""
Boson AI Higgs TTS skill / helper.
Supports emotion injection via inline tags in the input text.
Usage:
  python scripts/tts_boson.py --text "Hello, how are you?" --out audio/greet.mp3 --emotion friendly
  or pass full tagged text in --text
Key is read from env BOSON_API_KEY.
"""
import os
import requests
import argparse
from pathlib import Path

from env_utils import load_local_env

API_URL = "https://api.boson.ai/v1/audio/speech"
MODEL = "higgs-audio-v3-tts"  # or higgs-tts-3 per docs

def synthesize(text: str, out_path: str, voice: str = "default", response_format: str = "mp3"):
    load_local_env()
    key = os.environ.get("BOSON_API_KEY")
    if not key:
        raise RuntimeError("BOSON_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved: {out_path} ({len(resp.content)} bytes)")
    return out_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Input text. Use <|emotion:xxx|> tags for emotion injection e.g. <|emotion:happy|><|style:cheerful|>")
    parser.add_argument("--out", required=True)
    parser.add_argument("--voice", default="jake")
    parser.add_argument("--format", default="mp3")
    args = parser.parse_args()
    synthesize(args.text, args.out, args.voice, args.format)

if __name__ == "__main__":
    main()
