import json, sys, subprocess, os, math, numpy as np, cv2, soundfile as sf, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont
O = "/home/claude/petrov/out/"; W, H, FPS = 1080, 1920, 30; P = "/home/claude/paper/"
exec(open("/home/claude/elapsed/brand.py").read().split("# ------------------------------------------------ logo")[0])
word_ = word
SEG.update({"1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgecd", "7": "abc", "9": "abfgcd", "-": "g"})
FB = "/home/claude/bon2/fonts/"; FP = P + "fonts/"; _fc = {}
def F(n, s, w=None):
    key = (n, int(s), w)
    if key not in _fc:
        path = {"b6": FB + "barlow-condensed-600.ttf", "b7": FB + "barlow-condensed-700.ttf", "m5": FB + "ibm-plex-mono-500.ttf", "bb": FB + "bebas.ttf",
                "go": FP + "Oswald%5Bwght%5D.ttf", "os": FP + "OldStandard-Regular.ttf", "ob": FP + "OldStandard-Bold.ttf", "oi": FP + "OldStandard-Italic.ttf"}[n]
        f = ImageFont.truetype(path, int(s))
        if w: f.set_variation_by_axes([w])
        _fc[key] = f
    return _fc[key]
INK = np.array([.09, .08, .07], np.float32); REDN = np.array([.70, .12, .09], np.float32); AMB, GRN = (255, 196, 96), (125, 242, 180)
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else 1 - (1 - u) ** 3

sm = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else 1 - (1 - u) ** 3
J = json.load(open(O + "d.json")); D = {int(k): v for k, v in J["D"].items()}; TX = J["VO"]
exec(open("/home/claude/slogan/endcard.py").read()); TX.append(""); D[13] = SLG_SPEECH
NB = len(TX); GAP = {0: .35, 1: .2, 2: .45, 4: .35, 5: .25, 6: .45, 7: .3, 8: .3, 9: .45, 10: .3, 11: .35, 12: .6}
V = []; t = 0.0
for i in range(NB): V.append(t); t += D[i] + GAP.get(i, .2)
DUR = V[13] + SLG_TOTAL + .4; T_SLOGAN = V[13]; T_BANG = 0; G = lambda h, m, s: h * 3600 + m * 60 + s
REDS = (255, 70, 52); END_NOTE = "ILLUSTRATIONS, SCREENS AND DIAGRAMS ARE RECONSTRUCTIONS · SOURCE: BBC 2013"
S_ = [(0, 0, "screen", dict(w="LAUNCH", sub="SERPUKHOV-15 · 26 SEPTEMBER 1983")),
      (0, 2.7, "slam", dict(lines=[("ONE PHONE CALL", 190), ("FROM NUCLEAR", 190), ("WAR", 300)], kicker="THE ELAPSED RECORD · 26 SEPTEMBER 1983", stamp=None)),
      (1, 0, "clock", dict(v=G(0, 15, 0), lab="SERPUKHOV-15 · NEAR MOSCOW · CIRCA 00:15")),
      (1, 1.9, "illus", dict(var="bunker")),
      (2, 0, "screen", dict(w="LAUNCH", sub="AS PETROV DESCRIBED THE SCREEN · RECONSTRUCTION", big=True)),
      (3, 0, "map", dict(n=1)),
      (3, 2.3, "word", dict(w="ICBM", sub="ONE MISSILE, SAYS THE SYSTEM")),
      (4, 0, "count", {}),
      (5, 0, "illus", dict(var="bunker", ring=True)),
      (5, 1.7, "slam", dict(lines=[("STANISLAV", 220), ("PETROV", 300)], kicker="LIEUTENANT COLONEL · DUTY OFFICER", stamp=None)),
      (5, 3.6, "illus", dict(var="phone")),
      (6, 0, "quote", dict(who="STANISLAV PETROV · TO THE BBC, 2013", txt="All I had to do was reach for the phone. But I couldn't move.")),
      (7, 0, "map", dict(n=5)),
      (6, 3.2, "illus", dict(var="phone")),
      (7, 2.4, "word", dict(w="5?", sub="A REAL FIRST STRIKE: HUNDREDS")),
      (8, 0, "slam", dict(lines=[("HE REPORTS", 200), ("A FAULT", 260)], kicker="DUTY OFFICER'S DECISION", stamp="NOT AN ATTACK")),
      (8, 2.3, "word", dict(w="WAIT", sub="GROUND RADAR: NOTHING YET")),
      (9, 0, "wait", {}),
      (10, 0, "illus", dict(var="sat")),
      (10, 2.5, "word", dict(w="GLARE", sub="SUN ON CLOUDS, NOT ROCKETS")),
      (11, 0, "slam", dict(lines=[("SECRET", 240), ("UNTIL 1998", 220)], kicker="MADE PUBLIC BY GEN. YURI VOTINTSEV", stamp=None)),
      (11, 2.0, "word", dict(w="15", sub="YEARS OF SILENCE")),
      (12, 0, "screen", dict(w="FALSE ALARM", sub="NO MISSILES WERE LAUNCHED", green=True)),
      (13, -.15, "end", {})]
SHOTS = sorted([(max(0, V[l] + off - (.1 if off == 0 and l else 0)), k, p) for l, off, k, p in S_], key=lambda x: x[0])
CNT = None
if sys.argv[1] == "info":
    print(round(DUR, 1), int(DUR * FPS), len(SHOTS))
    for s_ in SHOTS: print(round(s_[0], 2), s_[1], s_[2].get("var", ""))
    sys.exit()
