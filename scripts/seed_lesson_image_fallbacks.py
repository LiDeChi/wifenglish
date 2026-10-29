#!/usr/bin/env python3
"""Seed fallback lesson images from existing WifEnglish showroom visuals.

This is a deterministic fallback for when AIClient2API image generation is not
available. It preserves the expected lesson image contract:

  visuals/lessonXX/scene-01..06.jpg
  web/visuals/lessonXX/scene-01..06.jpg
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FALLBACK_SOURCES = {
    "05": "visuals/lesson02",
    "06": "visuals/lesson03",
    "07": "visuals/lesson04",
    "08": "visuals",
}


def lesson_dir(lesson_number: str, web: bool = False) -> Path:
    base = ROOT / "web" / "visuals" if web else ROOT / "visuals"
    return base / f"lesson{lesson_number}"


def scene_path(base: Path, scene_id: int) -> Path:
    return base / f"scene-{scene_id:02d}.jpg"


def seed(force: bool) -> int:
    copied = 0
    for lesson_number, source_dir in FALLBACK_SOURCES.items():
        source_base = ROOT / source_dir
        target_base = lesson_dir(lesson_number)
        web_target_base = lesson_dir(lesson_number, web=True)
        target_base.mkdir(parents=True, exist_ok=True)
        web_target_base.mkdir(parents=True, exist_ok=True)

        for scene_id in range(1, 7):
            source = scene_path(source_base, scene_id)
            if not source.exists():
                raise FileNotFoundError(f"Missing fallback source: {source.relative_to(ROOT)}")

            for target in (scene_path(target_base, scene_id), scene_path(web_target_base, scene_id)):
                if target.exists() and not force:
                    continue
                shutil.copy2(source, target)
                copied += 1
                print(f"Seeded {target.relative_to(ROOT)} from {source.relative_to(ROOT)}")

    return copied


def verify() -> bool:
    ok = True
    for lesson_number in FALLBACK_SOURCES:
        for scene_id in range(1, 7):
            source = scene_path(lesson_dir(lesson_number), scene_id)
            web = scene_path(lesson_dir(lesson_number, web=True), scene_id)
            for path in (source, web):
                if not path.exists():
                    print(f"Missing: {path.relative_to(ROOT)}")
                    ok = False
                elif path.stat().st_size < 10_000:
                    print(f"Suspicious tiny file: {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
                    ok = False

            if source.exists() and web.exists() and source.read_bytes() != web.read_bytes():
                print(f"Web copy differs: {source.relative_to(ROOT)} -> {web.relative_to(ROOT)}")
                ok = False

    if ok:
        print("Verified fallback image files for lessons 05-08.")
    return ok


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite existing fallback images")
    parser.add_argument("--verify", action="store_true", help="verify files without copying")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.verify:
        return 0 if verify() else 1

    copied = seed(force=args.force)
    print(f"Done. Seeded {copied} file(s).")
    return 0 if verify() else 1


if __name__ == "__main__":
    raise SystemExit(main())
