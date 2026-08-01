"""Turn a square avatar into the ASCII column of the neofetch SVG.

The SVG draws light text (#c9d1d9) on a dark card, so bright pixels become
dense glyphs and dark pixels become spaces.
"""
import sys
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# 38 cols * ~9.6px advance (Consolas 16px at size-adjust 109%) + x=15 leaves the
# art ending at ~380px, clear of the panel's left edge at x=390.
COLS, ROWS = 38, 20
# light -> dark; index 0 is the brightest region of the picture
RAMP = "@%#*+=~:-.` "
# glyphs used where the luminance pass is empty but an edge runs through
EDGE_RAMP = "+=~:-.`"


def _grid(img):
    return img.resize((COLS, ROWS), Image.Resampling.BOX).load()


def build(path, gamma=0.75, contrast=2.0, floor=0.10, edge_gain=0.0,
          edge_floor=9.0, crop_top=0.0, bg_dot=".", bg_chroma=0.175):
    full = Image.open(path).convert("RGB")
    w, h = full.size
    # trim the dead ceiling and the empty margins so the subject fills the
    # column; the remaining box is portrait, matching COLS x ROWS
    box = (int(w * 0.12), int(h * crop_top), int(w * 0.92), h)
    full = full.crop(box)

    # The hair and the window behind it sit at the same luminance (~23/255), so
    # a brightness pass cannot separate them and the silhouette disappears.
    # They do differ in hue: the window is blue (red chromaticity ~0.14) and the
    # hair is warmer (~0.21-0.24). Classify the dark cells on that instead.
    cpx = full.resize((COLS, ROWS), Image.Resampling.BOX).load()

    src = full.convert("L")
    src = ImageOps.autocontrast(src, cutoff=1)

    # edges come off the full-resolution image, before the contrast stretch,
    # so the hair/background boundary survives even though both are dark
    edges = src.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
    epx = _grid(edges)

    lum = ImageEnhance.Contrast(src).enhance(contrast)
    lpx = _grid(lum)

    rows = []
    for y in range(ROWS):
        line = []
        for x in range(COLS):
            v = (lpx[x, y] / 255.0) ** gamma
            if v >= floor:
                line.append(RAMP[int((1.0 - v) * (len(RAMP) - 1) + 0.5)])
                continue
            e = min(1.0, (epx[x, y] / 255.0) * edge_gain)
            if e >= edge_floor:
                line.append(EDGE_RAMP[int((1.0 - e) * (len(EDGE_RAMP) - 1) + 0.5)])
            else:
                # dark cell: stipple it if it is the blue window, leave it empty
                # if it is hair, so the head reads as a void in the wallpaper
                r, g, b = cpx[x, y]
                total = r + g + b
                line.append(bg_dot if total and r / total < bg_chroma else " ")
        rows.append("".join(line).rstrip())
    return rows


if __name__ == "__main__":
    args = [float(a) for a in sys.argv[2:]]
    for r in build(sys.argv[1], *args):
        print("|" + r.ljust(COLS) + "|")
