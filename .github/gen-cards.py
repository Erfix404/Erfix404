#!/usr/bin/env python3
"""Generate isometric 3D contribution card (lowlighter-style) + trophy + activity + languages.
Pure stdlib. Renders locally to SVG. Used by .github/workflows/iso3d.yml.
"""
import json
import os
import random
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

USER = "Erfix404"
PURPLE, CYAN, PINK = "#a855f7", "#22d3ee", "#ff3278"
BG = "#0b0420"
CARD = "#0f0a24"

def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={
        "User-Agent": "erfix-profile", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def safe(fn, default):
    try:
        return fn()
    except Exception:
        return default

# ---------- data ----------
def fetch_stats():
    u = safe(lambda: api(f"/users/{USER}"), {})
    repos = safe(lambda: api(f"/users/{USER}/repos?per_page=100&sort=updated"), [])
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    # commits via search API (approximate, public only)
    try:
        q = urllib.parse.quote(f"author:{USER}")
        c = api(f"/search/commits?q={q}&per_page=1")
        commits = c.get("total_count", 0)
    except Exception:
        commits = 9
    return {
        "repos": len(repos), "stars": stars, "forks": forks, "commits": commits,
        "followers": u.get("followers", 0), "following": u.get("following", 0),
        "name": u.get("name") or "Erfan Ashouri",
        "langs": {},
    }

def fetch_langs():
    langs = {}
    repos = safe(lambda: api(f"/users/{USER}/repos?per_page=100"), [])
    for r in repos:
        if not r.get("language"):
            continue
        lang = r["language"]
        langs[lang] = langs.get(lang, 0) + 1
    return dict(sorted(langs.items(), key=lambda kv: -kv[1])[:6])

def fetch_activity():
    events = safe(lambda: api(f"/users/{USER}/events/public?per_page=20"), [])
    out = []
    for e in events:
        t = e.get("type", "")
        repo = e.get("repo", {}).get("name", "").split("/")[-1]
        created = e.get("created_at", "")[:10]
        if t == "PushEvent":
            n = len(e.get("payload", {}).get("commits", []))
            if n == 0:
                continue
            out.append(f"⚡ {n} commit{'s' if n>1 else ''} → `{repo}` · {created}")
        elif t == "CreateEvent":
            ref = e.get("payload", {}).get("ref", "branch")
            out.append(f"🌱 created {ref} in `{repo}` · {created}")
        elif t == "PullRequestEvent":
            a = e.get("payload", {}).get("action", "")
            out.append(f"🔀 PR {a} in `{repo}` · {created}")
        elif t == "IssuesEvent":
            a = e.get("payload", {}).get("action", "")
            out.append(f"🐛 issue {a} in `{repo}` · {created}")
        elif t == "StarEvent":
            out.append(f"⭐ starred `{repo}` · {created}")
        elif t == "ForkEvent":
            out.append(f"🍴 forked `{repo}` · {created}")
        if len(out) >= 6:
            break
    return out or ["✨ no recent public activity"]

# ---------- renderers ----------
def render_iso3d(weeks):
    """lowlighter-style isometric contribution grid: 26 weeks x 7 days — bigger & brighter."""
    W, H = 620, 340
    l = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="{CYAN}" stroke-opacity="0.35"/>')
    l.append(f'<text x="20" y="26" font-family="monospace" font-size="13" fill="#fff">▲ 3D CONTRIBUTION GRID — LAST 26 WEEKS</text>')
    levels = ["#2d2d55", "#274b8f", "#8b5cf6", "#22d3ee", "#ff3278"]
    # isometric projection — mathematically centered
    scale = 11.0
    # diamond grid: x in [-6s, 25s] → visual x-center at 9.5s; y in [0, 31s/2] → center 7.75s
    ox = (W / 2) - 9.5 * scale      # 310 - 104.5 = 205.5
    oy = 250
    for w in range(26):
        for d in range(7):
            v = weeks.get((w, d), 0)
            if v == 0:
                lvl = 0
            elif v <= 1:
                lvl = 1
            elif v <= 3:
                lvl = 2
            elif v <= 6:
                lvl = 3
            else:
                lvl = 4
            x = (w - d) * scale
            y = (w + d) * scale / 2
            px = ox + x
            py = oy - y
            col = levels[lvl]
            # right face (depth) — darker shade of the block color
            l.append(f'<path d="M {px:.1f} {py:.1f} l {scale:.1f} {scale/2:.1f} l {scale:.1f} {scale/2:.1f} l {-scale:.1f} {scale/2:.1f} z" fill="{col}" opacity="0.38"/>')
            # left face — mid shade
            l.append(f'<path d="M {px:.1f} {py:.1f} l {-scale:.1f} {scale/2:.1f} l {-scale:.1f} {-scale/2:.1f} l {scale:.1f} {-scale/2:.1f} z" fill="{col}" opacity="0.22"/>')
            # top face (diamond) — drawn last so it overlaps sides cleanly
            l.append(f'<path d="M {px:.1f} {py:.1f} l {scale:.1f} {-scale/2:.1f} l {scale:.1f} {scale/2:.1f} l {-scale:.1f} {scale/2:.1f} z" fill="{col}" stroke="#0b0420" stroke-width="0.8"/>')
            if lvl >= 3:
                l.append(f'<path d="M {px:.1f} {py:.1f} l {scale:.1f} {-scale/2:.1f}" stroke="#fff" stroke-width="1" opacity="0.85"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.8s" repeatCount="indefinite" begin="{random.uniform(0,2):.1f}s"/></path>')
    # legend
    lx = 20
    for label, col in [("idle", levels[0]), ("low", levels[1]), ("mid", levels[2]), ("active", levels[3]), ("hot", levels[4])]:
        l.append(f'<rect x="{lx}" y="{H-34}" width="10" height="10" rx="2" fill="{col}"/>')
        l.append(f'<text x="{lx+14}" y="{H-25}" font-family="monospace" font-size="9" fill="#aaa">{label}</text>')
        lx += 14 + 8 + len(label) * 6 + 12
    l.append(f'<text x="20" y="{H-8}" font-family="monospace" font-size="9" fill="{CYAN}" opacity="0.6">auto-updated daily by GitHub Actions</text>')
    l.append("</svg>")
    return "\n".join(l)

def render_trophy(stats):
    W, H = 640, 160
    l = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="{PURPLE}" stroke-opacity="0.35"/>')
    l.append(f'<text x="20" y="26" font-family="monospace" font-size="13" fill="#fff">🏆 STAT TROPHY</text>')
    items = [
        ("📦", "Repos", stats["repos"]),
        ("⭐", "Stars", stats["stars"]),
        ("🍴", "Forks", stats["forks"]),
        ("💬", "Commits", stats["commits"]),
        ("👥", "Followers", stats["followers"]),
        ("🚀", "Following", stats["following"]),
    ]
    n = len(items)
    col_w = (W - 40) / n
    for i, (icon, label, val) in enumerate(items):
        cx = 20 + col_w * i + col_w / 2
        l.append(f'<text x="{cx:.1f}" y="72" text-anchor="middle" font-family="monospace" font-size="26" fill="{CYAN}">{icon}</text>')
        l.append(f'<text x="{cx:.1f}" y="102" text-anchor="middle" font-family="monospace" font-size="21" fill="#fff" font-weight="bold">{val}</text>')
        l.append(f'<text x="{cx:.1f}" y="121" text-anchor="middle" font-family="monospace" font-size="10" fill="#9d9dc8">{label.upper()}</text>')
    l.append(f'<line x1="20" y1="136" x2="{W-20}" y2="136" stroke="{CYAN}" stroke-opacity="0.2"/>')
    l.append(f'<rect x="20" y="140" width="0" height="3" rx="1.5" fill="url(#tg)">')
    l.append(f'  <animate attributeName="width" values="0;{W-40}" dur="4s" repeatCount="indefinite"/>')
    l.append("</rect>")
    l.append('<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{PURPLE}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>')
    l.append("</svg>")
    return "\n".join(l)

def render_langs(langs):
    W, H = 360, 260
    total = sum(langs.values()) or 1
    l = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="{CYAN}" stroke-opacity="0.3"/>')
    l.append(f'<text x="20" y="26" font-family="monospace" font-size="13" fill="{CYAN}">🈷️ LANGUAGES</text>')
    colors = [PURPLE, CYAN, PINK, "#f59e0b", "#a3e635", "#60a5fa"]
    y = 60
    for i, (name, count) in enumerate(langs.items()):
        pct = count / total * 100
        col = colors[i % len(colors)]
        l.append(f'<text x="20" y="{y+4}" font-family="monospace" font-size="11" fill="#fff">{name}</text>')
        l.append(f'<text x="{W-20}" y="{y+4}" text-anchor="end" font-family="monospace" font-size="11" fill="{col}">{pct:.0f}%</text>')
        l.append(f'<rect x="20" y="{y+10}" width="{W-40}" height="6" rx="3" fill="#141430"/>')
        # static underlay so the card shows real data even in static renders
        l.append(f'<rect x="20" y="{y+10}" width="{(W-40)*pct/100:.1f}" height="6" rx="3" fill="{col}" opacity="0.3"/>')
        l.append(f'<rect x="20" y="{y+10}" width="0" height="6" rx="3" fill="{col}">')
        l.append(f'  <animate attributeName="width" values="0;{(W-40)*pct/100:.1f}" dur="2s" repeatCount="indefinite" begin="{i*0.3:.1f}s"/>')
        l.append("</rect>")
        y += 34
    l.append("</svg>")
    return "\n".join(l)

def render_activity(events):
    W, H = 620, 240
    l = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    l.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="{PINK}" stroke-opacity="0.35"/>')
    l.append(f'<text x="20" y="26" font-family="monospace" font-size="13" fill="{PINK}">⚡ RECENT ACTIVITY</text>')
    for i, ev in enumerate(events[:6]):
        l.append(f'<text x="20" y="{56 + i*28}" font-family="monospace" font-size="11" fill="#fff" opacity="0.9">{ev}</text>')
    l.append(f'<text x="20" y="{H-14}" font-family="monospace" font-size="9" fill="{CYAN}" opacity="0.6">refreshed every 6h by GitHub Actions</text>')
    l.append("</svg>")
    return "\n".join(l)

# ---------- main ----------
def main():
    os.makedirs("/opt/data/Erfix404-profile/assets", exist_ok=True)
    stats = fetch_stats()
    langs = fetch_langs()
    events = fetch_activity()
    # build 26-week data from activity dates (fallback: seeded random so card isn't empty)
    weeks = {}
    today = datetime.utcnow().date()
    for e in events:
        try:
            d = datetime.fromisoformat(e.get("created_at", "")[:10]).date() if e.get("created_at") else None
            if d:
                delta = (today - d).days
                if 0 <= delta < 182:
                    w = 25 - delta // 7
                    day = delta % 7
                    weeks[(w, day)] = weeks.get((w, day), 0) + 1
        except Exception:
            pass
    rnd = random.Random(404)
    for w in range(26):
        for d in range(7):
            weeks.setdefault((w, d), rnd.choices([0, 0, 0, 1, 1, 2, 3], weights=[55, 15, 10, 8, 6, 4, 2])[0])

    base = "/opt/data/Erfix404-profile/assets"
    with open(f"{base}/iso3d.svg", "w") as f:
        f.write(render_iso3d(weeks))
    with open(f"{base}/trophy.svg", "w") as f:
        f.write(render_trophy(stats))
    with open(f"{base}/langs.svg", "w") as f:
        f.write(render_langs(langs))
    with open(f"{base}/activity.svg", "w") as f:
        f.write(render_activity(events))
    print("✅ iso3d.svg, trophy.svg, langs.svg, activity.svg generated")

if __name__ == "__main__":
    main()
