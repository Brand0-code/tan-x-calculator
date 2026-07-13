"""
Dev-only helper (not part of the graded implementation): renders a
captured terminal transcript (plain text) into a PNG image, so tool
usage evidence for D3/Problem 7 can be saved as an image file. The
text content is real captured command output - this script only
formats it visually, it does not generate or alter the content.

Usage: python3 scripts/render_terminal_png.py <input.txt> <output.png> "<title>"
"""

import sys
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "/Library/Fonts/Courier New.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render(input_path, output_path, title):
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    font = load_font(14)
    title_font = load_font(16)

    pad = 20
    line_height = 19
    title_height = 30 if title else 0
    max_line_len = max((len(line) for line in lines), default=0)
    char_width = 8.4

    width = int(pad * 2 + max_line_len * char_width)
    width = max(width, 500)
    height = int(pad * 2 + title_height + line_height * len(lines))

    bg = (30, 30, 30)
    fg = (220, 220, 220)
    title_fg = (255, 255, 255)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    y = pad
    if title:
        draw.text((pad, y), title, font=title_font, fill=title_fg)
        y += title_height

    for line in lines:
        draw.text((pad, y), line, font=font, fill=fg)
        y += line_height

    img.save(output_path)
    print(f"Wrote {output_path} ({width}x{height})")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
