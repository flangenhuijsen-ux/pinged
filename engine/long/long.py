import sys, json, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/claude/long"); from script import L, CH, MOOD, CHARTS
O = "/home/claude/long/out/"; FD = "/home/claude/bon2/fonts/"
W, H, FPS = 1920, 1080, 24
_f = {}
def F(n, s):
    k = (n, int(s))
    if k not in _f: _f[k] = ImageFont.truetype(FD + {"bb": "bebas.ttf", "b5": "barlow-condensed-500.ttf", "b6": "barlow-condensed-600.ttf", "b7": "barlow-condensed-700.ttf", "m6": "ibm-plex-mono-600.ttf"}[n], int(s))
    return _f[k]
GOLD = (255, 196, 90)
# ---------------- timeline: chapter cards + lines
D = {}
for a in (0, 33, 66): D.update({int(k): v for k, v in json.load(open(f"{O}d_{a}.json")).items()})
EV = []; t = 0.6; prev = -1
for i, l in enumerate(L):
    if l["ch"] != prev:
        EV.append(dict(kind="title", ch=l["ch"], t0=t, t1=t + 2.6, i=i)); t += 2.6; prev = l["ch"]
    EV.append(dict(kind="line", ch=l["ch"], t0=t, t1=t + D[i] + 0.55, i=i, vo=t + 0.1)); t += D[i] + 0.55
DUR = round(t + 1.2, 2); N = int(DUR * FPS)
CHT = [next(e["t0"] for e in EV if e["ch"] == c) for c in range(len(CH))] + [DUR]
json.dump(dict(DUR=DUR, EV=[dict(kind=e["kind"], t0=e["t0"], i=e["i"], vo=e.get("vo"), ch=e["ch"], card=bool(L[e["i"]]["phone"].get("card")), count=bool(L[e["i"]]["count"])) for e in EV]), open(O + "tl.json", "w"))
# ---------------- resolved state per event
ST = []; ph = dict(date="", clock="", cards=[]); stg = dict(head="", big="", sub="", bc=(255, 255, 255), count=None, chart=None)
for e in EV:
    l = L[e["i"]]
    if e["kind"] == "title":
        ST.append(dict(title=True, ph=dict(date=ph["date"], clock=ph["clock"], cards=list(ph["cards"])), ch=e["ch"])); continue
    p = l["phone"]
    if p.get("clear"): ph["cards"] = []
    if "date" in p: ph["date"] = p["date"]
    if "clock" in p: ph["clock"] = p["clock"]
    if p.get("card"): ph["cards"] = [p["card"]] + ph["cards"]
    if l["head"] is not None or l["count"] or l["chart"]:
        stg = dict(head=l["head"] or "", big=l["big"] or "", sub=l["sub"] or "", bc=l["bc"], count=l["count"], chart=l["chart"])
    ST.append(dict(title=False, ph=dict(date=ph["date"], clock=ph["clock"], cards=list(ph["cards"])), stg=dict(stg), text=l["text"], ch=e["ch"]))
# ---------------- drawing helpers
def tracked(d, x, y, s, font, tr, fill, anchor="l"):
    ws = [d.textlength(c, font=font) for c in s]; tot = sum(ws) + tr * max(0, len(s) - 1)
    if anchor == "m": x -= tot / 2
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
PX, PY, PW, PH_ = 110, 70, 500, 900       # phone
SX, SW = 720, 1090                         # stage
def card_img(c):
    app, letter, col, title, big, bcol = c
    im = Image.new("RGBA", (PW - 44, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, PW - 45, 149], 28, fill=(255, 255, 255, 34), outline=(255, 255, 255, 70), width=2)
    d.rounded_rectangle([14, 14, 62, 62], 13, fill=col + (255,)); d.text((38, 38), letter, font=F("b7", 34), fill=(12, 16, 26, 255), anchor="mm")
    tracked(d, 76, 16, app, F("b6", 24), 3, (255, 255, 255, 190))
    bw = 0
    if big:
        fb = fit(d, big, "bb", 86, 190); bw = d.textlength(big, font=fb) + 14; d.text((PW - 62, 96), big, font=fb, fill=bcol + (255,), anchor="rm")
    ft = F("b7", 34); ls = wrap(d, title, ft, PW - 44 - 76 - 18 - bw)[:2]
    for j, s_ in enumerate(ls): d.text((76, 58 + j * 38 - (0 if len(ls) > 1 else -14)), s_, font=ft, fill=(255, 255, 255, 255))
    return im
