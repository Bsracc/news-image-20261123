"""News image for 23 November 2026 (make.fun news-image-20261123).

Redesigned as a real editorial newspaper front page: one dominant lead
story (COP31), the other stories as a compact headline list separated by
thin rules, no cartoon icons, paper off-white, ink navy, one red accent
for the lead headline only. Redesigned 23 Nov 2026 to remove the flat
template look (v2 editorial layout).
Draws with PIL and writes to /output/entry.png.
Deterministic: no randomness, no timestamps, no network.
The image is 1024x1024 pixels and under 1 MiB.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (247, 243, 232)
NAVY = (15, 42, 61)
INK = (24, 28, 32)
GREY = (96, 100, 102)
RED = (178, 44, 36)
GOLD = (176, 138, 58)
RULE = (198, 190, 172)
OCEAN = (133, 158, 176)
OCEAN_DARK = (110, 136, 156)
LAND = (184, 138, 86)
LAND_DARK = (139, 106, 69)
EARTH = (166, 124, 78)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def spaced(text, n=1):
    """Letterspace a kicker: insert n spaces between characters."""
    return (" " * n).join(text)


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
    leading = leading or int(fnt.size * 1.3)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def draw_globe(img, cx, cy, r):
    """Cracked globe, drawn with care: muted ocean, ochre land clipped to
    the circle, fine 2px crack lines, a dry-earth band at the bottom."""
    # Land layer, clipped to the circle by a mask.
    globe = Image.new("RGB", (2 * r, 2 * r), OCEAN)
    g = ImageDraw.Draw(globe)
    # Subtle ocean shading: a darker band low on the disc.
    g.ellipse([-r, r // 2, 2 * r, 3 * r], fill=OCEAN_DARK)
    # Land masses (organic shapes).
    g.ellipse([18, 30, 128, 108], fill=LAND)
    g.ellipse([150, 34, 268, 128], fill=LAND_DARK)
    g.ellipse([52, 168, 190, 262], fill=LAND)
    g.ellipse([208, 190, 262, 238], fill=LAND_DARK)
    # Dry-earth band across the bottom of the disc.
    g.polygon([(0, 236), (2 * r, 216), (2 * r, 2 * r), (0, 2 * r)], fill=EARTH)
    # Fine cracks: one long branching crack, plus small ones.
    g.line([(60, 60), (110, 120), (96, 168), (140, 210)], fill=INK, width=2)
    g.line([(110, 120), (150, 132)], fill=INK, width=2)
    g.line([(96, 168), (70, 196)], fill=INK, width=2)
    g.line([(190, 60), (200, 110), (176, 150)], fill=INK, width=2)
    g.line([(200, 110), (232, 122)], fill=INK, width=2)
    g.line([(30, 240), (90, 232), (140, 246), (210, 234), (270, 244)],
           fill=INK, width=2)
    g.line([(90, 232), (100, 262)], fill=INK, width=2)
    g.line([(210, 234), (196, 264)], fill=INK, width=2)
    # Stipple: a few small dots for dry texture on the band.
    for dx, dy in ((40, 262), (150, 272), (230, 262), (120, 252), (260, 276)):
        g.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=LAND_DARK)
    mask = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r, 2 * r], fill=255)
    img.paste(globe, (cx - r, cy - r), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 48  # left/right margin, used everywhere

    # --- Nameplate -------------------------------------------------------
    d.text((W // 2, 28), "WORLD NEWS", font=SERIF_BOLD(66), fill=NAVY,
           anchor="ma")
    d.text((W // 2, 104), spaced("MONDAY, 23 NOVEMBER 2026"),
           font=SANS_BOLD(19), fill=GREY, anchor="ma")
    d.line([(M, 138), (W - M, 138)], fill=NAVY, width=3)
    d.line([(M, 144), (W - M, 144)], fill=GOLD, width=1)

    # --- Lead story: COP31 ---------------------------------------------
    d.text((M, 168), spaced("CLIMATE  •  COP31"), font=SANS_BOLD(18),
           fill=GREY)
    # Headline, two lines; the word "collapses" carries the only red.
    d.text((M, 196), "COP31 deal", font=SERIF_BOLD(64), fill=NAVY)
    d.text((M, 268), "collapses", font=SERIF_BOLD(64), fill=RED)
    text_block(d, M, 356,
               "Climate talks fail on a fossil-fuel phase-out as "
               "negotiators walk out.",
               SERIF(26), INK, 480, leading=34)
    d.text((M, 470), "The summit ends without agreement",
           font=SERIF(20), fill=GREY)
    d.text((M, 496), "on ending fossil fuels.",
           font=SERIF(20), fill=GREY)

    # Cracked globe, right of the headline; cracked ground beneath it.
    draw_globe(img, 800, 330, 148)
    d = ImageDraw.Draw(img)
    d.ellipse([648, 492, 952, 506], fill=(222, 214, 196))
    d.line([(660, 500), (720, 492), (760, 502), (830, 494), (900, 500),
            (940, 496)], fill=INK, width=2)

    # --- Rule, then the rest of the news as a headline list -------------
    d.line([(M, 548), (W - M, 548)], fill=NAVY, width=2)
    d.text((M, 566), spaced("MORE FROM AROUND THE WORLD"),
           font=SANS_BOLD(16), fill=GREY)

    stories = [
        ("STRAIT OF HORMUZ",
         "Tankers hit in the Strait of Hormuz",
         "Two tankers attacked; US\u2013Iran tension rises."),
        ("UNITED STATES",
         "Democrats win Congress",
         "Voters hand Congress to the Democrats."),
        ("MEXICO",
         "Cartel chief arrested",
         "Chapo Isidro captured after a long hunt."),
        ("LIBYA",
         "Ukraine drones hit Russian warship off Benghazi",
         "A Russian warship is struck off the Libyan coast."),
    ]
    y = 606
    for kicker, headline, deck in stories:
        d.line([(M, y), (W - M, y)], fill=RULE, width=1)
        d.text((M, y + 12), spaced(kicker), font=SANS_BOLD(15), fill=NAVY)
        d.text((M, y + 34), headline, font=SERIF_BOLD(29), fill=INK)
        d.text((M, y + 70), deck, font=SERIF(19), fill=GREY)
        y += 92

    # --- Footer -----------------------------------------------------------
    d.line([(M, 976), (W - M, 976)], fill=RULE, width=1)
    d.text((W // 2, 986), spaced("23 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE"),
           font=SANS_BOLD(13), fill=GREY, anchor="ma")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path}: {size} bytes, {W}x{H}")
