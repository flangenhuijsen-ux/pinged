import sys, json, math, subprocess, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/claude/eng"); import builder
STORY = os.environ.get("STORY", "l1n"); _o = builder.build(STORY); globals().update(_o)
FD = "/home/claude/bon2/fonts/"
W, H, FPS = 1920, 1080, 30
_f = {}
def F(n, s):
    k = (n, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(FD + {"bb": "bebas.ttf", "b5": "barlow-condensed-500.ttf", "b6": "barlow-condensed-600.ttf", "b7": "barlow-condensed-700.ttf", "m6": "ibm-plex-mono-600.ttf"}[n], int(s))
    return _f[k]
R = (255, 92, 78); G = (96, 235, 140); A = (255, 196, 90); Wh = (255, 255, 255); N = (200, 205, 220); B = (110, 185, 255)
NF = int(DUR * FPS)
# ---------------- helpers
def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def spring(x):
    if x <= 0: return 0.0
    return 1 - math.exp(-7 * x) * math.cos(11 * x)
def tracked(d, x, y, s, font, tr, fill, anchor="l"):
    ws = [d.textlength(c, font=font) for c in s]; tot = sum(ws) + tr * max(0, len(s) - 1)
    if anchor == "m": x -= tot / 2
    if anchor == "r": x -= tot
    for c, w in zip(s, ws): d.text((x, y), c, font=font, fill=fill); x += w + tr
def fit(d, s, name, size, maxw):
    f = F(name, size)
    while d.textlength(s, font=f) > maxw and size > 20: size -= 4; f = F(name, size)
    return f
def wrap(d, s, font, maxw):
    out = []; cur = ""
    for w in s.split():
        if d.textlength((cur + " " + w).strip(), font=font) <= maxw: cur = (cur + " " + w).strip()
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out
def last(seq, t, key=lambda x: x[0]):
    r = None
    for x in seq:
        if key(x) <= t: r = x
    return r
PW, PH_ = 540, 890; PX, PY = (W - PW) // 2, 22
CW, CHh = PW - 40, 138
_cc = {}
def card_img(c):
    if c in _cc: return _cc[c]
    app, letter, col, title, big, bcol = c
    im = Image.new("RGBA", (CW, CHh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, CW - 1, CHh - 1], 28, fill=(8, 10, 16, 190)); d.rounded_rectangle([0, 0, CW - 1, CHh - 1], 28, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=2)
    d.rounded_rectangle([14, 14, 60, 60], 13, fill=col + (255,)); d.text((37, 37), letter, font=F("b7", 34), fill=(8, 10, 16, 255), anchor="mm")
    tracked(d, 74, 15, app, F("b6", 23), 3, (255, 255, 255, 180)); d.text((CW - 18, 16), "now", font=F("b5", 24), fill=(255, 255, 255, 120), anchor="ra")
    bw = 0
    if big:
        bcol = (255, 150, 132) if bcol == R else bcol; fb = fit(d, big, "bb", 84, 200); bw = d.textlength(big, font=fb) + 14; d.text((CW - 18, 92), big, font=fb, fill=bcol + (255,), anchor="rm")
    ft = F("b7", 33); ls = wrap(d, title, ft, CW - 74 - 18 - bw)[:2]
    for j, s_ in enumerate(ls): d.text((74, 54 + j * 36 + (12 if len(ls) == 1 else 0)), s_, font=ft, fill=(255, 255, 255, 255))
    _cc[c] = im; return im
def hidden_img(sh):
    im = Image.new("RGBA", (CW, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, CW - 1, 91], 26, fill=(20, 18, 10, 245), outline=A + (230,), width=3)
    d.rounded_rectangle([24, 40, 62, 72], 7, fill=A + (255,)); d.arc([30, 18, 56, 52], 180, 360, fill=A + (255,), width=6)
    tracked(d, 82, 14, "1 HIDDEN NOTIFICATION", F("b7", 32), 2, (255, 255, 255, 255)); tracked(d, 82, 54, HIDLAB, F("b6", 23), 3, A + (235,))
    x = int(-120 + (CW + 240) * sh)                                 # shimmer sweep
    ov = Image.new("RGBA", (CW, 92), (0, 0, 0, 0)); do = ImageDraw.Draw(ov); do.polygon([(x, 0), (x + 50, 0), (x + 10, 92), (x - 40, 92)], fill=(255, 255, 255, 46))
    msk = Image.new("L", (CW, 92), 0); ImageDraw.Draw(msk).rounded_rectangle([0, 0, CW - 1, 91], 26, fill=255)
    im.paste(Image.alpha_composite(im, ov), (0, 0), msk); return im
def fade(im, a):
    if a >= .999: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * max(0, a)))); return im
