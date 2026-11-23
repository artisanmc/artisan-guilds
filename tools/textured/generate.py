"""Draws the images of the `textured` variant (guild menus for players with the resource pack).

    python3 tools/textured/generate.py

Writes plugin/src/main/resources/artisan-system/guilds/assets/{textures,glyphs}/guilds_*.png and their
.yml descriptors. Pillow only. Vanilla palette (generic_54 / generic_27); no text in the images: the
texts are title texts and button labels, translated.
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[2] / "plugin/src/main/resources/artisan-system/guilds/assets"

CLEAR = (0, 0, 0, 0)
OUTLINE = (0, 0, 0, 255)
VBG = (198, 198, 198, 255)
VHI = (255, 255, 255, 255)
VSH = (85, 85, 85, 255)
VSLOT = (139, 139, 139, 255)
VSLOT_SH = (55, 55, 55, 255)
GOLD = (244, 200, 66, 255)
GOLD_D = (190, 132, 28, 255)
GOLD_H = (255, 238, 150, 255)
W = 176


def px(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)


def rect(img, x0, y0, x1, y1, c):  # inclusive
    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=c)


def bevel(img, x0, y0, x1, y1, fill, hi, sh):
    rect(img, x0, y0, x1, y1, fill)
    rect(img, x0, y0, x1 - 1, y0, hi)
    rect(img, x0, y0, x0, y1 - 1, hi)
    rect(img, x0 + 1, y1, x1, y1, sh)
    rect(img, x1, y0 + 1, x1, y1, sh)


def slot_xy(slot):
    return 7 + (slot % 9) * 18, 17 + (slot // 9) * 18


def vslot(img, x, y):
    """An 18x18 vanilla slot whose top-left pixel is (x, y)."""
    rect(img, x, y, x + 17, y + 17, VSLOT)
    rect(img, x, y, x + 16, y, VSLOT_SH)
    rect(img, x, y, x, y + 16, VSLOT_SH)
    rect(img, x + 1, y + 17, x + 17, y + 17, VHI)
    rect(img, x + 17, y + 1, x + 17, y + 17, VHI)


def sprite(rows, colors):
    t = Image.new("RGBA", (len(rows[0]), len(rows)), CLEAR)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in colors:
                t.putpixel((x, y), colors[ch])
    return t


# ------------------------------------------------------------------ windows

def panel(h):
    """The vanilla window panel, 176 wide, with the player's inventory at its usual place."""
    img = Image.new("RGBA", (W, h), CLEAR)
    rect(img, 3, 0, W - 4, h - 1, OUTLINE); rect(img, 0, 3, W - 1, h - 4, OUTLINE)
    rect(img, 1, 1, W - 2, h - 2, OUTLINE)
    rect(img, 2, 1, W - 3, h - 2, VBG); rect(img, 1, 2, W - 2, h - 3, VBG)
    rect(img, 3, 1, W - 5, 2, VHI); rect(img, 1, 3, 2, h - 5, VHI); px(img, 3, 3, VHI)
    rect(img, 4, h - 3, W - 3, h - 2, VSH); rect(img, W - 3, 4, W - 2, h - 4, VSH); px(img, W - 4, h - 4, VSH)
    inv = h - 83  # top of the inventory's slot frames: 139 in a 6-row window, 83 in a 3-row one
    for r in range(3):
        for c in range(9):
            vslot(img, 7 + c * 18, inv + r * 18)
    for c in range(9):
        vslot(img, 7 + c * 18, h - 25)
    return img


def groove(img, x0, x1, y):
    """An engraved line: dark, then light under it."""
    rect(img, x0, y, x1, y, VSH)
    rect(img, x0 + 1, y + 1, x1 + 1, y + 1, VHI)


def main_background():
    """The guild menu: the title area, a groove, the six cards (images of their own), the bottom row."""
    img = panel(222)
    groove(img, 7, 167, 33)
    groove(img, 7, 167, 106)
    return img


def list_background():
    """Members, ranks, rank permissions: the 28 slots of the list (10-16 ... 37-43)."""
    img = panel(222)
    gx0, gy0 = slot_xy(10)
    for r in range(4):
        for c in range(7):
            vslot(img, gx0 + c * 18, gy0 + r * 18)
    return img


def confirm_background():
    """The 3-row confirmations: one slot in the middle (13) for what is about to go, the two buttons
    under it (19-21, 23-25)."""
    img = panel(166)
    x, y = slot_xy(13)
    vslot(img, x, y)
    return img


# ------------------------------------------------------------------ icons (16x16)

