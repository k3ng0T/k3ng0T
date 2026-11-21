"""Generate the profile's original SVG cards and up-to-date public GitHub activity."""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG, PANEL, LINE, TEXT, MUTED, PINK = "#171719", "#232326", "#353438", "#f4f0ed", "#aaa2a5", "#e9a4bd"


def esc(value):
    return html.escape(str(value), quote=True)


def svg(height, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img">
<style>text{{font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}} .mono{{font-family: ui-monospace,Consolas,monospace}} .small{{font-size:13px;letter-spacing:1.6px;font-weight:700}} .body{{font-size:20px}} .muted{{fill:{MUTED}}}</style>
{content}
</svg>\n'''


def rect(x, y, w, h, fill, radius=20, stroke="none"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def text(x, y, value, size=20, fill=TEXT, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{esc(value)}</text>'


def heading(title, number):
    return (rect(28, 26, 45, 45, PANEL, 14)
            + text(50, 56, number, 14, PINK, 700, 'text-anchor="middle" class="mono"')
            + text(90, 58, title, 25, TEXT, 700))


def write(name, data):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(data, encoding="utf-8", newline="\n")


def pill(x, y, label, width, color=PINK):
    return (rect(x, y, width, 38, "#202023", 12, "#454047")
            + f'<circle cx="{x+16}" cy="{y+19}" r="4" fill="{color}"/>'
            + text(x+29, y+25, label, 16, TEXT, 600))


def design():
    hero = rect(0, 0, 900, 218, BG, 30)
    hero += '<defs><clipPath id="hero-clip"><rect width="900" height="218" rx="30"/></clipPath></defs>'
    hero += '<g clip-path="url(#hero-clip)"><circle cx="806" cy="-38" r="170" fill="#2b2028"/><circle cx="838" cy="195" r="95" fill="#30232b"/></g>'
    hero += '<circle cx="783" cy="93" r="56" fill="none" stroke="#8b5b70" stroke-width="1.5"/><circle cx="783" cy="93" r="38" fill="none" stroke="#624655" stroke-width="1"/>'
    hero += text(32, 47, "DEVELOPER  /  MAKER  /  CURIOUS MIND", 13, PINK, 700, 'class="mono"')
    hero += text(32, 116, "Gotanda", 64, TEXT, 750) + text(289, 116, ".", 64, PINK, 750)
    hero += text(34, 150, "Building things for the web and beyond.", 20, MUTED)
    hero += pill(33, 169, "k3ng0T", 116) + pill(160, 169, "NEW LEGENDA", 168, "#f4f0ed")
    write("profile-hero.svg", svg(218, hero))

    about = rect(0, 0, 900, 238, BG, 30) + heading("About me", "01")
    for y, label, value in [(104, "NOW", "Developer at NEW LEGENDA"),
                            (151, "BUILDING", "Web, desktop and mobile projects"),
                            (198, "LEARNING", "Swift — and whatever sparks curiosity")]:
        about += rect(28, y-27, 844, 39, PANEL, 13)
        about += text(45, y, label, 12, PINK, 700, 'class="mono"')
        about += text(168, y, value, 18, TEXT, 600)
    write("profile-about.svg", svg(238, about))

    stack = rect(0, 0, 900, 254, BG, 30) + heading("Tech stack", "02")
    stack += text(31, 99, "LANGUAGES", 12, MUTED, 700, 'class="mono"')
    x = 30
    for label, width in [("JavaScript",125),("TypeScript",128),("Python",94),("PHP",72),("C++",68),("Rust",76),("Kotlin",88),("AutoHotkey",133)]:
        stack += pill(x, 111, label, width)
        x += width + 7
    stack += text(31, 181, "WEB & LEARNING", 12, MUTED, 700, 'class="mono"')
    x = 30
    for label, width in [("React",92),("Node.js",108),("Swift · learning",166)]:
        stack += pill(x, 193, label, width, "#e9a4bd" if label.startswith("Swift") else "#ded8d6")
        x += width + 9
    write("profile-stack.svg", svg(254, stack))

    beyond = rect(0, 0, 900, 185, BG, 30) + heading("Beyond the code", "04")
    beyond += text(32, 105, "English · Russian · Chinese · Kazakh · Turkish", 19, TEXT, 600)
    beyond += text(32, 144, "Chess  /  card tricks  /  VALORANT 1,800+ h  /  Counter-Strike 1,000+ h", 17, MUTED, 500)
    write("profile-beyond.svg", svg(185, beyond))

    projects_header = rect(0, 0, 900, 94, BG, 30) + heading("Selected work", "03")
    write("profile-work.svg", svg(94, projects_header))
    projects = [
        ("univigate", "UniViGate", "Kazakhstan's universities, mapped", "JAVASCRIPT / TEAM PROJECT"),
        ("zero", "ZERO Model", "A voice-controlled AI agent", "RUST / PYTHON / WEB"),
        ("messenger", "messenger.app", "A messenger for local networks", "PYTHON / PYSIDE6 / SQL"),
        ("portfolio", "personal-hub", "My portfolio and personal space", "HTML / CSS / JAVASCRIPT"),
        ("sendflow", "SendFlow", "WhatsApp messaging and scheduling", "PYTHON / FLASK"),
        ("pdf", "PDF Reader", "PDF content structured as JSON", "PYTHON / PYMUPDF"),
    ]
    for slug, title, description, tech in projects:
        card = rect(0, 0, 900, 220, BG, 30)
        card += text(36, 57, tech, 19, PINK, 700, 'class="mono"')
        card += text(36, 116, title, 40, TEXT, 700) + text(845, 54, "↗", 28, MUTED, 500)
        card += text(36, 164, description, 26, MUTED)
        write(f"project-{slug}.svg", svg(220, card))


QUERY = '''query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount nodes { stargazerCount }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}'''


def github_data():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to fetch real GitHub activity")
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": "k3ng0T"}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "k3ng0t-profile-cards"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise RuntimeError("GitHub did not return the requested public activity")
    return payload["data"]["user"]


def stats(user):
    repos = user["repositories"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for week in weeks for d in week["contributionDays"]]
    longest = run = 0
    for day in days:
        run = run + 1 if day["contributionCount"] else 0
        longest = max(longest, run)
    today = dt.date.today().isoformat()
    recent = [d for d in days if d["date"] <= today]
    if recent and recent[-1]["date"] == today and recent[-1]["contributionCount"] == 0:
        recent.pop()
    current = 0
    for day in reversed(recent):
        if not day["contributionCount"]:
            break
        current += 1
    stats_card = rect(0, 0, 900, 350, BG, 30) + heading("GitHub activity", "05")
    stars = sum(repo["stargazerCount"] for repo in repos["nodes"])
    values = [(cal["totalContributions"], "Contributions · last year"), (repos["totalCount"], "Public repositories"),
              (stars, "Stars earned"), (user["followers"]["totalCount"], "Followers")]
    for i, (value, label) in enumerate(values):
        x = 28 + i*214
        stats_card += rect(x, 83, 202, 92, PANEL, 18)
        stats_card += text(x+19, 122, value, 28, TEXT, 700) + text(x+19, 151, label, 13, MUTED, 500)
    stats_card += text(31, 211, "PUBLIC CONTRIBUTIONS / LAST 26 WEEKS", 12, MUTED, 700, 'class="mono"')
    colors = ["#2b292d", "#724357", "#a7647f", "#d18aa5", "#efbfd0"]
    for wi, week in enumerate(weeks[-26:]):
        for day in week["contributionDays"]:
            weekday = (dt.date.fromisoformat(day["date"]).weekday()+1) % 7
            count = day["contributionCount"]
            level = 0 if count == 0 else 1 if count < 3 else 2 if count < 6 else 3 if count < 10 else 4
            stats_card += rect(31 + wi*22, 225 + weekday*14, 15, 10, colors[level], 3)
    stats_card += text(640, 258, "Updated daily", 16, TEXT, 600)
    stats_card += text(640, 283, "from GitHub", 15, MUTED)
    write("profile-activity.svg", svg(350, stats_card))
    streak = rect(0, 0, 900, 184, BG, 30) + heading("Streak", "06")
    for i, (value, label) in enumerate([(current, "Current streak"), (longest, "Longest · last year")]):
        x = 28 + i*427
        streak += rect(x, 82, 416, 76, PANEL, 18)
        streak += text(x+22, 127, value, 29, PINK if i == 0 else TEXT, 700)
        streak += text(x+80, 127, "days", 15, TEXT, 600) + text(x+135, 127, label, 16, MUTED)
    write("profile-streak.svg", svg(184, streak))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"design", "stats"}:
        raise SystemExit("Usage: profile_cards.py design|stats")
    try:
        design() if sys.argv[1] == "design" else stats(github_data())
    except (RuntimeError, urllib.error.URLError, KeyError) as exc:
        raise SystemExit(f"Could not generate profile cards: {exc}") from exc
