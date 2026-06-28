#!/usr/bin/env python3
"""
Generate lesson audios with consistent speaker voices using Boson reusable custom voices.

Workflow:
1. Create reusable voices for each speaker (Li Wei / Mr. Zhang) from reference audio.
   Voice IDs are cached in audio/voices.json.
2. Generate each line using the cached voice_id instead of uploading ref_audio every time.
   This gives much better speaker consistency across the whole lesson.

Usage:
    python scripts/generate_lesson_audio_ref.py
    python scripts/generate_lesson_audio_ref.py --lesson lesson-data.json --output-dir audio/lesson01
"""

import argparse
import json
import os
import re
import shutil
import time
from pathlib import Path

import requests

from env_utils import load_local_env

API_BASE = "https://api.boson.ai/v1"
SPEECH_URL = f"{API_BASE}/audio/speech"
VOICES_URL = f"{API_BASE}/audio/voices"
MODEL = "higgs-tts-3"

load_local_env()

# Speaker reference configuration
REFS = {
    "sales": {
        "name": "Li Wei",
        "audio": "audio/ref_liwei.mp3",
        # Keep this transcript aligned with the actual reference audio.
        "text": "Hello, welcome to our showroom. My name is Li Wei.",
    },
    "customer": {
        "name": "Mr. Zhang",
        "audio": "audio/ref_zhang.mp3",
        "text": "Hi, I'm looking for a sofa set for my new apartment.",
    },
}

VOICE_CACHE = Path("audio/voices.json")


def clean_text(t: str) -> str:
    t = re.sub(r"<\|.*?\|>", "", t)
    return " ".join(t.split()).strip()


def _headers() -> dict:
    key = os.environ.get("BOSON_API_KEY")
    if not key:
        raise RuntimeError("BOSON_API_KEY is not set")
    return {"Authorization": f"Bearer {key}"}


def load_voice_cache() -> dict:
    if VOICE_CACHE.exists():
        return json.loads(VOICE_CACHE.read_text(encoding="utf-8"))
    return {}


def save_voice_cache(cache: dict) -> None:
    VOICE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    VOICE_CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def create_voice(role: str) -> str:
    """Create a reusable Boson voice from reference audio. Return voice_id."""
    ref = REFS[role]
    audio_path = Path(ref["audio"])
    if not audio_path.exists():
        raise FileNotFoundError(f"Reference audio not found: {audio_path}")

    print(f"Creating reusable voice for {ref['name']} from {audio_path} ...")
    with open(audio_path, "rb") as f:
        files = {"ref_audio": (audio_path.name, f, "audio/mpeg")}
        data = {
            "title": ref["name"],
            "ref_text": ref["text"],
        }
        resp = requests.post(
            VOICES_URL,
            headers=_headers(),
            data=data,
            files=files,
            timeout=120,
        )

    resp.raise_for_status()
    result = resp.json()
    voice_id = result.get("voice_id") or result.get("voice")
    if not voice_id:
        raise RuntimeError(f"Failed to create voice for {role}: {result}")

    print(f"  -> voice_id: {voice_id}")
    return voice_id


def ensure_voices() -> dict:
    """Return a mapping {role: voice_id}, creating voices if needed."""
    cache = load_voice_cache()
    updated = False

    for role, ref in REFS.items():
        voice_id = cache.get(role)
        if not voice_id:
            voice_id = create_voice(role)
            cache[role] = voice_id
            updated = True
        else:
            print(f"Using cached voice for {ref['name']}: {voice_id}")

    if updated:
        save_voice_cache(cache)

    return cache


def synthesize_with_voice(text: str, out_path: Path, voice_id: str) -> None:
    """Synthesize one line using a reusable voice_id."""
    data = {
        "model": MODEL,
        "input": text,
        "voice": voice_id,
        "response_format": "mp3",
    }
    resp = requests.post(
        SPEECH_URL,
        headers={**_headers(), "Content-Type": "application/json"},
        json=data,
        timeout=90,
    )
    resp.raise_for_status()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    print(f"  Saved: {out_path} ({len(resp.content)} bytes)")


def synthesize_with_ref(text: str, out_path: Path, ref: dict) -> None:
    """Fallback: synthesize by uploading reference audio each time."""
    data = {
        "model": MODEL,
        "input": text,
        "response_format": "mp3",
        "ref_text": ref["text"],
    }
    with open(ref["audio"], "rb") as f:
        files = {"ref_audio": f}
        resp = requests.post(
            SPEECH_URL,
            headers=_headers(),
            data=data,
            files=files,
            timeout=90,
        )
    resp.raise_for_status()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    print(f"  Saved: {out_path} ({len(resp.content)} bytes)")