def icon_members():  # two members, one behind the other
    return sprite([
        "................",
        ".......kkkkkkkk.",
        ".......kKKKKKKk.",
        ".......kKKKKKKk.",
        "..hhhhhhhhssssk.",
        "..hhhhhhhhseseK.",
        "..hhhhhhhhssssk.",
        "..hsssssshssssk.",
        "..hweswesh.ssk..",
        "..hssssssh.ccc..",
        "..hssmmssh.cccc.",
        "...ssssss..cccc.",
        ".tttttttttttccc.",
        ".tttttttttttccc.",
        ".tTTTTTTTTTtccc.",
        "................",
    ], {"h": (74, 52, 34, 255), "s": (228, 178, 140, 255), "w": VHI, "e": (60, 60, 120, 255),
        "m": (170, 110, 90, 255), "t": (60, 150, 170, 255), "T": (40, 110, 130, 255),
        "k": (40, 34, 30, 255), "K": (60, 50, 44, 255), "c": (60, 80, 150, 255)})


def icon_ranks():  # a medal on its ribbon
    return sprite([
        "................",
        "..RRR......BBB..",
        "..RrRR....BBbB..",
        "...RrRR..BBbB...",
        "....RrRRBBbB....",
        ".....RRRBBB.....",
        "......ddddd.....",
        ".....dGGGGGd....",
        "....dGHHGGGGd...",
        "....dGHGGGGGd...",
        "....dGGGSGGGd...",
        "....dGGSSSGGd...",
        "....dGGGSGGGd...",
        ".....dGGGGGd....",
        "......ddddd.....",
        "................",
    ], {"R": (200, 50, 46, 255), "r": (240, 110, 90, 255), "B": (52, 92, 170, 255), "b": (110, 150, 230, 255),
        "d": GOLD_D, "G": GOLD, "H": GOLD_H, "S": (150, 96, 20, 255)})


def icon_chest():
    return sprite([
        "................",
        "................",
        ".oooooooooooooo.",
        ".oWwwwwwwwwwwWo.",
        ".oWwwwwwwwwwwWo.",
        ".oWwwwwwwwwwwWo.",
        ".oddddddggddddo.",
        ".oWwwwwwgGwwwWo.",
        ".oWwwwwwggwwwWo.",
        ".oWwwwwwwwwwwWo.",
        ".oWwwwwwwwwwwWo.",
        ".oWwwwwwwwwwwWo.",
        ".oWWWWWWWWWWWWo.",
        ".oooooooooooooo.",
        "................",
        "................",
    ], {"o": (40, 26, 12, 255), "W": (120, 78, 36, 255), "w": (164, 112, 56, 255), "d": (70, 44, 18, 255),
        "g": (210, 210, 210, 255), "G": (110, 110, 110, 255)})


def icon_bank():  # a stack of gold coins
    return sprite([
        "................",
        "................",
        "........dddd....",
        ".......dHGGGd...",
        ".......dGGGGd...",
        "....dddddddd....",
        "...dHGGGGGGGd...",
        "...ddddddddddd..",
        "...dHGGGGGGGGd..",
        "..dddddddddddd..",
        "..dHGGGGGGGGd...",
        "..dddddddddddd..",
        "..dHGGGGGGGGGd..",
        "..dGGGGGGGGGGd..",
        "...dddddddddd...",
        "................",
    ], {"d": GOLD_D, "G": GOLD, "H": GOLD_H})


def icon_home():  # a house
    return sprite([
        "................",
        ".......oo.......",
        "......oRRo..oo..",
        ".....oRrrRo.oo..",
        "....oRrrrrRooo..",
        "...oRrrrrrrRoo..",
        "..oRrrrrrrrrRo..",
        ".oRRRRRRRRRRRRo.",
        "..oWWWWWWWWWWo..",
        "..oWBBWWWWddWo..",
        "..oWBBWWWWddWo..",
        "..oWWWWWWWddWo..",
        "..oWWWWWWWdgWo..",
        "..oWWWWWWWddWo..",
        "..oooooooooooo..",
        "................",
    ], {"o": (50, 30, 24, 255), "R": (160, 40, 36, 255), "r": (210, 70, 56, 255), "W": (226, 208, 168, 255),
        "B": (110, 170, 220, 255), "d": (110, 70, 34, 255), "g": GOLD})


def icon_logs():  # a book and its quill
    return sprite([
        "............f...",
        "...........fFf..",
        "..........fFf...",
        "..oooooooFfoo...",
        "..oPPPPPFfPPo...",
        "..oPllllqlllPo..",
        "..oPPPPqPPPPPo..",
        "..oPllqllllPPo..",
        "..oPPPPPPPPPPo..",
        "..oPllllllllPo..",
        "..oPPPPPPPPPPo..",
        "..oPllllllPPPo..",
        "..oPPPPPPPPPPo..",
        "..oBBBBBBBBBBo..",
        "..oooooooooooo..",
        "................",
    ], {"o": (60, 34, 20, 255), "P": (236, 226, 196, 255), "l": (150, 140, 120, 255), "B": (140, 60, 40, 255),
        "f": (220, 220, 220, 255), "F": (255, 255, 255, 255), "q": (60, 60, 60, 255)})


