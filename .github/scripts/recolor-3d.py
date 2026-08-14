#!/usr/bin/env python3
"""Recolor the generated 3D contribution SVG to the cyber teal theme.

The github-profile-3d-contrib action regenerates profile-night-rainbow.svg
daily. Its output format varies by release: some versions animate cubes with
CSS @keyframes named rb-l{level}-{face}, others with SMIL <animate> elements
whose stop-set brightness encodes (level, face). This script rewrites both
formats to the profile palette (cyber teal -> deep cherry), preserving the
animation structure and the 3D lighting, plus fixes the static colors.
"""
import re

SVG = "profile-3d-contrib/profile-night-rainbow.svg"

# Aurora hue cycle (6 stops, 100% wraps to stop 0)
STOPS = [
    (0, 245, 212),    # cyber teal
    (64, 255, 228),   # bright teal
    (0, 210, 185),    # deep teal
    (255, 0, 85),     # deep cherry
    (204, 0, 68),     # dark cherry
    (120, 0, 45),     # deep plum
]

# Activity level brightness (l0 quiet -> l4 intense)
LEVELS = [0.30, 0.45, 0.62, 0.80, 1.0]
# Cube face brightness (top brightest, right darkest)
FACES = {"top": 1.0, "left": 0.83, "right": 0.70}


def shade(base, k):
    return tuple(max(0, min(255, int(c * k))) for c in base)


def css_cycle(level, face):
    k = LEVELS[level] * FACES[face]
    return [shade(STOPS[i % len(STOPS)], k) for i in range(7)]


def smil_cycle(brightness):
    return [shade(STOPS[i % len(STOPS)], brightness / max(STOPS[i % len(STOPS)])) for i in range(7)]


def recolor_css_keyframes(svg):
    def replace_keyframe(m):
        name, body = m.group(1), m.group(2)
        lm = re.match(r"rb-l(\d)-(top|left|right)", name)
        if not lm:
            return m.group(0)
        level, face = int(lm.group(1)), lm.group(2)
        if level > 4:
            return m.group(0)
        colors = css_cycle(level, face)
        idx = 0

        def sub_color(rgbm):
            nonlocal idx
            c = colors[idx]
            idx += 1
            return "rgb(%d, %d, %d)" % c

        body = re.sub(r"rgb\(\d+,\s*\d+,\s*\d+\)", sub_color, body)
        return "@keyframes " + name + "{" + body + "}"

    return re.sub(
        r"@keyframes (rb-l\d-(?:top|left|right))\{((?:[0-9.]+%\{fill:rgb\([^)]*\)\})+)\}",
        replace_keyframe,
        svg,
    )


def recolor_smil_animates(svg):
    def replace_animate(m):
        values = m.group(1)
        colors = re.findall(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", values)
        if not colors:
            return m.group(0)
        brightness = max(int(c) for rgb in colors for c in rgb)
        stops = smil_cycle(brightness)
        new_values = ";".join("rgb(%d,%d,%d)" % c for c in stops)
        return '<animate attributeName="fill" values="' + new_values + '"'

    return re.sub(
        r'<animate attributeName="fill" values="([^"]*)"', replace_animate, svg
    )


def fix_static_colors(svg):
    # Inline attributes (SMIL output)
    svg = svg.replace('fill="#00000f"', 'fill="#0d1117"')
    svg = svg.replace('stroke="#00000f"', 'stroke="#0d1117"')
    svg = svg.replace('fill="#eeeeff"', 'fill="#c9d1d9"')
    svg = svg.replace('fill="#aaaaaa"', 'fill="#8b98a5"')
    # CSS rules (keyframe output)
    svg = svg.replace(".fill-bg { fill: #00000f; }", ".fill-bg { fill: #0d1117; }")
    svg = svg.replace(".stroke-bg { stroke: #00000f; }", ".stroke-bg { stroke: #0d1117; }")
    svg = svg.replace(".fill-fg { fill: #eeeeff; }", ".fill-fg { fill: #c9d1d9; }")
    svg = svg.replace(".stroke-fg { stroke: #eeeeff; }", ".stroke-fg { stroke: #c9d1d9; }")
    svg = svg.replace(".fill-weak { fill: #aaaaaa; }", ".fill-weak { fill: #8b98a5; }")
    svg = svg.replace(".stroke-weak { stroke: #aaaaaa; }", ".stroke-weak { stroke: #8b98a5; }")
    svg = svg.replace("stroke: #aaaaaa;", "stroke: #30363d;")
    # Gold accent -> cyber teal
    svg = svg.replace("rgb(255,200,55)", "rgb(0,245,212)")
    svg = svg.replace("rgb(255, 200, 55)", "rgb(0, 245, 212)")
    return svg


def main():
    with open(SVG) as f:
        svg = f.read()

    svg = recolor_css_keyframes(svg)
    svg = recolor_smil_animates(svg)
    svg = fix_static_colors(svg)

    with open(SVG, "w") as f:
        f.write(svg)
    print(f"Recolored {SVG} to cyber teal theme")


if __name__ == "__main__":
    main()