_cc = {}
def layer(k):
    st = ST[k]; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # phone
    d.rounded_rectangle([PX - 8, PY - 8, PX + PW + 8, PY + PH_ + 8], 66, fill=(0, 0, 0, 150), outline=(255, 255, 255, 60), width=3)
    d.rounded_rectangle([PX, PY, PX + PW, PY + PH_], 58, fill=(8, 12, 22, 170))
    d.rounded_rectangle([PX + PW / 2 - 60, PY + 16, PX + PW / 2 + 60, PY + 40], 12, fill=(0, 0, 0, 230))
    p = st["ph"]
    tracked(d, PX + PW / 2, PY + 70, p["date"], F("b6", 28), 4, (255, 255, 255, 200), "m")
    d.text((PX + PW / 2, PY + 190), p["clock"], font=F("b5", 170), fill=(255, 255, 255, 245), anchor="mm")
    for j, c in enumerate(p["cards"][:3]):
        if c not in _cc: _cc[c] = card_img(c)
        ci = _cc[c]
        if j == 9: ci = ci.copy(); ci.putalpha(ci.getchannel("A").point(lambda a: a // 3))
        im.alpha_composite(ci, (PX + 22, PY + 300 + j * 160))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX + PW / 2 - 70, PY + PH_ - 22, PX + PW / 2 + 70, PY + PH_ - 14], 4, fill=(255, 255, 255, 150))
    # wordmark
    d.rounded_rectangle([W - 236, 44, W - 188, 92], 12, fill=(246, 248, 252, 255)); d.text((W - 212, 70), "P", font=F("bb", 40), fill=(10, 14, 24, 255), anchor="mm")
    d.ellipse([W - 200, 36, W - 176, 60], fill=GOLD + (255,), outline=(8, 12, 22, 255), width=3)
    tracked(d, W - 168, 46, "PINGED", F("bb", 46), 3, (255, 255, 255, 235))
    # chapter bar
    bx0, bx1, by = SX, SX + SW, H - 64
    for c in range(len(CH)):
        x0 = bx0 + (bx1 - bx0) * CHT[c] / DUR; x1 = bx0 + (bx1 - bx0) * CHT[c + 1] / DUR
        d.rounded_rectangle([x0 + 2, by, x1 - 2, by + 8], 4, fill=(255, 255, 255, 46))
        if c == st["ch"]: tracked(d, x0 + 4, by + 16, CH[c], F("b6", 22), 2, GOLD + (235,))
    if st["title"]:
        tracked(d, SX, 360, f"PART {st['ch'] + 1} OF {len(CH)}", F("b6", 44), 8, GOLD + (240,))
        f = fit(d, CH[st["ch"]], "bb", 230, SW); d.text((SX, 540), CH[st["ch"]], font=f, fill=(255, 255, 255, 255), anchor="lm")
        return im
    g = st["stg"]
    tracked(d, SX, 150, g["head"], F("b6", 46), 7, (255, 255, 255, 190))
    if g["big"]:
        f = fit(d, g["big"], "bb", 250, SW); d.text((SX, 370), g["big"], font=f, fill=g["bc"] + (255,), anchor="lm")
    if g["sub"]:
        f = fit(d, g["sub"], "b6", 62, SW); d.text((SX, 590 if g["chart"] is None else 196 + 40), g["sub"], font=f, fill=GOLD + (245,), anchor="lm")
    # subtitle
    fs = F("b5", 44); ls = wrap(d, st["text"], fs, SW - 40)[:3]; y0 = 900 - len(ls) * 54
    d.rounded_rectangle([SX - 20, y0 - 16, SX + SW, 900 + 4], 18, fill=(0, 0, 0, 120))
    for j, s_ in enumerate(ls): d.text((SX, y0 + j * 54), s_, font=fs, fill=(255, 255, 255, 235))
    return im
