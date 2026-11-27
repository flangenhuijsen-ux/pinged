import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = "/home/claude/bon2/fonts/"; W, H = 1080, 1920
F = lambda n, s: ImageFont.truetype(FD + {"bb": "bebas.ttf", "b7": "barlow-condensed-700.ttf", "b6": "barlow-condensed-600.ttf"}[n], int(s))
RED, GRN, AMB = (255, 92, 72), (86, 236, 140), (255, 200, 90)
C = [("01-free-app", "MONDAY, JANUARY 27 · 2025", "NVIDIA", "-$589B", RED, "IN ONE DAY", "WHAT CAUSED IT", (20, 40, 90)),
     ("02-78-minutes", "FRIDAY, JULY 19 · 2024", "ONE UPDATE · ONLINE FOR", "78 MIN", AMB, "8.5 MILLION COMPUTERS DOWN", "WHY IT TOOK DAYS", (18, 42, 110)),
     ("03-oil", "MONDAY, APRIL 20 · 2020", "ONE BARREL OF US OIL", "-$37.63", RED, "BELOW ZERO", "WHO PAID WHOM", (90, 30, 22)),
     ("08-nvidia", "MONDAY, NOVEMBER 23 · 2026", "NVIDIA", "+$952B", GRN, "IN ONE DAY", "WHAT CHANGED", (14, 70, 64)),
     ("04-wrong-answer", "WEDNESDAY, FEBRUARY 8 · 2023", "GOOGLE", "-$100B", RED, "IN ONE DAY", "THE QUESTION", (14, 62, 80)),
     ("05-six-hours", "MONDAY, OCTOBER 4 · 2021", "3.5 BILLION USERS · ALMOST", "6 HOURS", AMB, "OF SILENCE", "WHY IT TOOK SO LONG", (14, 62, 80)),
     ("06-one-server", "WEDNESDAY, AUGUST 1 · 2012", "ONE TRADING FIRM", "4M", RED, "TRADES FROM JUST 212 ORDERS", "THE CAUSE", (14, 62, 80)),
     ("07-moon", "MARCH 23 · 2021 · SUEZ CANAL", "SHIPS WAITING", "422", AMB, "FOR SIX DAYS", "WHAT FREED IT", (14, 62, 80))]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def tr(d, cx, y, s, f, sp, fill, anchor="m"):
    w = sum(d.textlength(c, font=f) + sp for c in s) - sp; x = cx - w / 2 if anchor == "m" else cx
    for c in s: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp
def glass(im, box, r=44, a=34):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([box[0], box[1] + 20, box[2], box[3] + 26], r, fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle(box, r, fill=(255, 255, 255, a), outline=(255, 255, 255, 70), width=3); im.alpha_composite(g)
for name, date, pre, big, col, sub, hid, base in C:
    bg = np.zeros((H, W, 3), np.float32) + np.array(base, np.float32) * .55
    bg += np.exp(-(((xx - W * .5) / (W * .7)) ** 2 + ((yy - H * .42) / (H * .35)) ** 2))[..., None] * np.array(base, np.float32) * 1.1
    bg += np.exp(-(((xx - W * .5) / (W * .45)) ** 2 + ((yy - H * .40) / (H * .10)) ** 2))[..., None] * np.array(col, np.float32) * .22
    bg *= np.clip(1.2 - (((xx - W / 2) / W) ** 2 * 1.2 + ((yy - H * .45) / H) ** 2 * 2.2), .3, 1)[..., None]
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
    d.rounded_rectangle([W / 2 - 22, 150, W / 2 + 22, 186], 8, fill=(255, 255, 255, 210)); d.arc([W / 2 - 15, 124, W / 2 + 15, 162], 180, 360, fill=(255, 255, 255, 210), width=6)
    tr(d, W / 2, 205, date, F("b6", 58), 6, (255, 255, 255, 240))
    # main notification: the number
    y0, y1 = 310, 1180; glass(im, [60, y0, W - 60, y1]); d = ImageDraw.Draw(im)
    d.rounded_rectangle([104, y0 + 44, 184, y0 + 124], 18, fill=(255, 205, 64, 255)); d.text((144, y0 + 84), "P", font=F("b7", 62), fill=(20, 20, 24, 255), anchor="mm")
    d.text((210, y0 + 54), "PINGED", font=F("b6", 46), fill=(255, 255, 255, 220)); d.text((W - 104, y0 + 54), "NOW", font=F("b6", 40), fill=(255, 255, 255, 170), anchor="ra")
    fp = 66
    while sum(d.textlength(c, font=F("b6", fp)) + 8 for c in pre) > W - 200: fp -= 4
    tr(d, W / 2, y0 + 165, pre, F("b6", fp), 8, (255, 255, 255, 225))
    fs = 520
    while d.textlength(big, font=F("bb", fs)) > W - 170: fs -= 10
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, y0 + 250 + (520 - fs) * .30), big, font=F("bb", fs), fill=col + (255,), anchor="mt")
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26))); im.alpha_composite(gl); d = ImageDraw.Draw(im)
    fs3 = 84
    while d.textlength(sub, font=F("b7", fs3)) > W - 200: fs3 -= 4
    d.text((W / 2, y1 - 40), sub, font=F("b7", fs3), fill=(255, 255, 255, 245), anchor="mb")
    # hidden notification: the answer stays locked
    h0, h1 = 1250, 1560; glass(im, [60, h0, W - 60, h1], a=22); d = ImageDraw.Draw(im)
    lx, ly = 150, h0 + 150
    d.rounded_rectangle([lx - 46, ly - 14, lx + 46, ly + 62], 12, fill=AMB + (255,)); d.arc([lx - 32, ly - 62, lx + 32, ly + 6], 180, 360, fill=AMB + (255,), width=12)
    d.ellipse([lx - 9, ly + 8, lx + 9, ly + 26], fill=(30, 26, 20, 255))
    fh = 84
    while sum(d.textlength(c, font=F("b7", fh)) + 3 for c in hid + "?") > W - 330: fh -= 4
    tr(d, 240, h0 + 50, hid + "?", F("b7", fh), 3, AMB + (255,), "l")
    bars = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bars)
    bd.rounded_rectangle([240, h0 + 175, 930, h0 + 211], 14, fill=(255, 255, 255, 150)); bd.rounded_rectangle([240, h0 + 232, 700, h0 + 268], 14, fill=(255, 255, 255, 110))
    im.alpha_composite(bars.filter(ImageFilter.GaussianBlur(7)))
    tr(d, W / 2, h1 + 40, "1 HIDDEN NOTIFICATION", F("b6", 52), 8, (255, 255, 255, 200))
    # red marker: circle around the lock + arrow from the number down to it (visual guide)
    mk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(mk); rc = (255, 60, 48, 255)
    md.ellipse([lx - 84, ly - 100, lx + 84, ly + 96], outline=rc, width=12)
    ax0, ay0, ax1, ay1 = W / 2 + 120, y1 + 2, lx + 62, ly - 100
    pts = [(ax0 + (ax1 - ax0) * u + 0 * np.sin(np.pi * u), ay0 - 40 * np.sin(np.pi * u) + 0 + (ay1 - ay0) * u) for u in np.linspace(0, 1, 30)]
    md.line(pts, fill=rc, width=14, joint="curve")
    import math
    a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0]); hx, hy = pts[-1]
    md.polygon([(hx + 18 * math.cos(a), hy + 18 * math.sin(a)), (hx - 50 * math.cos(a) + 32 * math.sin(a), hy - 50 * math.sin(a) - 32 * math.cos(a)), (hx - 50 * math.cos(a) - 32 * math.sin(a), hy - 50 * math.sin(a) + 32 * math.cos(a))], fill=rc)
    im.alpha_composite(mk); d = ImageDraw.Draw(im)
    # brand mark at the bottom
    d.rounded_rectangle([W / 2 - 150, 1700, W / 2 - 84, 1766], 14, fill=(255, 205, 64, 255)); d.text((W / 2 - 117, 1733), "P", font=F("b7", 52), fill=(20, 20, 24, 255), anchor="mm")
    d.text((W / 2 - 64, 1733), "PINGED", font=F("bb", 84), fill=(255, 255, 255, 235), anchor="lm")
    im.convert("RGB").save(f"/home/claude/covers/v3-cover-{name}.jpg", quality=90)
