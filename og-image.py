#!/usr/bin/env python3
"""Write the page that assets/og.png, the preview image for shared links,
is a screenshot of: the name, the tagline, and the hero's diagram.

    og-image.py SITE

SITE is an assembled site (see README.md). Render the page it writes,
SITE/og-card.html, at 1200x630 with every part of the diagram lit:

    google-chrome --headless --hide-scrollbars --force-prefers-reduced-motion \\
      --window-size=1200,630 --screenshot=assets/og.png SITE/og-card.html
"""
import pathlib
import re
import sys

site = pathlib.Path(sys.argv[1])
home = (site / "index.html").read_text()
svg = re.search(r'<svg viewBox="0 0 400 560".*?</svg>', home, re.S).group(0)
(site / "og-card.html").write_text(f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="assets/style.css">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: var(--bg); display: grid; grid-template-columns: 1fr 380px; gap: 40px;
         align-items: center; padding: 0 64px; box-sizing: border-box; }}
  .brand {{ display: flex; align-items: center; gap: 16px; font-weight: 700; font-size: 44px; color: var(--text); }}
  .brand img {{ width: 64px; height: 64px; }}
  .kick {{ margin: 28px 0 10px; color: var(--accent); font-weight: 700; font-size: 26px; }}
  h1 {{ margin: 0; font-size: 56px; line-height: 1.1; letter-spacing: -0.02em; color: var(--text); }}
  .url {{ margin-top: 30px; color: var(--muted); font-size: 24px; }}
  .tour {{ margin: 0; }}
  .tour svg {{ width: 380px; }}
</style>
</head>
<body>
<div>
  <div class="brand"><img src="assets/logo.svg" alt="">Sparewall</div>
  <p class="kick">Open-source Linux firewall</p>
  <h1>One document.<br>One image.<br>One node or a pair.</h1>
  <p class="url">sparewall.org</p>
</div>
<figure class="tour">{svg}</figure>
</body>
</html>
''')