# ---------------- background (near black, light from the edges)
lw, lh = 320, 180; ly, lx = np.mgrid[0:lh, 0:lw].astype(np.float32)
EDGE = np.clip((((lx - lw / 2) / (lw * .5)) ** 2 * .55 + ((ly - lh / 2) / (lh * .5)) ** 2 * .75), 0, 1.2) ** 2.2
CORE = np.exp(-(((lx - lw / 2) / (lw * .22)) ** 2 + ((ly - lh / 2) / (lh * .5)) ** 2))
rs = np.random.default_rng(7); PT = rs.uniform(0, 1, (70, 4))
_acc = [None]
def acc_at(t): return np.array(last(ACC, t)[1], np.float32) / 255
def pulse_at(t):                                                    # energy from recent notifications / slams
    p = 0.0
    for c in CARDS:
        if 0 <= t - c[0] < 1.2: p = max(p, math.exp(-(t - c[0]) * 3.5))
    for s in SLAM:
        if 0 <= t - s[0] < 1.5: p = max(p, 1.3 * math.exp(-(t - s[0]) * 2.5))
    return p
def bg(t):
    a = acc_at(t)
    if _acc[0] is None: _acc[0] = a.copy()
    _acc[0] += (a - _acc[0]) * 0.12
    wt = WPAL[tuple(last(ACC, t)[1])]
    if _wp[0] is None: _wp[0] = wt.copy()
    _wp[0] += (wt - _wp[0]) * 0.07
    p = pulse_at(t); br = 0.20 + 0.05 * math.sin(t * 1.3) + 0.34 * p
    img = EDGE[..., None] * _acc[0] * br + CORE[..., None] * _acc[0] * (0.035 + 0.05 * p) + np.array([.018, .021, .034], np.float32)
    img = cv2.resize(np.clip(img, 0, 1), (W, H), interpolation=cv2.INTER_LINEAR)
    for j, (x, y, s, ph) in enumerate(PT):                          # slow dust
        px = int(((x + t * (.004 + .012 * s)) % 1) * W); py = int(((y - t * (.006 + .02 * ph)) % 1) * H); v = (.10 + .25 * s) * (.5 + .5 * math.sin(t * (.6 + ph) + j))
        cv2.circle(img, (px, py), 1 + int(s * 2.2), (float(v), float(v), float(v * 1.1)), -1, cv2.LINE_AA)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)
# ---------------- phone wallpaper: the aurora of the Shorts
wl_w, wl_h = PW // 4, PH_ // 4; wy, wx = np.mgrid[0:wl_h, 0:wl_w].astype(np.float32)
WBL = np.random.default_rng(4).uniform(0, 1, (7, 6)).astype(np.float32)
WPAL = {B: [[0.05, 0.30, 0.55], [0.10, 0.55, 0.60], [0.22, 0.20, 0.60], [0.04, 0.42, 0.50], [0.30, 0.30, 0.75], [0.06, 0.25, 0.45], [0.12, 0.48, 0.70]],
        R: [[0.75, 0.06, 0.05], [0.55, 0.03, 0.10], [0.90, 0.20, 0.05], [0.45, 0.02, 0.04], [0.70, 0.10, 0.18], [0.40, 0.03, 0.03], [0.85, 0.12, 0.06]],
        G: [[0.05, 0.55, 0.25], [0.03, 0.40, 0.20], [0.10, 0.70, 0.30], [0.02, 0.30, 0.15], [0.08, 0.50, 0.35], [0.02, 0.22, 0.12], [0.06, 0.62, 0.22]],
        A: [[0.95, 0.62, 0.12], [0.80, 0.45, 0.08], [1.0, 0.78, 0.30], [0.55, 0.30, 0.05], [0.95, 0.55, 0.15], [0.45, 0.22, 0.04], [1.0, 0.70, 0.22]],
        N: [[0.20, 0.22, 0.27], [0.14, 0.15, 0.19], [0.26, 0.28, 0.34], [0.10, 0.11, 0.14], [0.22, 0.23, 0.30], [0.12, 0.13, 0.17], [0.24, 0.26, 0.32]]}
