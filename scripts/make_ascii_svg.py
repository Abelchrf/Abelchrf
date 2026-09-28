"""Convert source-prepped.png into a self-typing monochrome ASCII portrait: abel-ascii.svg.

Each row sits behind a horizontal clip that wipes left-to-right with a block
cursor riding the edge, staggered top to bottom. It's SMIL inside the SVG, so
GitHub plays it: once, then it freezes.

Usage: python scripts/make_ascii_svg.py [--src source-prepped.png] [--cols 64] [--invert]
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from terminal import FONT, PROMPT, STATIC, TITLE_H, esc, open_svg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "abel-ascii.svg"

# dense -> blank, so white (the background) prints as spaces
RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
FILL = "#c9d1d9"  # one light-grey fill: no per-character colour noise

FONT_SIZE = 10
CHAR_W = FONT_SIZE * 0.6
LINE_H = 11
PAD = 22
ROW_STAGGER = 0.055  # seconds between rows starting
ROW_DUR = 0.32  # seconds for one row to type out
START = 0.3


def to_ascii(img: Image.Image, cols: int, invert: bool) -> list[str]:
    rows = round(cols * img.height / img.width * CHAR_W / LINE_H)
    px = np.asarray(img.convert("L").resize((cols, rows), Image.Resampling.LANCZOS), dtype=np.float32)
    if invert:
        px = 255 - px
    idx = (px / 255.0 * (len(RAMP) - 1)).round().astype(int)
    lines = ["".join(RAMP[i] for i in row) for row in idx]

    # trim blank margins shared by every row
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    left = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    right = max(len(l.rstrip()) for l in lines)
    return [l[left:right] for l in lines]


def render(lines: list[str]) -> str:
    cols = max(len(l) for l in lines)
    row_w = cols * CHAR_W
    width = round(row_w + 2 * PAD)
    top = TITLE_H + PAD
    height = round(top + len(lines) * LINE_H + PAD)

    out = open_svg(width, height, f"{PROMPT}: ~/portrait", "ASCII portrait of Abel")
    defs, body = [], []
    t = START
    for i, line in enumerate(lines):
        y = top + i * LINE_H
        if not line.strip():
            continue
        text_attrs = (f'x="{PAD}" y="{y + LINE_H - 2}" font-family="{FONT}" font-size="{FONT_SIZE}" '
                      f'fill="{FILL}" xml:space="preserve" textLength="{row_w:g}" lengthAdjust="spacing"')
        text = esc(line.ljust(cols))
        if STATIC:
            body.append(f"<text {text_attrs}>{text}</text>")
            continue
        begin, end = f"{t:.3f}s", f"{t + ROW_DUR:.3f}s"
        defs.append(
            f'<clipPath id="r{i}"><rect x="{PAD}" y="{y}" width="0" height="{LINE_H}">'
            f'<animate attributeName="width" from="0" to="{row_w:g}" begin="{begin}" dur="{ROW_DUR}s" '
            f'fill="freeze"/></rect></clipPath>'
        )
        body.append(f'<text clip-path="url(#r{i})" {text_attrs}>{text}</text>')
        body.append(
            f'<rect x="{PAD}" y="{y + 1}" width="{CHAR_W:g}" height="{LINE_H - 1}" fill="{FILL}" opacity="0">'
            f'<set attributeName="opacity" to="0.85" begin="{begin}"/>'
            f'<animate attributeName="x" from="{PAD}" to="{PAD + row_w:g}" begin="{begin}" '
            f'dur="{ROW_DUR}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" begin="{end}"/></rect>'
        )
        t += ROW_STAGGER

    if defs:
        out.append("<defs>" + "".join(defs) + "</defs>")
    out.extend(body)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=ROOT / "source-prepped.png")
    ap.add_argument("--cols", type=int, default=64)
    ap.add_argument("--invert", action="store_true", help="map bright pixels to dense glyphs")
    args = ap.parse_args()

    lines = to_ascii(Image.open(args.src), args.cols, args.invert)
    OUT.write_text(render(lines), encoding="utf-8")
    print(f"wrote {OUT.name} ({max(map(len, lines))}x{len(lines)} chars)")


if __name__ == "__main__":
    main()
