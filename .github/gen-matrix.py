#!/usr/bin/env python3
"""Build the final Matrix-rain banner (animated SMIL + static glyphs for initial paint).
Colors: Erfix neon palette (purple/cyan/pink). Output: assets/matrix-banner.svg
"""
import os
import random

random.seed(42)

W, H = 1200, 300
GLYPHS = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF"
COLORS = ["#a855f7", "#22d3ee", "#ff3278"]

parts = []
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="mg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#ff3278" stop-opacity="0.9"/>
    </linearGradient>
    <radialGradient id="mv" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#050208" stop-opacity="0"/>
      <stop offset="100%" stop-color="#050208" stop-opacity="0.55"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="#050208"/>
  <rect width="{W}" height="{H}" fill="url(#mv)"/>''')

# static glyph columns (initial paint + static-render safety)
n_cols = W // 28
for c in range(n_cols):
    x = 6 + c * 28
    n_glyphs = random.randint(3, 10)
    y = random.randint(30, H - 20)
    color = COLORS[c % 3]
    for i in range(n_glyphs):
        gy = y - i * 22
        if gy < 10:
            continue
        op = max(0.15, 0.85 - i * 0.12)
        parts.append(f'<text x="{x}" y="{gy}" fill="{color}" opacity="{op:.2f}" font-family="monospace" font-size="17">{random.choice(GLYPHS)}</text>')

# animated columns (SMIL rain)
for c in range(n_cols):
    x = 6 + c * 28
    color = COLORS[c % 3]
    dur = round(random.uniform(2.2, 4.5), 2)
    delay = round(random.uniform(-4.5, 0), 2)
    n = random.randint(8, 16)
    for i in range(n):
        y0 = -20 - i * 24
        parts.append(
            f'<text x="{x}" y="{y0}" fill="{color}" font-family="monospace" font-size="17" opacity="0.85">'
            f'{random.choice(GLYPHS)}'
            f'<animateTransform attributeName="transform" type="translate" values="0,0;0,{H + 60}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.15;0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</text>'
        )

parts.append('</svg>\n')
out = "".join(parts)
os.makedirs("assets", exist_ok=True)
with open("assets/matrix-banner.svg", "w") as f:
    f.write(out)
print(f"✅ matrix-banner.svg written ({len(out)} bytes, {n_cols} columns)")
