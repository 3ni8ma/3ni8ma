#!/usr/bin/env python3
"""Recolor the generated 3D contribution SVG to the cyber teal theme.

The github-profile-3d-contrib action regenerates profile-night-rainbow.svg
daily with a rainbow hue cycle. This script rewrites its CSS to the profile
palette: dark obsidian #0d1117 background, cyber teal -> deep cherry aurora
cycle (#00F5D4 -> #FF0055), keeping the animation structure intact.
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


def shade(base, level, face):
    k = LEVELS[level] * FACES[face]
    return tuple(max(0, min(255, int(c * k))) for c in base)


def recolor_rgb(rgb):
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def main():
    with open(SVG) as f:
        svg = f.read()

    def replace_keyframe(m):
        name, body = m.group(1), m.group(2)
        lm = re.match(r"rb-l(\d)-(top|left|right)", name)
        if not lm:
            return m.group(0)
        level, face = int(lm.group(1)), lm.group(2)
        if level > 4:
            return m.group(0)
        colors = [shade(STOPS[i % len(STOPS)], level, face) for i in range(7)]
        idx = 0

        def sub_color(rgbm):
            nonlocal idx
            c = colors[idx]
            idx += 1
            return "rgb(%d, %d, %d)" % c

        body = re.sub(r"rgb\(\d+,\s*\d+,\s*\d+\)", sub_color, body)
        return "@keyframes " + name + "{" + body + "}"

    svg = re.sub(
        r"@keyframes (rb-l\d-(?:top|left|right))\{((?:[0-9.]+%\{fill:rgb\([^)]*\)\})+)\}",
        replace_keyframe,
        svg,
    )

    svg = svg.replace(".fill-bg { fill: #00000f; }", ".fill-bg { fill: #0d1117; }")
    svg = svg.replace(".stroke-bg { stroke: #00000f; }", ".stroke-bg { stroke: #0d1117; }")
    svg = svg.replace(".fill-fg { fill: #eeeeff; }", ".fill-fg { fill: #c9d1d9; }")
    svg = svg.replace(".stroke-fg { stroke: #eeeeff; }", ".stroke-fg { stroke: #c9d1d9; }")
    svg = svg.replace(".fill-weak { fill: #aaaaaa; }", ".fill-weak { fill: #8b98a5; }")
    svg = svg.replace(".stroke-weak { stroke: #aaaaaa; }", ".stroke-weak { stroke: #8b98a5; }")
    svg = svg.replace("rgb(255,200,55)", "rgb(0,245,212)")
    svg = svg.replace("rgb(255, 200, 55)", "rgb(0, 245, 212)")

    with open(SVG, "w") as f:
        f.write(svg)
    print(f"Recolored {SVG} to cyber teal theme")


if __name__ == "__main__":
    main()
