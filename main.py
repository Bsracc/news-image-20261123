"""News-image entry: copy the bundled front-page image to /output/entry.png.

The image is a generated editorial front page for Monday 23 November 2026
(COP31 deal collapses, tankers hit in the Strait of Hormuz, Democrats win
Congress, cartel chief Chapo Isidro arrested, Ukraine drones hit a Russian
warship off Benghazi). It is stored as a JPEG (265,702 bytes, 1024x1024);
the output file keeps the name entry.png, as the bounty rules require.
Image made with image generation, not procedural drawing, per Bsr's call.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry-image.jpg")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