def expected_audio_files(data: dict, output_dir: Path) -> list[Path]:
    files = []
    for scene in data["scenes"]:
        sid = scene["id"]
        for idx, _line in enumerate(scene["lines"]):
            files.append(output_dir / f"scene{sid:02d}_line{idx:02d}.mp3")
    return files


def print_audio_status(lesson_path: str, output_dir: Path) -> None:
    data = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
    expected = expected_audio_files(data, output_dir)
    existing = [path for path in expected if path.exists()]
    missing = [path for path in expected if not path.exists()]
    tiny = [path for path in existing if path.stat().st_size < 1000]

    print(f"Lesson: {lesson_path}")
    print(f"Output: {output_dir}")
    print(f"Expected files: {len(expected)}")
    print(f"Existing files: {len(existing)}")
    print(f"Missing files: {len(missing)}")
    print(f"Suspicious tiny files: {len(tiny)}")

    if existing:
        print("\nExisting files:")
        for path in existing:
            stat = path.stat()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
            print(f"  {timestamp} {stat.st_size:>7} {path}")

    if missing:
        print("\nMissing files:")
        for path in missing:
            print(f"  {path}")

    if tiny:
        print("\nSuspicious tiny files:")
        for path in tiny:
            print(f"  {path} ({path.stat().st_size} bytes)")


def sync_to_web(output_dir: Path, web_output_dir: Path, data: dict) -> None:
    missing = [path for path in expected_audio_files(data, output_dir) if not path.exists()]
    if missing:
        raise RuntimeError(
            "Cannot sync to web; generated audio is incomplete: "
            + ", ".join(str(path) for path in missing[:5])
        )

    web_output_dir.mkdir(parents=True, exist_ok=True)
    for path in expected_audio_files(data, output_dir):
        target = web_output_dir / path.name
        shutil.copy2(path, target)
        print(f"  Synced: {target}")


def generate(
    lesson_path: str,
    output_dir: Path,
    force: bool = False,
    allow_ref_fallback: bool = False,
    sync_web_dir: Path | None = None,
) -> None:
    data = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        voices = ensure_voices()
        use_voice_id = True
    except Exception as e:
        if not allow_ref_fallback:
            raise RuntimeError(
                f"Could not create or load reusable voices: {e}. "
                "Set BOSON_API_KEY and retry, or pass --allow-ref-fallback to use per-request ref_audio."
            ) from e

        print(f"Warning: could not create reusable voices ({e}). Falling back to per-request ref audio.")
        voices = {}
        use_voice_id = False

    total = sum(len(s["lines"]) for s in data["scenes"])
    done = 0

    for scene in data["scenes"]:
        sid = scene["id"]
        print(f"Scene {sid}")
        for idx, line in enumerate(scene["lines"]):
            role = line.get("role", "customer")
            ref = REFS.get(role)
            if not ref:
                print(f"  Skip unknown role '{role}' in scene {sid} line {idx}")
                continue

            clean = clean_text(line["en"])
            out = output_dir / f"scene{sid:02d}_line{idx:02d}.mp3"

            if out.exists() and not force:
                print(f"  Skip existing: {out}")
                done += 1
                continue

            if use_voice_id:
                synthesize_with_voice(clean, out, voices[role])
            else:
                synthesize_with_ref(clean, out, ref)

            done += 1
            # Small polite delay to avoid rate limits.
            time.sleep(0.3)

    print(f"\nDone. {done}/{total} files in {output_dir}")
    if use_voice_id:
        print(f"Reusable voice IDs cached in {VOICE_CACHE}")
    if sync_web_dir:
        print(f"\nSyncing generated audio to {sync_web_dir}")
        sync_to_web(output_dir, sync_web_dir, data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lesson audios with consistent voices.")
    parser.add_argument("--lesson", default="lesson-data.json", help="Input lesson JSON file")
    parser.add_argument("--output-dir", default="audio/lesson01", help="Output audio directory")
    parser.add_argument("--force", action="store_true", help="Regenerate existing files")
    parser.add_argument(
        "--allow-ref-fallback",
        action="store_true",
        help="Use per-request ref_audio if reusable custom voices cannot be created.",
    )
    parser.add_argument(
        "--sync-web-dir",
        help="Copy generated lesson audio files to a web audio directory after generation.",
    )
    parser.add_argument("--status", action="store_true", help="Report expected/existing audio files and exit")
    args = parser.parse_args()

    if args.status:
        print_audio_status(args.lesson, Path(args.output_dir))
        return

    generate(
        args.lesson,
        Path(args.output_dir),
        force=args.force,
        allow_ref_fallback=args.allow_ref_fallback,
        sync_web_dir=Path(args.sync_web_dir) if args.sync_web_dir else None,
    )


if __name__ == "__main__":
    main()