def chart(d, spec, upto, p):
    c = CHARTS[spec]; pts = c["pts"]; x0, x1, y0, y1 = SX + 40, SX + SW - 120, 330, 650
    X = [x0 + (x1 - x0) * j / (len(pts) - 1) for j in range(len(pts))]; Y = [y1 - (y1 - y0) * (v - c["lo"]) / (c["hi"] - c["lo"]) for _, v, _ in pts]
    for gy in (y0, (y0 + y1) / 2, y1): d.line([x0 - 20, gy, x1 + 60, gy], fill=(255, 255, 255, 34), width=2)
    prog = p * (upto - 1); done = [(X[0], Y[0])]
    for j in range(1, upto):
        a = min(1, max(0, prog - (j - 1)))
        if a <= 0: break
        done.append((X[j - 1] + (X[j] - X[j - 1]) * a, Y[j - 1] + (Y[j] - Y[j - 1]) * a))
    if len(done) > 1: d.line(done, fill=c["col"] + (255,), width=8, joint="curve")
    for j in range(upto):
        if prog >= j - 0.001:
            d.ellipse([X[j] - 12, Y[j] - 12, X[j] + 12, Y[j] + 12], fill=(255, 255, 255, 255), outline=c["col"] + (255,), width=5)
            d.text((X[j] + (26 if j == 0 else 0), Y[j] - 78 if j % 2 == 0 else Y[j] + 22), pts[j][2], font=F("bb", 58), fill=(255, 255, 255, 255), anchor="ma")
            d.text((X[j], y1 + 44), pts[j][0], font=F("m6", 26), fill=(255, 255, 255, 170), anchor="ma")
# ---------------- background
lw, lh = 384, 216; ly, lx = np.mgrid[0:lh, 0:lw].astype(np.float32)
PAL = {0: [(.05, .30, .55), (.10, .50, .60), (.22, .20, .60), (.04, .40, .50), (.30, .30, .75)], 1: [(.75, .06, .05), (.55, .03, .10), (.90, .20, .05), (.45, .02, .04), (.70, .10, .18)],
       2: [(.05, .40, .38), (.10, .50, .45), (.20, .22, .50), (.04, .36, .34), (.26, .28, .55)], 3: [(.05, .55, .25), (.03, .40, .20), (.10, .70, .30), (.02, .30, .15), (.08, .50, .35)],
       5: [(.95, .62, .12), (.80, .40, .08), (1.0, .78, .30), (.55, .30, .05), (.90, .55, .20)]}
PALA = {k: np.array(v, np.float32) for k, v in PAL.items()}
rs = np.random.default_rng(5); BL = [dict(cx=rs.uniform(.1, .9), cy=rs.uniform(.1, .9), r=rs.uniform(.3, .55), ph=rs.uniform(0, 6.28), sp=rs.uniform(.03, .08)) for _ in range(5)]
VIG = (1 - 0.6 * np.clip(((lx - lw / 2) / (lw * .72)) ** 2 + ((ly - lh / 2) / (lh * .72)) ** 2, 0, 1.4))[..., None]
def mood_at(t, k):
    st = ST[k]; e = EV[k]; m = MOOD[st["ch"]]
    if st["ch"] == 4: m = 1 if t < next(x["t0"] for x in EV if x["kind"] == "line" and L[x["i"]]["text"].startswith("Shortly before")) else 3
    if st["ch"] == 1 and e["i"] < 14: m = 0
    return m
