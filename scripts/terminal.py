"""Shared look for the three profile SVGs: a dark terminal window frame."""
import os
from xml.sax.saxutils import escape

FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
BG = "#0d1117"
BAR = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"
TITLE_H = 30
PROMPT = "abel@github"  # shown in every window title

# STATIC=1 emits a frozen final frame (handy for local previews that don't animate).
STATIC = os.environ.get("STATIC") == "1"


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def open_svg(width: float, height: float, title: str, label: str) -> list[str]:
    """Start an SVG with the window chrome drawn; caller appends content and '</svg>'."""
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" '
        f'viewBox="0 0 {width:g} {height:g}" role="img" aria-label="{esc(label)}">',
        f"<title>{esc(label)}</title>",
        f'<rect x="0.5" y="0.5" width="{width - 1:g}" height="{height - 1:g}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0.5 {TITLE_H} V10.5 a10 10 0 0 1 10 -10 H{width - 10.5:g} '
        f'a10 10 0 0 1 10 10 V{TITLE_H} Z" fill="{BAR}" stroke="{BORDER}"/>',
        f'<circle cx="18" cy="15" r="5.5" fill="#ff5f56"/>',
        f'<circle cx="36" cy="15" r="5.5" fill="#ffbd2e"/>',
        f'<circle cx="54" cy="15" r="5.5" fill="#27c93f"/>',
        f'<text x="{width / 2:g}" y="19.5" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" fill="{MUTED}">{esc(title)}</text>',
    ]
