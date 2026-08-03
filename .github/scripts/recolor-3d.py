#!/usr/bin/env python3
"""Recolor the generated 3D contribution SVG to the liquid glass theme.

The github-profile-3d-contrib action regenerates profile-night-rainbow.svg
daily with a rainbow hue cycle. This script rewrites its CSS to the site's
palette: dark #0d1117 background, cyan -> blue -> crimson -> coral aurora
cycle, keeping the animation structure intact.
"""
import re

SVG = "profile-3d-contrib/profile-night-rainbow.svg"

# Aurora hue cycle (6 stops, 100% wraps to stop 0)
STOPS = [
    (0, 110, 130),    # deep teal
    (0, 170, 190),    # teal
    (0, 242, 254),    # cyan
    (74, 144, 217),   # blue
    (230, 0, 73),     # crimson
    (214, 121, 100),  # coral
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
    svg = svg.replace(".fill-fg { fill: #eeeeff; }", ".fill-fg { fill: #c8d2dc; }")
    svg = svg.replace(".stroke-fg { stroke: #eeeeff; }", ".stroke-fg { stroke: #c8d2dc; }")
    svg = svg.replace(".fill-weak { fill: #aaaaaa; }", ".fill-weak { fill: #8b98a5; }")
    svg = svg.replace(".stroke-weak { stroke: #aaaaaa; }", ".stroke-weak { stroke: #8b98a5; }")
    svg = svg.replace("rgb(255,200,55)", "rgb(0,242,254)")
    svg = svg.replace("rgb(255, 200, 55)", "rgb(0, 242, 254)")

    with open(SVG, "w") as f:
        f.write(svg)
    print(f"Recolored {SVG} to liquid glass theme")


if __name__ == "__main__":
    main()
