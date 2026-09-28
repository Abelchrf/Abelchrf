"""Render data/contributions.json as an animated 53x7 heatmap: contrib-heatmap.svg.

Cells drop in once along the diagonal (CSS keyframes, played on load, then
frozen), with a Less->More legend and a stats footer.
"""
import json
from datetime import date, timedelta
from pathlib import Path

from terminal import FONT, FG, MUTED, PROMPT, STATIC, TITLE_H, open_svg

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32",
           "#26a641", "#39d353", "#69f0a0"]
#           none   ->   brightest (level 5 is a neon top end)

CELL, GAP = 12, 3
STEP = CELL + GAP
PAD = 22
LABEL_W = 32
MONTH_H = 18
DIAG_DELAY_MS = 22


def sunday_index(d: date) -> int:
    return (d.weekday() + 1) % 7  # GitHub columns run Sunday..Saturday


def levels(days: list[dict]) -> list[int]:
    """GitHub's 0-4 levels, with the top 10% of busy days promoted to neon level 5."""
    busy = sorted(d["count"] for d in days if d["count"] > 0)
    top = busy[int(len(busy) * 0.9)] if len(busy) >= 5 else None
    return [5 if top and d["level"] == 4 and d["count"] >= top else d["level"] for d in days]


def streaks(days: list[dict]) -> tuple[int, int]:
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    current = 0
    # today may not have contributions yet; don't break the streak on it
    tail = days[:-1] if days and not days[-1]["count"] else days
    for d in reversed(tail):
        if not d["count"]:
            break
        current += 1
    return longest, current


def render(data: dict) -> str:
    days = data["days"]
    start = date.fromisoformat(days[0]["date"])
    first_sunday = start - timedelta(days=sunday_index(start))
    weeks = (date.fromisoformat(days[-1]["date"]) - first_sunday).days // 7 + 1

    grid_x = PAD + LABEL_W
    grid_y = TITLE_H + PAD + MONTH_H
    grid_w = weeks * STEP - GAP
    grid_h = 7 * STEP - GAP
    width = grid_x + grid_w + PAD
    footer_y = grid_y + grid_h + 30
    height = footer_y + PAD

    out = open_svg(width, height, f"{PROMPT}: ~/contributions",
                   f"{data['total']} GitHub contributions in the last year")

    max_diag = weeks + 6
    if not STATIC:
        css = [
            ".c{animation:drop .5s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box}",
            "@keyframes drop{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:none}}",
            f".f{{animation:fade .6s ease-out {max_diag * DIAG_DELAY_MS}ms both}}",
            "@keyframes fade{from{opacity:0}to{opacity:1}}",
        ]
        css += [f".d{i}{{animation-delay:{i * DIAG_DELAY_MS}ms}}" for i in range(max_diag + 1)]
        out.append(f"<style>{''.join(css)}</style>")

    text = f'font-family="{FONT}" font-size="11" fill="{MUTED}"'

    # month labels over the first column that starts in a new month
    last_month, last_x = None, -99
    for w in range(weeks):
        month = (first_sunday + timedelta(weeks=w)).month
        x = grid_x + w * STEP
        if month != last_month and x - last_x >= 3 * STEP:
            label = (first_sunday + timedelta(weeks=w)).strftime("%b")
            out.append(f'<text x="{x}" y="{grid_y - 7}" {text}>{label}</text>')
            last_x = x
        last_month = month

    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="{PAD}" y="{grid_y + row * STEP + CELL - 2}" {text}>{name}</text>')

    for d, lvl in zip(days, levels(days)):
        day = date.fromisoformat(d["date"])
        w = (day - first_sunday).days // 7
        r = sunday_index(day)
        cls = "" if STATIC else f' class="c d{w + r}"'
        stroke = "" if lvl else ' stroke="#21262d"'
        out.append(
            f'<rect{cls} x="{grid_x + w * STEP}" y="{grid_y + r * STEP}" width="{CELL}" '
            f'height="{CELL}" rx="2.5" fill="{PALETTE[lvl]}"{stroke}>'
            f'<title>{d["count"]} on {d["date"]}</title></rect>'
        )

    longest, current = streaks(days)
    best = max(days, key=lambda d: d["count"])
    fclass = "" if STATIC else ' class="f"'
    out.append(f"<g{fclass}>")
    out.append(
        f'<text x="{grid_x}" y="{footer_y}" font-family="{FONT}" font-size="12" fill="{FG}">'
        f'<tspan font-weight="bold">{data["total"]:,}</tspan> contributions in the last year'
        f'<tspan fill="{MUTED}">  ·  longest streak {longest}d  ·  current {current}d'
        f'  ·  best day {best["count"]}</tspan></text>'
    )
    legend_x = grid_x + grid_w - len(PALETTE) * STEP - 34
    out.append(f'<text x="{legend_x - 8}" y="{footer_y}" text-anchor="end" {text}>Less</text>')
    for i, color in enumerate(PALETTE):
        out.append(f'<rect x="{legend_x + i * STEP}" y="{footer_y - 10}" width="{CELL}" '
                   f'height="{CELL}" rx="2.5" fill="{color}"/>')
    out.append(f'<text x="{legend_x + len(PALETTE) * STEP + 5}" y="{footer_y}" {text}>More</text>')
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.write_text(render(data), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
