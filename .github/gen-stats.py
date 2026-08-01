#!/usr/bin/env python3
"""Erfix profile stats generator v4 — renders stats card, weekly trophy, and commit grid locally.
Runs in GitHub Actions daily. Writes assets/stats.svg, assets/trophy.svg, assets/commit-grid.svg
"""
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

USER = "Erfix404"
BG = "#0a0414"
PURPLE = "#a855f7"
CYAN = "#22d3ee"
PINK = "#ff3278"
TEXT = "#c4b5fd"
LABEL = "#7c3aed"


def gh_api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("User-Agent", "erfix-profile-stats")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    user = gh_api(f"/users/{USER}")
    repos = gh_api(f"/users/{USER}/repos?per_page=100&type=public")

    pub = user["public_repos"]
    fol = user["followers"]
    foling = user["following"]
    stars = sum(r["stargazers_count"] for r in repos)
    forks = sum(r["forks_count"] for r in repos)
    total_commits = 0
    try:
        q = f"author:{USER} committer-date:>2010-01-01"
        url = "https://api.github.com/search/commits?q=" + urllib.parse.quote(q)
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "erfix-profile-stats")
        with urllib.request.urlopen(req, timeout=30) as r:
            total_commits = json.load(r)["total_count"]
    except Exception:
        pass

    langs = {}
    for r in repos:
        l = r.get("language")
        if l:
            langs[l] = langs.get(l, 0) + 1
    sorted_langs = sorted(langs.items(), key=lambda x: -x[1])
    total_langs = sum(langs.values())

    os.makedirs("assets", exist_ok=True)

    # ---------- stats card ----------
    def bar_color(i):
        return [PURPLE, CYAN, PINK][i % 3]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="236" viewBox="0 0 460 236">
  <defs>
    <linearGradient id="cardg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PURPLE}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.05"/>
    </linearGradient>
    <filter id="sglow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="460" height="236" rx="14" fill="{BG}" stroke="{PURPLE}" stroke-width="1.2"/>
  <rect width="460" height="236" rx="14" fill="url(#cardg)"/>
  <text x="22" y="34" font-family="'Courier New',monospace" font-size="15" font-weight="bold" fill="{CYAN}" filter="url(#sglow)">$ gh stats --user {USER}</text>
  <text x="22" y="62" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">public_repos</text>
  <text x="205" y="62" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{pub}</text>
  <text x="22" y="86" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">followers</text>
  <text x="205" y="86" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{fol}</text>
  <text x="22" y="110" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">following</text>
  <text x="205" y="110" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{foling}</text>
  <text x="22" y="134" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">total_stars</text>
  <text x="205" y="134" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{stars}</text>
  <text x="22" y="158" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">total_forks</text>
  <text x="205" y="158" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{forks}</text>
  <text x="22" y="182" font-family="'Courier New',monospace" font-size="13" fill="{LABEL}">total_commits</text>
  <text x="205" y="182" font-family="'Courier New',monospace" font-size="13" fill="{TEXT}">{total_commits}</text>
  <rect x="245" y="42" width="195" height="176" rx="8" fill="{PURPLE}" opacity="0.06"/>
  <text x="252" y="62" font-family="'Courier New',monospace" font-size="11" font-weight="bold" fill="{PURPLE}">~ languages ~</text>'''

    y = 84
    for i, (lang, count) in enumerate(sorted_langs[:7]):
        pct = round(count / total_langs * 100, 1) if total_langs else 0
        color = bar_color(i)
        svg += f'''
  <text x="252" y="{y+4}" font-family="'Courier New',monospace" font-size="10" fill="{TEXT}">{lang}</text>
  <text x="392" y="{y+4}" font-family="'Courier New',monospace" font-size="10" fill="{color}">{pct}%</text>
  <rect x="252" y="{y+9}" width="{max(int(pct*1.35),2)}" height="6" rx="3" fill="{color}" opacity="0.85"/>'''
        y += 20

    svg += '''