WPAL = {k: np.array(v, np.float32) for k, v in WPAL.items()}; WPAL[Wh] = WPAL[B]
def inrew(t): return any(a <= t < b for a, b in REWS)
_wp = [None]; WMASK = Image.new("L", (PW, PH_), 0); ImageDraw.Draw(WMASK).rounded_rectangle([0, 0, PW - 1, PH_ - 1], 60, fill=255)
WDOT = np.random.default_rng(9).uniform(0, 1, (46, 4))
def wallpaper(t):
    pal = _wp[0]; m = 1.0 if tuple(last(ACC, t)[1]) == R else 0.3; img = np.zeros((wl_h, wl_w, 3), np.float32); sp = 0.5 + 1.2 * m
    for k in range(7):
        cx = wl_w * (0.5 + 0.48 * np.sin(t * 0.21 * sp * (0.6 + WBL[k, 0]) + WBL[k, 1] * 6.28)); cy = wl_h * (0.5 + 0.48 * np.sin(t * 0.17 * sp * (0.6 + WBL[k, 2]) + WBL[k, 3] * 6.28)); r = wl_w * (0.42 + 0.3 * WBL[k, 4])
        img += np.exp(-(((wx - cx) / r) ** 2 + ((wy - cy) / (r * 1.5)) ** 2))[..., None] * pal[k] * 0.42
    img *= (0.55 + 0.45 * (wy / wl_h))[..., None] * 0.9 * 0.56; img += np.array([0.012, 0.014, 0.022], np.float32)
    im = Image.fromarray((np.clip(cv2.resize(img, (PW, PH_), interpolation=cv2.INTER_CUBIC), 0, 1) * 255).astype(np.uint8)).convert("RGBA"); ov = Image.new("RGBA", (PW, PH_), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for j, (x, y, s_, ph) in enumerate(WDOT):
        px = ((x + t * .006 * (s_ - .5)) % 1) * PW; py = ((y - t * (.004 + .012 * ph)) % 1) * PH_; r = 2 + 4 * s_; a = int(34 * (.5 + .5 * math.sin(t * (.5 + ph) + j)))
        d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 255, 255, a))
    im.alpha_composite(ov); return im
