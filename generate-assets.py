#!/usr/bin/env python3
"""Generate animated background assets for the 3ni8ma profile README."""
import random, xml.etree.ElementTree as ET

random.seed(42)

TEAL = "#00F5D4"
CHERRY = "#FF0055"
SLATE = "#C9D1D9"
BG = "#0D1117"
BORDER = "#30363D"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def banner_svg():
    W, H = 1920, 420
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">')
    parts.append('<defs>')
    parts.append(f'<radialGradient id="glowTeal" cx="0.5" cy="0.5" r="0.5"><stop offset="0%" stop-color="{TEAL}" stop-opacity="0.16"/><stop offset="100%" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>')
    parts.append(f'<radialGradient id="glowCherry" cx="0.5" cy="0.5" r="0.5"><stop offset="0%" stop-color="{CHERRY}" stop-opacity="0.13"/><stop offset="100%" stop-color="{CHERRY}" stop-opacity="0"/></radialGradient>')
    parts.append(f'<linearGradient id="fadeBottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{BG}" stop-opacity="0"/><stop offset="100%" stop-color="{BG}" stop-opacity="1"/></linearGradient>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # pulsing glows
    parts.append(f'<circle cx="260" cy="110" r="520" fill="url(#glowTeal)"><animate attributeName="opacity" values="0.5;1;0.5" dur="9s" repeatCount="indefinite"/></circle>')
    parts.append(f'<circle cx="1660" cy="360" r="560" fill="url(#glowCherry)"><animate attributeName="opacity" values="0.55;1;0.55" dur="12s" repeatCount="indefinite"/></circle>')

    # faint grid
    vlines = "".join(f"M{x} 0V{H}" for x in range(80, W, 80))
    hlines = "".join(f"M0 {y}H{W}" for y in range(60, H, 60))
    parts.append(f'<path d="{vlines}" stroke="{BORDER}" stroke-width="1" opacity="0.35"/>')
    parts.append(f'<path d="{hlines}" stroke="{BORDER}" stroke-width="1" opacity="0.35"/>')

    # scan line sweep
    parts.append(f'<line x1="0" y1="210" x2="1920" y2="210" stroke="{TEAL}" stroke-width="2" opacity="0.10"><animateTransform attributeName="transform" type="translate" values="-600 0;2600 0" dur="11s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.0;0.12;0.0" dur="11s" repeatCount="indefinite"/></line>')

    # circuit traces
    traces = [
        "M60 330h240v-90h160",
        "M340 60v130h190v110h120",
        "M1560 60h140v150h130v-60h120",
        "M60 90h110v60h140",
        "M1780 330h80v-70h-160v-90h60",
    ]
    for i, d in enumerate(traces):
        parts.append(f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.4"><animate attributeName="opacity" values="0.25;0.55;0.25" dur="{6+i*2}s" repeatCount="indefinite"/></path>')

    # nodes at trace ends (pulse)
    nodes = [(300, 240), (690, 300), (1800, 200), (270, 150), (1940, 260)]
    for i, (x, y) in enumerate(nodes):
        parts.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{TEAL}"><animate attributeName="r" values="2.5;5.5;2.5" dur="{2.5+i*0.7:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0.25;0.9" dur="{2.5+i*0.7:.1f}s" repeatCount="indefinite"/></circle>')

    # HUD corner brackets
    bracket = (
        f'<g stroke="{TEAL}" stroke-width="2" fill="none" opacity="0.55">'
        f'<path d="M28 46V28h18"/><path d="M1892 28h18v18"/>'
        f'<path d="M28 374v18h18"/><path d="M1892 356v18h-18"/>'
        f'</g>'
    )
    parts.append(bracket)

    # drifting particles
    colors = [TEAL, CHERRY, SLATE, TEAL, TEAL, CHERRY]
    for i in range(24):
        x = random.randint(40, W - 40)
        y = random.randint(30, H - 30)
        r = round(random.uniform(1.2, 3.2), 1)
        c = colors[i % len(colors)]
        dx = random.randint(30, 120)
        dy = random.randint(-90, -25)
        dur = round(random.uniform(9, 22), 1)
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.75;0" dur="{dur}s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    # bottom fade to blend into page
    parts.append(f'<rect x="0" y="{H-70}" width="{W}" height="70" fill="url(#fadeBottom)"/>')
    parts.append('</svg>')
    return "".join(parts)

def footer_svg():
    W, H = 1920, 150
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">')
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    def wave(period, amp, y, color, opacity, dur, phase, width):
        """single path spanning 2*width; periodic -> seamless -width translate loop"""
        pts = []
        for px in range(0, 2 * width + period, 8):
            yy = y + amp * __import__("math").sin(2 * __import__("math").pi * (px + phase) / period)
            pts.append(f"{px},{yy:.1f}")
        return (
            f'<g opacity="{opacity}"><path d="M{"L".join(pts)}" fill="none" stroke="{color}" stroke-width="3">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-width} 0" dur="{dur}s" repeatCount="indefinite"/></path></g>'
        )

    parts.append(wave(640, 16, 78, TEAL, 0.35, 14, 0, W))
    parts.append(wave(880, 22, 104, CHERRY, 0.22, 19, 260, W))
    parts.append(wave(480, 10, 128, TEAL, 0.12, 11, 120, W))

    # rising bubbles
    random.seed(7)
    for i in range(10):
        x = random.randint(60, W - 60)
        r = round(random.uniform(1.5, 4.5), 1)
        dy = random.randint(40, 90)
        dur = round(random.uniform(8, 16), 1)
        c = [TEAL, CHERRY, SLATE][i % 3]
        parts.append(
            f'<circle cx="{x}" cy="{H - 10}" r="{r}" fill="{c}">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-random.randint(20, 60)} {-dy};0 0" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.6;0" dur="{dur}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    parts.append('</svg>')
    return "".join(parts)

for name, fn in (("banner", banner_svg), ("footer", footer_svg)):
    svg = fn()
    ET.fromstring(svg)
    path = f"/var/folders/wf/5k_x1rnj6vzbvbpcd4rp_0hr0000gp/T/opencode/profile-repo/assets/{name}.svg"
    with open(path, "w") as f:
        f.write(svg)
    print(f"{name}.svg: {len(svg)} bytes, valid XML, animate count = {svg.count('<animate')}")