def icon_star():
    return sprite([
        "........",
        "...dd...",
        "...HG...",
        "dHHGGGGd",
        ".dGGGGd.",
        "..GGGG..",
        ".GGddGG.",
        ".Gd..dG.",
    ], {"d": GOLD_D, "G": GOLD, "H": GOLD_H})


def icon_lock():
    return sprite([
        "..oooo..",
        ".o....o.",
        ".o....o.",
        "oooooooo",
        "oGGGGGGo",
        "oGGddGGo",
        "oGGddGGo",
        "oooooooo",
    ], {"o": (60, 60, 60, 255), "G": (170, 170, 170, 255), "d": (60, 60, 60, 255)})


# ------------------------------------------------------------------ buttons

def card(icon):
    """An entry of the guild menu over 3x2 slots (54x36): a raised plate, its icon on top. The
    entry's name is the button's label, under the icon."""
    t = Image.new("RGBA", (54, 36), CLEAR)
    d = ImageDraw.Draw(t)
    d.rectangle([2, 1, 51, 34], fill=OUTLINE)
    d.rectangle([1, 2, 52, 33], fill=OUTLINE)
    d.rectangle([2, 2, 51, 33], fill=(214, 214, 214, 255))
    d.rectangle([2, 2, 50, 3], fill=VHI); d.rectangle([2, 2, 3, 32], fill=VHI)
    d.rectangle([3, 32, 51, 33], fill=(150, 150, 150, 255)); d.rectangle([50, 3, 51, 33], fill=(150, 150, 150, 255))
    t.alpha_composite(icon, (19, 5))
    return t


def button(kind):
    """A vanilla-style button over 3 slots (54x18). green: the main action; red: what cannot be
    undone; plain: a vanilla button (cancel); off: greyed, nothing to do. Its label is a title text."""
    fill, hi, sh = {
        "green": ((60, 133, 39, 255), (108, 192, 76, 255), (30, 82, 20, 255)),
        "red": ((160, 40, 36, 255), (214, 86, 74, 255), (96, 20, 18, 255)),
        "plain": ((128, 128, 128, 255), (176, 176, 176, 255), (84, 84, 84, 255)),
        "off": ((84, 84, 84, 255), (108, 108, 108, 255), (60, 60, 60, 255)),
    }[kind]
    t = Image.new("RGBA", (54, 18), CLEAR)
    d = ImageDraw.Draw(t)
    d.rectangle([0, 1, 53, 16], fill=OUTLINE)
    d.rectangle([1, 2, 52, 15], fill=fill)
    d.rectangle([1, 2, 52, 3], fill=hi); d.rectangle([1, 2, 1, 14], fill=hi)
    d.rectangle([1, 14, 52, 15], fill=sh); d.rectangle([52, 3, 52, 15], fill=sh)
    return t


def button_locked():
    t = button("off")
    t.alpha_composite(icon_lock(), (5, 5))
    return t


def tile(base, rim, rim_hi, rim_sh):
    t = Image.new("RGBA", (16, 16), CLEAR)
    bevel(t, 1, 1, 14, 14, base, rim_hi, rim_sh)
    ImageDraw.Draw(t).rectangle([0, 0, 15, 15], outline=rim)
    for c in ((0, 0), (15, 0), (0, 15), (15, 15)):
        t.putpixel(c, CLEAR)
    return t


def rank_tile(level):
    """A rank: gold with a crown for the highest, steel with two chevrons in between, wood with one for
    the lowest (that of new members)."""
    if level == "top":
        t = tile((150, 92, 200, 255), (70, 30, 110, 255), (200, 160, 236, 255), (110, 60, 160, 255))
        crown = sprite([
            "d...d...d.",
            "Gd.dGd.dG.",
            "GGdGGGdGG.",
            "GGGGGGGGG.",
            "GRGGBGGRG.",
            "ddddddddd.",
        ], {"d": GOLD_D, "G": GOLD, "R": (220, 50, 50, 255), "B": (60, 140, 240, 255)})
        t.alpha_composite(crown, (3, 5))
        return t
    if level == "middle":
        t = tile((176, 196, 214, 255), (70, 90, 120, 255), (226, 236, 246, 255), (130, 150, 176, 255))
        ink = (50, 70, 110, 255)
        n = 2
    else:
        t = tile((196, 160, 110, 255), (110, 70, 34, 255), (230, 206, 160, 255), (160, 122, 76, 255))
        ink = (100, 60, 26, 255)
        n = 1
    for k in range(n):
        yb = 11 - k * 4  # the chevron's lowest row (its two ends)
        for i in range(5):
            for dy in (0, 1):
                px(t, 3 + i, yb - i + dy, ink)
                px(t, 12 - i, yb - i + dy, ink)
    return t


