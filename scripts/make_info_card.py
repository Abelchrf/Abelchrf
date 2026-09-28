"""Hand-authored neofetch-style info card: info-card.svg.

Edit INFO below when your details change, then re-run. Each line fades and
slides in on a short stagger; STATIC=1 emits a frozen frame for previews.
"""
from pathlib import Path

from terminal import BLUE, FONT, FG, GREEN, MUTED, STATIC, TITLE_H, esc, open_svg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"

WIDTH = 490

USER, HOST = "abel", "github"
INFO = [
    ("Now", "Bachelor IA @ ETNA, en alternance"),
    ("Focus", "Cloud / DevOps -> Cloud Security"),
    ("Prev", "Data Science & ML (NLP, vision)"),
    ("Location", "Paris, FR"),
    None,
    ("Stack", "AWS · Terraform · Docker · GitHub Actions"),
    ("DevSecOps", "Trivy · gitleaks · Bandit · hadolint"),
    ("Langs", "Python · SQL · Bash"),
    ("ML", "scikit-learn · PyTorch · FastAPI"),
    None,
    ("Certs", "AWS Cloud Practitioner"),
    ("Next", "AWS SAA · CompTIA Security+"),
    ("Goal", "alternance Cloud / DevOps / DevSecOps"),
    None,
    ("Highlights", ""),
    ("", "▸ aws-secure-baseline   Terraform AWS hardening"),
    ("", "▸ devsecops-ml-api      CI/CD security pipeline"),
    ("", "▸ vision-plus           YOLOv8 object detection"),
    ("", "▸ TweetSentiment        DistilBERT fine-tuning"),
]

FONT_SIZE = 13
LINE_H = 21
PAD_X = 24
KEY_W = 12  # characters reserved for the key column
CHAR_W = FONT_SIZE * 0.6
STAGGER_MS = 70


def render() -> str:
    header = f"{USER}@{HOST}"
    lines = [
        f'<tspan fill="{GREEN}" font-weight="bold">{USER}</tspan>'
        f'<tspan fill="{FG}">@</tspan>'
        f'<tspan fill="{GREEN}" font-weight="bold">{HOST}</tspan>',
        f'<tspan fill="{MUTED}">{"-" * len(header)}</tspan>',
    ]
    for row in INFO:
        if row is None:
            lines.append("")
            continue
        key, value = row
        key_part = f'<tspan fill="{BLUE}" font-weight="bold">{esc(key)}</tspan>' \
                   f'<tspan fill="{FG}">:</tspan>' if key else ""
        val_x = PAD_X + KEY_W * CHAR_W
        lines.append(f'{key_part}<tspan x="{val_x:g}" fill="{FG}">{esc(value)}</tspan>')

    height = TITLE_H + 26 + len(lines) * LINE_H + 40

    out = open_svg(WIDTH, height, f"{header}: ~ — neofetch", f"{USER} — neofetch-style profile card")
    if not STATIC:
        out.append(
            "<style>.l{animation:in .45s cubic-bezier(.2,.8,.2,1) both}"
            "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"
            + "".join(f".l{i}{{animation-delay:{150 + i * STAGGER_MS}ms}}" for i in range(len(lines) + 1))
            + "</style>"
        )

    y = TITLE_H + 32
    for i, line in enumerate(lines):
        if line:
            cls = "" if STATIC else f' class="l l{i}"'
            out.append(f'<text{cls} x="{PAD_X}" y="{y}" font-family="{FONT}" '
                       f'font-size="{FONT_SIZE}" xml:space="preserve">{line}</text>')
        y += LINE_H

    # the classic neofetch colour swatches
    swatches = ["#484f58", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]
    cls = "" if STATIC else f' class="l l{len(lines)}"'
    out.append(f"<g{cls}>")
    for i, color in enumerate(swatches):
        out.append(f'<rect x="{PAD_X + i * 22}" y="{y - 4}" width="22" height="14" fill="{color}"/>')
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    OUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
