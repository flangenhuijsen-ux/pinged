import sys, os, subprocess, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = "/home/claude/bon2/fonts/"
O = "/home/claude/lock2/out/"


def F(name, size):
    return ImageFont.truetype(FD + {"bebas": "bebas.ttf", "m5": "ibm-plex-mono-500.ttf", "m6": "ibm-plex-mono-600.ttf", "m7": "ibm-plex-mono-700.ttf", "b4": "barlow-condensed-400.ttf", "b5": "barlow-condensed-500.ttf", "b6": "barlow-condensed-600.ttf", "b7": "barlow-condensed-700.ttf"}[name], size)


def smooth(u):
    u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)


def ease(u):
    u = np.clip(u, 0, 1); return 1 - (1 - u) ** 3


def spring(u):
    u = np.clip(u, 0, 1); return 1 - np.exp(-6.5 * u) * np.cos(9.0 * u)


def tracked(d, x, y, text, fnt, track=0, anchor="l", fill=255):
    ws = [d.textlength(c, font=fnt) for c in text]
    tot = sum(ws) + track * (len(text) - 1)
    if anchor == "m": x -= tot / 2
    if anchor == "r": x -= tot
    for c, w in zip(text, ws):
        d.text((x, y), c, font=fnt, fill=fill); x += w + track
    return tot


# ---------------- timeline ----------------
VD = json.load(open(O + "vo.json"))
VSTART = {}
t = 0.5
for i in range(10):
    VSTART[i] = round(t, 3); t += VD[i] + {7: 0.7, 8: 0.4}.get(i, 0.36)
DUR = round(t + 1.5, 2)
N = int(FPS * DUR)
W3 = json.load(open(O + "w3.json"))
T_A = VSTART[1] + 2.9      # update installed
T_B = VSTART[2] + 0.4      # crashing card
T_BL = VSTART[2] + 2.5     # "turn blue"
T_C1, T_C2, T_C3 = [VSTART[3] + w for w in W3]
T_D = VSTART[4] + 0.9      # flights
T_F = VSTART[5] + 0.15     # the count
T_G = VSTART[5] + 2.1      # "crashed" -> sub line
T_E = VSTART[6] + 1.3      # the bill
T_Q = VSTART[7]
T_H = VSTART[8]            # 78 minutes
T_P = VSTART[9] + 0.3      # window pill
json.dump({"VSTART": VSTART, "DUR": DUR, "T": dict(A=T_A, B=T_B, BL=T_BL, C1=T_C1, C2=T_C2, C3=T_C3, D=T_D, F=T_F, G=T_G, E=T_E, Q=T_Q, H=T_H, P=T_P)}, open(O + "tl.json", "w"))

CLOCK = [(0.0, 3 * 60 + 58), (T_A, 4 * 60 + 9), (T_C1, 6 * 60), (T_D, 11 * 60), (T_F, 17 * 60), (T_E, 23 * 60 + 59), (T_H + 0.95, 5 * 60 + 27), (DUR, 5 * 60 + 27)]


def clock_at(t):
    for (t0, m0), (t1, m1) in zip(CLOCK, CLOCK[1:]):
        if t <= t1:
            lead = min(0.9, (t1 - t0))          # spin during the last part before each key
            u = smooth((t - (t1 - lead)) / lead)
            return m0 + (m1 - m0) * u
    return CLOCK[-1][1]


MOOD = [(0, 0.0), (T_B, 0.1), (T_BL - 0.1, 0.25), (T_BL + 0.15, 0.9), (T_F + 2.0, 1.0), (T_Q, 0.8), (T_H, 0.35), (DUR, 0.25)]
GOLD = [(0, 0.0), (T_H - 0.1, 0.0), (T_H + 0.4, 0.7), (T_P + 0.3, 1.0), (DUR, 1.0)]


def key(K, t):
    for (t0, v0), (t1, v1) in zip(K, K[1:]):
        if t <= t1: return v0 + (v1 - v0) * float(smooth((t - t0) / max(1e-6, t1 - t0)))
    return K[-1][1]


