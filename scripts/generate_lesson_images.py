#!/usr/bin/env python3
"""Generate scene images for lessons 2-4 using APIMart GPT-Image-2."""

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_SCRIPT = Path.home() / ".codex/skills/apimart-gpt-image-2/scripts/generate_image.py"

BASE_SCENE = (
    "Photorealistic commercial lifestyle photography. Bright warm daylight, soft natural light "
    "from large floor-to-ceiling windows. Modern furniture showroom in a Chinese city with "
    "light oak wooden flooring, high ceilings, recessed lighting, neutral warm beige walls. "
    "Indoor plants (fiddle leaf fig, monstera) and modern sofas/coffee tables in the background. "
    "Eye-level 35-50mm lens feel, good depth of field. "
)

CHARACTERS = {
    "liwei": (
        "Li Wei: 28-year-old Chinese woman, friendly professional, shoulder-length straight black hair "
        "with slight waves, light makeup, warm genuine smile, light blue collared blouse, small silver name tag, "
        "dark slim trousers, small pearl earrings."
    ),
    "zhang": (
        "Mr. Zhang: 35-year-old Chinese man, polite thoughtful, short neat black hair, light stubble, "
        "fitted grey polo shirt, dark chinos, brown belt, watch on left wrist."
    ),
    "customer": (
        "Business customer: 40-year-old professional man in navy blazer, light shirt, dark trousers, "
        "carrying a tablet folder, attentive expression."
    ),
}

LESSONS = [
    ("lesson-02-data.json", "visuals/lesson02"),
    ("lesson-03-data.json", "visuals/lesson03"),
    ("lesson-04-data.json", "visuals/lesson04"),
]


def build_prompt(scene):
    """Build a concise prompt for one scene."""
    title = scene["title_en"]
    desc = scene["description"]
    # Determine which characters appear
    speakers = {line["speaker"] for line in scene["lines"]}
    chars = []
    if "Li Wei" in speakers:
        chars.append(CHARACTERS["liwei"])
    if "Mr. Zhang" in speakers:
        chars.append(CHARACTERS["zhang"])
    if "Customer" in speakers and "Mr. Zhang" not in speakers:
        chars.append(CHARACTERS["customer"])

    chars_text = " ".join(chars)
    action = f"Scene: {title}. {desc}"
    prompt = (
        f"{BASE_SCENE} {chars_text} {action} "
        "Both characters in frame, salesperson on left/center-left, customer on right, "
        "clear eye contact or gesture toward furniture, subjects occupy 40-60% of frame. "
        "High detail, realistic, inviting retail atmosphere."
    )
    return prompt


def generate_image(prompt, out_path):
    """Call APIMart image generation skill."""
    cmd = [
        sys.executable,
        str(SKILL_SCRIPT),
        "--prompt", prompt,
        "--out", str(out_path),
        "--resolution", "1k",
        "--quality", "low",
    ]
    print(f"Generating {out_path} ...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print(f"FAILED {out_path}:\n{result.stderr}", file=sys.stderr)
        return False
    print(f"OK {out_path}")
    return True


def main():
    if not SKILL_SCRIPT.exists():
        print(f"Skill script not found: {SKILL_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    for json_file, out_dir in LESSONS:
        data = json.loads(Path(json_file).read_text(encoding="utf-8"))
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        print(f"\n=== {data['title_en']} ===")
        for scene in data["scenes"]:
            sid = scene["id"]
            image_file = out_path / f"scene-{sid:02d}.jpg"
            if image_file.exists() and image_file.stat().st_size > 10000:
                print(f"Skipping existing {image_file}")
                continue
            prompt = build_prompt(scene)
            generate_image(prompt, image_file)

    print("\nAll image generation attempts finished.")


if __name__ == "__main__":
    main()
