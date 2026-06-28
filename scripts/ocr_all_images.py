#!/usr/bin/env python3
"""OCR all source HEIC images and save text to furniture_ocr/."""

import os
import re
import subprocess
from pathlib import Path

SRC_DIR = Path("家具")
OUT_DIR = Path("furniture_ocr")
OUT_DIR.mkdir(exist_ok=True)

# Sort files numerically
def sort_key(p):
    m = re.search(r"IMG_(\d+)", p.name)
    return int(m.group(1)) if m else 0


def convert_heic_to_jpg(heic_path, jpg_path):
    cmd = [
        "ffmpeg",
        "-i", str(heic_path),
        "-q:v", "2",
        str(jpg_path),
        "-y",
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def run_ocr(jpg_path, txt_path):
    cmd = [
        "tesseract",
        str(jpg_path),
        str(txt_path.with_suffix("")),
        "-l", "eng+chi_sim",
        "--psm", "6",
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def main():
    heic_files = sorted(SRC_DIR.glob("*.HEIC"), key=sort_key)
    print(f"Found {len(heic_files)} HEIC files to OCR")

    for heic in heic_files:
        base = heic.stem
        out_txt = OUT_DIR / f"{base}.txt"
        tmp_jpg = OUT_DIR / f".{base}_ocr.jpg"

        if out_txt.exists() and out_txt.stat().st_size > 100:
            print(f"Skipping {base} (already OCR'd)")
            continue

        try:
            print(f"OCR {base} ...", end=" ")
            convert_heic_to_jpg(heic, tmp_jpg)
            run_ocr(tmp_jpg, out_txt)
            print("done")
        except subprocess.CalledProcessError as e:
            print(f"FAILED: {e}")
            out_txt.write_text(f"# OCR failed for {base}\n")

    print("\nAll done. Output in furniture_ocr/")


if __name__ == "__main__":
    main()
