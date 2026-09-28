"""Scrape the public contribution calendar into data/contributions.json.

Reads the same HTML endpoint that backs the graph on a GitHub profile, so no
token is needed.  Usage: python scripts/fetch_contributions.py [username]
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"
DEFAULT_USER = "Abelchrf"
COUNT_RE = re.compile(r"^([\d,]+) contributions?\b")


def fetch(user: str) -> dict:
    url = f"https://github.com/users/{user}/contributions"
    resp = requests.get(url, headers={"User-Agent": f"{user}-profile-heatmap"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Each day cell is paired with a <tool-tip for="cell-id"> holding its count.
    counts = {}
    for tip in soup.find_all("tool-tip"):
        m = COUNT_RE.match(tip.get_text(strip=True))
        counts[tip.get("for")] = int(m.group(1).replace(",", "")) if m else 0

    days = [
        {
            "date": td["data-date"],
            "count": counts.get(td.get("id"), 0),
            "level": int(td.get("data-level", 0)),
        }
        for td in soup.select("td.ContributionCalendar-day[data-date]")
    ]
    if not days:
        sys.exit("No contribution cells found: GitHub's markup may have changed.")
    days.sort(key=lambda d: d["date"])

    total = sum(d["count"] for d in days)
    header = soup.find(id="js-contribution-activity-description")
    if header:
        m = re.search(r"([\d,]+)", header.get_text())
        if m:
            total = int(m.group(1).replace(",", ""))

    return {
        "user": user,
        "total": total,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "days": days,
    }


def main() -> None:
    user = (sys.argv[1] if len(sys.argv) > 1 else None) \
        or os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USER
    data = fetch(user)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(f"{user}: {data['total']} contributions over {len(data['days'])} days -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