# ---------------- clock / date
def clock_at(t):
    for (t0, m0), (t1, m1) in zip(CLOCK, CLOCK[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / max(1e-6, t1 - t0); u = u * u * (3 - 2 * u) if abs(m1 - m0) > 600 else u
            m = int(m0 + (m1 - m0) * u) % 1440; return f"{m // 60:02d}:{m % 60:02d}", abs(m1 - m0) / max(.01, t1 - t0)
    return "08:16", 0
def draw_world(t, hb):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ac = tuple(int(v * 255) for v in _acc[0])
    # ---- phone
    d.rounded_rectangle([PX - 9, PY - 9, PX + PW + 9, PY + PH_ + 9], 70, fill=(0, 0, 0, 255), outline=tuple(int(40 + v * .55) for v in ac) + (255,), width=4)
    im.paste(wallpaper(t), (PX, PY), WMASK); d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX + PW / 2 - 13, PY + 68, PX + PW / 2 + 13, PY + 88], 5, fill=(255, 255, 255, 210)); d.arc([PX + PW / 2 - 9, PY + 54, PX + PW / 2 + 9, PY + 80], 180, 360, fill=(255, 255, 255, 210), width=4)
    d.rounded_rectangle([PX + PW / 2 - 62, PY + 16, PX + PW / 2 + 62, PY + 42], 13, fill=(0, 0, 0, 255))
    # date with roll
    cur = last(DATES, t); idx = DATES.index(cur); u = ease((t - cur[0]) / .22)
    roll = last(ROLL, t)
    if roll and t < roll[1]:
        tracked(d, PX + PW / 2, PY + 100, roll[2], F("b7", 30), 5, roll[3] + (255,), "m")
    else:
        if u < 1 and idx > 0: tracked(d, PX + PW / 2, PY + 100 - 26 * u, DATES[idx - 1][1], F("b6", 27), 3, (255, 255, 255, int(200 * (1 - u))), "m")
        tracked(d, PX + PW / 2, PY + 100 + 26 * (1 - u), cur[1], F("b6", 27), 3, (255, 255, 255, int(215 * u)), "m")
    ck, speed = clock_at(t); fast = speed > 40; ov_ = last(CLKTXT, t)
    if ov_ and ov_[1]: ck = ov_[1]; fast = False
    d.text((PX + PW / 2, PY + 212), ck, font=F("b5", 160), fill=(ac if fast else (255, 255, 255)) + (250,), anchor="mm")
    if fast:
        for j in (1, 2): d.text((PX + PW / 2, PY + 212 + j * 9 * (-1 if inrew(t) else 1)), ck, font=F("b5", 160), fill=ac + (60 // j,), anchor="mm")
    # cards
    clr = last(CLEAR, t, key=lambda x: x); live = [c for c in CARDS if c[0] <= t and (clr is None or c[0] > clr)]
    prevc = max([x for x in CLEAR if clr is not None and x < clr], default=-1)
    gone = [c for c in CARDS if clr is not None and prevc < c[0] <= clr and t - clr < .35]
    y0 = PY + 300; step = CHh + 12
    for c in gone[-3:]:
        j = len([x for x in gone if x[0] > c[0]]); u = (t - clr) / .35
        im.alpha_composite(fade(card_img(c[1:]), 1 - u), (PX + 20, int(y0 + j * step - 240 * u * u)))
    dim = any(a <= t < b for a, b in DIMC)
    for c in live:
        newer = [x for x in live if x[0] > c[0]]; pos = 0.0
        for x in newer: pos += ease((t - x[0]) / .22)
        if pos > 3.2: continue
        age = t - c[0]; s = spring(age / .5); ci = card_img(c[1:]); a = min(1, age / .08) * (1 if pos <= 2 else max(0, 3 - pos)) * (.32 if dim else 1)
        sc = 1 + .10 * (1 - min(1, s)) if age < .5 else 1
        if sc != 1: ci = ci.resize((int(CW * sc), int(CHh * sc)), Image.BILINEAR)
        x = PX + 20 - (ci.width - CW) // 2; y = int(y0 + pos * step - 70 * (1 - s))
        if age < .35:                                                # glow ring behind a fresh card
            gl = Image.new("RGBA", (CW + 60, CHh + 60), (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle([14, 14, CW + 46, CHh + 46], 40, outline=c[3] + (int(210 * (1 - age / .35)),), width=10)
            im.alpha_composite(gl, (PX - 10, y - 30))
        im.alpha_composite(fade(ci, a), (x, max(0, y)))
    # hidden (locked) notification = the open loop
    hv = 0
    for h0, h1 in HID:
        if h0 <= t < h1: hv = spring((t - h0) / .5)
    if hv > 0: im.alpha_composite(fade(hidden_img((t * .45) % 1), min(1, hv)), (PX + 20, int(PY + PH_ - 124 + 40 * (1 - min(1, hv)))))
    for u0 in UNLOCK:
        if 0 <= t - u0 < .6:
            k = 1 - (t - u0) / .6; gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle([PX - 9 - 60 * (1 - k), PY - 9 - 60 * (1 - k), PX + PW + 9 + 60 * (1 - k), PY + PH_ + 9 + 60 * (1 - k)], 80, outline=A + (int(255 * k),), width=14); im.alpha_composite(gl)
    d = ImageDraw.Draw(im); d.rounded_rectangle([PX + PW / 2 - 70, PY + PH_ - 18, PX + PW / 2 + 70, PY + PH_ - 11], 4, fill=(255, 255, 255, 150))
    # ---- left: live timeline log
    LX0, LX1 = 70, PX - 60
    tracked(d, LX0, 64, "TIMELINE", F("b6", 30), 8, A + (235,)); d.ellipse([LX0 + 190, 72, LX0 + 206, 88], fill=R + (int(255 * (.45 + .55 * (math.sin(t * 6) > 0))),)); tracked(d, LX0 + 216, 68, "LIVE", F("b6", 24), 4, (255, 255, 255, 170))
    d.line([LX0, 112, LX1, 112], fill=(255, 255, 255, 50), width=2)
    lc = last(LOGCLR, t, key=lambda x: x); ents = [e for e in LOG if e[0] <= t and (lc is None or e[0] > lc)][::-1]
    yy = 138.0
    for j, e in enumerate(ents[:6]):
        age = t - e[0]; push = 0.0
        if j > 0: push = 1 - ease((t - ents[j - 1][0]) / .25)
        y = yy - 118 * push if j > 0 else yy - 40 * (1 - ease(age / .25)); al = (1 if j == 0 else max(.22, .72 - .13 * j)) * min(1, age / .12)
        if j == 0: d.rounded_rectangle([LX0 - 14, y - 8, LX1, y + 100], 14, fill=e[3] + (int(34 * al + 60 * max(0, 1 - age / .4)),)); d.rectangle([LX0 - 14, y - 8, LX0 - 8, y + 100], fill=e[3] + (255,))
        d.text((LX0 + 6, y), e[1], font=F("m6", 24), fill=e[3] + (int(255 * al),))
        f = fit(d, e[2], "b7", 36, LX1 - LX0 - 16); d.text((LX0 + 6, y + 36), e[2], font=f, fill=(255, 255, 255, int(255 * al)))
        yy += 118
    # ---- right: meter + monitor line
    RX0, RX1 = PX + PW + 60, W - 70
    m = last(METER, t); age = t - m[0]; al = int(255 * min(1, age / .15))
    tracked(d, RX0, 64, m[1], F("b6", 28), 5, (255, 255, 255, int(.75 * al)))
    d.line([RX0, 112, RX1, 112], fill=(255, 255, 255, 50), width=2)
    val = m[2]
    if m[5]: val = m[5][1].format(m[5][0] * ease(age / m[5][2]))
    f = fit(d, m[2], "bb", 150, RX1 - RX0); pop = 1 + .0 * age
    d.text((RX0, 210 + 30 * (1 - ease(age / .2))), val, font=f, fill=m[3] + (al,), anchor="lm")
    f2 = fit(d, m[4], "b6", 34, RX1 - RX0); d.text((RX0, 300), m[4], font=f2, fill=A + (int(.9 * al),))
    bx0, bx1, by0, by1 = RX0, RX1, 400, 640
    d.rounded_rectangle([bx0, by0, bx1, by1], 18, fill=(255, 255, 255, 10), outline=(255, 255, 255, 40), width=2)
    sp = next((s for s in SPARK if s[0] <= t < s[1]), None)
    if sp:
        pts, ts, col = sp[2], sp[3], sp[4]; lo, hi = min(pts) - 4, max(pts) + 6; ts = [ts[0] - 9] + list(ts[1:])
        X = [bx0 + 40 + (bx1 - bx0 - 110) * j / (len(pts) - 1) for j in range(len(pts))]; Y = [by1 - 30 - (by1 - by0 - 60) * (v - lo) / (hi - lo) for v in pts]
        done = [(X[0], Y[0])]
        for j in range(1, len(pts)):
            u = ease((t - ts[j]) / .5) if t >= ts[j] else 0
            if u <= 0: break
            done.append((X[j - 1] + (X[j] - X[j - 1]) * u, Y[j - 1] + (Y[j] - Y[j - 1]) * u))
        if len(done) > 1: d.line(done, fill=col + (255,), width=7, joint="curve")
        d.ellipse([done[-1][0] - 11, done[-1][1] - 11, done[-1][0] + 11, done[-1][1] + 11], fill=(255, 255, 255, 255), outline=col + (255,), width=4)
        k = len(done) - 1; far = done[-1][0] > bx1 - 150
        d.text((done[-1][0] - 4 if far else done[-1][0] + 18, done[-1][1] - 30 if far else done[-1][1] - 2), f"${pts[k]:.2f}", font=F("m6", 26), fill=(255, 255, 255, 235), anchor="rm" if far else "lm")
        tracked(d, bx0 + 16, by0 + 12, sp[5], F("b6", 22), 3, (255, 255, 255, 150))
    else:                                                            # decorative monitor line that jumps on every notification
        tracked(d, bx0 + 16, by0 + 12, "NOTIFICATION ACTIVITY", F("b6", 22), 3, (255, 255, 255, 150)); mid = (by0 + by1) / 2 + 14; pts = []
        for j in range(0, 121):
            tt = t - (120 - j) * .035; v = 0.0
            for c in hb:
                dt = tt - c
                if 0 <= dt < .5: v += math.sin(dt * 46) * math.exp(-dt * 9)
            pts.append((bx0 + 14 + (bx1 - bx0 - 28) * j / 120, mid - 84 * max(-1, min(1, v)) - 3 * math.sin(tt * 9)))
        d.line(pts, fill=ac + (255,), width=4, joint="curve"); d.ellipse([pts[-1][0] - 7, pts[-1][1] - 7, pts[-1][0] + 7, pts[-1][1] + 7], fill=(255, 255, 255, 255))
    nn = len([c for c in CARDS if c[0] <= t]); tracked(d, RX0, 676, "NOTIFICATIONS", F("b6", 26), 5, (255, 255, 255, 170)); d.text((RX1, 664), f"{nn:02d}", font=F("bb", 64), fill=ac + (255,), anchor="ra")
    lv = last(V, t, key=lambda x: x); tracked(d, RX0, 748, "STORY CLOCK", F("b6", 26), 5, (255, 255, 255, 170)); d.text((RX1, 740), f"{int(t // 60):02d}:{t % 60:05.2f}", font=F("m6", 40), fill=(255, 255, 255, 220), anchor="ra")
    return im
HB = sorted([c[0] for c in CARDS] + [s[0] for s in SLAM])
_sl = {}
def slam_img(txt, col, sub):
    k = (txt, col, sub)
    if k not in _sl:
        im = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = fit(d, txt, "bb", 330, W - 330)
        d.text((W / 2 + 6, 236), txt, font=f, fill=(0, 0, 0, 200), anchor="mm"); d.text((W / 2, 230), txt, font=f, fill=col + (255,), anchor="mm")
        if sub: tracked(d, W / 2, 430, sub, F("b6", 62), 10, A + (255,), "m")
        _sl[k] = im
    return _sl[k]
def frame(n):
    t = n / FPS; fr = bg(t); base = Image.fromarray(fr).convert("RGBA"); base.alpha_composite(draw_world(t, HB)); fr = np.asarray(base.convert("RGB")).astype(np.float32)
    # camera: slow push-in per scene + punch + shake
    cut = last(CUTS, t, key=lambda x: x); nxt = next((c for c in CUTS if c > t), DUR); sc = 1.0 + .07 * (t - cut) / max(1, nxt - cut)
    p = pulse_at(t); sc += .022 * p; shx = shy = 0.0
    for c in CARDS:
        dt = t - c[0]
        if 0 <= dt < .35: a = 9 * math.exp(-dt * 9); shx += a * math.sin(dt * 95); shy += a * .6 * math.cos(dt * 80)
    sl = next((s for s in SLAM if s[0] <= t < s[1]), None)
    if sl:
        dt = t - sl[0]; a = 22 * math.exp(-dt * 7); shx += a * math.sin(dt * 70); shy += a * math.cos(dt * 61)
    M = np.float32([[sc, 0, W / 2 * (1 - sc) + shx], [0, sc, H * .42 * (1 - sc) + shy]]); fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    rw = inrew(t)
    if sl:
        dt = t - sl[0]; k = .22 + .78 * max(0, 1 - dt / .12); sm = cv2.resize(cv2.resize(fr, (W // 8, H // 8)), (W, H), interpolation=cv2.INTER_LINEAR); fr = sm * k
    if rw:
        g = fr.mean(axis=2, keepdims=True); fr = g * .8 + fr * .2; ro = int((t * 900) % H); fr = np.roll(fr, -int(40 * math.sin(t * 30)), axis=1)
        for j in range(0, H, 6): fr[(j + ro) % H] *= .55
    for g0, gd in GLITCH:
        if g0 <= t < g0 + gd:
            k = 1 - (t - g0) / gd; r_ = np.random.default_rng(n); o = int(14 * k) + 2; fr[..., 0] = np.roll(fr[..., 0], o, axis=1); fr[..., 2] = np.roll(fr[..., 2], -o, axis=1)
            for _ in range(int(2 + 5 * k)):
                y = int(r_.integers(0, H - 60)); hh = int(r_.integers(8, 54)); fr[y:y + hh] = np.roll(fr[y:y + hh], int(r_.integers(-90, 90) * k), axis=1)
    base = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(base)
    if sl:
        dt = t - sl[0]; txt = sl[2]
        if sl[5]:
            v = sl[5][0] * ease(dt / sl[5][2]); v = round(v / 1e8) * 1e8 if dt < sl[5][2] else sl[5][0]; txt = sl[5][1].format(v)
            im = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); f = fit(dd, sl[2], "bb", 330, W - 330); x0 = W / 2 - dd.textlength(sl[2], font=f) / 2
            dd.text((x0 + dd.textlength(sl[2], font=f), 230), txt, font=f, fill=sl[3] + (255,), anchor="rm")
            if sl[4] and dt > sl[5][2]: tracked(dd, W / 2, 430, sl[4], F("b6", 62), 10, A + (255,), "m")
        else: im = slam_img(sl[2], sl[3], sl[4])
        land = sl[5][2] if sl[5] else 0; z = 1 + .55 * (1 - ease((dt - land) / .16)) if (not sl[5] or dt >= land) and dt - land < .16 else 1 + .03 * (dt - land) / max(.5, sl[1] - sl[0])
        if sl[5] and dt < land: z = 1.0
        a = min(1, dt / .06) * min(1, max(0, (sl[1] - t) / .1))
        if abs(z - 1) > .002:
            zi = im.resize((int(W * z), int(560 * z)), Image.BILINEAR); im = zi.crop(((zi.width - W) // 2, (zi.height - 560) // 2, (zi.width - W) // 2 + W, (zi.height - 560) // 2 + 560)) if z > 1 else zi
        base.alpha_composite(fade(im, a), (0, 200))
        fl = max(0, 1 - abs(dt - land) / .09) if dt >= land else 0
        if fl > 0: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(70 * fl))))
        d = ImageDraw.Draw(base)
    if rw:
        tracked(d, W / 2, 470, "«  REWIND", F("bb", 150), 12, (255, 255, 255, 235), "m")
    # caption
    i = max(j for j in range(len(VO)) if V[j] <= max(t, V[0])) if t >= V[0] else 0
    if VO[i] and V[i] - .05 <= t <= V[i] + D[i] + .25 and not rw:
        fs = F("b6", 46); ls = wrap(d, VO[i], fs, 1300); ch = [ls[j:j + 2] for j in range(0, len(ls), 2)]; tot = sum(len(" ".join(c)) for c in ch); u = min(.999, max(0, (t - V[i]) / D[i])); acc_ = 0; ls = ch[-1]
        for c in ch:
            acc_ += len(" ".join(c)) / tot
            if u < acc_: ls = c; break
        wd = max(d.textlength(s_, font=fs) for s_ in ls); y0 = 1044 - len(ls) * 52
        d.rounded_rectangle([W / 2 - wd / 2 - 26, y0 - 10, W / 2 + wd / 2 + 26, 1050], 16, fill=(0, 0, 0, 200))
        for j, s_ in enumerate(ls): d.text((W / 2, y0 + j * 52), s_, font=fs, fill=(255, 255, 255, 245), anchor="ma")
    d.rectangle([0, H - 8, W, H], fill=(255, 255, 255, 30)); d.rectangle([0, H - 8, W * t / DUR, H], fill=A + (255,))
    d.rounded_rectangle([W - 222, 962, W - 180, 1004], 10, fill=(246, 248, 252, 255)); d.text((W - 201, 984), "P", font=F("bb", 36), fill=(10, 14, 24, 255), anchor="mm"); d.ellipse([W - 190, 954, W - 170, 974], fill=A + (255,), outline=(8, 12, 22, 255), width=3)
    tracked(d, W - 160, 964, "PINGED", F("bb", 40), 3, (255, 255, 255, 235))
    out = np.asarray(base.convert("RGB"))
    if t < .4: out = (out * (t / .4)).astype(np.uint8)
    if t > DUR - .6: out = (out * max(0, (DUR - t) / .6)).astype(np.uint8)
    return out
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "info": print(DUR, NF, len(V), len(CARDS), len(SLAM))
    elif c == "test":
        for x in sys.argv[2:]:
            for n in range(max(0, int(float(x) * FPS) - 40), int(float(x) * FPS)): bg(n / FPS)
            Image.fromarray(frame(int(float(x) * FPS))).save(f"{O}t_{float(x):06.2f}.jpg", quality=86)
    elif c == "render":
        a, b, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        for n in range(max(0, a - 60), a): bg(n / FPS)
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{O}{name}.part.mp4"], stdin=subprocess.PIPE)
        for n in range(a, b): p.stdin.write(frame(n).tobytes())
        p.stdin.close(); p.wait(); os.replace(f"{O}{name}.part.mp4", f"{O}{name}.mp4"); print("ok", name)