# ---------------- wallpaper (aurora) ----------------
lw, lh = W // 8, H // 8
ly, lx = np.mgrid[0:lh, 0:lw].astype(np.float32)
rb = np.random.default_rng(4)
BL = rb.uniform(0, 1, (7, 6)).astype(np.float32)
CALM = np.array([[0.05, 0.40, 0.38], [0.10, 0.50, 0.45], [0.20, 0.22, 0.50], [0.04, 0.36, 0.34], [0.26, 0.28, 0.55], [0.05, 0.24, 0.30], [0.10, 0.44, 0.42]], np.float32)
RED = np.array([[0.0, 0.42, 0.95], [0.02, 0.25, 0.85], [0.05, 0.55, 1.0], [0.0, 0.18, 0.62], [0.10, 0.35, 0.95], [0.0, 0.12, 0.5], [0.0, 0.5, 0.9]], np.float32)
GLD = np.array([[0.95, 0.62, 0.12], [0.80, 0.45, 0.08], [1.0, 0.78, 0.30], [0.55, 0.30, 0.05], [0.95, 0.55, 0.15], [0.45, 0.22, 0.04], [1.0, 0.70, 0.22]], np.float32)


def wallpaper(t):
    m = key(MOOD, t); g = key(GOLD, t)
    pal = (CALM * (1 - m) + RED * m) * (1 - g) + GLD * g
    img = np.zeros((lh, lw, 3), np.float32)
    sp = 0.5 + 1.2 * m
    for k in range(7):
        cx = lw * (0.5 + 0.48 * np.sin(t * 0.21 * sp * (0.6 + BL[k, 0]) + BL[k, 1] * 6.28))
        cy = lh * (0.5 + 0.48 * np.sin(t * 0.17 * sp * (0.6 + BL[k, 2]) + BL[k, 3] * 6.28))
        r = lw * (0.42 + 0.3 * BL[k, 4])
        img += np.exp(-(((lx - cx) / r) ** 2 + ((ly - cy) / (r * 1.5)) ** 2))[..., None] * pal[k] * 0.42
    img *= (0.55 + 0.45 * (ly / lh))[..., None] * 0.9
    img += np.array([0.012, 0.014, 0.022], np.float32)
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)


# ---------------- cards ----------------
CW = 980
CX0 = (W - CW) // 2
RED8 = (255, 132, 112); AMB8 = (255, 190, 80); WHT = (255, 255, 255); BLU = (110, 185, 255); GRN = (120, 225, 150); NWS = (200, 205, 220)


def card_base(h, tint=(255, 255, 255), fill_a=30, border_a=70, radius=46):
    im = Image.new("RGBA", (CW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, CW - 1, h - 1], radius=radius, fill=(8, 10, 16, 185))
    d.rounded_rectangle([0, 0, CW - 1, h - 1], radius=radius, fill=tint + (fill_a,), outline=tint + (border_a,), width=3)
    return im, d


def icon(d, x, y, letter, col):
    d.rounded_rectangle([x, y, x + 104, y + 104], radius=28, fill=col + (255,))
    d.text((x + 52, y + 54), letter, font=F("b7", 80), fill=(12, 14, 20, 255), anchor="mm")


def std_card(app, letter, col, when, title, big, bigcol):
    h = 276
    im, d = card_base(h)
    icon(d, 34, 34, letter, col)
    tracked(d, 164, 30, app, F("b6", 50), 5, fill=(255, 255, 255, 200))
    d.text((CW - 40, 34), when, font=F("m6", 44), fill=(255, 255, 255, 180), anchor="ra")
    f = F("b7", 72 if big else 84)
    words = title.split(); lines = [""]
    maxw = CW - 164 - (345 if big else 40)
    for w in words:
        if d.textlength((lines[-1] + " " + w).strip(), font=f) <= maxw: lines[-1] = (lines[-1] + " " + w).strip()
        else: lines.append(w)
    yy0 = 118 if len(lines) == 1 else 100
    for i, ln in enumerate(lines[:2]):
        d.text((164, yy0 + i * 80), ln, font=f, fill=(255, 255, 255, 255))
    if big:
        fb = F("bebas", 200)
        while d.textlength(big, font=fb) > 320: fb = F("bebas", fb.size - 6)
        d.text((CW - 40, 186), big, font=fb, fill=bigcol + (255,), anchor="rm")
    return np.asarray(im).copy()


CARDS = {
    "A": (T_A, std_card("SECURITY", "S", GRN, "04:09 UTC", "Security update installed", "", WHT)),
    "B": (T_B, std_card("NEWS", "N", NWS, "MINUTES LATER", "Windows PCs are crashing worldwide", "", WHT)),
    "C1": (T_C1, std_card("NEWS", "N", NWS, "TODAY", "Airlines ground flights", "", WHT)),
    "C2": (T_C2, std_card("NEWS", "N", NWS, "TODAY", "Banks hit by outage", "", WHT)),
    "C3": (T_C3, std_card("NEWS", "N", NWS, "TODAY", "Hospitals hit by outage", "", WHT)),
    "D": (T_D, std_card("FLIGHTS", "F", BLU, "CIRIUM · WORLDWIDE", "Flights cancelled", "5,078", RED8)),
    "E": (T_E, std_card("DAMAGE", "$", AMB8, "PARAMETRIX EST.", "Estimated cost, Fortune 500", "$5.4B", AMB8)),
}
FH = 520
fnum = F("bebas", 200)
_d = ImageDraw.Draw(Image.new("L", (8, 8)))
fnum = F("bebas", 236)
while _d.textlength("8,500,000", font=fnum) > CW - 90: fnum = F("bebas", fnum.size - 4)
_fc = {}