if sys.argv[1] == "audio":
    SR = 44100; n = int(DUR * SR); v = np.zeros(n); rms = lambda x: np.sqrt((x ** 2).mean()); rng = np.random.default_rng(2)
    for i, t0 in enumerate(V):
        if not TX[i]: continue
        a, _ = sf.read(f"{O}w{i}.wav"); k = int(t0 * SR); v[k:k + len(a)] += a[:n - k]
    v = v / np.abs(v).max() * .9; tt = np.arange(n) / SR; TU = 432 / 440; pad = np.zeros(n)
    for f, a in ((55.0, .5), (65.41, .35), (110.0, .3), (130.81, .15)): pad += a * np.sin(2 * np.pi * f * TU * tt + 2.5 * np.sin(2 * np.pi * .07 * tt + f))
    hb = (.5 + .5 * np.sin(2 * np.pi * (1.0 + .8 * np.clip((tt - V[1]) / (V[8] - V[1]), 0, 1)) * tt)) ** 6 * (tt > V[1]) * (tt < V[8])
    pad += .45 * np.sin(2 * np.pi * 49 * TU * tt) * hb; pad *= np.where(tt < V[9], 1.0, .7)
    bq, aq = sg.butter(2, [30 / (SR / 2), 1800 / (SR / 2)], "band"); pad = sg.lfilter(bq, aq, pad); pad *= rms(v[np.abs(v) > .02]) * 10 ** (-12 / 20) / rms(pad); pad *= np.clip((T_SLOGAN - .15 - tt) / .5, 0, 1)
    fx = np.zeros(n)
    def put(x, t0, g=1.0):
        k = int(t0 * SR); m = min(len(x), n - k)
        if m > 0 and k >= 0: fx[k:k + m] += x[:m] * g
    e = np.arange(int(SR * .3)) / SR; whoosh = sg.lfilter(*sg.butter(2, [400 / (SR / 2), 4000 / (SR / 2)], "band"), rng.normal(0, 1, len(e))) * np.sin(np.pi * e / e[-1]) ** 2 * .05
    e2 = np.arange(int(SR * .5)) / SR; thump = .2 * np.sin(2 * np.pi * 55 * e2) * np.exp(-e2 * 9)
    e3 = np.arange(int(SR * 1.2)) / SR; siren = .07 * np.sin(2 * np.pi * (600 + 250 * np.sin(2 * np.pi * 1.6 * e3)) * e3) * np.minimum(1, (1.2 - e3) / .2)
    for t0, k, p in SHOTS[1:]:
        if k in ("slam", "word", "count"): put(thump, t0)
        elif k == "screen": put(siren, t0, 1.0); put(thump, t0, 1.2)
        elif k not in ("end",): put(whoosh, t0 - .08)
    put(siren, 0.0, .9)
    for q in range(4): put(thump, V[4] + D[4] * (q * .25 + .1), 1.0)
    e4 = np.arange(int(SR * .9)) / SR; ring = .05 * np.sin(2 * np.pi * 900 * e4) * (np.sin(2 * np.pi * 20 * e4) > 0) * (e4 < .9)
    for kk in (0, 1.5, 3.0): put(ring, V[5] + kk)
    tick = np.sin(2 * np.pi * 1700 * np.arange(int(SR * .012)) / SR) * .06
    for kk in np.arange(V[9], V[10] - .3, .12): put(tick, kk)
    key = rng.normal(0, 1, int(SR * .025)) * np.exp(-np.arange(int(SR * .025)) / SR * 200) * .07
    for kk in np.arange(V[6] + .25, V[6] + .25 + 60 / 30, 1 / 30): put(key * (.7 + .5 * rng.random()), kk)
    fx += add_slogan(rms(v[np.abs(v) > .02]), n, SR, T_SLOGAN)
    fade = np.clip(np.minimum(tt / .03, (DUR - tt) / .6), 0, 1); mix = (v + pad + fx) * fade
    mix = np.stack([mix, mix], 1) / max(1, np.abs(mix).max() / .97); sf.write(O + "mix.wav", mix, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", O + "mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "44100", O + "mixn.wav"], check=True)
    print("ok"); sys.exit()

