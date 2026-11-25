#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up
Wednesday 25 November 2026 in six verified stories.

Pure Pillow drawing primitives: no photos, no network, no external
assets beyond the system DejaVu fonts. The render is deterministic —
the same code always writes the same bytes.

Run:  python3 draw.py   (writes entry.png beside this file)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26  # outer margin

PAPER = (247, 243, 231)
INK = (24, 24, 24)
MUTED = (96, 91, 80)
NAVY = (21, 34, 62)
GOLD = (196, 152, 58)
RED = (176, 32, 22)
GREEN = (28, 118, 50)
BLUE = (34, 82, 136)
ORANGE = (212, 94, 18)
CARD = (255, 253, 245)
CARD_LINE = (203, 196, 176)
TINT_BLUE = (224, 234, 244)
TINT_RED = (244, 226, 222)
TINT_GOLD = (243, 234, 210)
TINT_GREEN = (230, 242, 230)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, fill, lead):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lead
    return y


# ------------------------------------------------------------- pictograms
def pic_pumpjack(d, x, y, s):
    """Oil pumpjack on a desert strip: Baghdad's oilfields move."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_GOLD, outline=CARD_LINE)
    d.rectangle([x, y + s * 0.82, x + s, y + s], fill=(210, 182, 120))
    # tower legs
    d.line([(x + s * 0.30, y + s * 0.82), (x + s * 0.42, y + s * 0.30)],
           fill=INK, width=6)
    d.line([(x + s * 0.62, y + s * 0.82), (x + s * 0.50, y + s * 0.30)],
           fill=INK, width=6)
    # walking beam
    d.line([(x + s * 0.18, y + s * 0.34), (x + s * 0.86, y + s * 0.24)],
           fill=INK, width=8)
    # horse head + rod
    d.polygon([(x + s * 0.80, y + s * 0.24), (x + s * 0.92, y + s * 0.30),
               (x + s * 0.86, y + s * 0.40), (x + s * 0.78, y + s * 0.34)],
              fill=INK)
    d.line([(x + s * 0.86, y + s * 0.38), (x + s * 0.86, y + s * 0.82)],
           fill=INK, width=4)
    # counterweight
    d.ellipse([x + s * 0.12, y + s * 0.30, x + s * 0.26, y + s * 0.44],
              fill=INK)
    # sun
    d.ellipse([x + s * 0.68, y + s * 0.08, x + s * 0.84, y + s * 0.24],
              fill=GOLD)


def pic_falling(d, x, y, s):
    """Three shrinking bars and a red down arrow: the market slide."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_RED, outline=CARD_LINE)
    base = y + s * 0.80
    widths = s * 0.17
    heights = (0.52, 0.36, 0.20)
    for i, h in enumerate(heights):
        bx = x + s * 0.16 + i * s * 0.26
        d.rectangle([bx, base - s * h, bx + widths, base], fill=RED)
    d.line([(x + s * 0.14, y + s * 0.16), (x + s * 0.44, y + s * 0.38),
            (x + s * 0.62, y + s * 0.30), (x + s * 0.88, y + s * 0.62)],
           fill=INK, width=6)
    d.polygon([(x + s * 0.88, y + s * 0.62), (x + s * 0.72, y + s * 0.58),
               (x + s * 0.86, y + s * 0.76)], fill=INK)