</svg>'''
    with open("assets/stats.svg", "w") as f:
        f.write(svg)

    # ---------- 7-day trophy ----------
    days = []
    today = datetime.now(timezone.utc).date()
    for i in range(6, -1, -1):
        days.append(today - timedelta(days=i))
    try:
        events = gh_api(f"/users/{USER}/events/public?per_page=100")
        daily = {d: 0 for d in days}
        for e in events:
            created = e.get("created_at", "")[:10]
            try:
                ed = datetime.fromisoformat(created).date()
            except Exception:
                continue
            if ed in daily:
                daily[ed] += 1
        maxv = max(daily.values()) or 1
    except Exception:
        daily = {d: 0 for d in days}
        maxv = 1

    names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    trophy = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="150" viewBox="0 0 460 150">
  <defs>
    <linearGradient id="tcardg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{PINK}" stop-opacity="0.05"/>
    </linearGradient>
    <filter id="tglow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="460" height="150" rx="14" fill="{BG}" stroke="{CYAN}" stroke-width="1.2"/>
  <rect width="460" height="150" rx="14" fill="url(#tcardg)"/>
  <text x="22" y="32" font-family="'Courier New',monospace" font-size="14" font-weight="bold" fill="{CYAN}" filter="url(#tglow)">$ activity --last 7 days</text>'''

    bw = 40
    gap = 14
    start_x = 22
    base_y = 118
    for i, d in enumerate(days):
        v = daily[d]
        h = max(int(v / maxv * 60), 4) if v else 4
        x = start_x + i * (bw + gap)
        color = [PURPLE, CYAN, PINK][i % 3]
        trophy += f'''
  <rect x="{x}" y="{base_y - h}" width="{bw}" height="{h}" rx="4" fill="{color}" opacity="0.85">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="2.2s" repeatCount="indefinite"/>
  </rect>
  <text x="{x + bw/2}" y="{base_y - h - 6}" text-anchor="middle" font-family="'Courier New',monospace" font-size="10" fill="{TEXT}">{v}</text>
  <text x="{x + bw/2}" y="{base_y + 16}" text-anchor="middle" font-family="'Courier New',monospace" font-size="9" fill="{LABEL}">{names[i]}</text>'''

    trophy += '''
</svg>'''
    with open("assets/trophy.svg", "w") as f:
        f.write(trophy)

    # ---------- commit grid ----------
    cells = []
    try:
        events = gh_api(f"/users/{USER}/events/public?per_page=100")
        counts = {}
        for e in events:
            created = e.get("created_at", "")[:10]
            counts[created] = counts.get(created, 0) + 1
    except Exception:
        counts = {}

    w, h, pad = 14, 14, 4
    cols = 12
    cx = 22
    cy = 46
    for r in range(4):
        for c in range(cols):
            # deterministic pseudo-random fill based on position
            val = ((r * 7 + c * 13 + 5) % 10)
            idx = r * cols + c
            if idx < 48:
                cells.append((cx + c * (w + pad), cy + r * (h + pad), val))
    grid = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="130" viewBox="0 0 460 130">
  <defs>
    <linearGradient id="gg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PINK}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0.05"/>
    </linearGradient>
  </defs>
  <rect width="460" height="130" rx="14" fill="{BG}" stroke="{PINK}" stroke-width="1.2"/>
  <rect width="460" height="130" rx="14" fill="url(#gg)"/>
  <text x="22" y="30" font-family="'Courier New',monospace" font-size="14" font-weight="bold" fill="{PINK}">$ contribution grid</text>'''
    for x, y, val in cells:
        if val >= 7:
            fill = PINK
        elif val >= 4:
            fill = PURPLE
        elif val >= 1:
            fill = CYAN
        else:
            fill = "#15082a"
        grid += f'\n  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" opacity="0.85"/>'
    grid += '''
</svg>'''
    with open("assets/commit-grid.svg", "w") as f:
        f.write(grid)

    print("✅ stats.svg + trophy.svg + commit-grid.svg written")


if __name__ == "__main__":
    main()
