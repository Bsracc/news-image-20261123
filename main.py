"""News image for 23 November 2026 (make.fun news-image-20261123).

Draws one 1024x1024 flat illustration with PIL and writes it to
/output/entry.png. Deterministic: no randomness, no timestamps, no
network. The image is 1024x1024 pixels and under 1 MiB.
Output verified byte-identical across runs (same sha256 every run).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (250, 245, 233)
NAVY = (15, 42, 61)
GOLD = (193, 154, 61)
RED = (178, 44, 36)
TEAL = (32, 110, 130)
SKY = (220, 233, 242)
EARTH = (176, 124, 74)
DARK_EARTH = (122, 82, 46)
WHITE = (255, 255, 255)
INK = (24, 28, 32)
GREY = (90, 96, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text, return y after the last line."""
    leading = leading or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def draw_globe(draw, cx, cy, r):
    """Cracked dry-earth globe: blue ocean, brown land, black cracks."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 178))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=5)
    # Land masses (flat brown blobs, kept inside the circle).
    draw.ellipse([cx - 95, cy - 70, cx - 30, cy - 10], fill=EARTH)
    draw.ellipse([cx - 20, cy + 20, cx + 75, cy + 90], fill=EARTH)
    draw.ellipse([cx + 30, cy - 90, cx + 70, cy - 40], fill=DARK_EARTH)
    # Cracks across the globe.
    draw.line([(cx - r + 18, cy - 40), (cx - 30, cy + 5), (cx - 55, cy + 45)],
              fill=INK, width=5)
    draw.line([(cx + 10, cy - r + 25), (cx + 45, cy - 20), (cx + 30, cy + 35)],
              fill=INK, width=5)
    draw.line([(cx - 30, cy + 5), (cx + 5, cy + 25)], fill=INK, width=4)


def draw_tanker(draw, x, y, w, h):
    """Oil tanker on a teal sea with a small flame on deck."""
    sea_y = y + int(h * 0.62)
    draw.rectangle([x, sea_y, x + w, y + h], fill=TEAL)
    for i in range(3):
        wy = sea_y + 14 + i * 16
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(120, 190, 205), width=3)
    # Hull.
    draw.polygon([(x + 12, sea_y - 6), (x + w - 12, sea_y - 6),
                  (x + w - 34, sea_y + 26), (x + 34, sea_y + 26)], fill=RED)
    # Deck containers.
    draw.rectangle([x + 30, sea_y - 34, x + 70, sea_y - 6], fill=GOLD)
    draw.rectangle([x + 78, sea_y - 34, x + 118, sea_y - 6], fill=WHITE)
    draw.rectangle([x + 126, sea_y - 34, x + 166, sea_y - 6], fill=(70, 70, 70))
    # Bridge tower.
    draw.rectangle([x + w - 58, sea_y - 52, x + w - 22, sea_y - 6], fill=NAVY)
    # Flame on deck (kept inside the drawing area).
    fx = x + 52
    draw.polygon([(fx, sea_y - 62), (fx + 14, sea_y - 40), (fx + 28, sea_y - 62),
                  (fx + 14, sea_y - 50)], fill=(240, 140, 40))
    draw.polygon([(fx + 7, sea_y - 54), (fx + 14, sea_y - 40),
                  (fx + 21, sea_y - 54)], fill=(250, 210, 60))


def draw_capitol(draw, x, y, w, h):
    """US Capitol dome silhouette in white on navy (fits inside h)."""
    base = y + h - 4
    # Steps.
    draw.rectangle([x + 20, base - 5, x + w - 20, base], fill=NAVY)
    draw.rectangle([x + 34, base - 10, x + w - 34, base - 5], fill=NAVY)
    # Columns.
    for i in range(5):
        cx = x + 52 + i * 42
        draw.rectangle([cx, base - 38, cx + 14, base - 10], fill=NAVY)
    # Dome.
    draw.rectangle([x + 52, base - 43, x + w - 52, base - 38], fill=NAVY)
    draw.pieslice([x + w // 2 - 48, base - 78, x + w // 2 + 48, base - 43],
                  180, 360, fill=NAVY)
    draw.rectangle([x + w // 2 - 4, base - 86, x + w // 2 + 4, base - 78],
                   fill=NAVY)
    draw.ellipse([x + w // 2 - 7, base - 92, x + w // 2 + 7, base - 80],
                 fill=NAVY)
    # Ballot box.
    draw.rectangle([x + w - 78, base - 24, x + w - 34, base - 4], fill=GOLD)
    draw.polygon([(x + w - 66, base - 32), (x + w - 46, base - 32),
                  (x + w - 56, base - 24)], fill=NAVY)


def draw_handcuffs(draw, x, y, w, h):
    """Two gold handcuff rings joined by a chain, on dark slate."""
    cy = y + h // 2 + 6
    for cx in (x + 62, x + w - 62):
        draw.ellipse([cx - 44, cy - 44, cx + 44, cy + 44],
                     outline=GOLD, width=12)
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20],
                     outline=GOLD, width=4)
    # Chain links between the rings.
    for i, cx in enumerate(range(x + 118, x + w - 118, 26)):
        draw.ellipse([cx, cy - 10, cx + 20, cy + 10], outline=WHITE, width=4)


def draw_warship(draw, x, y, w, h):
    """Grey warship on a dark sea with two small drones above."""
    sea_y = y + int(h * 0.66)
    draw.rectangle([x, sea_y, x + w, y + h], fill=(28, 68, 96))
    draw.line([(x + 10, sea_y + 16), (x + w - 10, sea_y + 16)],
              fill=(120, 170, 200), width=3)
    # Hull.
    draw.polygon([(x + 14, sea_y - 4), (x + w - 14, sea_y - 4),
                  (x + w - 40, sea_y + 24), (x + 40, sea_y + 24)],
                 fill=(70, 78, 86))
    # Superstructure and mast.
    draw.rectangle([x + w // 2 - 50, sea_y - 34, x + w // 2 + 30, sea_y - 4],
                   fill=(96, 104, 112))
    draw.rectangle([x + w // 2 + 8, sea_y - 58, x + w // 2 + 16, sea_y - 34],
                   fill=(96, 104, 112))
    # Drones: small quadcopters with rotor lines.
    for dx in (x + 60, x + w - 90):
        dy = y + 18
        draw.ellipse([dx - 8, dy - 6, dx + 8, dy + 6], fill=INK)
        draw.line([(dx - 22, dy - 8), (dx + 22, dy - 8)], fill=INK, width=3)
        draw.line([(dx - 22, dy + 8), (dx + 22, dy + 8)], fill=INK, width=3)
    # Blast star near the bow.
    bx, by = x + w - 60, sea_y - 46
    draw.polygon([(bx, by - 18), (bx + 6, by - 6), (bx + 18, by - 4),
                  (bx + 8, by + 6), (bx + 12, by + 18), (bx, by + 10),
                  (bx - 12, by + 18), (bx - 8, by + 6), (bx - 18, by - 4),
                  (bx - 6, by - 6)], fill=(250, 190, 40))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=GOLD)
    d.text((W // 2, 16), "WORLD NEWS", font=BOLD(78), fill=WHITE, anchor="ma")
    d.text((W // 2, 104), "MONDAY  23  NOVEMBER  2026", font=BOLD(34),
           fill=GOLD, anchor="ma")

    # --- Lead story: COP31 ---------------------------------------------
    d.rectangle([24, 176, 1000, 556], fill=SKY, outline=NAVY, width=3)
    # Dry cracked ground at the bottom of the panel.
    d.polygon([(24, 470), (1000, 470), (1000, 556), (24, 556)], fill=EARTH)
    d.line([(120, 470), (200, 510), (180, 556)], fill=DARK_EARTH, width=5)
    d.line([(420, 470), (470, 505), (540, 556)], fill=DARK_EARTH, width=5)
    d.line([(760, 470), (720, 512), (790, 556)], fill=DARK_EARTH, width=5)
    # Globe, left.
    draw_globe(d, 190, 320, 120)
    # Headline, right.
    text_block(d, 350, 196, "COP31 DEAL", BOLD(58), NAVY, 620)
    text_block(d, 350, 262, "COLLAPSES", BOLD(58), RED, 620)
    text_block(d, 350, 340,
               "Climate talks fail on a fossil-fuel phase-out",
               BOLD(28), INK, 600, leading=36)
    text_block(d, 350, 420,
               "Negotiators walk out as the talks fail",
               REG(24), GREY, 600, leading=32)

    # --- Three panels ----------------------------------------------------
    panels = [
        ("STRAIT OF HORMUZ", "TANKERS HIT", "Two tankers attacked; US-Iran tension rises",
         draw_tanker, TEAL),
        ("UNITED STATES", "DEMOCRATS WIN CONGRESS", "Voters hand Congress to the Democrats",
         draw_capitol, NAVY),
        ("MEXICO", "CARTEL CHIEF ARRESTED", "Chapo Isidro captured after long hunt",
         draw_handcuffs, (52, 52, 58)),
    ]
    pw, gap, py, ph = 312, 20, 576, 264
    for i, (kicker, title, caption, draw_fn, color) in enumerate(panels):
        x = 24 + i * (pw + gap)
        d.rectangle([x, py, x + pw, py + ph], fill=WHITE, outline=NAVY, width=3)
        d.rectangle([x, py, x + pw, py + 34], fill=color)
        d.text((x + 12, py + 5), kicker, font=BOLD(19), fill=WHITE)
        draw_fn(d, x + 12, py + 44, pw - 24, 96)
        y = py + 150
        y = text_block(d, x + 12, y, title, BOLD(24), NAVY, pw - 24, leading=30)
        text_block(d, x + 12, y + 4, caption, REG(19), GREY, pw - 24, leading=25)

    # --- Bottom strip: Benghazi ------------------------------------------
    d.rectangle([24, 860, 1000, 992], fill=(16, 36, 52), outline=NAVY, width=3)
    text_block(d, 44, 876, "UKRAINE DRONES HIT", BOLD(30), WHITE, 560, leading=38)
    text_block(d, 44, 914, "RUSSIAN WARSHIP", BOLD(30), GOLD, 560, leading=38)
    text_block(d, 44, 952, "OFF BENGHAZI", BOLD(30), GOLD, 560, leading=38)
    draw_warship(d, 640, 872, 340, 104)

    # --- Footer -----------------------------------------------------------
    d.text((W // 2, 998), "23 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=BOLD(16), fill=GREY, anchor="ma")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path}: {size} bytes, {W}x{H}")
