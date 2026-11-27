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
    d.rounded_rectangle([W / 2 - 22, 300, W / 2 + 22, 336], 8, fill=(255, 255, 255, 210)); d.arc([W / 2 - 15, 274, W / 2 + 15, 312], 180, 360, fill=(255, 255, 255, 210), width=6)
    tr(d, W / 2, 360, date, F("b6", 50), 6, (255, 255, 255, 235))
    # main notification: the number
    y0, y1 = 520, 1150; glass(im, [60, y0, W - 60, y1]); d = ImageDraw.Draw(im)
    d.rounded_rectangle([104, y0 + 44, 184, y0 + 124], 18, fill=(255, 205, 64, 255)); d.text((144, y0 + 84), "P", font=F("b7", 62), fill=(20, 20, 24, 255), anchor="mm")
    d.text((210, y0 + 54), "PINGED", font=F("b6", 46), fill=(255, 255, 255, 220)); d.text((W - 104, y0 + 54), "NOW", font=F("b6", 40), fill=(255, 255, 255, 170), anchor="ra")
    tr(d, W / 2, y0 + 160, pre, F("b6", 50), 8, (255, 255, 255, 210))
    fs = 320
    while d.textlength(big, font=F("bb", fs)) > W - 200: fs -= 10
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, y0 + 225 + (320 - fs) * .35), big, font=F("bb", fs), fill=col + (255,), anchor="mt")
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26))); im.alpha_composite(gl); d = ImageDraw.Draw(im)
    fs3 = 64
    while d.textlength(sub, font=F("b7", fs3)) > W - 200: fs3 -= 4
    d.text((W / 2, y1 - 40), sub, font=F("b7", fs3), fill=(255, 255, 255, 245), anchor="mb")
    # hidden notification: the answer stays locked
    h0, h1 = 1200, 1420; glass(im, [60, h0, W - 60, h1], a=22); d = ImageDraw.Draw(im)
    lx, ly = 140, h0 + 110
    d.rounded_rectangle([lx - 34, ly - 10, lx + 34, ly + 46], 10, fill=AMB + (255,)); d.arc([lx - 24, ly - 46, lx + 24, ly + 4], 180, 360, fill=AMB + (255,), width=9)
    d.ellipse([lx - 7, ly + 6, lx + 7, ly + 20], fill=(30, 26, 20, 255))
    tr(d, 210, h0 + 40, hid, F("b7", 56), 3, AMB + (255,), "l")
    bars = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bars)
    bd.rounded_rectangle([210, h0 + 122, 860, h0 + 150], 12, fill=(255, 255, 255, 150)); bd.rounded_rectangle([210, h0 + 166, 640, h0 + 194], 12, fill=(255, 255, 255, 110))
    im.alpha_composite(bars.filter(ImageFilter.GaussianBlur(7)))
    tr(d, W / 2, h1 + 34, "1 HIDDEN NOTIFICATION", F("b6", 40), 8, (255, 255, 255, 170))
    im.convert("RGB").save(f"/home/claude/covers/v2-cover-{name}.jpg", quality=90)