# ------------------------------------------------ shared looks
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); rng0 = np.random.default_rng(7)
def nz(sh, s, a): return cv2.GaussianBlur(rng0.normal(0, 1, sh).astype(np.float32), (0, 0), s) * a
mott = cv2.resize(nz((H // 8, W // 8), 5, 20), (W, H)) * .012 + nz((H, W), .8, 2) * .01
PAPER = (np.array([228, 216, 189], np.float32) / 255)[None, None] * (1 + mott[..., None]) * np.clip(1.1 - (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * .9, .6, 1)[..., None]
DARK = np.zeros((H, W, 3), np.float32) + np.array([.03, .035, .04], np.float32); DARK += np.exp(-(((xx - W / 2) / 700) ** 2 + ((yy - 820) / 900) ** 2))[..., None] * np.array([.03, .045, .05], np.float32)
VIG = np.clip(1.15 - (((xx - W / 2) / W) ** 2 * 1.2 + ((yy - H * .45) / H) ** 2 * 1.4), .45, 1)[..., None].astype(np.float32)
INKN = np.clip(.82 + nz((H, W), 1.2, 2.4) * .08, .55, 1).astype(np.float32)
HATCH45 = ((xx + yy) % 7 < 3).astype(np.float32); HATCHH = ((yy % 6) < 2).astype(np.float32)
def ink_layer(img, L, col=INK, k=1.0):
    a = np.asarray(L).astype(np.float32) / 255
    a = np.clip((cv2.GaussianBlur(a, (0, 0), 1.0) - .3 + (INKN - .82)) * 1.8, 0, 1) * k
    return img * (1 - a[..., None]) + np.asarray(col, np.float32)[None, None] * a[..., None]
def comp(img, lay):
    a = np.asarray(lay).astype(np.float32) / 255; return img * (1 - a[..., 3:]) + a[..., :3] * a[..., 3:]
PH_ = {k: cv2.cvtColor(cv2.imread(f"/home/claude/exh/img/{k}.jpg"), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255 for k in ("lm", "dmg")}
STARS = [(rng0.uniform(0, W), rng0.uniform(0, H), rng0.uniform(.3, 1), rng0.uniform(1, 2.6)) for _ in range(260)]
# ------------------------------------------------ shot renderers
def slam(p, lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); u = ease(lt / .16); sc = 1.12 - .12 * u; y = 560
    tw = d.textlength(p["kicker"], font=F("ob", 36)); d.text(((W - tw) / 2, 450), p["kicker"], font=F("ob", 36), fill=255); d.rectangle([90, 512, W - 90, 516], fill=255)
    for txt, sz in p["lines"]:
        f = F("go", int(sz * sc), 700)
        while d.textlength(txt, font=f) > W - 110: sz -= 8; f = F("go", int(sz * sc), 700)
        bb = d.textbbox((0, 0), txt, font=f); d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y - bb[1]), txt, font=f, fill=255); y += (bb[3] - bb[1]) + 30
    d.rectangle([90, y + 6, W - 90, y + 10], fill=255); img = ink_layer(img, L)
    if p.get("stamp") and lt > .55:
        uu = ease((lt - .55) / .12); st = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(st); f = F("go", int(92 * (1.3 - .3 * uu)), 700); tw = sd.textlength(p["stamp"], font=f)
        sd.rounded_rectangle([(W - tw) / 2 - 36, 1170, (W + tw) / 2 + 36, 1320], 18, outline=255, width=12); sd.text(((W - tw) / 2, 1180), p["stamp"], font=f, fill=255)
        img = ink_layer(img, st.rotate(-7, center=(W / 2, 1245)), REDN, .9 * uu)
    if lt < .2: k = (1 - lt / .2) * 18; img = cv2.warpAffine(img, np.float32([[1, 0, k * math.sin(lt * 80)], [0, 1, k * math.cos(lt * 70)]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return img
def word(p, lt):
    img = PAPER.copy(); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L)
    u = ease(lt / .12); dr.text((W / 2, 780), p["w"], font=F("go", int(340 * (1.3 - .3 * u)), 700), fill=255, anchor="mm")
    d.text((W / 2, 1010), p["sub"], font=F("ob", 46), fill=255, anchor="mm"); d.rectangle([200, 1060, W - 200, 1063], fill=255)
    img = ink_layer(img, L); img = ink_layer(img, R, REDN)
    if lt < .18: k = (1 - lt / .18) * 22; img = cv2.warpAffine(img, np.float32([[1, 0, k * math.sin(lt * 80)], [0, 1, k * math.cos(lt * 70)]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return img
def clock_img(sec, col=GRN, ghost=True):
    img = DARK.copy(); s_ = f"{int(sec) // 3600:02d}:{int(sec) % 3600 // 60:02d}:{int(sec) % 60:02d}"
    w, h, th, gap, cw = 104, 196, 26, 22, 40; tw = width(s_, w, gap, cw); x0 = (W - tw) / 2
    gl, _ = word_((W, H), "88:88:88", x0, 680, w, h, th, gap, cw); _, lt = word_((W, H), s_, x0, 680, w, h, th, gap, cw)
    m = np.asarray(lt).astype(np.float32)[..., 3:] / 255; g = np.asarray(gl).astype(np.float32) / 255; img = img * (1 - g[..., 3:] * .5) + g[..., :3] * g[..., 3:] * .5
    c = np.array(col, np.float32) / 255; img = img * (1 - m) + c * m; img = img + cv2.GaussianBlur(m * c, (0, 0), 18) * 1.2 + cv2.GaussianBlur(m * c, (0, 0), 50) * .8
    return img
def traj(lt, dur, t):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    ex, ey, er = 250, 860, 120; mx, my, mr = 860, 640, 52
    E_ = Image.new("L", (W, H), 0); ImageDraw.Draw(E_).ellipse([ex - er, ey - er, ex + er, ey + er], fill=255); Ea = np.asarray(E_) > 0
    hl = np.zeros((H, W), np.uint8); hl[Ea & (HATCH45 > 0)] = 200; L = Image.fromarray(hl); d = ImageDraw.Draw(L)
    d.ellipse([ex - er, ey - er, ex + er, ey + er], outline=255, width=5); d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=255, width=5)
    for k in range(9): a0 = k * 0.7; d.ellipse([mx + 22 * math.cos(a0) - 7, my + 22 * math.sin(a0 * 1.3) - 7, mx + 22 * math.cos(a0) + 7, my + 22 * math.sin(a0 * 1.3) + 7], outline=255, width=2)
    d.text((ex, ey + er + 50), "EARTH", font=F("ob", 52), fill=255, anchor="mm"); d.text((mx, my - mr - 46), "MOON", font=F("ob", 48), fill=255, anchor="mm")
    pts = [(ex + (er + 10) * math.cos(-1.0), ey + (er + 10) * math.sin(-1.0))]; P1, P2 = (520, 520), (mx - mr - 40, my + 6)
    path = [((1 - u) ** 2 * pts[0][0] + 2 * (1 - u) * u * P1[0] + u * u * P2[0], (1 - u) ** 2 * pts[0][1] + 2 * (1 - u) * u * P1[1] + u * u * P2[1]) for u in np.linspace(0, 1, 120)]
    for k in range(0, 119, 3): d.line([path[k], path[k + 1]], fill=255, width=5)
    uu = .84 * ease(lt / max(dur * .7, .1)); idx = int(uu * 119)
    for k in range(0, idx): dr.line([path[k], path[k + 1]], fill=255, width=7)
    cx, cy = path[idx]; dr.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=255)
    if lt > dur * .5:
        a8 = ease((lt - dur * .5) / .3); dr.text((cx - 40, cy + 40), "APOLLO 13", font=F("b7", int(52 * a8 + 1)), fill=255)
    d.text((W / 2, 1190), "EARTH TO MOON · DIAGRAM, NOT TO SCALE", font=F("oi", 34), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def km(lt):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    v = int(329399 * ease(lt / 1.1)); d.text((W / 2, 600), "DISTANCE FROM EARTH · 055:47", font=F("b6", 42), fill=AMB + (255,), anchor="mm")
    d.text((W / 2, 760), f"{v:,} KM", font=F("bb", 190), fill=(255, 255, 255, 255), anchor="mm"); d.text((W / 2, 900), f"{int(v / 1.609344):,} MILES", font=F("b6", 64), fill=(170, 210, 190, 255), anchor="mm")
    d.text((W / 2, 990), "SOURCE: NASA APOLLO 13 CHRONOLOGY", font=F("b6", 28), fill=(255, 255, 255, 140), anchor="mm"); return comp(img, lay)
def tr(p, lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    d.text((W / 2, 330), "AIR-TO-GROUND TRANSCRIPT", font=F("ob", 52), fill=255, anchor="mm"); d.text((W / 2, 392), "APOLLO 13 · 13 APRIL 1970 · TIMES IN GROUND ELAPSED TIME", font=F("oi", 30), fill=255, anchor="mm")
    d.rectangle([80, 430, W - 80, 434], fill=255); d.rectangle([80, 440, W - 80, 441], fill=255)
    y = 640; d.text((90, y), p["get"], font=F("m5", 44), fill=255); (dr if p.get("red") else d).text((380, y), p["who"], font=F("m5", 44), fill=255)
    txt = p["txt"]; n = len(txt) if not p.get("typed") else min(len(txt), int(max(0, lt - .25) * 34)); f = F("m5", 50); words = txt.split(" "); lines, cur = [], ""
    for w_ in words:
        if d.textlength((cur + " " + w_).strip(), font=f) > W - 180: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur); shown = 0; hs = txt.find(p["hl"]); y = 730
    for ln in lines:
        x = 90
        for ch in ln + " ":
            if shown >= n: break
            on = hs <= shown < hs + len(p["hl"]) and lt > .5; (dr if on else d).text((x, y), ch, font=f, fill=255); x += d.textlength(ch, font=f); shown += 1
        y += 74
    if p.get("typed") and n < len(txt) and int(lt * 6) % 2 == 0: d.rectangle([x, y - 74 + 8, x + 26, y - 74 + 58], fill=255)
    if lt > .5 and hs >= 0:
        u = ease((lt - .5) / .3); dr.rectangle([90, y + 16, 90 + (W - 180) * u, y + 24], fill=255)
    d.text((W / 2, 1230), "SOURCE: NASA, DETAILED CHRONOLOGY OF THE APOLLO 13 ACCIDENT", font=F("b6", 28), fill=200, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def gauge(lt, t):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tb = T_BANG - (t - lt); u = np.clip(lt / tb, 0, 1); get = G(55, 53, 20) + (G(55, 54, 53) - G(55, 53, 20)) * u
    s_ = f"{int(get) // 3600:03d}:{int(get) % 3600 // 60:02d}:{int(get) % 60:02d}"; d.text((W / 2, 300), s_, font=F("m5", 96), fill=GRN + (255,), anchor="mm"); d.text((W / 2, 380), "GROUND ELAPSED TIME · SPEEDED UP", font=F("b6", 34), fill=(170, 210, 190, 255), anchor="mm")
    cx, cy, r = W / 2, 900, 340; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(18, 20, 22, 255), outline=(200, 200, 200, 255), width=6)
    pv = lambda v: math.radians(135 + (v / 1100) * 270)
    for v_ in range(0, 1101, 50):
        a = pv(v_); l1 = r - (40 if v_ % 200 == 0 else 22); d.line([cx + l1 * math.cos(a), cy + l1 * math.sin(a), cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)], fill=(220, 220, 220, 255), width=5 if v_ % 200 == 0 else 3)
        if v_ % 200 == 0: d.text((cx + (r - 85) * math.cos(a), cy + (r - 85) * math.sin(a)), str(v_), font=F("b6", 40), fill=(220, 220, 220, 255), anchor="mm")
    a0, a1 = pv(1000), pv(1100); d.arc([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], math.degrees(a0), math.degrees(a1), fill=(220, 60, 40, 255), width=14)
    pk = G(55, 54, 45); pu = (pk - G(55, 53, 20)) / (G(55, 54, 53) - G(55, 53, 20))
    val = 890 + (1008.3 - 890) * sm(u / pu) if u < pu else 1008.3 - 300 * ((u - pu) / (1 - pu)) ** 2
    val += 4 * math.sin(t * 40) * (u > .6); a = pv(val); d.line([cx, cy, cx + (r - 50) * math.cos(a), cy + (r - 50) * math.sin(a)], fill=(255, 90, 60, 255), width=12); d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(230, 230, 230, 255))
    d.text((cx, cy + 150), "PSIA", font=F("b7", 48), fill=(220, 220, 220, 255), anchor="mm"); d.text((W / 2, 1330), "OXYGEN TANK 2 · PRESSURE", font=F("b7", 56), fill=AMB + (255,), anchor="mm")
    if u > pu: d.text((W / 2, 1400), "PEAK 1,008.3 PSIA AT 055:54:45", font=F("b6", 40), fill=(255, 120, 90, 255), anchor="mm")
    return comp(img, lay)
def caution(lt, t):
    img = DARK.copy() * .7; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    labs = ["CRYO PRESS", "O2 FLOW HI", "FC 1", "FC 3", "MN BUS A UNDERVOLT", "MN BUS B UNDERVOLT", "AC BUS 2", "CMC"]
    blink = (int(t * 4) % 2 == 0)
    d.rounded_rectangle([110, 300, W - 110, 560], 26, fill=(60, 8, 6, 255) if not blink else (230, 30, 20, 255), outline=(255, 255, 255, 120), width=4)
    d.text((W / 2, 430), "MASTER ALARM", font=F("bb", 130), fill=(255, 230, 220, 255 if blink else 110), anchor="mm")
    for k, lb in enumerate(labs):
        x0 = 110 + (k % 2) * 440; y0 = 640 + (k // 2) * 170; on = lb == "MN BUS B UNDERVOLT" and lt > .3
        d.rectangle([x0, y0, x0 + 420, y0 + 140], fill=(250, 196, 70, 255) if on else (36, 32, 24, 255), outline=(120, 110, 90, 255), width=3)
        d.text((x0 + 210, y0 + 70), lb, font=F("b7", 42), fill=(30, 20, 10, 255) if on else (150, 140, 120, 140), anchor="mm")
    d.text((W / 2, 1360), "“We've had a main B bus undervolt.” · LOVELL, 055:55:35", font=F("b6", 36), fill=(255, 255, 255, 210), anchor="mm")
    return comp(img, lay)
def date(lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    k = min(4, int(lt / .25)); day = 13 + k; u = ease((lt % .25) / .08) if k < 4 else 1
    d.text((W / 2, 470), "THE CREW HAS NOT SEEN THE DAMAGE", font=F("ob", 44), fill=255, anchor="mm"); d.rectangle([110, 515, W - 110, 519], fill=255)
    dr.text((W / 2, 790), str(day), font=F("go", int(420 * (1.15 - .15 * u)), 700), fill=255, anchor="mm"); d.text((W / 2, 1060), "APRIL 1970", font=F("ob", 80), fill=255, anchor="mm")
    if k == 4: d.text((W / 2, 1160), "THE DAY THE SERVICE MODULE IS RELEASED", font=F("oi", 40), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def photo(p, lt, dur):
    im = PH_[p["k"]]; ih, iw = im.shape; u = np.clip(lt / max(dur, .1), 0, 1); z = p["z0"] + (p["z1"] - p["z0"]) * sm(u)
    s = max(W / iw, H * .62 / ih) * z; cx, cy = p["c"]; Mx = np.float32([[s, 0, W / 2 - cx * iw * s], [0, s, H * .42 - cy * ih * s]])
    g = cv2.warpAffine(im, Mx, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return np.clip(g * 1.05, 0, 1)[..., None] * np.array([.97, .97, .95], np.float32)

REDBG = np.zeros((H, W, 3), np.float32) + np.array([.05, .012, .01], np.float32)
def screen(p, lt, t):
    green = p.get("green"); col = (110, 240, 170) if green else REDS
    img = (DARK.copy() * .5 if green else REDBG.copy()); fl = .75 + .25 * abs(math.sin(t * (2 if green else 7)))
    pw, ph_ = (980, 520) if p.get("big") else (900, 420); x0, y0 = (W - pw) / 2, 560
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0 - 26, y0 - 26, x0 + pw + 26, y0 + ph_ + 26], 30, fill=(28, 26, 26, 255), outline=(80, 74, 70, 255), width=6)
    d.rectangle([x0, y0, x0 + pw, y0 + ph_], fill=tuple(int(c * .25 * fl) for c in col) + (255,))
    for yy_ in range(int(y0), int(y0 + ph_), 6): d.line([x0, yy_, x0 + pw, yy_], fill=(0, 0, 0, 60))
    u = ease(lt / .15); fs = 260 if len(p["w"]) < 8 else 170
    while d.textlength(p["w"], font=F("bb", fs)) > pw - 80: fs -= 10
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); gd.text((W / 2, y0 + ph_ / 2), p["w"], font=F("bb", int(fs * (1.15 - .15 * u))), fill=col + (int(255 * fl),), anchor="mm")
    ga = np.asarray(gl).astype(np.float32) / 255; img = img + cv2.GaussianBlur(ga[..., :3] * ga[..., 3:], (0, 0), 30) * .9
    lay.alpha_composite(gl); d = ImageDraw.Draw(lay)
    d.text((W / 2, y0 + ph_ + 90), p["sub"], font=F("b6", 36), fill=(255, 255, 255, 190), anchor="mm")
    if not green:
        for k in range(2):
            lx = 200 + k * 680; on = (int(t * 4) + k) % 2 == 0; d.ellipse([lx - 26, 380, lx + 26, 432], fill=(255, 40, 30, 255) if on else (70, 20, 18, 255))
    d.rounded_rectangle([50, 120, 390, 180], 12, fill=(20, 18, 16, 200)); d.text((220, 150), "RECONSTRUCTION", font=F("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; img = img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    if lt < .12 and t > .2: img = img + (1 - lt / .12) * .35
    return img
def mapshot(p, lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy, R = W / 2, 820, 430
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(70, 110, 95, 255), width=3)
    for k in range(1, 4): r = R * k / 4; d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 70, 60, 255), width=1)
    for k in range(12): a = k * math.pi / 6; d.line([cx, cy, cx + R * math.cos(a), cy + R * math.sin(a)], fill=(40, 70, 60, 255), width=1)
    d.text((cx, cy - 20), "NORTH POLE", font=F("b6", 26), fill=(120, 170, 150, 255), anchor="mm")
    us, su = (cx - 250, cy + 250), (cx + 230, cy - 260)
    d.text((us[0], us[1] + 60), "USA", font=F("b7", 52), fill=(180, 200, 190, 255), anchor="mm"); d.text((su[0], su[1] - 60), "USSR", font=F("b7", 52), fill=(180, 200, 190, 255), anchor="mm")
    nshow = p["n"] if p["n"] == 1 else min(5, 1 + int(lt / .35))
    for k in range(nshow):
        ox = us[0] + (k - 2) * 26; prog = ease((lt - (k * .35 if p["n"] > 1 else 0)) / 1.4)
        pts = [(ox + (su[0] - ox) * s_ - 140 * math.sin(math.pi * s_), us[1] + (su[1] - us[1]) * s_ - 60 * math.sin(math.pi * s_)) for s_ in np.linspace(0, prog * .55, 30)]
        if len(pts) > 1: d.line(pts, fill=REDS + (255,), width=6)
        if pts: d.ellipse([pts[-1][0] - 10, pts[-1][1] - 10, pts[-1][0] + 10, pts[-1][1] + 10], fill=(255, 220, 200, 255))
    d.text((W / 2, 300), f"OKO SATELLITES: {nshow} LAUNCH{'ES' if nshow > 1 else ''} REPORTED", font=F("b7", 52), fill=REDS + (255,), anchor="mm")
    d.text((W / 2, 1300), "DIAGRAM, NOT TO SCALE · WHAT THE SYSTEM CLAIMED", font=F("b6", 30), fill=(255, 255, 255, 140), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def count(lt, t, dur):
    img = REDBG.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k = 2 + min(3, int(lt / (dur * .25))); u = ease(((lt / (dur * .25)) % 1) / .1)
    d.text((W / 2, 400), "MISSILES REPORTED", font=F("b7", 60), fill=(255, 200, 190, 255), anchor="mm")
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, 800), str(k), font=F("bb", int(620 * (1.2 - .2 * u))), fill=REDS + (255,), anchor="mm")
    ga = np.asarray(gl).astype(np.float32) / 255; img = img + cv2.GaussianBlur(ga[..., :3] * ga[..., 3:], (0, 0), 40) * .8; lay.alpha_composite(gl)
    for q in range(5):
        x = W / 2 + (q - 2) * 120; on = q < k; d.rounded_rectangle([x - 40, 1150, x + 40, 1230], 10, fill=REDS + (255,) if on else (60, 20, 18, 255))
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def quote(p, lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    d.text((W / 2, 420), "IN HIS OWN WORDS", font=F("ob", 52), fill=255, anchor="mm"); d.rectangle([110, 470, W - 110, 474], fill=255)
    txt = p["txt"]; n = min(len(txt), int(max(0, lt - .25) * 30)); f = F("os", 76); words = txt.split(" "); lines, cur = [], ""
    for w_ in words:
        if d.textlength((cur + " " + w_).strip(), font=f) > W - 200: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur); shown = 0; y = 600
    dr.text((70, 505), "“", font=F("ob", 130), fill=255)
    for ln in lines:
        part = ln[:max(0, n - shown)]; d.text((W / 2, y), part, font=f, fill=255, anchor="mt") if False else d.text(((W - d.textlength(ln, font=f)) / 2, y), part, font=f, fill=255); shown += len(ln) + 1; y += 100
    d.text((W / 2, y + 60), "— " + p["who"], font=F("b6", 38), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def wait(lt, dur):
    m = 23 * 60 * ease(lt / max(dur * .85, .1)); img = clock_img(m / 60 * 60 if False else m, GRN) if False else None
    s_ = f"{int(m) // 60:02d}:{int(m) % 60:02d}"; img = DARK.copy(); w_, h_, th_, gap_, cw_ = 120, 220, 28, 26, 46; tw_ = width(s_, w_, gap_, cw_)
    gl_, lt_ = word_((W, H), "88:88", (W - tw_) / 2, 640, w_, h_, th_, gap_, cw_); _, lt_ = word_((W, H), s_, (W - tw_) / 2, 640, w_, h_, th_, gap_, cw_)
    la = np.asarray(lt_).astype(np.float32) / 255; g = np.asarray(gl_).astype(np.float32) / 255
    img = img * (1 - g[..., 3:] * .4) + g[..., :3] * g[..., 3:] * .4; img = img * (1 - la[..., 3:]) + la[..., :3] * la[..., 3:]; img = img + cv2.GaussianBlur(la[..., :3] * la[..., 3:], (0, 0), 20) * .9
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, 560), "MINUTES WAITED", font=F("b6", 44), fill=AMB + (255,), anchor="mm")
    d.text((W / 2, 960), "NO MISSILE ON GROUND RADAR · NO IMPACT", font=F("b6", 36), fill=(255, 255, 255, int(200 * ease((lt - dur * .6) / .3))), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def illus_pv(var, u, t, ring=False):
    img = PAPER.copy() * .97; L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    if var == "bunker":
        for yv in range(160, 1360, 8): d.line([0, yv, W, yv], fill=60, width=1)
        d.rectangle([140, 300, 940, 760], fill=255); dr.rectangle([180, 340, 900, 720], fill=int(255 * (.55 + .45 * abs(math.sin(t * 6)))))   # the wall panel
        d.text((540, 530), "LAUNCH", font=F("bb", 170), fill=0, anchor="mm")
        d.rectangle([80, 1080, 1000, 1130], fill=255); d.rectangle([130, 1130, 170, 1360], fill=255); d.rectangle([910, 1130, 950, 1360], fill=255)    # desk
        px, py = 420, 1040; d.ellipse([px - 46, py - 220, px + 46, py - 128], fill=255); d.polygon([(px - 110, py), (px + 110, py), (px + 80, py - 130), (px - 80, py - 130)], fill=255)  # seated figure, from behind
        ph = 700 + (6 * math.sin(t * 60) if ring and int(t * 2) % 2 == 0 else 0); d.rectangle([ph - 70, 1030, ph + 70, 1080], fill=255); d.rounded_rectangle([ph - 80, 1000, ph + 80, 1030], 14, fill=255)   # telephone
        if ring and int(t * 2) % 2 == 0:
            for k in range(3): r = 40 + k * 26; dr.arc([ph - r, 990 - r, ph + r, 990 + r], 200, 340, fill=255, width=5)
        d.text((W / 2, 230), "SERPUKHOV-15 · COMMAND BUNKER", font=F("b7", 52), fill=255, anchor="mm")
    elif var == "phone":
        for yv in range(160, 1360, 10): d.line([0, yv, W, yv], fill=50, width=1)
        cx, cy = 560, 900; d.rounded_rectangle([cx - 300, cy - 60, cx + 300, cy + 200], 40, fill=255); d.rounded_rectangle([cx - 330, cy - 170, cx + 330, cy - 70], 50, fill=255)
        d.ellipse([cx - 90, cy - 20, cx + 90, cy + 160], fill=0); d.ellipse([cx - 40, cy + 30, cx + 40, cy + 110], fill=255)
        d.line([cx + 300, cy + 120, cx + 380, cy + 260, cx + 300, cy + 380, cx + 420, cy + 470], fill=255, width=10)
        if int(t * 2) % 2 == 0:
            jx = 6 * math.sin(t * 60)
            for k in range(3): r = 120 + k * 50; dr.arc([cx - r + jx, cy - 120 - r, cx + r + jx, cy - 120 + r], 210, 330, fill=255, width=8)
        d.text((W / 2, 1220), "IT NEVER RANG IN MOSCOW", font=F("ob", 56), fill=255, anchor="mm") if False else None
        dr.text((W / 2, 260), "THE DIRECT LINE TO HIS COMMANDERS", font=F("b7", 48), fill=255, anchor="mm")
    else:
        sky = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sky)
        for yv in range(0, 1100, 5): sd.line([0, yv, W, yv], fill=255, width=4)
        sa = np.asarray(sky).astype(np.float32) / 255 * .8; img = img * (1 - sa[..., None] * .85) + INK * sa[..., None] * .85
        d.chord([-600, 1000, W + 600, 2600], 180, 360, fill=200)                                                         # Earth's curve
        for k in range(9):
            cx_ = 80 + k * 120 + 20 * math.sin(t + k); cy_ = 1020 - (k % 3) * 18
            for j in range(4): r = 36 + j * 10; d.ellipse([cx_ + j * 26 - r, cy_ - r * .45, cx_ + j * 26 + r, cy_ + r * .45], fill=255)
        sx, sy = 820, 330; d.rectangle([sx - 40, sy - 30, sx + 40, sy + 30], fill=255); d.rectangle([sx - 170, sy - 12, sx - 50, sy + 12], fill=255); d.rectangle([sx + 50, sy - 12, sx + 170, sy + 12], fill=255)
        sunx, suny = 210, 340; dr.ellipse([sunx - 70, suny - 70, sunx + 70, suny + 70], fill=255)
        ph_ = (t * .8) % 1
        for k in range(3):
            q = (ph_ + k / 3) % 1; ax, ay = sunx + (540 - sunx) * min(1, q * 2), suny + (1000 - suny) * min(1, q * 2)
            if q > .5: ax, ay = 540 + (sx - 540) * (q - .5) * 2, 1000 + (sy - 1000) * (q - .5) * 2
            dr.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=255)
        dr.line([sunx, suny, 540, 1000], fill=180, width=3); dr.line([540, 1000, sx, sy], fill=180, width=3)
        lab = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lab); pc = (236, 226, 200, 255)
        dl.text((sx, sy + 70), "OKO SATELLITE", font=F("b7", 40), fill=pc, anchor="mm"); dl.text((540, 960), "HIGH CLOUDS", font=F("b7", 40), fill=pc, anchor="mm")
        dl.text((W / 2, 1180), "SUNLIGHT OFF CLOUD TOPS, READ AS ROCKET FLAMES", font=F("b6", 34), fill=(40, 34, 28, 255), anchor="mm")
        img = ink_layer(img, L, np.array([.93, .90, .82], np.float32), .9); img = ink_layer(img, R, np.array([1.0, .82, .45], np.float32), .95)
        A = np.asarray(lab).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    img = ink_layer(img, L); img = ink_layer(img, R, REDN, .9); return img
def frame(n):
    t = n / FPS; si = max([k for k in range(len(SHOTS)) if t >= SHOTS[k][0]] or [0]); t0, kind, p = SHOTS[si]; t1 = SHOTS[si + 1][0] if si + 1 < len(SHOTS) else DUR; lt = t - t0; dur = t1 - t0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if kind == "screen": img = screen(p, lt, t)
    elif kind == "slam": img = slam(p, lt)
    elif kind == "word": img = word(p, lt)
    elif kind == "clock": img = clock_img(p["v"]); d.text((W / 2, 600), p["lab"], font=F("b6", 40), fill=(170, 210, 190, 255), anchor="mm")
    elif kind == "map": img = mapshot(p, lt, t, dur)
    elif kind == "count": img = count(lt, t, dur)
    elif kind == "quote": img = quote(p, lt)
    elif kind == "wait": img = wait(lt, dur)
    elif kind == "illus":
        img = illus_pv(p["var"], np.clip(lt / max(dur, .1), 0, 1), t, p.get("ring", False)); d.rounded_rectangle([50, 120, 330, 180], 12, fill=(20, 18, 16, 200)); d.text((190, 150), "ILLUSTRATION", font=F("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    else:
        img, lay_e = end_card(t - T_SLOGAN); lay.alpha_composite(lay_e)
    if kind not in ("end",):
        zz = 1.0 + .06 * sm(np.clip(lt / max(dur, .1), 0, 1)) + .01 * math.sin(t * 1.7)
        img = cv2.warpAffine(img, np.float32([[zz, 0, W / 2 * (1 - zz)], [0, zz, 860 * (1 - zz)]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        d.text((W - 56, 92), "ELAPSED", font=F("bb", 64), fill=(255, 255, 255, 235), anchor="ra")
    if si > 0 and lt < 2 / FPS and kind in ("slam", "word", "screen", "count"): img = img * .6 + .4
    elif si > 0 and lt < .12 and kind != "end": kk = int(50 * (1 - lt / .12)) | 1; img = cv2.filter2D(img, -1, np.ones((1, kk), np.float32) / kk)
    for k_ in range(NB):
        if not TX[k_]: continue
        if V[k_] <= t < V[k_] + D[k_] + .2:
            f = F("b7", 62); ws_ = TX[k_].split(); Ls = [len(x) + 1 for x in ws_]; tot = sum(Ls); ws = [(x, V[k_] + D[k_] * sum(Ls[:q]) / tot) for q, x in enumerate(ws_)]; rows, cur = [], []
            for x, t_ in ws:
                if cur and d.textlength(" ".join(q for q, _ in cur + [(x, t_)]), font=f) > 900: rows.append(cur); cur = []
                cur.append((x, t_))
            rows.append(cur)
            if len(rows) > 1 and len(rows[-1]) == 1: rows[-1].insert(0, rows[-2].pop())
            pg_ = max([q for q in range(0, len(rows), 2) if t >= rows[q][0][1]] or [0]); yb = 1480
            band = np.clip(1 - np.abs(yy - (yb + 70)) / 170, 0, 1)[..., None] ** .7 * .8; img = img * (1 - band)
            for r, row in enumerate(rows[pg_:pg_ + 2]):
                x_ = (W - d.textlength(" ".join(q for q, _ in row), font=f)) / 2
                for x, t_ in row:
                    if t >= t_: pe = ease((t - t_) / .1); d.text((x_, yb + r * 76 + 8 * (1 - pe)), x, font=f, fill=(AMB if t - t_ < .22 else (255, 255, 255)) + (255,))
                    x_ += d.textlength(x + " ", font=f)
    A_ = np.asarray(lay).astype(np.float32) / 255
    img = img * VIG; img = img * (1 - A_[..., 3:]) + A_[..., :3] * A_[..., 3:]
    img += np.random.default_rng(n).normal(0, .011, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1)
    img *= min(1, (DUR - t) / .5)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)
if sys.argv[1] == "test":
    for x in sys.argv[2:]: Image.fromarray(frame(int(float(x) * FPS))).save(f"{O}t_{float(x):05.1f}.jpg", quality=86)
else:
    a, b_, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", f"{O}{name}.part.mp4"], stdin=subprocess.PIPE)
    for n in range(a, b_): pr.stdin.write(frame(n).tobytes())
    pr.stdin.close(); pr.wait(); os.rename(f"{O}{name}.part.mp4", f"{O}{name}.mp4")
