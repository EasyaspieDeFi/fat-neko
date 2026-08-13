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
# Held items must OVERLAP the body silhouette to read as held — the cat has no
# visible paws, so anything floating clear of the outline just looks detached.
HAND_X = 300                  # held items sit to the cat's left in frame (our right)
OFF_X = 74                    # off-hand items mirror them on the far side
HELD_Y = 318                  # belly height — held things hang beside the body, not the head

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
SILVER = (198, 208, 218, 255)
SILVER_D = (132, 146, 160, 255)
GREEN = (110, 200, 120, 255)
GREEN_D = (58, 138, 78, 255)
BLACK = (24, 24, 30, 255)
CHAR = (52, 52, 62, 255)       # charcoal — goth/alt fills that still read against the outline
CREAM = (245, 232, 200, 255)
NAVY = (46, 62, 122, 255)
MAROON = (140, 44, 62, 255)
LIME = (198, 240, 90, 255)
CYAN = (120, 240, 240, 255)
LILAC = (198, 170, 255, 255)


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


# ===========================================================================
# Themed sets. Each set covers enough slots that a full outfit is wearable,
# which is what makes "collect the set" mean anything in the wardrobe UI.
# ===========================================================================

def _dome(a, col, h, w=78, y=None):
    """Rounded hat crown sitting on the head."""
    y = HAT_Y if y is None else y
    a.ellipse(HEAD_CX, y - h // 2, w, h // 2, col)
    a.r(HEAD_CX - w, y - h // 2, w * 2, h // 2, col)


def _brim(a, col, w=100, h=18, y=None):
    y = HAT_Y if y is None else y
    a.r(HEAD_CX - w, y - h, w * 2, h, col)


def _torso(a, col, h=88, w=104, top=None):
    """A body garment covering the chest."""
    top = COLLAR_Y - 6 if top is None else top
    a.r(BODY_CX - w, top, w * 2, h, col)


def _shaft(a, col, x, top, bot, w=20):
    """Vertical handle for held weapons and tools."""
    a.r(x - w // 2, top, w, bot - top, col)


# ---------------------------- FANTASY (LOTR) -------------------------------
@item
def helm_knight(a):
    _dome(a, SILVER, 74, 80)
    a.r(HEAD_CX - 80, HAT_Y - 26, 160, 26, SILVER_D)      # brow band
    a.raw(HEAD_CX - 7, HAT_Y - 20, 15, 74, SILVER_D)      # nose guard
    a.r(HEAD_CX - 12, HAT_Y - 92, 24, 34, RED)            # plume socket
    a.tri(HEAD_CX, HAT_Y - 140, 20, HAT_Y - 86, RED)      # plume


@item
def plate_armor(a):
    _torso(a, SILVER, h=92, w=106)
    a.r(BODY_CX - 128, COLLAR_Y - 2, 52, 44, SILVER_D)    # pauldrons
    a.r(BODY_CX + 76, COLLAR_Y - 2, 52, 44, SILVER_D)
    a.raw(BODY_CX - 6, COLLAR_Y + 12, 12, 76, SILVER_D)   # centre seam
    a.r(BODY_CX - 106, COLLAR_Y + 64, 212, 18, GOLD)      # belt


@item
def sword(a):
    _shaft(a, SILVER, HAND_X, HELD_Y - 150, HELD_Y + 20, 26)      # blade
    a.raw(HAND_X - 14, HELD_Y - 150, 28, 22, SILVER_D)            # tip highlight
    a.r(HAND_X - 46, HELD_Y + 16, 92, 18, GOLD)                   # crossguard
    _shaft(a, BROWN, HAND_X, HELD_Y + 32, HELD_Y + 80, 18)        # grip
    a.raw(HAND_X - 13, HELD_Y + 76, 26, 18, GOLD)                 # pommel


@item
def shield_kite(a):
    cx, top = OFF_X, HELD_Y - 96
    a.r(cx - 46, top, 92, 96, SILVER)
    a.tri(cx, top + 172, 46, top + 92, SILVER)            # tapered point
    a.r(cx - 46, top, 92, 20, SILVER_D)
    a.raw(cx - 9, top + 24, 18, 92, RED)                  # cross device
    a.raw(cx - 34, top + 50, 68, 18, RED)


@item
def cloak_ranger(a):
    a.r(BODY_CX - 92, COLLAR_Y - 14, 184, 26, GREEN_D)    # shoulder yoke
    a.tri(BODY_CX, BODY_BOT + 6, 150, COLLAR_Y + 6, GREEN)
    a.r(BODY_CX - 150, BODY_BOT - 24, 300, 22, GREEN_D)   # hem


@item
def circlet_elven(a):
    a.r(HEAD_CX - 72, HAT_Y - 22, 144, 16, GOLD)
    a.raw(HEAD_CX - 11, HAT_Y - 34, 22, 22, CYAN)         # brow gem
    a.raw(HEAD_CX - 52, HAT_Y - 28, 10, 10, GOLD)
    a.raw(HEAD_CX + 42, HAT_Y - 28, 10, 10, GOLD)


@item
def hood_ranger(a):
    _dome(a, GREEN_D, 86, 92)
    a.r(HEAD_CX - 96, HAT_Y - 30, 192, 46, GREEN)         # cowl draping past the ears
    a.r(HEAD_CX - 96, HAT_Y + 8, 40, 46, GREEN_D)
    a.r(HEAD_CX + 56, HAT_Y + 8, 40, 46, GREEN_D)


@item
def bow_elven(a):
    x = HAND_X + 10
    # stepped limbs give the recurve its curve without antialiasing
    for i, (dy, off) in enumerate(((-120, 0), (-74, 12), (-26, 20), (26, 20), (74, 12), (120, 0))):
        a.raw(x + off - 11, HELD_Y + dy, 22, 48, BROWN)
    a.raw(x - 16, HELD_Y - 120, 7, 240, CREAM)            # string


@item
def axe_dwarf(a):
    _shaft(a, BROWN, HAND_X, HELD_Y - 96, HELD_Y + 74, 20)
    a.r(HAND_X - 60, HELD_Y - 102, 60, 74, SILVER)        # bit
    a.r(HAND_X, HELD_Y - 102, 44, 74, SILVER_D)
    a.raw(HAND_X - 60, HELD_Y - 76, 20, 30, SILVER_D)


@item
def staff_wizard(a):
    _shaft(a, BROWN, HAND_X, HELD_Y - 120, BODY_BOT + 8, 20)
    a.ellipse(HAND_X, HELD_Y - 134, 30, 28, LILAC)        # crystal
    a.raw(HAND_X - 10, HELD_Y - 144, 14, 14, WHITE)


# ------------------------------- Y2K ---------------------------------------
@item
def clips_butterfly(a):
    for dx, col in ((-72, PINK), (66, CYAN)):
        cx = HEAD_CX + dx
        a.tri(cx - 14, HAT_Y - 66, 18, HAT_Y - 30, col)
        a.tri(cx + 14, HAT_Y - 66, 18, HAT_Y - 30, col)
        a.raw(cx - 5, HAT_Y - 62, 10, 34, WHITE)


@item
def shades_tiny(a):
    for cx in (EYE_L, EYE_R):
        a.raw(cx - 20, EYE_CY - 9, 40, 20, PINK)
        a.raw(cx - 16, EYE_CY - 5, 32, 12, LILAC)
    a.raw(EYE_L + 20, EYE_CY - 3, 44, 7, PINK)


@item
def vest_puffer(a):
    for i in range(4):                                     # quilted horizontal baffles
        a.r(BODY_CX - 100, COLLAR_Y + 2 + i * 22, 200, 18, LILAC)
    a.r(BODY_CX - 100, COLLAR_Y - 12, 200, 18, CYAN)       # collar
    a.raw(BODY_CX - 6, COLLAR_Y + 2, 12, 88, CYAN)         # zip


@item
def flip_phone(a):
    x, y = HAND_X, HELD_Y - 34
    a.r(x - 30, y, 60, 60, PINK)
    a.r(x - 30, y + 58, 60, 56, LILAC)
    a.raw(x - 20, y + 10, 40, 34, CYAN)                    # screen
    a.raw(x - 20, y + 68, 40, 34, WHITE)                   # keypad


@item
def trucker_hat(a):
    _dome(a, WHITE, 52, 74)
    a.r(HEAD_CX - 74, HAT_Y - 30, 148, 30, PINK)           # foam front panel
    a.r(HEAD_CX - 140, HAT_Y - 16, 78, 18, PINK)           # flat brim
    a.raw(HEAD_CX - 24, HAT_Y - 26, 48, 16, CYAN)


# --------------------------- STREETWEAR ------------------------------------
@item
def snapback(a):
    _dome(a, CHAR, 54, 76)
    a.r(HEAD_CX - 76, HAT_Y - 22, 152, 22, BLACK)
    a.r(HEAD_CX + 60, HAT_Y - 20, 92, 20, BLACK)           # flat brim, worn forward
    a.raw(HEAD_CX - 26, HAT_Y - 48, 52, 18, LIME)          # logo patch


@item
def chain_gold(a):
    for i, dx in enumerate(range(-70, 82, 22)):
        dip = abs(i - 3) * 6
        a.raw(BODY_CX + dx, COLLAR_Y + 34 - dip, 20, 20, GOLD)
    a.raw(BODY_CX - 16, COLLAR_Y + 52, 32, 32, GOLD_D)     # pendant


@item
def bucket_hat(a):
    _dome(a, LIME, 46, 76)
    a.r(HEAD_CX - 108, HAT_Y - 20, 216, 26, GREEN)         # downturned brim
    a.r(HEAD_CX - 78, HAT_Y - 34, 156, 14, GREEN_D)


@item
def boombox(a):
    x, y = HAND_X - 6, HELD_Y - 26
    a.r(x - 56, y, 112, 78, CHAR)
    a.ellipse(x - 28, y + 38, 22, 22, SILVER)              # speakers
    a.ellipse(x + 28, y + 38, 22, 22, SILVER)
    a.raw(x - 20, y + 8, 40, 16, LIME)                     # tape deck
    a.raw(x - 46, y - 26, 92, 8, SILVER_D)                 # handle


@item
def puffer_jacket(a):
    for i in range(5):
        a.r(BODY_CX - 112, COLLAR_Y - 4 + i * 21, 224, 17, ORANGE)
    a.r(BODY_CX - 96, COLLAR_Y - 22, 192, 20, (214, 120, 58, 255))
    a.raw(BODY_CX - 6, COLLAR_Y - 4, 12, 106, SILVER)


# --------------------------- WORLD CUP -------------------------------------
@item
def jersey(a):
    _torso(a, WHITE, h=92, w=104)
    for dx in (-72, -24, 24, 72):                          # vertical stripes
        a.raw(BODY_CX + dx - 11, COLLAR_Y - 6, 22, 92, BLUE)
    a.r(BODY_CX - 104, COLLAR_Y - 6, 208, 18, NAVY)        # collar
    a.raw(BODY_CX - 14, COLLAR_Y + 34, 28, 40, NAVY)       # squad number


@item
def soccer_ball(a):
    cx, cy = HAND_X + 4, HELD_Y + 34
    a.ellipse(cx, cy, 46, 46, WHITE)
    a.raw(cx - 13, cy - 24, 26, 26, BLACK)                 # pentagons
    a.raw(cx - 34, cy + 6, 20, 20, BLACK)
    a.raw(cx + 14, cy + 6, 20, 20, BLACK)


@item
def headband_sport(a):
    a.r(HEAD_CX - 78, HAT_Y + 2, 156, 26, WHITE)
    a.raw(HEAD_CX - 78, HAT_Y + 10, 156, 9, RED)


@item
def trophy(a):
    x = OFF_X
    a.ellipse(x, HELD_Y - 28, 42, 40, GOLD)
    a.r(x - 42, HELD_Y - 62, 84, 34, GOLD)                 # cup mouth
    a.raw(x - 62, HELD_Y - 52, 22, 44, GOLD_D)             # handles
    a.raw(x + 40, HELD_Y - 52, 22, 44, GOLD_D)
    _shaft(a, GOLD_D, x, HELD_Y + 8, HELD_Y + 46, 22)
    a.r(x - 40, HELD_Y + 42, 80, 24, GOLD_D)               # plinth


@item
def keeper_gloves(a):
    x = OFF_X
    a.r(x - 34, HELD_Y - 26, 68, 76, LIME)
    a.raw(x - 34, HELD_Y - 32, 68, 16, CHAR)               # cuff
    for dx in (-24, -2, 20):                               # fingers
        a.raw(x + dx, HELD_Y - 48, 16, 30, LIME)


# ------------------------------ GOTH ---------------------------------------
@item
def choker_spike(a):
    a.r(BODY_CX - 68, COLLAR_Y + 2, 136, 24, BLACK)
    for dx in range(-58, 62, 20):                          # spikes
        a.tri(BODY_CX + dx, COLLAR_Y - 12, 8, COLLAR_Y + 4, SILVER)


@item
def veil_black(a):
    _dome(a, BLACK, 40, 68)
    a.r(HEAD_CX - 90, HAT_Y - 24, 180, 22, CHAR)
    for i in range(4):                                     # lace falling past the ears
        a.raw(HEAD_CX - 90 + i * 48, HAT_Y - 2, 34, 62, (52, 52, 62, 190))


@item
def bat_wings(a):
    for s in (-1, 1):
        for i in range(4):
            span = 120 - i * 22
            x = BODY_CX + s * (92 + i * 30)
            a.r(x - (28 if s < 0 else 0), BODY_TOP - 34 + i * 20, 30, span, CHAR)
            a.tri(x + (-14 if s < 0 else 14), BODY_TOP - 34 + i * 20 + span + 26,
                  15, BODY_TOP - 34 + i * 20 + span, CHAR)   # scalloped tips


@item
def candelabra(a):
    x = HAND_X
    _shaft(a, SILVER_D, x, HELD_Y - 40, HELD_Y + 60, 18)
    a.r(x - 52, HELD_Y - 44, 104, 16, SILVER_D)            # arms
    for dx in (-46, 0, 46):
        a.raw(x + dx - 9, HELD_Y - 78, 18, 36, CREAM)      # candles
        a.tri(x + dx, HELD_Y - 104, 8, HELD_Y - 78, ORANGE)
    a.r(x - 34, HELD_Y + 54, 68, 18, SILVER_D)


@item
def shades_goth(a):
    for cx in (EYE_L, EYE_R):
        a.ellipse(cx, EYE_CY, 30, 28, BLACK)
        a.raw(cx - 18, EYE_CY - 14, 14, 7, (120, 120, 140, 255))
    a.raw(EYE_L + 26, EYE_CY - 4, 34, 8, BLACK)


# ------------------------------- ALT ---------------------------------------
@item
def band_tee(a):
    _torso(a, BLACK, h=88, w=100)
    a.raw(BODY_CX - 58, COLLAR_Y + 20, 116, 12, WHITE)     # scrawled band logo
    a.raw(BODY_CX - 42, COLLAR_Y + 40, 84, 10, WHITE)
    a.raw(BODY_CX - 26, COLLAR_Y + 58, 52, 8, RED)


@item
def studded_jacket(a):
    _torso(a, CHAR, h=92, w=106)
    a.raw(BODY_CX - 106, COLLAR_Y - 6, 30, 92, BLACK)      # open lapels
    a.raw(BODY_CX + 76, COLLAR_Y - 6, 30, 92, BLACK)
    for dx in range(-96, 100, 24):                         # shoulder studs
        a.raw(BODY_CX + dx, COLLAR_Y + 4, 10, 10, SILVER)


@item
def guitar(a):
    x = HAND_X - 2
    a.ellipse(x, HELD_Y + 44, 52, 46, RED_D)               # body
    a.ellipse(x, HELD_Y + 12, 40, 34, RED_D)
    a.raw(x - 9, HELD_Y + 8, 18, 26, BLACK)                # sound hole
    _shaft(a, BROWN, x, HELD_Y - 108, HELD_Y, 20)          # neck
    a.r(x - 18, HELD_Y - 124, 36, 22, CHAR)                # headstock


@item
def dyed_bangs(a):
    a.r(HEAD_CX - 82, HAT_Y - 14, 164, 34, LILAC)
    for i, dx in enumerate(range(-76, 80, 26)):            # choppy fringe
        a.raw(HEAD_CX + dx, HAT_Y + 16, 22, 26 + (10 if i % 2 else 0), LILAC)
    a.raw(HEAD_CX - 82, HAT_Y - 14, 40, 20, CYAN)          # streak


@item
def piercings(a):
    a.raw(EYE_L - 34, EYE_CY - 26, 12, 12, SILVER)         # brow bar
    a.raw(EYE_L - 34, EYE_CY - 26, 30, 5, SILVER)
    a.raw(EYE_CX - 4, EYE_CY + 30, 12, 12, SILVER)         # septum
    a.raw(EYE_R + 26, EYE_CY + 4, 10, 10, SILVER)


# ------------------------------- PREP --------------------------------------
@item
def sweater_vest(a):
    _torso(a, GOLD, h=86, w=98)
    a.tri(BODY_CX, COLLAR_Y + 38, 40, COLLAR_Y - 8, NAVY)  # V-neck
    a.r(BODY_CX - 98, COLLAR_Y + 68, 196, 18, NAVY)        # ribbed hem
    for dx in (-60, 0, 60):
        a.raw(BODY_CX + dx - 20, COLLAR_Y + 46, 40, 8, NAVY)


@item
def polo_collar(a):
    _torso(a, MINT, h=80, w=96)
    a.tri(BODY_CX - 34, COLLAR_Y + 30, 26, COLLAR_Y - 14, WHITE)   # popped collar
    a.tri(BODY_CX + 34, COLLAR_Y + 30, 26, COLLAR_Y - 14, WHITE)
    a.raw(BODY_CX - 5, COLLAR_Y + 6, 10, 40, WHITE)                # placket
    a.raw(BODY_CX + 44, COLLAR_Y + 26, 20, 16, NAVY)               # crest


@item
def tennis_racket(a):
    x = HAND_X + 2
    # strings first, then the frame over them
    for i in range(-2, 3):
        a.raw(x + i * 16 - 3, HELD_Y - 116, 6, 92, CREAM)
        a.raw(x - 40, HELD_Y - 108 + i * 18, 80, 6, CREAM)
    a.d.ellipse([x - 44, HELD_Y - 124, x + 44, HELD_Y - 20], outline=NAVY, width=13)
    _shaft(a, NAVY, x, HELD_Y - 24, HELD_Y + 58, 18)


@item
def headband_prep(a):
    a.r(HEAD_CX - 76, HAT_Y - 2, 152, 22, NAVY)
    a.raw(HEAD_CX - 76, HAT_Y + 4, 152, 7, WHITE)
    a.raw(HEAD_CX + 44, HAT_Y - 12, 22, 22, WHITE)


@item
def pearls(a):
    for i, dx in enumerate(range(-64, 70, 18)):
        dip = abs(i - 3) * 5
        a.raw(BODY_CX + dx, COLLAR_Y + 26 - dip, 17, 17, CREAM)


# ------------------------------- JOCK --------------------------------------
@item
def sweatband(a):
    a.r(HEAD_CX - 80, HAT_Y - 4, 160, 30, WHITE)
    a.raw(HEAD_CX - 80, HAT_Y + 4, 160, 8, RED)
    a.raw(HEAD_CX - 80, HAT_Y + 14, 160, 8, BLUE)


@item
def gym_tank(a):
    _torso(a, WHITE, h=84, w=88)
    a.raw(BODY_CX - 88, COLLAR_Y - 6, 26, 84, TEAL_D)      # deep armholes
    a.raw(BODY_CX + 62, COLLAR_Y - 6, 26, 84, TEAL_D)
    a.raw(BODY_CX - 30, COLLAR_Y + 24, 60, 34, RED)        # big number


@item
def football(a):
    cx, cy = HAND_X + 2, HELD_Y + 8
    a.ellipse(cx, cy, 52, 36, BROWN)
    a.raw(cx - 22, cy - 4, 44, 8, WHITE)                   # laces
    for dx in (-12, 0, 12):
        a.raw(cx + dx, cy - 12, 6, 24, WHITE)


@item
def whistle(a):
    a.raw(BODY_CX - 60, COLLAR_Y + 4, 120, 7, RED)         # lanyard
    a.raw(BODY_CX + 30, COLLAR_Y + 8, 8, 44, RED)
    a.r(BODY_CX + 18, COLLAR_Y + 46, 44, 26, SILVER)
    a.raw(BODY_CX + 54, COLLAR_Y + 52, 18, 14, SILVER_D)


@item
def medal_gold(a):
    a.raw(BODY_CX - 26, COLLAR_Y - 6, 12, 54, BLUE)        # ribbon
    a.raw(BODY_CX + 14, COLLAR_Y - 6, 12, 54, BLUE)
    a.ellipse(BODY_CX, COLLAR_Y + 66, 34, 32, GOLD)
    a.raw(BODY_CX - 10, COLLAR_Y + 54, 20, 24, GOLD_D)     # embossed "1"


# ------------------------------- NERD --------------------------------------
@item
def glasses_thick(a):
    for cx in (EYE_L, EYE_R):
        a.d.rectangle([cx - 38, EYE_CY - 30, cx + 38, EYE_CY + 30], outline=CHAR, width=11)
        a.raw(cx - 30, EYE_CY - 22, 22, 9, (255, 255, 255, 110))
    a.raw(EYE_L + 38, EYE_CY - 5, 40, 11, CHAR)
    a.raw(EYE_CX - 6, EYE_CY - 8, 14, 16, WHITE)           # taped bridge


@item
def lab_coat(a):
    _torso(a, WHITE, h=104, w=110)
    a.raw(BODY_CX - 6, COLLAR_Y - 6, 12, 104, (208, 214, 220, 255))   # button placket
    a.tri(BODY_CX - 40, COLLAR_Y + 30, 28, COLLAR_Y - 10, (208, 214, 220, 255))
    a.tri(BODY_CX + 40, COLLAR_Y + 30, 28, COLLAR_Y - 10, (208, 214, 220, 255))
    a.raw(BODY_CX + 40, COLLAR_Y + 50, 44, 34, (208, 214, 220, 255))  # chest pocket
    a.raw(BODY_CX + 52, COLLAR_Y + 42, 8, 22, BLUE)                   # pens
    a.raw(BODY_CX + 66, COLLAR_Y + 42, 8, 22, RED)


@item
def book(a):
    x, y = HAND_X - 2, HELD_Y - 16
    a.r(x - 48, y, 96, 74, MAROON)
    a.raw(x - 40, y + 8, 80, 58, CREAM)                    # pages
    a.raw(x - 2, y + 8, 6, 58, MAROON)                     # spine
    for i in range(4):
        a.raw(x - 34, y + 18 + i * 11, 28, 5, (150, 150, 160, 255))


@item
def propeller_beanie(a):
    _dome(a, RED, 46, 66)
    a.raw(HEAD_CX - 66, HAT_Y - 24, 132, 14, BLUE)
    a.raw(HEAD_CX - 5, HAT_Y - 74, 12, 30, SILVER_D)       # spindle
    a.raw(HEAD_CX - 62, HAT_Y - 82, 58, 14, LIME)          # blades
    a.raw(HEAD_CX + 6, HAT_Y - 92, 58, 14, CYAN)


@item
def calculator(a):
    x, y = OFF_X, HELD_Y - 40
    a.r(x - 34, y, 68, 92, CHAR)
    a.raw(x - 26, y + 8, 52, 22, LIME)                     # display
    for r_ in range(3):
        for c_ in range(3):
            a.raw(x - 26 + c_ * 20, y + 40 + r_ * 17, 14, 12, SILVER_D)


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


BACK_SLOT = {"cape", "jetpack", "wings", "sun_aura", "cloak_ranger", "bat_wings"}
NO_OUTLINE = {"sun_aura"}      # soft glows an outline would ruin


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
        rendered[name] = a.finish(name, ow=0 if name in NO_OUTLINE else 5)
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