def pic_shield(d, x, y, s):
    """A shield split by a crack: the intelligence breach."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_BLUE, outline=CARD_LINE)
    cx, top, bot = x + s * 0.5, y + s * 0.14, y + s * 0.88
    pts = [(cx - s * 0.30, top), (cx + s * 0.30, top),
           (cx + s * 0.30, y + s * 0.52), (cx, bot), (cx - s * 0.30, y + s * 0.52)]
    d.polygon(pts, fill=NAVY)
    # crack down the middle
    d.line([(cx, top + s * 0.06), (cx - s * 0.05, y + s * 0.38),
            (cx + s * 0.05, y + s * 0.55), (cx - s * 0.02, y + s * 0.74)],
           fill=(255, 255, 255), width=5)
    # keyhole
    d.ellipse([cx - s * 0.05, y + s * 0.34, cx + s * 0.05, y + s * 0.44],
              fill=(255, 255, 255))
    d.polygon([(cx - s * 0.03, y + s * 0.42), (cx + s * 0.03, y + s * 0.42),
               (cx + s * 0.06, y + s * 0.56), (cx - s * 0.06, y + s * 0.56)],
              fill=(255, 255, 255))


def pic_gavel(d, x, y, s):
    """A judge's gavel over a document: the sanctions."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_BLUE, outline=CARD_LINE)
    # document
    d.rectangle([x + s * 0.16, y + s * 0.52, x + s * 0.84, y + s * 0.86],
                fill=(255, 255, 255), outline=INK, width=3)
    for i in range(3):
        yy = y + s * (0.60 + i * 0.08)
        d.line([(x + s * 0.24, yy), (x + s * 0.76, yy)], fill=MUTED, width=3)
    # gavel head
    d.line([(x + s * 0.24, y + s * 0.30), (x + s * 0.68, y + s * 0.12)],
           fill=INK, width=16)
    d.line([(x + s * 0.30, y + s * 0.44), (x + s * 0.62, y + s * 0.28)],
           fill=INK, width=4)
    # handle
    d.line([(x + s * 0.46, y + s * 0.22), (x + s * 0.70, y + s * 0.52)],
           fill=INK, width=8)


