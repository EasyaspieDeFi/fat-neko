#!/usr/bin/env python3
"""Generate placeholder cosmetic PNGs for the Fat Neko wardrobe.

These are stand-ins so the layer pipeline can be built and tested before the real
art lands. Every file written here goes to assets/cosmetics/_gen/ — the app prefers
a same-named file in assets/cosmetics/, so dropping a hand-drawn PNG there silently
supersedes the placeholder with no code change.

    python3 tools/gen_placeholder_cosmetics.py

Canvas: 400x400 "doll" space. The base sprite (300x272) sits at (50,112) inside it,
which is what gives hats headroom the tightly-cropped base sprite doesn't have.
See assets/cosmetics/README.md for the artist-facing version of this.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops

DOLL = 400
BASE_OFF = (50, 112)          # where the 300x272 base sprite sits in doll space
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "cosmetics", "_gen")

# --- anchors, measured off the base sprite (doll coords) ---------------------
HEAD_CX = 210                 # visual centre of the skull
CROWN_Y = 135                 # flat top of the skull, between the ears
HAT_Y = 168                   # hats sit DOWN to here so they overlap the forehead
                              # and ear bases — drawing from CROWN_Y up leaves a gap
EAR_L = (139, 160)            # left ear tip x-range
EAR_R = (250, 268)            # right ear tip x-range
EYE_CX, EYE_CY = 225, 207     # midpoint of the two eyes
EYE_L, EYE_R = 186, 264       # individual eye centres
COLLAR_Y = 268                # bottom of the face patch — reads as the chin line
BODY_CX = 198
BODY_TOP, BODY_BOT = 265, 383

# --- palette, harmonised with the base sprite -------------------------------
K = (0, 0, 0, 255)            # outline
TEAL = (144, 224, 208, 255)
TEAL_D = (80, 160, 144, 255)
WHITE = (240, 240, 240, 255)
PURPLE = (160, 128, 240, 255)
GOLD = (255, 208, 94, 255)
GOLD_D = (214, 160, 40, 255)
RED = (255, 109, 122, 255)
RED_D = (198, 62, 78, 255)
BLUE = (94, 200, 255, 255)
BLUE_D = (46, 140, 200, 255)
MINT = (111, 233, 203, 255)
ORANGE = (255, 154, 82, 255)
BROWN = (150, 100, 60, 255)
GREY = (127, 140, 154, 255)
GREY_D = (74, 86, 98, 255)
DARK = (28, 38, 44, 255)
PINK = (255, 143, 212, 255)


class Art:
    """A doll-space canvas with block-snapped drawing helpers."""

    B = 11  # the base sprite's apparent pixel-block size

    def __init__(self):
        self.im = Image.new("RGBA", (DOLL, DOLL), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def r(self, x, y, w, h, c):
        """Filled rect, snapped to the block grid so it reads as pixel art."""
        b = self.B
        x0, y0 = round(x / b) * b, round(y / b) * b
        x1, y1 = round((x + w) / b) * b, round((y + h) / b) * b
        if x1 <= x0 or y1 <= y0:
            return
        self.d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=c)

    def raw(self, x, y, w, h, c):
        """Unsnapped rect, for thin details where the grid is too coarse."""
        self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

    def tri(self, cx, top, halfw, bot, c):
        """Block-stepped triangle — cones, wizard hats, wings."""
        b = self.B
        rows = max(1, int((bot - top) / b))
        for i in range(rows):
            t = (i + 1) / rows
            w = halfw * t
            self.r(cx - w, top + i * b, w * 2, b, c)

    def ellipse(self, cx, cy, rx, ry, c):
        b = self.B
        rows = max(1, int(ry * 2 / b))
        for i in range(rows):
            y = cy - ry + i * b
            t = (y + b / 2 - cy) / ry
            if abs(t) >= 1:
                continue
            w = rx * (1 - t * t) ** 0.5
            self.r(cx - w, y, w * 2, b, c)

    def finish(self, name, ow=5):
        """Auto-outline the whole composite, then write the PNG.

        Outlining from the finished alpha (rather than by hand per shape) is what
        keeps 28 placeholders visually consistent with the base sprite's chunky
        black keyline for a few lines of code.
        """
        im = self.im
        if ow:
            a = im.getchannel("A").point(lambda v: 255 if v > 128 else 0)
            dil = a.filter(ImageFilter.MaxFilter(2 * ow + 1))
            ring = ImageChops.subtract(dil, a)
            out = Image.new("RGBA", im.size, K)
            out.putalpha(ring)
            out.alpha_composite(im)
            im = out
        os.makedirs(OUT, exist_ok=True)
        im.save(os.path.join(OUT, name + ".png"))
        return im


ITEMS = {}


def item(fn):
    ITEMS[fn.__name__] = fn
    return fn


# ============================ HEAD =========================================
@item
def beanie(a):
    a.r(HEAD_CX - 76, HAT_Y - 56, 152, 56, RED)
    a.r(HEAD_CX - 82, HAT_Y - 22, 164, 22, RED_D)      # folded brim
    a.ellipse(HEAD_CX, HAT_Y - 68, 20, 18, WHITE)      # pom


@item
def cap(a):
    a.r(HEAD_CX - 70, HAT_Y - 50, 140, 50, BLUE)
    a.r(HEAD_CX - 70, HAT_Y - 18, 140, 18, BLUE_D)
    a.r(HEAD_CX - 138, HAT_Y - 20, 72, 18, BLUE_D)     # brim, worn backwards
    a.raw(HEAD_CX - 8, HAT_Y - 58, 16, 12, BLUE_D)     # button


@item
def sleep_cap(a):
    a.tri(HEAD_CX + 10, HAT_Y - 104, 64, HAT_Y - 12, PURPLE)
    a.r(HEAD_CX - 68, HAT_Y - 24, 140, 24, WHITE)      # fur brim
    a.ellipse(HEAD_CX + 52, HAT_Y - 108, 17, 15, WHITE)


@item
def party_hat(a):
    a.tri(HEAD_CX, HAT_Y - 108, 48, HAT_Y - 6, PINK)
    a.r(HEAD_CX - 32, HAT_Y - 52, 64, 11, WHITE)
    a.r(HEAD_CX - 19, HAT_Y - 82, 38, 11, WHITE)
    a.ellipse(HEAD_CX, HAT_Y - 116, 14, 13, GOLD)


@item
def chef_hat(a):
    a.r(HEAD_CX - 62, HAT_Y - 40, 124, 40, WHITE)      # band
    a.ellipse(HEAD_CX - 40, HAT_Y - 70, 32, 28, WHITE)
    a.ellipse(HEAD_CX + 40, HAT_Y - 70, 32, 28, WHITE)
    a.ellipse(HEAD_CX, HAT_Y - 84, 38, 32, WHITE)


@item
def top_hat(a):
    a.r(HEAD_CX - 100, HAT_Y - 22, 200, 22, DARK)      # brim
    a.r(HEAD_CX - 54, HAT_Y - 104, 108, 86, DARK)      # stovepipe
    a.r(HEAD_CX - 54, HAT_Y - 44, 108, 18, RED)        # band


@item
def crown_gold(a):
    a.r(HEAD_CX - 74, HAT_Y - 38, 148, 38, GOLD)
    for dx in (-74, -25, 24):
        a.tri(HEAD_CX + dx + 25, HAT_Y - 72, 25, HAT_Y - 34, GOLD)
    a.r(HEAD_CX - 74, HAT_Y - 16, 148, 16, GOLD_D)
    a.raw(HEAD_CX - 7, HAT_Y - 30, 16, 16, RED)        # jewel


@item
def flame_crown(a):
    for dx, h in ((-48, 78), (0, 108), (48, 78)):
        a.tri(HEAD_CX + dx, HAT_Y - h, 25, HAT_Y - 8, ORANGE)
    for dx, h in ((-48, 50), (0, 72), (48, 50)):
        a.tri(HEAD_CX + dx, HAT_Y - h, 13, HAT_Y - 12, GOLD)
    a.r(HEAD_CX - 70, HAT_Y - 20, 140, 20, ORANGE)


@item
def halo(a):
    cy = CROWN_Y - 40                                   # floats clear of the ears
    a.ellipse(HEAD_CX, cy, 56, 19, GOLD)
    # punch the middle out so it reads as a ring, not a disc
    a.d.ellipse([HEAD_CX - 38, cy - 9, HEAD_CX + 38, cy + 9], fill=(0, 0, 0, 0))


@item
def headphones(a):
    a.r(HEAD_CX - 86, HAT_Y - 44, 172, 22, GREY_D)     # band over the crown
    a.r(HEAD_CX - 98, HAT_Y - 36, 24, 56, GREY)
    a.r(HEAD_CX + 74, HAT_Y - 36, 24, 56, GREY)
    a.r(HEAD_CX - 104, HAT_Y + 6, 34, 50, MINT)        # ear cups, over the ears
    a.r(HEAD_CX + 70, HAT_Y + 6, 34, 50, MINT)


@item
def wizard_hat(a):
    a.tri(HEAD_CX - 6, HAT_Y - 142, 64, HAT_Y - 20, PURPLE)
    a.r(HEAD_CX - 108, HAT_Y - 26, 216, 22, PURPLE)    # wide brim
    a.r(HEAD_CX - 58, HAT_Y - 56, 104, 16, GOLD)       # band
    a.raw(HEAD_CX - 42, HAT_Y - 100, 12, 12, GOLD)     # stars
    a.raw(HEAD_CX + 16, HAT_Y - 122, 10, 10, GOLD)


# ============================ FACE =========================================
@item
def shades(a):
    a.r(EYE_L - 32, EYE_CY - 20, 64, 42, DARK)
    a.r(EYE_R - 32, EYE_CY - 20, 64, 42, DARK)
    a.raw(EYE_L + 32, EYE_CY - 4, 46, 9, DARK)         # bridge
    a.raw(EYE_L - 24, EYE_CY - 12, 20, 7, (255, 255, 255, 100))  # glint


@item
def monocle(a):
    cx, cy = EYE_R, EYE_CY
    a.d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], outline=GOLD, width=8)
    a.raw(cx + 30, cy + 28, 7, 52, GOLD)               # chain
    a.raw(cx + 20, cy + 74, 24, 7, GOLD)


@item
def eyepatch(a):
    a.r(EYE_L - 32, EYE_CY - 24, 64, 50, DARK)
    a.raw(EYE_L - 62, EYE_CY - 34, 150, 9, DARK)       # strap across the face


@item
def laser_eyes(a):
    for cx, d in ((EYE_L, -1), (EYE_R, 1)):
        a.raw(cx - 22, EYE_CY - 10, 44, 22, RED)
        a.raw(cx - 18, EYE_CY - 6, 36, 14, (255, 230, 230, 255))
        # beam fires outward from each eye, away from the muzzle
        bx = cx + 20 if d > 0 else cx - 20 - 150
        a.raw(bx, EYE_CY - 5, 150, 11, (255, 70, 90, 140))


# ============================ BODY =========================================
@item
def bib(a):
    a.r(BODY_CX - 62, COLLAR_Y, 124, 20, BLUE)
    a.ellipse(BODY_CX, COLLAR_Y + 44, 62, 40, WHITE)
    a.raw(BODY_CX - 18, COLLAR_Y + 34, 36, 12, BLUE)


@item
def scarf(a):
    a.r(BODY_CX - 84, COLLAR_Y - 8, 168, 32, RED)
    a.r(BODY_CX + 40, COLLAR_Y + 18, 42, 70, RED)      # tail hangs off one shoulder
    a.r(BODY_CX + 40, COLLAR_Y + 74, 42, 14, RED_D)    # fringe
    for i in range(3):
        a.raw(BODY_CX - 84, COLLAR_Y - 2 + i * 11, 168, 5, RED_D)


@item
def bowtie(a):
    a.tri(BODY_CX - 40, COLLAR_Y + 34, 34, COLLAR_Y - 4, PURPLE)
    a.tri(BODY_CX + 40, COLLAR_Y + 34, 34, COLLAR_Y - 4, PURPLE)
    a.r(BODY_CX - 16, COLLAR_Y + 2, 32, 30, (120, 92, 200, 255))


@item
def hoodie(a):
    a.r(BODY_CX - 96, COLLAR_Y - 4, 192, 34, ORANGE)   # hood down, bunched
    a.r(BODY_CX - 78, COLLAR_Y + 26, 156, 22, (214, 120, 58, 255))
    a.raw(BODY_CX - 30, COLLAR_Y + 30, 10, 46, WHITE)  # drawstrings
    a.raw(BODY_CX + 22, COLLAR_Y + 30, 10, 46, WHITE)


@item
def varsity(a):
    a.r(BODY_CX - 96, COLLAR_Y - 6, 192, 24, GOLD)     # ribbed collar
    a.r(BODY_CX - 104, COLLAR_Y + 14, 208, 64, RED_D)
    a.r(BODY_CX - 104, COLLAR_Y + 64, 208, 14, GOLD)   # hem stripe
    a.raw(BODY_CX - 46, COLLAR_Y + 26, 20, 38, WHITE)  # a chunky "F"
    a.raw(BODY_CX - 46, COLLAR_Y + 26, 48, 11, WHITE)
    a.raw(BODY_CX - 46, COLLAR_Y + 41, 36, 10, WHITE)


@item
def bandana(a):
    a.r(BODY_CX - 74, COLLAR_Y - 2, 148, 24, MINT)
    a.tri(BODY_CX, COLLAR_Y + 66, 52, COLLAR_Y + 16, MINT)
    a.raw(BODY_CX - 40, COLLAR_Y + 26, 12, 12, (60, 180, 150, 255))
    a.raw(BODY_CX + 14, COLLAR_Y + 40, 12, 12, (60, 180, 150, 255))


# ============================ BACK =========================================
@item
def cape(a):
    a.r(BODY_CX - 96, COLLAR_Y - 12, 192, 26, RED_D)   # collar, just past the shoulders
    # stops above the feet and only just clears the flanks — a full-width hem at floor
    # level reads as a red platform under the cat rather than as cloth behind it
    a.tri(BODY_CX, BODY_BOT - 14, 138, COLLAR_Y + 8, RED)
    a.r(BODY_CX - 138, BODY_BOT - 36, 276, 22, RED_D)  # hem


@item
def jetpack(a):
    # sits behind and above the shoulders so it clears the body silhouette
    for s in (-1, 1):
        x = BODY_CX + s * 104 - (30 if s < 0 else 0)
        a.r(x, BODY_TOP - 34, 46, 128, GREY)
        a.r(x, BODY_TOP - 34, 46, 26, RED)             # nose cone
        a.tri(x + 23, BODY_BOT + 34, 24, BODY_TOP + 92, ORANGE)
        a.tri(x + 23, BODY_BOT + 12, 13, BODY_TOP + 96, GOLD)


@item
def wings(a):
    # four stepped feathers per side, fanning up and out from the shoulders
    for s in (-1, 1):
        for i in range(4):
            span = 128 - i * 16
            x = BODY_CX + s * (96 + i * 30)
            a.r(x - (28 if s < 0 else 0), BODY_TOP - 44 + i * 22, 30, span, WHITE)


@item
def sun_aura(a):
    cx, cy = BODY_CX, (BODY_TOP + BODY_BOT) // 2
    a.ellipse(cx, cy, 178, 178, (255, 208, 94, 70))
    a.ellipse(cx, cy, 150, 150, (255, 154, 82, 60))
    for i in range(12):                                 # radiating spikes
        import math
        ang = i * math.pi / 6
        a.raw(int(cx + math.cos(ang) * 170) - 9, int(cy + math.sin(ang) * 170) - 9, 20, 20, GOLD)


# ============================ HAND =========================================
@item
def torch(a):
    x = BODY_CX + 116                                   # tucked against the right flank
    a.r(x, BODY_TOP + 32, 26, 116, BROWN)
    a.r(x - 12, BODY_TOP + 16, 50, 22, GOLD_D)          # cup
    a.tri(x + 13, BODY_TOP - 52, 30, BODY_TOP + 18, ORANGE)
    a.tri(x + 13, BODY_TOP - 26, 16, BODY_TOP + 12, GOLD)


@item
def fish_toy(a):
    x, y = BODY_CX - 130, BODY_TOP + 74
    a.ellipse(x + 44, y, 44, 27, BLUE)
    a.tri(x - 2, y, 25, y + 1, BLUE_D)                  # tail
    a.raw(x + 58, y - 9, 10, 10, DARK)                  # eye


@item
def boba(a):
    x, y = BODY_CX + 112, BODY_TOP + 40
    a.r(x, y, 72, 100, (236, 214, 190, 225))
    a.r(x, y + 56, 72, 44, (168, 122, 84, 255))         # tea
    a.r(x - 8, y - 12, 88, 18, PINK)                    # lid
    a.raw(x + 44, y - 44, 12, 42, WHITE)                # straw
    for dx, dy in ((10, 76), (32, 84), (52, 76), (22, 88)):
        a.raw(x + dx, y + dy, 13, 13, DARK)             # pearls


def contact_sheet(rendered):
    """One image with every placeholder over the base cat, for eyeballing fit."""
    base = Image.open(os.path.join(os.path.dirname(__file__), "..",
                                   "assets", "cosmetics", "_base_ref.png")).convert("RGBA")
    cols, cell = 7, 200
    rows = (len(rendered) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (18, 40, 34, 255))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(sorted(rendered.items())):
        doll = Image.new("RGBA", (DOLL, DOLL), (0, 0, 0, 0))
        doll.alpha_composite(base, BASE_OFF)
        if name in BACK_SLOT:
            under = Image.new("RGBA", (DOLL, DOLL), (0, 0, 0, 0))
            under.alpha_composite(im)
            under.alpha_composite(base, BASE_OFF)
            doll = under
        else:
            doll.alpha_composite(im)
        cx, cy = (i % cols) * cell, (i // cols) * cell
        sheet.alpha_composite(doll.resize((cell - 16, cell - 16), Image.NEAREST), (cx + 8, cy + 8))
        d.text((cx + 10, cy + cell - 14), name, fill=(200, 255, 240, 255))
    sheet.convert("RGB").save(os.path.join(OUT, "..", "_contact_sheet.png"))


BACK_SLOT = {"cape", "jetpack", "wings", "sun_aura"}


def templates():
    """Author-ready canvases: open in Aseprite, add a layer, draw, export that layer.

    TEMPLATE.png is the clean tracing base. TEMPLATE_guides.png marks the anchor lines
    measured off the sprite, so a hat brim or a pair of glasses lands first time.
    """
    base = Image.open(os.path.join(COS, "_base_ref.png")).convert("RGBA")
    clean = Image.new("RGBA", (DOLL, DOLL), (0, 0, 0, 0))
    clean.alpha_composite(base, BASE_OFF)
    clean.save(os.path.join(COS, "TEMPLATE.png"))

    g = clean.copy()
    d = ImageDraw.Draw(g)
    for y, label, col in ((HAT_Y, "HAT_Y 168  hats sit down to here", (255, 80, 160, 255)),
                          (CROWN_Y, "CROWN_Y 135  top of skull", (255, 160, 60, 255)),
                          (EYE_CY, "EYE_CY 207  eye line", (94, 200, 255, 255)),
                          (COLLAR_Y, "COLLAR_Y 268  chin / collar", (111, 233, 203, 255)),
                          (BODY_BOT, "BODY_BOT 383  feet", (200, 200, 200, 255))):
        d.line([(0, y), (DOLL, y)], fill=col, width=1)
        d.text((4, y + 2), label, fill=col)
    d.rectangle([BASE_OFF[0], BASE_OFF[1],
                 BASE_OFF[0] + base.width - 1, BASE_OFF[1] + base.height - 1],
                outline=(255, 0, 255, 160))
    d.text((4, 4), "400x400 doll canvas · base sprite 300x272 at (50,112)", fill=(255, 0, 255, 255))
    for x, label in ((HEAD_CX, "HEAD_CX 210"), (BODY_CX, "BODY_CX 198")):
        d.line([(x, 0), (x, 40)], fill=(255, 255, 255, 120), width=1)
        d.text((x + 3, 44), label, fill=(255, 255, 255, 160))
    g.save(os.path.join(COS, "TEMPLATE_guides.png"))


COS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "assets", "cosmetics"))

if __name__ == "__main__":
    rendered = {}
    for name, fn in ITEMS.items():
        a = Art()
        fn(a)
        # the aura is a soft glow — an outline would ruin it
        rendered[name] = a.finish(name, ow=0 if name == "sun_aura" else 5)
    print(f"wrote {len(rendered)} placeholders to {os.path.normpath(OUT)}")
    try:
        contact_sheet(rendered)
        print("wrote contact sheet")
    except FileNotFoundError:
        print("(no _base_ref.png yet — skipping contact sheet)")
    try:
        templates()
        print("wrote TEMPLATE.png + TEMPLATE_guides.png")
    except FileNotFoundError:
        pass
    import sync_cosmetics
    sync_cosmetics.main()   # keep art.json in step with what's on disk