def card_F(t):
    v = 8.5e6 * float(ease((t - T_F - 0.25) / 2.0)); v = round(v / 1e3) * 1e3 if v < 8.5e6 else 8.5e6
    g = float(smooth((t - T_G) / 0.4))
    kkey = (int(v // 1e3), round(g, 2))
    if kkey not in _fc:
        im, d = card_base(FH, tint=(90, 170, 255), fill_a=46, border_a=170)
        icon(d, 34, 34, "W", BLU)
        tracked(d, 164, 30, "SYSTEM", F("b6", 50), 5, fill=(255, 255, 255, 200))
        d.text((CW - 40, 34), "MICROSOFT EST.", font=F("m6", 44), fill=(255, 255, 255, 170), anchor="ra")
        tracked(d, 40, 150, "WINDOWS DEVICES CRASHED", F("b6", 54), 6, fill=(255, 255, 255, 220))
        s = f"{v:,.0f}"
        wfull = d.textlength("8,500,000", font=fnum)
        d.text((CW / 2 + wfull / 2, 330), s, font=fnum, fill=(255, 240, 234, 255), anchor="rm")
        if g > 0:
            fg = F("b7", 64)
            while d.textlength("FEWER THAN 1% OF ALL WINDOWS PCS", font=fg) > CW - 70: fg = F("b7", fg.size - 2)
            d.text((CW / 2, 462), "FEWER THAN 1% OF ALL WINDOWS PCS", font=fg, fill=AMB8 + (int(255 * g),), anchor="mm")
        _fc[kkey] = np.asarray(im).copy()
        if len(_fc) > 400: _fc.pop(next(iter(_fc)))
    return _fc[kkey]


HH = 640
_hc = {}


def card_H(t):
    p = float(spring((t - T_P) / 0.5)) if t >= T_P else 0.0
    kkey = round(p, 2)
    if kkey not in _hc:
        im, d = card_base(HH, tint=(255, 196, 90), fill_a=52, border_a=230, radius=56)
        icon(d, 34, 34, "S", (255, 196, 90))
        tracked(d, 164, 30, "SECURITY  ·  UPDATE PULLED", F("b6", 50), 5, fill=(255, 255, 255, 210))
        tracked(d, CW / 2, 128, "THE FAULTY UPDATE WAS ONLINE FOR", F("b6", 54), 8, "m", fill=(255, 255, 255, 220))
        fb = F("bebas", 300)
        while d.textlength("78 MINUTES", font=fb) > CW - 90: fb = F("bebas", fb.size - 6)
        d.text((CW / 2, 352), "78 MINUTES", font=fb, fill=(255, 255, 255, 255), anchor="mm")
        if p > 0:
            sc = min(1.15, p)
            wp, hp_ = int(800 * sc), int(150 * sc)
            x0, y0 = CW / 2 - wp / 2, 548 - hp_ / 2
            d.rounded_rectangle([x0, y0, x0 + wp, y0 + hp_], radius=hp_ // 2, fill=(255, 196, 90, 255))
            d.text((CW / 2, 552), "04:09 \u2013 05:27 UTC", font=F("m7", int(74 * sc)), fill=(20, 16, 8, 255), anchor="mm")
        _hc[kkey] = np.asarray(im).copy()
    return _hc[kkey]


STACK_Y = 640
GAP = 24
ORDERC = ["A", "B", "C1", "C2", "C3", "D", "F", "E", "H"]
TIN = {"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}
HGT = {k: 276 for k in ORDERC}; HGT["F"] = FH; HGT["H"] = HH
GL = [(T_BL, 1.0), (T_C1, 0.45), (T_C2, 0.45), (T_C3, 0.55), (T_D, 0.5), (T_F, 0.8), (T_E, 0.5), (T_H, 0.7)]


def blit(img, card, x, y, sc, alpha):
    """alpha-blend an RGBA uint8 card, scaled about its centre, top-left at (x,y) for sc=1."""
    if alpha <= 0.003: return
    h, w = card.shape[:2]
    if abs(sc - 1) > 0.002:
        nw, nh = max(2, int(w * sc)), max(2, int(h * sc))
        card = cv2.resize(card, (nw, nh), interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)
        x += (w - nw) / 2; y += (h - nh) / 2; h, w = nh, nw
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    c = card[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32) / 255
    a = c[..., 3:4] * alpha
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + c[..., :3] * a


# particles
rp = np.random.default_rng(9)
ST = np.stack([rp.uniform(0, W, 150), rp.uniform(0, H, 150), rp.uniform(6, 30, 150), rp.uniform(0.4, 1.6, 150), rp.uniform(0, 6.28, 150), rp.uniform(0.5, 2.4, 150)], 1).astype(np.float32)
BU = np.stack([rp.uniform(0, 6.28, 260), rp.uniform(120, 900, 260), rp.uniform(0.5, 1.0, 260), rp.uniform(0.6, 2.2, 260)], 1).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.42 * np.clip((((xx - W / 2) / (W * 0.85)) ** 2 + ((yy - H * 0.5) / (H * 0.66)) ** 2), 0, 1.6))[..., None]
FD_ = F("b6", 60); FCL = F("b5", 400)
BUZZ = [(T_A, 4), (T_B, 6), (T_BL, 14), (T_C1, 7), (T_C2, 7), (T_C3, 8), (T_D, 8), (T_E, 10), (T_F, 16), (T_H, 14), (T_P, 12)]


def frame(i):
    t = i / FPS
    img = wallpaper(t)
    gold = key(GOLD, t)
    # stars / motes
    mt = np.zeros((H // 4, W // 4, 3), np.float32)
    sx = (ST[:, 0] + np.sin(t * ST[:, 3] + ST[:, 4]) * 26) % W; sy = (ST[:, 1] - t * ST[:, 2]) % H
    tw = (0.5 + 0.5 * np.sin(t * 2.4 * ST[:, 3] + ST[:, 4] * 3)) * ST[:, 5]
    colp = np.array([0.8, 0.9, 1.0], np.float32) * (1 - gold) + np.array([1.0, 0.8, 0.4], np.float32) * gold
    np.add.at(mt, ((sy / 4).astype(np.int32), (sx / 4).astype(np.int32)), tw[:, None] * colp)
    # final burst
    if t >= T_P:
        u = t - T_P
        r = BU[:, 1] * (1 - np.exp(-u * 2.6 * BU[:, 3]))
        bx = W / 2 + np.cos(BU[:, 0]) * r; by = 1160 + np.sin(BU[:, 0]) * r * 0.8 + 90 * u * u
        ok = (bx >= 0) & (bx < W) & (by >= 0) & (by < H)
        np.add.at(mt, ((by[ok] / 4).astype(np.int32), (bx[ok] / 4).astype(np.int32)), (np.exp(-u * 1.5) * 5.0 * BU[ok, 2])[:, None] * np.array([1.0, 0.78, 0.36], np.float32))
    img = img + cv2.resize(cv2.GaussianBlur(mt, (0, 0), 1.5), (W, H)) * 0.9
    # red pulse when the number lands
    if t >= T_BL: img = img + np.exp(-(t - T_BL) * 3.2) * np.array([0.0, 0.42, 0.80], np.float32)
    for t0, amp in ((T_F, 0.14), (T_E, 0.08)):
        if t >= t0: img[..., 2] += amp * np.exp(-(t - t0) * 2.5)
    # buzz shake
    dx = dy = 0.0
    for t0, amp in BUZZ:
        if 0 <= t - t0 < 0.5:
            e = np.exp(-(t - t0) * 11) * amp
            dx += e * np.sin((t - t0) * 95); dy += e * 0.5 * np.sin((t - t0) * 71 + 1)
    # --- UI layer (PIL) ---
    ui = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ui)
    fade_in = float(smooth(t / 0.8))
    a8 = int(255 * fade_in)
    # lock glyph
    d.rounded_rectangle([W / 2 - 22, 92, W / 2 + 22, 128], radius=8, fill=(255, 255, 255, int(a8 * 0.85)))
    d.arc([W / 2 - 15, 66, W / 2 + 15, 104], 180, 360, fill=(255, 255, 255, int(a8 * 0.85)), width=6)
    tracked(d, W / 2, 160, "FRIDAY, JULY 19  ·  UTC", FD_, 8, "m", fill=(255, 255, 255, int(a8 * 0.9)))
    mins = clock_at(t); hh_, mm_ = int(mins // 60), int(mins % 60)
    s = f"{hh_:02d}:{mm_:02d}"
    cw = 150; x = W / 2 - (4 * cw + 70) / 2
    for ch in s:
        wd = 70 if ch == ":" else cw
        d.text((x + wd / 2, 400), ch, font=FCL, fill=(255, 255, 255, a8), anchor="mm"); x += wd
    d.rounded_rectangle([W / 2 - 150, H - 62, W / 2 + 150, H - 50], radius=6, fill=(255, 255, 255, int(a8 * 0.6)))
    tracked(d, W / 2, H - 128, "SOURCES: CROWDSTRIKE · MICROSOFT · CIRIUM · PARAMETRIX", F("m5", 27), 2, "m", fill=(255, 255, 255, int(a8 * 0.45)))
    uia = np.asarray(ui).astype(np.float32) / 255
    sh = cv2.GaussianBlur(uia[..., 3], (0, 0), 12)[..., None] * 0.5
    img = img * (1 - sh)
    img = img * (1 - uia[..., 3:4]) + uia[..., :3] * uia[..., 3:4]
    # --- notification stack: newest on top ---
    active = [k for k in ORDERC if t >= TIN[k]]
    y = float(STACK_Y)
    for k in reversed(active):
        age = t - TIN[k]
        # how far this card has been pushed is implied by the cards above it (smoothly as they enter)
        ent = float(spring(age / 0.55))
        card = card_F(t) if k == "F" else card_H(t) if k == "H" else CARDS[k][1]
        dim = 1.0
        if t >= T_Q and k != "H": dim = 1 - 0.62 * float(smooth((t - T_Q) / 0.6))
        fade = float(np.clip((1750 - (y + HGT[k])) / 130 + 1, 0, 1))
        sc = 0.86 + 0.14 * min(ent, 1.08)
        blit(img, card, CX0 + dx, y - 70 * (1 - min(ent, 1.0)) + dy, sc, float(smooth(age / 0.22)) * dim * fade)
        y += (HGT[k] + GAP) * float(ease(age / 0.38))
    # gold sweep on the final card
    if t >= T_P:
        u = (t - T_P) / 1.0
        if u < 1:
            pos = -300 + (W + 900) * u
            band = np.exp(-(((xx + yy * 0.4) - pos) / 120.0) ** 2)[..., None]
            msk = ((yy > STACK_Y) & (yy < STACK_Y + HH) & (xx > CX0) & (xx < CX0 + CW))[..., None]
            img = img + band * msk * 0.35 * np.sin(np.pi * u) * np.array([1.0, 0.85, 0.5], np.float32)
        fl = np.exp(-(t - T_P) * 9) * 0.5
        img = img + fl
    for t0, amp in GL:
        u = t - t0
        if 0 <= u < 0.36:
            rg0 = np.random.default_rng(i * 7 + 1); k = amp * (1 - u / 0.36)
            for _ in range(7):
                y0 = int(rg0.integers(0, H - 200)); hh2 = int(rg0.integers(18, 150)); sx_ = int(rg0.integers(-90, 90) * k)
                img[y0:y0 + hh2] = np.roll(img[y0:y0 + hh2], sx_, axis=1)
            o = int(14 * k) + 1
            img[..., 0] = np.roll(img[..., 0], o, axis=1); img[..., 2] = np.roll(img[..., 2], -o, axis=1)
    br = cv2.resize(np.clip(img - 0.78, 0, 1), (W // 4, H // 4))
    img = img + cv2.resize(cv2.GaussianBlur(br, (0, 0), 9), (W, H)) * 0.5
    img *= VIG
    img *= fade_in
    if t > DUR - 0.6: img *= max(0.0, (DUR - t) / 0.6)
    rg = np.random.default_rng(3000 + i)
    img += rg.standard_normal((H, W, 1), dtype=np.float32) * 0.012
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


if __name__ == "__main__":
    if sys.argv[1] == "info":
        print(DUR, N, json.load(open(O + 'tl.json')))
    elif sys.argv[1] == "test":
        for t in [float(x) for x in sys.argv[2:]]:
            Image.fromarray(frame(int(t * FPS))).save(f"{O}t_{t:05.2f}.jpg", quality=90)
    else:
        a, b, name = int(sys.argv[2]), min(int(sys.argv[3]), N), sys.argv[4]
        tmp = f"{O}{name}.part.mp4"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(a, b): p.stdin.write(frame(i).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(tmp, f"{O}{name}.mp4")