def pic_ball(d, x, y, s):
    """A football: the Champions League night."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_GREEN, outline=CARD_LINE)
    cx, cy, r = x + s * 0.5, y + s * 0.52, s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=4)
    # centre pentagon
    pr = r * 0.34
    pent = []
    for k in range(5):
        ang = -90 + k * 72
        import math
        pent.append((cx + pr * math.cos(math.radians(ang)),
                     cy + pr * math.sin(math.radians(ang))))
    d.polygon(pent, fill=INK)
    # seams to the edge
    for k in range(5):
        ang = -90 + k * 72
        import math
        ex = cx + r * 0.95 * math.cos(math.radians(ang))
        ey = cy + r * 0.95 * math.sin(math.radians(ang))
        vx = cx + pr * math.cos(math.radians(ang))
        vy = cy + pr * math.sin(math.radians(ang))
        d.line([(vx, vy), (ex, ey)], fill=INK, width=3)


def pic_blast(d, x, y, s):
    """A blast burst over a street: the car bomb."""
    import math
    d.rectangle([x, y, x + s, y + s], fill=TINT_RED, outline=CARD_LINE)
    cx, cy = x + s * 0.5, y + s * 0.44
    star = []
    for k in range(16):
        ang = k * 22.5
        rr = s * 0.36 if k % 2 == 0 else s * 0.16
        star.append((cx + rr * math.cos(math.radians(ang)),
                     cy + rr * math.sin(math.radians(ang))))
    d.polygon(star, fill=ORANGE, outline=INK)
    d.ellipse([cx - s * 0.09, cy - s * 0.09, cx + s * 0.09, cy + s * 0.09],
              fill=(255, 255, 255))
    # street + building silhouettes
    d.rectangle([x + s * 0.10, y + s * 0.78, x + s * 0.34, y + s * 0.96],
                fill=INK)
    d.rectangle([x + s * 0.62, y + s * 0.72, x + s * 0.90, y + s * 0.96],
                fill=INK)
    d.rectangle([x, y + s * 0.96, x + s, y + s], fill=(60, 60, 60))


# ------------------------------------------------------------------ layout
def card(d, x, y, w, h, kicker, head, body, pic, kicker_col):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=2)
    ps = h - 24
    pic(d, x + 12, y + 12, ps)
    tx = x + 12 + ps + 14
    tw = w - (12 + ps + 14) - 14
    f_kick = load(SANS_B, 17)
    f_head = load(SERIF, 26)
    f_body = load(SANS, 19)
    d.text((tx, y + 14), kicker, font=f_kick, fill=kicker_col)
    lines = wrap(d, head, f_head, tw)
    yy = block(d, tx, y + 38, lines, f_head, INK, 29)
    blines = wrap(d, body, f_body, tw)
    # never let the body spill past the card's bottom edge
    room = y + h - 12 - (yy + 4)
    blines = blines[: max(1, room // 23)]
    block(d, tx, yy + 4, blines, f_body, MUTED, 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([(M, M + 6), (W - M, M + 6)], fill=NAVY, width=4)
    f_title = load(SERIF, 62)
    title = "WEDNESDAY ECHO"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, M + 16), title, font=f_title, fill=NAVY)
    f_sub = load(SANS, 23)
    sub = "The world in one page  ·  Wednesday 25 November 2026"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, M + 92), sub, font=f_sub, fill=MUTED)
    d.line([(M, M + 128), (W - M, M + 128)], fill=GOLD, width=3)

    y = M + 142
    cw = W - 2 * M

    # lead story: Iraq
    lead_h = 218
    d.rectangle([M, y, M + cw, y + lead_h], fill=CARD, outline=CARD_LINE,
                width=2)
    pic_pumpjack(d, M + 12, y + 12, lead_h - 24)
    tx = M + 12 + (lead_h - 24) + 16
    tw = cw - (12 + (lead_h - 24) + 16) - 16
    d.text((tx, y + 16), "MIDDLE EAST  ·  LEAD", font=load(SANS_B, 18),
           fill=RED)
    head = "Baghdad orders takeover of Kurdish oilfields"
    hl = wrap(d, head, load(SERIF, 34), tw)
    yy = block(d, tx, y + 44, hl, load(SERIF, 34), INK, 38)
    body = ("PM Ali al-Zaidi puts the Oil Ministry in charge of fields in "
            "four provinces and all border crossings after a smuggling "
            "probe. Kurdish leaders reject the move outright.")
    bl = wrap(d, body, load(SANS, 21), tw)
    block(d, tx, yy + 6, bl, load(SANS, 21), MUTED, 26)
    y += lead_h + 12

    # two-by-two grid
    grid = [
        ("MARKETS", "Nvidia falls 7% as Congress turns on Huang",
         "Down about 7% to $153 after Monday's 31% surge.",
         pic_falling, RED),
        ("UNITED STATES", "CIA and US intelligence hit by cyber breach",
         "Unclassified data exposed; classified systems safe.",
         pic_shield, NAVY),
        ("EUROPE", "Britain sanctions the Houthis and four officials",
         "Asset freezes, travel bans over torture of detainees.",
         pic_gavel, BLUE),
        ("SPORT", "Real Madrid 5–1 PSV: five goals, five wins",
         "Mbappé brace; Bellingham stunner seals it.",
         pic_ball, GREEN),
    ]
    gw = (cw - 12) // 2
    gh = 198
    for i, (kick, head, body, pic, col) in enumerate(grid):
        gx = M + (i % 2) * (gw + 12)
        gy = y + (i // 2) * (gh + 12)
        card(d, gx, gy, gw, gh, kick, head, body, pic, col)
    y += 2 * gh + 12 + 12

    # bottom strip: Colombia
    strip_h = 132
    d.rectangle([M, y, M + cw, y + strip_h], fill=CARD, outline=CARD_LINE,
                width=2)
    pic_blast(d, M + 12, y + 12, strip_h - 24)
    tx = M + 12 + (strip_h - 24) + 16
    tw = cw - (12 + (strip_h - 24) + 16) - 16
    d.text((tx, y + 14), "AMERICAS", font=load(SANS_B, 17), fill=ORANGE)
    hl = wrap(d, "Car bomb wounds 23 in Colombia", load(SERIF, 27), tw)
    yy = block(d, tx, y + 38, hl, load(SERIF, 27), INK, 30)
    bl = wrap(d, "A blast outside government offices in Villavicencio; "
              "prosecutors suspect FARC-EMC rebels.",
              load(SANS, 20), tw)
    block(d, tx, yy + 4, bl, load(SANS, 20), MUTED, 24)
    y += strip_h + 12

    # footer
    f_foot = load(SANS, 16)
    foot = "Six stories, each verified against at least two sources  ·  25 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, y + 2), foot, font=f_foot, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
