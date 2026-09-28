"""Prep a portrait photo for ASCII conversion -> source-prepped.png.

A flatly-lit face converts to a dark, unreadable blob, so:
  1. remove the background with rembg to isolate the subject,
  2. boost local contrast with OpenCV's CLAHE for real highlights/shadows,
  3. composite onto pure white so the background maps to spaces.

Usage: python scripts/prep_photo.py source-photo.jpg [out.png]
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parent.parent
MAX_SIDE = 1024


def prep(src: Path) -> Image.Image:
    img = Image.open(src).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))

    rgba = np.array(remove(img))  # background -> alpha 0
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0

    gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray).astype(np.float32)

    out = gray * alpha + 255.0 * (1.0 - alpha)

    # crop to the subject, with a little breathing room
    ys, xs = np.where(alpha > 0.1)
    if len(xs):
        m = int(0.04 * max(out.shape))
        y0, y1 = max(ys.min() - m, 0), min(ys.max() + m, out.shape[0])
        x0, x1 = max(xs.min() - m, 0), min(xs.max() + m, out.shape[1])
        out = out[y0:y1, x0:x1]

    return Image.fromarray(out.clip(0, 255).astype(np.uint8), mode="L")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source-prepped.png"
    prep(src).save(dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
