#!/usr/bin/env python3
"""Generate WifEnglish lesson images through the APIMart GPT Image 2 skill.

This script wraps the skill-local helper and is designed to replace deterministic
fallback images for lessons 05-08 with real scene-specific generated images.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_GUIDE = ROOT / "style-guide.md"
APIMART_HELPER = Path.home() / ".codex/skills/apimart-gpt-image-2/scripts/generate_image.py"

FALLBACK_SOURCES = {
    "05": ROOT / "visuals/lesson02",
    "06": ROOT / "visuals/lesson03",
    "07": ROOT / "visuals/lesson04",
    "08": ROOT / "visuals",
}


def lesson_path(lesson_number: str) -> Path:
    return ROOT / f"lesson-{lesson_number}-data.json"


def image_path(lesson_number: str, scene_id: int, web: bool = False) -> Path:
    prefix = ROOT / "web" / "visuals" if web else ROOT / "visuals"
    return prefix / f"lesson{lesson_number}" / f"scene-{scene_id:02d}.jpg"


def fallback_path(lesson_number: str, scene_id: int) -> Path | None:
    base = FALLBACK_SOURCES.get(lesson_number)
    if not base:
        return None
    return base / f"scene-{scene_id:02d}.jpg"


def is_fallback_image(path: Path, lesson_number: str, scene_id: int) -> bool:
    source = fallback_path(lesson_number, scene_id)
    if not path.exists() or not source or not source.exists():
        return False
    return path.read_bytes() == source.read_bytes()


def build_prompt(lesson: dict, scene: dict, style_guide: str) -> str:
    lines = " ".join(line["en"] for line in scene["lines"])
    speakers = ", ".join(sorted({line["speaker"] for line in scene["lines"]}))
    return (
        "Photorealistic commercial lifestyle photography for WifEnglish lesson art. "
        "Use a consistent modern Chinese furniture showroom with warm daylight, large windows, "
        "light oak flooring, neutral warm walls, plants, sofas, tables, and showroom furniture. "
        "Keep fixed characters: Li Wei is a friendly 28-year-old Chinese saleswoman in a light blue "
        "collared blouse, dark trousers, silver name tag, shoulder-length black hair; Mr. Zhang is a "
        "35-year-old Chinese man in a fitted grey polo or light sweater, dark chinos, brown belt, watch. "
        "Eye-level 35-50mm lens, both characters in frame, salesperson left or center-left, customer right. "
        "No text, captions, logos, watermarks, or UI.\n\n"
        f"Style constraints summary from style-guide.md:\n{style_guide[:1200]}\n\n"
        f"Lesson: {lesson['title_en']} / {lesson['title_zh']}.\n"
        f"Scene {scene['id']}: {scene['title_en']} / {scene['title_zh']}.\n"
        f"Scene description: {scene['description']}.\n"
        f"Speakers: {speakers}.\n"
        f"Dialogue context: {lines}\n\n"
        "Create one realistic 16:9 scene-specific lesson illustration. Only vary the action, exact furniture, "
        "gestures, and composition needed by this scene while preserving the showroom and character identities."
    )


def generate_one(lesson_number: str, scene: dict, lesson: dict, args: argparse.Namespace, style_guide: str) -> bool:
    scene_id = int(scene["id"])
    out_path = image_path(lesson_number, scene_id)
    web_path = image_path(lesson_number, scene_id, web=True)

    should_generate = args.force or not out_path.exists()
    if args.replace_fallbacks and is_fallback_image(out_path, lesson_number, scene_id):
        should_generate = True

    if out_path.exists() and out_path.stat().st_size > 10_000 and not should_generate:
        print(f"skip existing {out_path.relative_to(ROOT)}")
        if not web_path.exists() or web_path.read_bytes() != out_path.read_bytes():
            web_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_path, web_path)
            print(f"synced {web_path.relative_to(ROOT)}")
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(lesson, scene, style_guide)
    if args.dry_run:
        print(f"dry-run {out_path.relative_to(ROOT)}")
        print(prompt[:600].replace("\n", " ") + ("..." if len(prompt) > 600 else ""))
        return False

    cmd = [
        sys.executable,
        str(APIMART_HELPER),
        "--prompt",
        prompt,
        "--out",
        str(out_path),
        "--resolution",
        args.resolution,
        "--timeout",
        str(args.timeout),
    ]
    print(f"generating {out_path.relative_to(ROOT)}")
    result = None
    for attempt in range(1, args.submit_retries + 1):
        if attempt > 1:
            wait = min(30, 5 * attempt)
            print(f"retrying submit for {out_path.relative_to(ROOT)} in {wait}s ({attempt}/{args.submit_retries})")
            time.sleep(wait)
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        if result.returncode == 0:
            break
        task_id = extract_task_id(result.stdout + "\n" + result.stderr)
        if task_id:
            poll_existing_task(task_id, out_path, args)
            break
    else:
        raise subprocess.CalledProcessError(result.returncode if result else 1, cmd)

    web_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_path, web_path)
    print(f"synced {web_path.relative_to(ROOT)}")
    return True


def extract_task_id(output: str) -> str | None:
    match = re.search(r"task_[A-Z0-9]+", output)
    return match.group(0) if match else None


def poll_existing_task(task_id: str, out_path: Path, args: argparse.Namespace) -> None:
    cmd = [
        sys.executable,
        str(APIMART_HELPER),
        "--task-id",
        task_id,
        "--out",
        str(out_path),
        "--timeout",
        str(args.timeout),
    ]
    last_output = ""
    for attempt in range(1, args.poll_retries + 1):
        if attempt > 1:
            wait = min(30, 5 * attempt)
            print(f"retrying task poll {task_id} in {wait}s ({attempt}/{args.poll_retries})")
            time.sleep(wait)
        result = subprocess.run(cmd, capture_output=True, text=True)
        last_output = result.stdout + "\n" + result.stderr
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 10_000:
            return
    raise RuntimeError(f"Could not complete APIMart task {task_id} after retries:\n{last_output[-2000:]}")


def run(args: argparse.Namespace) -> int:
    if not APIMART_HELPER.exists():
        raise FileNotFoundError(f"APIMart helper not found: {APIMART_HELPER}")

    style_guide = STYLE_GUIDE.read_text(encoding="utf-8")
    lesson_numbers = [args.lesson_number] if args.lesson_number else ["05", "06", "07", "08"]
    generated = 0

    for lesson_number in lesson_numbers:
        lesson_number = lesson_number.zfill(2)
        lesson = json.loads(lesson_path(lesson_number).read_text(encoding="utf-8"))
        print(f"\n=== Lesson {lesson_number}: {lesson['title_en']} ===")
        for scene in lesson["scenes"]:
            if args.scene_id and int(scene["id"]) != args.scene_id:
                continue
            if generate_one(lesson_number, scene, lesson, args, style_guide):
                generated += 1

    print(f"\nDone. Generated {generated} image(s).")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson-number", help="lesson number such as 05; defaults to 05-08")
    parser.add_argument("--scene-id", type=int, help="generate only one scene id")
    parser.add_argument("--force", action="store_true", help="regenerate all selected images")
    parser.add_argument(
        "--replace-fallbacks",
        action="store_true",
        help="regenerate images that are still byte-identical to fallback sources",
    )
    parser.add_argument("--dry-run", action="store_true", help="print prompt previews only")
    parser.add_argument("--resolution", default="1k", help="APIMart image resolution")
    parser.add_argument("--timeout", type=int, default=300, help="APIMart task timeout in seconds")
    parser.add_argument("--submit-retries", type=int, default=4, help="retry image task submission after transient failures")
    parser.add_argument("--poll-retries", type=int, default=6, help="retry task polling after transient network failures")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
