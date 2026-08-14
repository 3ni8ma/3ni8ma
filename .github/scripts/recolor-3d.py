#!/usr/bin/env python3
"""Recolor the generated 3D contribution SVG to the cyber teal theme.

The github-profile-3d-contrib action generates profile-night-rainbow.svg with
SMIL <animate> elements: every cube face animates its fill through 7 color
stops of a muted rainbow hue cycle. The brightness of a stop set (its max
channel value) encodes the cube's activity level and face shading, so this
script rewrites each stop set to the profile palette (cyber teal -> deep
cherry) scaled to the exact same brightness, keeping the animation structure
and the 3D lighting intact.
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


def shade(base, brightness):
    m = max(base)
    return tuple(max(0, min(255, round(c * brightness / m))) for c in base)


def main():
    with open(SVG) as f:
        svg = f.read()

    def replace_animate(m):
        values = m.group(1)
        colors = re.findall(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", values)
        if not colors:
            return m.group(0)
        brightness = max(int(c) for rgb in colors for c in rgb)
        stops = [shade(STOPS[i % len(STOPS)], brightness) for i in range(7)]
        new_values = ";".join("rgb(%d,%d,%d)" % c for c in stops)
        return '<animate attributeName="fill" values="' + new_values + '"'

    svg = re.sub(r'<animate attributeName="fill" values="([^"]*)"', replace_animate, svg)

    # Static colors (inline attributes in the SMIL output, CSS rules as backup)
    svg = svg.replace('fill="#00000f"', 'fill="#0d1117"')
    svg = svg.replace('stroke="#00000f"', 'stroke="#0d1117"')
    svg = svg.replace(".fill-bg { fill: #00000f; }", ".fill-bg { fill: #0d1117; }")
    svg = svg.replace(".stroke-bg { stroke: #00000f; }", ".stroke-bg { stroke: #0d1117; }")
    svg = svg.replace('fill="#eeeeff"', 'fill="#c9d1d9"')
    svg = svg.replace(".fill-fg { fill: #eeeeff; }", ".fill-fg { fill: #c9d1d9; }")
    svg = svg.replace(".stroke-fg { stroke: #eeeeff; }", ".stroke-fg { stroke: #c9d1d9; }")
    svg = svg.replace('fill="#aaaaaa"', 'fill="#8b98a5"')
    svg = svg.replace(".fill-weak { fill: #aaaaaa; }", ".fill-weak { fill: #8b98a5; }")
    svg = svg.replace(".stroke-weak { stroke: #aaaaaa; }", ".stroke-weak { stroke: #8b98a5; }")
    svg = svg.replace("stroke: #aaaaaa;", "stroke: #30363d;")
    svg = svg.replace("rgb(255,200,55)", "rgb(0,245,212)")
    svg = svg.replace("rgb(255, 200, 55)", "rgb(0, 245, 212)")

    with open(SVG, "w") as f:
        f.write(svg)
    print(f"Recolored {SVG} to cyber teal theme")


if __name__ == "__main__":
    main()
