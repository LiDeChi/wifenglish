#!/usr/bin/env python3
"""
Generate all audio assets for the scenarios using Boson Higgs TTS.
Injects emotion tags based on speaker and context.
"""

import json
import os
import subprocess
from pathlib import Path

SCENARIOS = "scenes/scenarios.json"
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

# Emotion map - simple heuristics
EMOTION_MAP = {
    "Salesperson": "<|emotion:friendly|><|style:professional|>",
    "Customer": "<|emotion:curious|><|style:casual|>",
    "Wife": "<|emotion:warm|><|style:polite|>",
    "Husband": "<|emotion:thoughtful|>",
    "销售员": "<|emotion:friendly|><|style:professional|>",
    "顾客": "<|emotion:curious|><|style:casual|>",
    "妻子": "<|emotion:warm|>",
    "丈夫": "<|emotion:thoughtful|>",
}


def build_tagged_text(speaker, text, emotion_hint=None):
    prefix = EMOTION_MAP.get(speaker, "<|emotion:neutral|>")
    if emotion_hint:
        prefix = f"<|emotion:{emotion_hint}|>"
    # Keep it clean
    return f"{prefix}{text}"


def generate(text, out_file):
    cmd = [
        "python3",
        "scripts/tts_boson.py",
        "--text",
        text,
        "--out",
        str(out_file),
        "--voice",
        "jake",
    ]
    print("Generating:", out_file.name)
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    data = json.load(open(SCENARIOS))
    for level in data["levels"]:
        lid = level["id"]
        print(f"\n=== Level {lid}: {level['title']} ===")
        for version, key in [
            ("clear", "english_clear"),
            ("natural", "english_natural"),
            ("zh", "chinese"),
        ]:
            lines = level["dialogue"][key]
            for i, turn in enumerate(lines):
                speaker = turn["speaker"]
                text = turn["text"]
                tagged = build_tagged_text(speaker, text)
                out = AUDIO_DIR / f"level{lid}_{version}_{i:02d}.mp3"
                if not out.exists() or out.stat().st_size < 1000:
                    generate(tagged, out)
    print("\nAll audios generated (or skipped if exist).")


if __name__ == "__main__":
    main()
