#!/usr/bin/env python3
"""MEGA MASTERPIECE banner generator — Erfix404.
1500x500 SVG, ~1500 lines, all SMIL animations (GitHub-safe).
Combines: aurora gradients, isometric blocks, neural core, meteors,
starfield, data streams, waves, heatmap, HUD, terminal.
"""
import math
import os
import random

random.seed(404)
W, H = 1500, 500
COLORS = ["#a855f7", "#22d3ee", "#ff3278"]
L = []
add = L.append

# ============ HEADER ============
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add("  <defs>")
add('    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">')
add('      <stop offset="0%" stop-color="#030109"/>')
add('      <stop offset="40%" stop-color="#0b0420"/>')
add('      <stop offset="100%" stop-color="#030109"/>')
add("    </linearGradient>")
# aurora
add('    <radialGradient id="aurora1" cx="30%" cy="30%" r="60%">')
add('      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.16"/>')
add('      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>')
add("    </radialGradient>")
add('    <radialGradient id="aurora2" cx="75%" cy="25%" r="55%">')
add('      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.13"/>')
add('      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>')
add("    </radialGradient>")
add('    <radialGradient id="aurora3" cx="50%" cy="85%" r="60%">')
add('      <stop offset="0%" stop-color="#ff3278" stop-opacity="0.1"/>')
add('      <stop offset="100%" stop-color="#ff3278" stop-opacity="0"/>')
add("    </radialGradient>")
# title
add('    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
add('      <stop offset="0%" stop-color="#a855f7"/>')
add('      <stop offset="30%" stop-color="#22d3ee"/>')
add('      <stop offset="65%" stop-color="#a855f7"/>')
add('      <stop offset="100%" stop-color="#ff3278"/>')
add("    </linearGradient>")
add('    <linearGradient id="titleShine" x1="0%" y1="0%" x2="100%" y2="0%">')
add('      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>')
add('      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.5"/>')
add('      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.5"/>')
add('      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>')
add("    </linearGradient>")
add('    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
add('      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.45"/>')
add('      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.45"/>')
add('      <stop offset="100%" stop-color="#ff3278" stop-opacity="0.45"/>')
add("    </linearGradient>")
add('    <linearGradient id="termBg" x1="0%" y1="0%" x2="0%" y2="100%">')
add('      <stop offset="0%" stop-color="#0a0a1a"/>')
add('      <stop offset="100%" stop-color="#04040c"/>')
add("    </linearGradient>")
# core glow gradients — dimmer so code text stays readable
add('    <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">')
add('      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.4"/>')
add('      <stop offset="55%" stop-color="#a855f7" stop-opacity="0.1"/>')
add('      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>')
add("    </radialGradient>")
add('    <radialGradient id="corePulse" cx="50%" cy="50%" r="50%">')
add('      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.32"/>')
add('      <stop offset="60%" stop-color="#22d3ee" stop-opacity="0.07"/>')
add('      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>')
add("    </radialGradient>")
add('    <radialGradient id="vignette" cx="50%" cy="50%" r="72%">')
add('      <stop offset="0%" stop-color="#030109" stop-opacity="0"/>')
add('      <stop offset="100%" stop-color="#030109" stop-opacity="0.55"/>')
add("    </radialGradient>")
# filters
for fid, blur in (("glow", 3.5), ("bigGlow", 9), ("meteorGlow", 4), ("softGlow", 2)):
    add(f'    <filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">')
    add(f'      <feGaussianBlur stdDeviation="{blur}" result="b"/>')
    add("      <feMerge><feMergeNode in=\"b\"/><feMergeNode in=\"SourceGraphic\"/></feMerge>")
    add("    </filter>")
# patterns
add('    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">')
add('      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#22d3ee" stroke-opacity="0.05" stroke-width="1"/>')
add("    </pattern>")
add('    <pattern id="dotGrid" width="44" height="44" patternUnits="userSpaceOnUse">')
add('      <circle cx="2" cy="2" r="1" fill="#a855f7" opacity="0.22"/>')
add("    </pattern>")
# symbols
add('    <g id="hex">')
add('      <path d="M 0 -20 L 17.3 -10 L 17.3 10 L 0 20 L -17.3 10 L -17.3 -10 Z" fill="none" stroke="#22d3ee" stroke-width="1.4" stroke-opacity="0.85"/>')
add('      <circle cx="0" cy="0" r="4" fill="#22d3ee" opacity="0.9"/>')
add("    </g>")
add('    <g id="star">')
add('      <path d="M 0 -4 L 1 -1 L 4 0 L 1 1 L 0 4 L -1 1 L -4 0 L -1 -1 Z" fill="#ffffff"/>')
add("    </g>")
add('    <g id="chip">')
add('      <rect x="-9" y="-9" width="18" height="18" rx="3" fill="none" stroke="#22d3ee" stroke-width="1.2" stroke-opacity="0.8"/>')
add('      <rect x="-3" y="-3" width="6" height="6" rx="1" fill="#22d3ee" opacity="0.7"/>')
add("    </g>")
add('    <g id="isoBlock">')
add('      <path d="M 0 0 L 16 -9 L 32 0 L 16 9 Z" fill="#1f3a6b" stroke="#22d3ee" stroke-opacity="0.7" stroke-width="1"/>')
add('      <path d="M 16 9 L 32 0 L 32 9 L 16 18 Z" fill="#14284f" stroke="#a855f7" stroke-opacity="0.6" stroke-width="1"/>')
add('      <path d="M 0 0 L 16 9 L 16 18 L 0 9 Z" fill="#182f5e" stroke="#ff3278" stroke-opacity="0.5" stroke-width="1"/>')
add("    </g>")
# meteor trails
for mid, c in [("pink", "#ff3278"), ("cyan", "#22d3ee"), ("purple", "#a855f7"), ("amber", "#f59e0b"), ("lime", "#a3e635"), ("blue", "#60a5fa")]:
    add(f'    <linearGradient id="trail-{mid}" x1="0%" y1="0%" x2="100%" y2="0%">')
    add(f'      <stop offset="0%" stop-color="{c}" stop-opacity="0"/>')
    add(f'      <stop offset="100%" stop-color="{c}" stop-opacity="1"/>')
    add("    </linearGradient>")
add("  </defs>")

# ============ BACKGROUND ============
add("")
add("  <!-- ================= BACKGROUND ================= -->")
add(f'  <rect width="{W}" height="{H}" fill="url(#bg)"/>')
add(f'  <rect width="{W}" height="{H}" fill="url(#aurora1)"/>')
add(f'  <rect width="{W}" height="{H}" fill="url(#aurora2)"/>')
add(f'  <rect width="{W}" height="{H}" fill="url(#aurora3)"/>')
add(f'  <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.9"/>')
add(f'  <rect width="{W}" height="{H}" fill="url(#dotGrid)"/>')

# ============ STARFIELD ============
add("")
add("  <!-- ================= STARFIELD (48 twinkling) ================= -->")
add("  <g>")
for i in range(48):
    x = random.randint(8, W - 8)
    y = random.randint(8, 360)
    r = round(random.uniform(0.7, 1.6), 1)
    dur = round(random.uniform(2, 6.5), 1)
    delay = round(random.uniform(0, 3.5), 1)
    col = random.choice(COLORS)
    add(f'    <use href="#star" x="{x}" y="{y}" transform="scale({r})" fill="{col}" opacity="0">')
    add(f'      <animate attributeName="opacity" values="0;{round(random.uniform(0.5, 0.95), 1)};0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>')
    add("    </use>")
add("  </g>")

# ============ PERSPECTIVE FLOOR ============
add("")
add("  <!-- ================= PERSPECTIVE FLOOR GRID ================= -->")
add('  <g opacity="0.75">')
for i in range(16):
    x1 = i * 100 - 60
    x2 = W - x1
    op = round(0.4 - i * 0.024, 3)
    if op > 0.03:
        add(f'    <path d="M {x1} {H} L {W/2} {H - 60 - i * 8} L {x2} {H}" fill="none" stroke="#a855f7" stroke-opacity="{op}" stroke-width="1"/>')
    add(f'    <line x1="{i * 100}" y1="{H}" x2="{i * 100}" y2="{H - 44 - i * 9}" stroke="#22d3ee" stroke-opacity="{max(0.04, 0.28 - i * 0.018)}" stroke-width="1"/>')
add("  </g>")

# ============ ISOMETRIC BLOCK CITY (mini skyline) ============
add("")
add("  <!-- ================= ISOMETRIC BLOCK CITY ================= -->")
add('  <g transform="translate(60, 385)">')
for i, (bx, by, s) in enumerate([
    (0, 0, 1.2), (30, 6, 0.9), (60, 0, 1.4), (96, 8, 0.8),
    (124, 2, 1.1), (158, 0, 1.5), (200, 9, 0.7), (226, 4, 1.0),
]):
    add(f'    <use href="#isoBlock" x="{bx}" y="{by}" transform="scale({s})">')
    add(f'      <animate attributeName="opacity" values="0.75;1;0.75" dur="{2 + i * 0.3:.1f}s" repeatCount="indefinite" begin="{i * 0.2:.1f}s"/>')
    add("    </use>")
add("  </g>")
add('  <g transform="translate(1280, 385)">')
for i, (bx, by, s) in enumerate([
    (0, 4, 1.0), (32, 0, 1.3), (70, 7, 0.85), (100, 2, 1.15), (134, 0, 1.4),
]):
    add(f'    <use href="#isoBlock" x="{bx}" y="{by}" transform="scale({s})">')
    add(f'      <animate attributeName="opacity" values="0.75;1;0.75" dur="{2.4 + i * 0.25:.1f}s" repeatCount="indefinite" begin="{i * 0.25:.1f}s"/>')
    add("    </use>")
add("  </g>")

# ============ WAVES ============
add("")
add("  <!-- ================= WAVES (4 layers) ================= -->")
add('  <g fill="none" stroke="url(#waveGrad)" stroke-width="2">')
for k, (base, amp, dur, op) in enumerate([(430, 22, 8, 1.0), (452, 14, 10, 0.7), (474, 18, 12, 0.5), (496, 10, 9, 0.35)]):
    add(f'    <path d="M 0 {base} Q {W/8} {base - amp} {W/4} {base} T {W/2} {base} T {W*3/4} {base} T {W} {base}" opacity="{op}">')
    add(f'      <animate attributeName="d" values="M 0 {base} Q {W/8} {base - amp} {W/4} {base} T {W/2} {base} T {W*3/4} {base} T {W} {base};M 0 {base} Q {W/8} {base + amp} {W/4} {base} T {W/2} {base} T {W*3/4} {base} T {W} {base};M 0 {base} Q {W/8} {base - amp} {W/4} {base} T {W/2} {base} T {W*3/4} {base} T {W} {base}" dur="{dur}s" repeatCount="indefinite"/>')
    add("    </path>")
add("  </g>")

# ============ DATA STREAMS ============
add("")
add("  <!-- ================= DATA STREAMS (10 columns) ================= -->")
for col in range(10):
    x0 = 660 + col * 22
    color = COLORS[col % 3]
    dur = round(random.uniform(4, 7), 1)
    delay = round(random.uniform(-6, 0), 1)
    add(f'  <g font-family="\'Courier New\',monospace" font-size="10" opacity="0.5">')
    for g in range(18):
        y0 = -30 - g * 22
        add(f'    <text x="{x0}" y="{y0}" fill="{color}">{random.choice("01アイウエオカキクケコサシスセソタチツテト")}</text>')
        add(f'      <animateTransform attributeName="transform" type="translate" values="0,0;0,{H + 60}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>')
    add("  </g>")

# ============ NEURAL CORE ============
add("")
add("  <!-- ================= NEURAL CORE ================= -->")
add('  <g transform="translate(255, 260)">')
add('    <circle r="150" fill="url(#coreGlow)">')
add('      <animate attributeName="r" values="150;168;150" dur="3.2s" repeatCount="indefinite"/>')
add("    </circle>")
add('    <circle r="88" fill="url(#corePulse)">')
add('      <animate attributeName="r" values="88;104;88" dur="2.6s" repeatCount="indefinite"/>')
add("    </circle>")
add('    <circle r="132" fill="none" stroke="#a855f7" stroke-opacity="0.28" stroke-width="1">')
add('      <animate attributeName="r" values="132;146;132" dur="3.8s" repeatCount="indefinite"/>')
add("    </circle>")
add('    <circle r="150" fill="none" stroke="#22d3ee" stroke-opacity="0.15" stroke-width="1">')
add('      <animate attributeName="r" values="150;165;150" dur="4.4s" repeatCount="indefinite"/>')
add("    </circle>")
# ring 1 hexes
add("    <g>")
add('      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="16s" repeatCount="indefinite"/>')
for i in range(6):
    ang = i * 60
    hx = 108 * math.cos(math.radians(ang))
    hy = 108 * math.sin(math.radians(ang))
    add(f'      <use href="#hex" x="{hx:.1f}" y="{hy:.1f}"/>')
add("    </g>")
# ring 2 chips
add('    <g opacity="0.75">')
add('      <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="24s" repeatCount="indefinite"/>')
for i in range(8):
    ang = i * 45 + 22.5
    cx = 68 * math.cos(math.radians(ang))
    cy = 68 * math.sin(math.radians(ang))
    add(f'      <use href="#chip" x="{cx:.1f}" y="{cy:.1f}" transform="scale(1.15)"/>')
add("    </g>")
# ring 3 blinking nodes
add("    <g>")
add('      <animateTransform attributeName="transform" type="rotate" from="180" to="540" dur="28s" repeatCount="indefinite"/>')
for i in range(6):
    ang = i * 60
    nx = 150 * math.cos(math.radians(ang))
    ny = 150 * math.sin(math.radians(ang))
    add(f'      <circle cx="{nx:.1f}" cy="{ny:.1f}" r="4" fill="#ff3278">')
    add(f'        <animate attributeName="opacity" values="0;1;0" dur="2.4s" repeatCount="indefinite" begin="{i * 0.4:.2f}s"/>')
    add("      </circle>")
add("    </g>")
# connecting lines
add('    <g stroke="#22d3ee" stroke-opacity="0.22" stroke-width="1">')
for i in range(6):
    ang = i * 60
    hx = 108 * math.cos(math.radians(ang))
    hy = 108 * math.sin(math.radians(ang))
    nx = 150 * math.cos(math.radians(ang))
    ny = 150 * math.sin(math.radians(ang))
    add(f'      <line x1="{hx:.1f}" y1="{hy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}">')
    add(f'        <animate attributeName="stroke-opacity" values="0.22;0.75;0.22" dur="3s" repeatCount="indefinite" begin="{i * 0.5:.2f}s"/>')
    add("      </line>")
add("    </g>")
# center node
add('    <circle r="18" fill="#22d3ee" opacity="0.28">')
add('      <animate attributeName="r" values="18;26;18" dur="2s" repeatCount="indefinite"/>')
add('      <animate attributeName="opacity" values="0.28;0.65;0.28" dur="2s" repeatCount="indefinite"/>')
add("    </circle>")
add('    <circle r="6" fill="#22d3ee">')
add('      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>')
add("    </circle>")
add("  </g>")

# ============ CIRCUIT TRACES ============
add("")
add("  <!-- ================= CIRCUIT TRACES ================= -->")
for i, d in enumerate([
    "M 40 110 L 130 110 L 160 140 L 240 140",
    "M 40 420 L 120 420 L 150 390 L 230 390",
    "M 1260 110 L 1340 110 L 1370 140 L 1460 140",
    "M 1260 420 L 1330 420 L 1360 390 L 1460 390",
]):
    add(f'  <path d="{d}" fill="none" stroke="{COLORS[i % 3]}" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="6 8">')
    add(f'    <animate attributeName="stroke-dashoffset" values="0;-140" dur="{3 + i}s" repeatCount="indefinite"/>')
    add("  </path>")

# ============ LEFT CODE CHIPS ============
add("")
add("  <!-- ================= LEFT CODE CHIPS ================= -->")
add('  <g font-family="\'Courier New\',monospace" opacity="0.85">')
for i, (code, col) in enumerate([
    ("def build():", "#22d3ee"),
    ("    agent = Erfix()", "#a855f7"),
    ("    return agent", "#22d3ee"),
    ("", ""),
    ("while True:", "#ff3278"),
    ("    ship_code()", "#22d3ee"),
    ("    level_up()", "#a855f7"),
    ("    vibes.check()", "#ff3278"),
]):
    if not code:
        continue
    add(f'    <text x="30" y="{70 + i * 15}" font-size="12" font-weight="bold" fill="{col}">{code}</text>')
add("  </g>")

# ============ METEORS ============
add("")
add("  <!-- ================= METEORS (6 shooting) ================= -->")
meteors = [
    ("python", "#ff3278", "🐍", 160, 58, 9, 0),
    ("cyan", "#22d3ee", "🐙", 420, 62, 8, 2.5),
    ("purple", "#a855f7", "🗄️", 700, 55, 10, 5),
    ("amber", "#f59e0b", "⚡", 950, 60, 7.5, 7.5),
    ("lime", "#a3e635", "🧠", 300, 65, 11, 10),
    ("blue", "#60a5fa", "🔥", 1150, 58, 9.5, 12.5),
]
add('  <g filter="url(#meteorGlow)">')
for name, trail, emoji, start_x, ang_deg, dur, delay in meteors:
    ang = math.radians(ang_deg)
    reach = H + 200
    dx = math.cos(ang) * reach
    dy = math.sin(ang) * reach
    add(f'    <g>')
    add(f'      <line x1="{start_x}" y1="-50" x2="{start_x + 50}" y2="-20" stroke="url(#trail-{name})" stroke-width="2.5" stroke-linecap="round">')
    add(f'        <animate attributeName="x1" values="{start_x};{start_x + dx:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add(f'        <animate attributeName="y1" values="-50;{-50 + dy:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add(f'        <animate attributeName="x2" values="{start_x + 50};{start_x + 50 + dx:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add(f'        <animate attributeName="y2" values="-20;{-20 + dy:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add("      </line>")
    add("      <g>")
    add(f'        <animate attributeName="x" values="{start_x + 25};{start_x + 25 + dx:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add(f'        <animate attributeName="y" values="{-35};{-35 + dy:.0f}" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>')
    add(f'        <text font-family="monospace" font-size="26" fill="{trail}" text-anchor="middle">{emoji}</text>')
    add("      </g>")
    add("    </g>")
add("  </g>")

# ============ TITLE ============
add("")
add("  <!-- ================= TITLE (ERFIX) ================= -->")
add("  <g>")
add('    <text x="470" y="215" font-family="Arial,Helvetica,sans-serif" font-size="118" font-weight="900" letter-spacing="8" fill="#ff3278" opacity="0.22">')
add("      ERFIX")
add('      <animate attributeName="opacity" values="0.3;0;0.3;0;0.3" dur="4s" repeatCount="indefinite" keyTimes="0;0.06;0.12;0.2;1"/>')
add("    </text>")
add('    <text x="470" y="215" font-family="Arial,Helvetica,sans-serif" font-size="118" font-weight="900" letter-spacing="8" fill="url(#titleGrad)" filter="url(#glow)" stroke="#030109" stroke-width="2" paint-order="stroke">')
add('      <animate attributeName="opacity" values="1;0.55;1" dur="3s" repeatCount="indefinite"/>')
add("      ERFIX")
add("    </text>")
add('    <text x="470" y="215" font-family="Arial,Helvetica,sans-serif" font-size="118" font-weight="900" letter-spacing="8" fill="url(#titleShine)" opacity="0">')
add('      <animate attributeName="opacity" values="0;0.9;0" dur="4.5s" repeatCount="indefinite"/>')
add("      ERFIX")
add("    </text>")
add('    <text x="492" y="258" font-family="\'Courier New\',monospace" font-size="17" fill="#22d3ee" opacity="0.9">')
add('      <animate attributeName="opacity" values="0.9;0.5;0.9" dur="2.8s" repeatCount="indefinite"/>')
add("      &gt; erfan ashouri · python · ai agents · n8n")
add("    </text>")
add('    <text x="492" y="278" font-family="\'Courier New\',monospace" font-size="11" fill="#22d3ee" opacity="0.75" filter="url(#glow)">')
add("      import intelligence; from future import coding · MEGA v1.0")
add("    </text>")
add("  </g>")

# ============ HEATMAP ============
add("")
add("  <!-- ================= MINI CONTRIBUTION HEATMAP (5x14) ================= -->")
add('  <g transform="translate(1000, 60)">')
add('    <text x="0" y="-6" font-family="\'Courier New\',monospace" font-size="10" fill="#a855f7" opacity="0.7">CONTRIBUTION MATRIX</text>')
heat_colors = ["#141430", "#1f3a5f", "#a855f7", "#22d3ee", "#ff3278"]
for row in range(5):
    for colw in range(14):
        intensity = random.choices([0, 1, 2, 3, 4], weights=[30, 25, 20, 15, 10])[0]
        x = colw * 11
        y = row * 11
        add(f'    <rect x="{x}" y="{y}" width="9" height="9" rx="1.5" fill="{heat_colors[intensity]}">')
        if intensity >= 3 and random.random() < 0.7:
            add(f'      <animate attributeName="opacity" values="0.55;1;0.55" dur="{random.uniform(1.5, 3):.1f}s" repeatCount="indefinite" begin="{random.uniform(0, 2):.1f}s"/>')
        add("    </rect>")
add("  </g>")

# ============ LANGUAGE BARS ============
add("")
add("  <!-- ================= MINI LANGUAGE BARS ================= -->")
langs = [("Python", 78, "#a855f7"), ("JavaScript", 22, "#22d3ee"), ("Shell", 10, "#ff3278"), ("n8n", 6, "#f59e0b")]
add('  <g transform="translate(1000, 178)">')
add('    <text x="0" y="-6" font-family="\'Courier New\',monospace" font-size="10" fill="#a855f7" opacity="0.7">STACK SPLIT</text>')
for i, (name, pct, col) in enumerate(langs):
    y = i * 24
    add(f'    <text x="0" y="{y + 9}" font-family="\'Courier New\',monospace" font-size="11" fill="#22d3ee" opacity="0.9">{name}</text>')
    add(f'    <rect x="80" y="{y + 2}" width="150" height="8" rx="4" fill="#141430"/>')
    add(f'    <rect x="80" y="{y + 2}" width="0" height="8" rx="4" fill="{col}">')
    add(f'      <animate attributeName="width" values="0;{pct * 1.5:.0f}" dur="2.5s" repeatCount="indefinite" begin="{i * 0.4}s"/>')
    add("    </rect>")
add("  </g>")

# ============ TERMINAL ============
add("")
add("  <!-- ================= TERMINAL ================= -->")
add('  <g transform="translate(1000, 248)">')
add('    <rect width="410" height="222" rx="10" fill="url(#termBg)" stroke="#22d3ee" stroke-opacity="0.4" stroke-width="1.2"/>')
add('    <rect width="410" height="30" rx="10" fill="#22d3ee" fill-opacity="0.08"/>')
add('    <circle cx="22" cy="15" r="5" fill="#ff3278" opacity="0.95"/>')
add('    <circle cx="38" cy="15" r="5" fill="#f59e0b" opacity="0.95"/>')
add('    <circle cx="54" cy="15" r="5" fill="#22d3ee" opacity="0.95"/>')
add('    <text x="200" y="20" text-anchor="middle" font-family="\'Courier New\',monospace" font-size="11" fill="#22d3ee" opacity="0.85">erfix@core:~/mega</text>')
boot = [
    ("$ ./erfix --deploy --ultra --mega", "#22d3ee", 0.95),
    ("[init] loading neural core ..........", "#a855f7", 0.85),
    ("[ok]   agent modules linked", "#a855f7", 0.85),
    ("[ok]   python runtime ready", "#22d3ee", 0.9),
    ("[ok]   n8n workflows synced", "#22d3ee", 0.9),
    ("[ok]   skillicons loaded", "#22d3ee", 0.9),
    ("[warn] vibes: maximum 🔥", "#ff3278", 0.95),
    ("[info] building mega profile...", "#f59e0b", 0.85),
    ("$ git commit -m \"mega ship\"", "#22d3ee", 0.9),
]
for i, (txt, col, op) in enumerate(boot):
    add(f'    <text x="16" y="{46 + i * 15}" font-family="\'Courier New\',monospace" font-size="11" fill="{col}" opacity="{op}">{txt}</text>')
add('    <rect x="16" y="190" width="330" height="7" rx="3.5" fill="#22d3ee" fill-opacity="0.12"/>')
add('    <rect x="16" y="190" width="0" height="7" rx="3.5" fill="url(#titleGrad)">')
add('      <animate attributeName="width" values="0;330" dur="4.5s" repeatCount="indefinite"/>')
add("    </rect>")
add('    <text x="16" y="214" font-family="\'Courier New\',monospace" font-size="10" fill="#22d3ee" opacity="0.7">status: DEPLOYING MEGA MASTERPIECE ▓▓▓▓▓▓░</text>')
add('    <text x="340" y="214" font-family="\'Courier New\',monospace" font-size="11" fill="#22d3ee">')
add('      <animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/>')
add("      █")
add("    </text>")
add("  </g>")

# ============ HUD ============
add("")
add("  <!-- ================= HUD ================= -->")
add('  <g transform="translate(1340, 26)">')
add('    <rect x="0" y="0" width="126" height="24" rx="12" fill="#0a0a18" stroke="#22d3ee" stroke-opacity="0.45" stroke-width="1"/>')
add('    <circle cx="15" cy="12" r="4" fill="#22d3ee">')
add('      <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>')
add("    </circle>")
add('    <text x="28" y="16" font-family="\'Courier New\',monospace" font-size="10" fill="#22d3ee">AI ONLINE</text>')
add("  </g>")
add('  <text x="750" y="34" text-anchor="middle" font-family="\'Courier New\',monospace" font-size="10" fill="#22d3ee" opacity="0.6" letter-spacing="5">')
add("    SYS://ERFIX-404")
add('    <animate attributeName="opacity" values="0.6;0.2;0.6" dur="5s" repeatCount="indefinite"/>')
add("  </text>")
add('  <line x1="0" y1="12" x2="1500" y2="12" stroke="#a855f7" stroke-opacity="0.15" stroke-width="1"/>')

# ============ CORNER BRACKETS ============
add("")
add("  <!-- ================= CORNER BRACKETS ================= -->")
add('  <g stroke="#22d3ee" stroke-opacity="0.3" stroke-width="1.5" fill="none">')
add('    <path d="M 16 34 L 16 16 L 34 16"/>')
add('    <path d="M 1484 34 L 1484 16 L 1466 16"/>')
add('    <path d="M 16 466 L 16 484 L 34 484"/>')
add('    <path d="M 1484 466 L 1484 484 L 1466 484"/>')
add("  </g>")

# ============ SPARK DOTS ============
add("")
add("  <!-- ================= SPARK DOTS ================= -->")
add("  <g>")
for i in range(5):
    add(f'    <circle cx="{520 + i * 95}" cy="243" r="2" fill="{COLORS[i % 3]}">')
    add(f'      <animate attributeName="opacity" values="0;1;0" dur="3.2s" repeatCount="indefinite" begin="{i * 0.64:.2f}s"/>')
    add("    </circle>")
add("  </g>")

# ============ STATUS BAR ============
add("")
add("  <!-- ================= STATUS BAR ================= -->")
add('  <g transform="translate(0, 464)">')
add('    <line x1="0" y1="0" x2="1500" y2="0" stroke="#a855f7" stroke-opacity="0.45" stroke-width="2"/>')
add('    <rect y="4" width="1500" height="30" fill="#a855f7" fill-opacity="0.08"/>')
add('    <text x="30" y="25" font-family="\'Courier New\',monospace" font-size="15" fill="#a855f7" font-weight="bold">● 13 repos · Python · n8n</text>')
add('    <text x="420" y="25" font-family="\'Courier New\',monospace" font-size="15" fill="#22d3ee" font-weight="bold">▲ 3 stars · 9 commits</text>')
add('    <text x="820" y="25" font-family="\'Courier New\',monospace" font-size="15" fill="#ff3278" font-weight="bold">◉ EST. 2024 · SHAHRUD, IR</text>')
add('    <text x="1470" y="25" font-family="\'Courier New\',monospace" font-size="15" fill="#22d3ee" opacity="0.95" text-anchor="end">erfix404 · MEGA v1.0</text>')
add("  </g>")

# ============ SCANLINES + VIGNETTE ============
add("")
add("  <!-- ================= SCANLINES + VIGNETTE ================= -->")
add('  <g stroke="#22d3ee" stroke-opacity="0.03" stroke-width="1">')
for y in range(20, 500, 40):
    add(f'    <line x1="0" y1="{y}" x2="1500" y2="{y}"/>')
add("  </g>")
add(f'  <rect width="{W}" height="{H}" fill="url(#vignette)"/>')
add("</svg>")
add("")

out = "\n".join(L)
os.makedirs("assets", exist_ok=True)
path = "assets/banner.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write(out)
print(f"✅ MEGA banner: {out.count(chr(10))} lines, {len(out)} bytes")