_pm = [None, None, 0.0]
def bg(t, m):
    if _pm[0] is None: _pm[0] = PALA[m].copy()
    _pm[0] += (PALA[m] - _pm[0]) * 0.06
    img = np.zeros((lh, lw, 3), np.float32)
    for j, b in enumerate(BL):
        cx = (b["cx"] + .07 * math.sin(t * b["sp"] * 6.28 + b["ph"])) * lw; cy = (b["cy"] + .08 * math.cos(t * b["sp"] * 5 + b["ph"] * 1.7)) * lh; r = b["r"] * lw
        img += np.exp(-(((lx - cx) / r) ** 2 + ((ly - cy) / r) ** 2))[..., None] * _pm[0][j] * 0.36
    img = (img * 0.7 + np.array([.012, .016, .028], np.float32)) * VIG
    return cv2.resize((np.clip(img, 0, 1) * 255).astype(np.uint8), (W, H), interpolation=cv2.INTER_CUBIC)
def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
_lay = {}
def get_layer(k):
    if k not in _lay:
        if len(_lay) > 3: _lay.pop(next(iter(_lay)))
        _lay[k] = layer(k)
    return _lay[k]
def frame(n):
    t = n / FPS; k = max(j for j, e in enumerate(EV) if e["t0"] <= t) if t >= EV[0]["t0"] else 0
    e = EV[k]; base = Image.fromarray(bg(t, mood_at(t, k))).convert("RGBA")
    cur = get_layer(k); a = ease((t - e["t0"]) / 0.4)
    if a < 1 and k > 0:
        prev = get_layer(k - 1); base.alpha_composite(Image.blend(prev, cur, a))
    else: base.alpha_composite(cur)
    st = ST[k]
    if not st["title"]:
        g = st["stg"]; d = ImageDraw.Draw(base); u = (t - e["t0"]) / max(0.5, e["t1"] - e["t0"])
        own = L[e["i"]]["count"] is not None or L[e["i"]]["chart"] is not None
        if g["count"]:
            v = g["count"][0] * (ease((t - e["t0"] - 0.3) / 2.2) if own else 1); v = round(v / 1e6) * 1e6
            f = fit(d, g["count"][1].format(g["count"][0]), "bb", 250, SW); d.text((SX, 370), g["count"][1].format(v), font=f, fill=g["bc"] + (255,), anchor="lm")
        if g["chart"]: chart(d, g["chart"][0], g["chart"][1], ease(u / 0.7) if own else 1)
    d = ImageDraw.Draw(base); bx0, bx1, by = SX, SX + SW, H - 64
    d.rounded_rectangle([bx0, by, bx0 + (bx1 - bx0) * t / DUR, by + 8], 4, fill=GOLD + (255,))
    fr = np.asarray(base.convert("RGB"))
    if t < 0.6: fr = (fr * (t / 0.6)).astype(np.uint8)
    if t > DUR - 0.8: fr = (fr * max(0, (DUR - t) / 0.8)).astype(np.uint8)
    return fr
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "info": print(DUR, N, len(EV))
    elif c == "test":
        for x in sys.argv[2:]: Image.fromarray(frame(int(float(x) * FPS))).save(f"{O}t_{float(x):07.2f}.jpg", quality=88)
    elif c == "render":
        a, b, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        for n in range(max(0, a - 60), a): bg(n / FPS, mood_at(n / FPS, max(j for j, e in enumerate(EV) if e["t0"] <= n / FPS) if n / FPS >= EV[0]["t0"] else 0))
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", f"{O}{name}.part.mp4"], stdin=subprocess.PIPE)
        for n in range(a, b): p.stdin.write(frame(n).tobytes())
        p.stdin.close(); p.wait(); import os; os.replace(f"{O}{name}.part.mp4", f"{O}{name}.mp4"); print("ok", name)
