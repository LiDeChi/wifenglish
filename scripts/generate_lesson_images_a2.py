#!/usr/bin/env python3
"""Generate lesson scene images through a local AIClient2API provider.

Default endpoint follows AIClient2API's OpenAI-compatible image route:
http://localhost:3000/v1/images/generations
"""

from __future__ import annotations

import argparse
import base64
import json
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_GUIDE = ROOT / "style-guide.md"
DEFAULT_BASE_URL = "http://localhost:3000"
DEFAULT_PROVIDER_PATH = "/v1/images/generations"
DEFAULT_API_KEY = "123456"
DEFAULT_PROVIDER = "openai-codex-oauth"
DEFAULT_SIZE = "1024x576"

VISUAL_STYLE_ANCHOR = (
    "Photorealistic commercial lifestyle photography in the fixed WifEnglish showroom: "
    "large modern furniture showroom in a Chinese city, floor-to-ceiling windows, light oak flooring, "
    "warm daylight, high ceilings, recessed lighting, neutral warm beige walls, plants, modern sofas, "
    "coffee tables, and dining sets in the background. Fixed characters: Li Wei, a 28-year-old Chinese "
    "saleswoman with shoulder-length straight black hair, light blue collared blouse, silver name tag, "
    "dark slim trousers, pearl earrings; Mr. Zhang, a 35-year-old Chinese man with short neat black hair, "
    "light stubble, fitted grey polo or light sweater, dark chinos, brown belt, watch. Eye-level 35-50mm "
    "lens, both characters in frame, salesperson left or center-left, customer right, clear gesture toward furniture."
)


def lesson_json_path(lesson_number: str) -> Path:
    if lesson_number == "01":
        return ROOT / "lesson-data.json"
    return ROOT / f"lesson-{lesson_number}-data.json"


def lesson_image_dir(lesson_number: str) -> Path:
    if lesson_number == "01":
        return ROOT / "visuals"
    return ROOT / "visuals" / f"lesson{lesson_number}"


def web_image_dir(lesson_number: str) -> Path:
    if lesson_number == "01":
        return ROOT / "web" / "visuals"
    return ROOT / "web" / "visuals" / f"lesson{lesson_number}"


def available_lesson_numbers() -> list[str]:
    numbers = ["01"] if (ROOT / "lesson-data.json").exists() else []
    for path in sorted(ROOT.glob("lesson-*-data.json")):
        numbers.append(path.name.removeprefix("lesson-").removesuffix("-data.json"))
    return numbers


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_prompt(style_guide: str, lesson: dict, scene: dict) -> str:
    speakers = ", ".join(sorted({line.get("speaker", "") for line in scene.get("lines", []) if line.get("speaker")}))
    dialogue = " ".join(line.get("en", "") for line in scene.get("lines", []))
    style_guard = "See style-guide.md for the authoritative full visual rules." if style_guide else ""
    return (
        f"{VISUAL_STYLE_ANCHOR}\n"
        f"{style_guard}\n\n"
        f"Lesson: {lesson.get('title_en')} / {lesson.get('title_zh')}.\n"
        f"Scene {scene.get('id')}: {scene.get('title_en')} / {scene.get('title_zh')}.\n"
        f"Scene description: {scene.get('description')}.\n"
        f"Speakers in frame: {speakers}.\n"
        f"Dialogue context: {dialogue}\n\n"
        "Create one realistic 16:9 lesson illustration for this scene. Keep the fixed showroom, "
        "character appearances, lighting, camera style, and composition from the style guide. "
        "Only vary the furniture, gesture, and action needed by this scene. No text, captions, logos, "
        "watermarks, or UI elements in the image."
    )


def post_json(url: str, payload: dict, api_key: str, provider: str, timeout: int = 600) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Model-Provider": provider,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def write_image_from_response(response: dict, out_path: Path) -> None:
    data = response.get("data") or []
    if not data:
        raise RuntimeError("image response did not include data")

    first = data[0]
    if first.get("b64_json"):
        out_path.write_bytes(base64.b64decode(first["b64_json"]))
        return

    if first.get("url"):
        with urllib.request.urlopen(first["url"], timeout=300) as image_response:
            out_path.write_bytes(image_response.read())
        return

    raise RuntimeError("image response did not include b64_json or url")


def sync_to_web(source: Path, lesson_number: str) -> Path:
    target = web_image_dir(lesson_number) / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def generate_scene(
    *,
    endpoint: str,
    model: str,
    prompt: str,
    out_path: Path,
    force: bool,
    dry_run: bool,
    api_key: str,
    provider: str,
    size: str,
) -> bool:
    if out_path.exists() and out_path.stat().st_size > 10_000 and not force:
        print(f"skip existing {out_path.relative_to(ROOT)}")
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"dry-run {out_path.relative_to(ROOT)}")
        print(prompt[:500].replace("\n", " ") + ("..." if len(prompt) > 500 else ""))
        return False

    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": "low",
        "n": 1,
    }
    response = post_json(endpoint, payload, api_key=api_key, provider=provider)
    write_image_from_response(response, out_path)
    print(f"generated {out_path.relative_to(ROOT)}")
    return True


def run(args: argparse.Namespace) -> int:
    style_guide = STYLE_GUIDE.read_text(encoding="utf-8")
    endpoint = args.endpoint or f"{args.base_url.rstrip('/')}{DEFAULT_PROVIDER_PATH}"
    lesson_numbers = available_lesson_numbers() if args.all_missing else [args.lesson_number]

    generated = 0
    for lesson_number in lesson_numbers:
        path = lesson_json_path(lesson_number)
        if not path.exists():
            print(f"missing lesson data: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1

        lesson = read_json(path)
        print(f"\n=== Lesson {lesson_number}: {lesson.get('title_en')} ===")
        for scene in lesson.get("scenes", []):
            scene_id = int(scene.get("id", 0))
            if args.scene_id and scene_id != args.scene_id:
                continue
            out_path = lesson_image_dir(lesson_number) / f"scene-{scene_id:02d}.jpg"
            prompt = build_prompt(style_guide, lesson, scene)
            did_generate = generate_scene(
                endpoint=endpoint,
                model=args.model,
                prompt=prompt,
                out_path=out_path,
                force=args.force,
                dry_run=args.dry_run,
                api_key=args.api_key,
                provider=args.provider,
                size=args.size,
            )
            if did_generate:
                generated += 1
                target = sync_to_web(out_path, lesson_number)
                print(f"synced {target.relative_to(ROOT)}")

    print(f"\nDone. Generated {generated} image(s).")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    lesson = parser.add_mutually_exclusive_group(required=True)
    lesson.add_argument("--lesson-number", help="lesson number such as 05")
    lesson.add_argument("--all-missing", action="store_true", help="process every lesson and skip existing images")
    parser.add_argument("--force", action="store_true", help="regenerate images even when files exist")
    parser.add_argument("--scene-id", type=int, help="generate only one scene id from the selected lesson")
    parser.add_argument("--dry-run", action="store_true", help="print prompt previews without calling A2")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="AIClient2API base URL")
    parser.add_argument("--endpoint", help="full image generation endpoint; overrides --base-url")
    parser.add_argument("--model", default="gpt-image-2", help="OpenAI-compatible image model name")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="OpenAI-compatible image size")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="AIClient2API static API key")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER, help="AIClient2API model provider header")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        raise SystemExit(run(parse_args()))
    except urllib.error.URLError as exc:
        print(f"AIClient2API request failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