def perm_on():  # granted: the green check
    t = tile((176, 200, 140, 255), (88, 112, 64, 255), (214, 230, 186, 255), (130, 156, 100, 255))
    for (x, y) in ((4, 8), (5, 9), (6, 10), (7, 9), (8, 8), (9, 7), (10, 6), (11, 5)):
        for dy in (0, 1):
            t.putpixel((x, y + dy), (40, 120, 50, 255))
    return t


def perm_off():  # not granted: a grey plate with an empty round
    t = tile((150, 150, 150, 255), (80, 80, 80, 255), (184, 184, 184, 255), (118, 118, 118, 255))
    d = ImageDraw.Draw(t)
    d.ellipse([4, 4, 11, 11], outline=(96, 96, 96, 255))
    return t


def arrow(left, enabled, w=18, h=36):
    t = Image.new("RGBA", (w, h), CLEAR)
    d = ImageDraw.Draw(t)
    cx, cy = w // 2, h // 2
    hw, hh = min(w, h * 2) // 2 - 3, h // 2 - 3
    if left:
        pts = [(cx + hw // 2, cy - hh), (cx - hw // 2 - 2, cy), (cx + hw // 2, cy + hh)]
    else:
        pts = [(cx - hw // 2, cy - hh), (cx + hw // 2 + 2, cy), (cx - hw // 2, cy + hh)]
    d.polygon(pts, fill=GOLD if enabled else (150, 150, 150, 255), outline=OUTLINE if enabled else (110, 110, 110, 255))
    return t


def close():
    t = Image.new("RGBA", (16, 16), CLEAR)
    for i in range(3, 13):
        for (x, y) in ((i, i), (i, 15 - i)):
            for dx in (0, 1):
                t.putpixel((min(15, x + dx), y), (220, 60, 50, 255))
    for i in range(3, 13):
        t.putpixel((i, i), (255, 120, 100, 255))
    return t


def back():  # back to the menu before: a small gold arrow pointing left
    return arrow(True, True, 16, 16)


def level_box():
    """The level box over slots 45-47 (54x16): a vanilla text box with a star. The level is its label."""
    t = Image.new("RGBA", (54, 16), CLEAR)
    rect(t, 0, 0, 53, 15, (160, 160, 160, 255))
    rect(t, 1, 1, 52, 14, OUTLINE)
    t.alpha_composite(icon_star(), (4, 4))
    return t


# Title glyphs (assets/glyphs): the windows, drawn by a `background` title layer from the window's top
# left (ascent 13 puts the top row at chest-y 0). Codepoints are only hints: the pack moves a glyph
# whose codepoint another project already uses.
GLYPHS = {
    "guilds_main_background": (main_background(), 0xE7C0),
    "guilds_list_background": (list_background(), 0xE7C1),
    "guilds_confirm_background": (confirm_background(), 0xE7C2),
}

# Image buttons (assets/textures).
IMAGES = {
    "guilds_card_members": card(icon_members()),
    "guilds_card_ranks": card(icon_ranks()),
    "guilds_card_chest": card(icon_chest()),
    "guilds_card_bank": card(icon_bank()),
    "guilds_card_home": card(icon_home()),
    "guilds_card_logs": card(icon_logs()),
    "guilds_level": level_box(),
    "guilds_button": button("green"),
    "guilds_button_danger": button("red"),
    "guilds_button_plain": button("plain"),
    "guilds_button_locked": button_locked(),
    "guilds_rank_top": rank_tile("top"),
    "guilds_rank": rank_tile("middle"),
    "guilds_rank_bottom": rank_tile("bottom"),
    "guilds_permission_on": perm_on(),
    "guilds_permission_off": perm_off(),
    "guilds_prev": arrow(True, True),
    "guilds_prev_off": arrow(True, False),
    "guilds_next": arrow(False, True),
    "guilds_next_off": arrow(False, False),
    "guilds_back": back(),
    "guilds_close": close(),
}


def main():
    textures, glyphs = OUT / "textures", OUT / "glyphs"
    textures.mkdir(parents=True, exist_ok=True)
    glyphs.mkdir(parents=True, exist_ok=True)
    for name, img in IMAGES.items():
        img.save(textures / f"{name}.png", optimize=True)
        (textures / f"{name}.yml").write_text(f"width: {img.width}\nheight: {img.height}\nusages: [button]\n")
    for name, (img, codepoint) in GLYPHS.items():
        img.save(glyphs / f"{name}.png", optimize=True)
        (glyphs / f"{name}.yml").write_text(
            f"codepoint: {codepoint}\nascent: 13\nwidth: {img.width}\nheight: {img.height}\nusages: [background]\n")
    print(len(IMAGES) + len(GLYPHS), "images in", OUT)


if __name__ == "__main__":
    main()
