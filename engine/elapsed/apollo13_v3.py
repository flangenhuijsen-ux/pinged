import json, sys, subprocess, os, math, numpy as np, cv2, soundfile as sf, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont
O = "/home/claude/a13v3/out/"; W, H, FPS = 1080, 1920, 30; P = "/home/claude/paper/"
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
J = json.load(open(O + "d.json")); D = {int(k): v for k, v in J["D"].items()}; TX = J["VO"]
NB = len(TX); GAP = {0: .35, 1: .25, 4: .4, 6: .55, 8: .35, 9: .3, 10: .35, 11: .3}
V = []; t = 0.0
for i in range(NB): V.append(t); t += D[i] + GAP.get(i, .2)
DUR = t + 1.6
G = lambda h, m, s: h * 3600 + m * 60 + s
T_BANG = V[6] + D[6] * .62; T_ALARM = V[7] + .05
# ------------------------------------------------ shot list
S_ = [(0, 0, "slam", dict(lines=[("“HOUSTON,", 230), ("WE'VE HAD", 230), ("A PROBLEM”", 230)], kicker="APOLLO 13 · 13 APRIL 1970", stamp="2 MIN EARLIER?")),
      (0, 1.55, "clock", dict(v=G(55, 55, 20), lab="GROUND ELAPSED TIME · THE PROBLEM CALL")),
      (0, 2.55, "rewind", dict(a=G(55, 55, 20), b=G(55, 53, 6), lab="2 MIN 14 S EARLIER")),
      (0, 3.75, "word", dict(w="OKAY.", sub="SWIGERT · 055:53:06")),
      (1, 0, "traj", {}),
      (1, 2.9, "km", {}),
      (2, 0, "illus", dict(var="mocr")),
      (3, 0, "tr", dict(get="055:52:58", who="CAPCOM", txt="13, we've got one more item for you, when you get a chance. We'd like you to stir up your cryo tanks.", hl="stir up your cryo tanks.", typed=False)),
      (4, 0, "tr", dict(get="055:53:06", who="SWIGERT", txt="Okay.", hl="Okay.", typed=True)),
      (4, 1.15, "word", dict(w="OKAY.", sub="ONE WORD · LOGGED AT 055:53:06")),
      (5, 0, "illus", dict(var="tank")),
      (5, 2.35, "illus", dict(var="spark")),
      (6, 0, "gauge", {}),
      (6, T_BANG - V[6], "flash", {}),
      (7, 0, "tr", dict(get="055:55:20", who="SWIGERT", txt="Okay, Houston, we've had a problem here.", hl="we've had a problem here.", typed=True, red=True)),
      (7, 1.45, "caution", {}),
      (8, 0, "tr", dict(get="055:55:28", who="CAPCOM", txt="This is Houston. Say again, please.", hl="Say again, please.", typed=True)),
      (9, 0, "illus", dict(var="vent")),
      (9, 2.35, "photo", dict(k="lm", z0=1.0, z1=1.14, c=(.48, .48), cap="AQUARIUS · THE LIFEBOAT", src="NASA · TAKEN BY THE CREW, 17 APRIL 1970")),
      (10, 0, "date", {}),
      (10, 1.55, "photo", dict(k="dmg", z0=1.0, z1=1.1, c=(.42, .45), cap="THE SERVICE MODULE · 17 APRIL 1970", src="NASA · TAKEN BY THE CREW")),
      (10, 3.15, "photo", dict(k="dmg", z0=1.75, z1=1.95, c=(.47, .36), cap="ONE PANEL, BLOWN OFF", src="NASA · TAKEN BY THE CREW")),
      (11, 0, "illus", dict(var="splash")),
      (12, 0, "end", {})]
SHOTS = sorted([(max(0, V[l] + off - (.1 if off == 0 and l else 0)), k, p) for l, off, k, p in S_], key=lambda x: x[0])
if sys.argv[1] == "info":
    print(round(DUR, 1), int(DUR * FPS), len(SHOTS), round(T_BANG, 2))
    for s in SHOTS: print(round(s[0], 2), s[1], s[2].get("var", ""))
    sys.exit()
if sys.argv[1] == "audio":
    SR = 44100; n = int(DUR * SR); v = np.zeros(n); rms = lambda x: np.sqrt((x ** 2).mean()); rng = np.random.default_rng(2)
    for i, t0 in enumerate(V):
        a, _ = sf.read(f"{O}w{i}.wav"); k = int(t0 * SR); v[k:k + len(a)] += a[:n - k]
    v = v / np.abs(v).max() * .9; tt = np.arange(n) / SR; TU = 432 / 440; pad = np.zeros(n)
    for f, a in ((55.0, .5), (82.41, .4), (110.0, .3), (164.81, .16), (220.0, .08)): pad += a * np.sin(2 * np.pi * f * TU * tt + 2.5 * np.sin(2 * np.pi * .07 * tt + f))
    pulse = (.5 + .5 * np.sin(2 * np.pi * (1.0 + 1.6 * np.clip((tt - V[5]) / (T_BANG - V[5]), 0, 1)) * tt)) ** 5 * (tt > V[5]) * (tt < T_BANG)
    pad += .5 * np.sin(2 * np.pi * 49 * TU * tt) * pulse
    pad *= np.where(tt < T_BANG, .6 + .5 * np.clip((tt - V[2]) / (T_BANG - V[2]), 0, 1), np.where(tt < V[11], .85, 1.0))
    bq, aq = sg.butter(2, [30 / (SR / 2), 1800 / (SR / 2)], "band"); pad = sg.lfilter(bq, aq, pad); pad *= rms(v[np.abs(v) > .02]) * 10 ** (-12 / 20) / rms(pad)
    fx = np.zeros(n)
    def put(x, t0, g=1.0):
        k = int(t0 * SR); m = min(len(x), n - k)
        if m > 0 and k >= 0: fx[k:k + m] += x[:m] * g
    e = np.arange(int(SR * .3)) / SR; whoosh = sg.lfilter(*sg.butter(2, [400 / (SR / 2), 4000 / (SR / 2)], "band"), rng.normal(0, 1, len(e))) * np.sin(np.pi * e / e[-1]) ** 2 * .05
    e2 = np.arange(int(SR * .5)) / SR; thump = .2 * np.sin(2 * np.pi * 55 * e2) * np.exp(-e2 * 9)
    key = rng.normal(0, 1, int(SR * .025)) * np.exp(-np.arange(int(SR * .025)) / SR * 200) * .07
    for t0, k, p in SHOTS[1:]:
        if k in ("slam", "word", "date"): put(thump, t0)
        elif k != "flash": put(whoosh, t0 - .08)
        if k == "tr" and p.get("typed"):
            for kk in np.arange(t0 + .25, t0 + .25 + len(p["txt"]) / 34, 1 / 34): put(key * (.7 + .5 * rng.random()), kk)
    e = np.arange(SR * 3) / SR; bang = .7 * np.sin(2 * np.pi * 42 * e) * np.exp(-e * 2.2) + .35 * sg.lfilter(*sg.butter(2, 300 / (SR / 2)), rng.normal(0, 1, len(e))) * np.exp(-e * 3)
    put(bang, T_BANG - .02)
    e = np.arange(int(SR * .9)) / SR; alarm = .09 * np.sign(np.sin(2 * np.pi * 750 * e)) * (np.sin(2 * np.pi * 4 * e) > 0) * np.minimum(1, (.9 - e) / .1)
    alarm = sg.lfilter(*sg.butter(2, 2500 / (SR / 2)), alarm); put(alarm, V[7] + D[7] * .55); put(alarm, V[7] + 1.45 + .05, .8)
    tick = np.sin(2 * np.pi * 1800 * np.arange(int(SR * .012)) / SR) * .06
    for kk in np.arange(V[6], T_BANG - .05, .09): put(tick, kk)
    fade = np.clip(np.minimum(tt / .03, (DUR - tt) / 1.2), 0, 1); mix = (v + pad + fx) * fade
    mix = np.stack([mix, mix], 1) / max(1, np.abs(mix).max() / .97); sf.write(O + "mix.wav", mix, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", O + "mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "44100", O + "mixn.wav"], check=True)
    print("voice", round(20 * np.log10(rms(v[np.abs(v) > .02])), 1), "pad", round(20 * np.log10(rms(pad)), 1)); sys.exit()
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
# ------------------------------------------------ moving engravings
def sky_lines(d, y0, y1, step=9, every=2, val=70):
    for yv in range(y0, y1, step):
        if (yv // step) % every == 0: d.line([0, yv, W, yv], fill=val, width=1)
def illus(var, u, t, lt):
    img = PAPER.copy() * .97; L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    if var == "mocr":                         # Mission Control: rows of consoles, a wall screen, blinking lamps
        d.rectangle([140, 260, 940, 720], outline=255, width=6); sky_lines(d, 266, 716, 7, 1, 60)
        d.rectangle([146, 266, 934, 714], fill=0); hl = (HATCHH > 0)
        path = [(200 + k * 12, 600 - 260 * math.sin(k / 58 * math.pi) * .9 + 20 * math.sin(k * .2)) for k in range(59)]
        d.line(path, fill=255, width=4); k_ = int(40 + 3 * math.sin(t)); d.ellipse([path[k_][0] - 10, path[k_][1] - 10, path[k_][0] + 10, path[k_][1] + 10], fill=255)
        d.text((540, 690), "FLIGHT PLAN · DAY 3", font=F("os", 30), fill=255, anchor="mm")
        for row, (y0, sc, nc) in enumerate(((880, .78, 4), (1040, .92, 4), (1225, 1.08, 3))):
            cw_ = 215 * sc; gapc = 30 * sc; tot = nc * cw_ + (nc - 1) * gapc; xs = (W - tot) / 2
            for c in range(nc):
                x0 = xs + c * (cw_ + gapc)
                d.rectangle([x0 + 18 * sc, y0 - 78 * sc, x0 + cw_ - 18 * sc, y0], outline=255, width=4); d.rectangle([x0 + 26 * sc, y0 - 70 * sc, x0 + cw_ - 26 * sc, y0 - 8 * sc], fill=255)
                for j in range(6):
                    if (int(t * 3 + c * 1.7 + j * 2.3 + row) % 3) != 0: d.rectangle([x0 + 40 * sc + j * 24 * sc, y0 - 54 * sc, x0 + 52 * sc + j * 24 * sc, y0 - 44 * sc], fill=0)
                d.polygon([(x0, y0), (x0 + cw_, y0), (x0 + cw_ + 10 * sc, y0 + 105 * sc), (x0 - 10 * sc, y0 + 105 * sc)], fill=150); d.line([(x0, y0), (x0 + cw_, y0)], fill=255, width=4)
                hx = x0 + cw_ / 2 + 8 * math.sin(t * .6 + c * 2 + row); hy = y0 + 70 * sc
                d.ellipse([hx - 22 * sc, hy - 22 * sc, hx + 22 * sc, hy + 22 * sc], fill=255); d.chord([hx - 52 * sc, hy + 14 * sc, hx + 52 * sc, hy + 110 * sc], 180, 360, fill=255)
        L = Image.fromarray(np.asarray(L)); img = ink_layer(img, L)
        d2 = ImageDraw.Draw(R); d2.ellipse([path[k_][0] - 10, path[k_][1] - 10, path[k_][0] + 10, path[k_][1] + 10], fill=255); img = ink_layer(img, R, REDN, .9)
        return img
    if var in ("tank", "spark"):              # cut-away oxygen tank with a spinning fan and damaged wiring
        zoom = 1.0 if var == "tank" else 1.6 + .1 * u; cx, cy = W / 2, 860 if var == "tank" else 1010
        def T(x, y): return (cx + (x - 540) * zoom, cy + (y - 860) * zoom)
        sph = Image.new("L", (W, H), 0); ImageDraw.Draw(sph).ellipse([*T(240, 560), *T(840, 1160)], fill=255); sa = np.asarray(sph) > 0
        hl = np.zeros((H, W), np.uint8); hl[sa & (HATCH45 > 0)] = 90; L = Image.fromarray(hl); d = ImageDraw.Draw(L)
        d.ellipse([*T(240, 560), *T(840, 1160)], outline=255, width=8); d.ellipse([*T(262, 582), *T(818, 1138)], outline=255, width=3)
        d.rectangle([*T(510, 470), *T(570, 560)], fill=255)
        for fy in (700, 1020):                # two fans, rotating blades
            fx = 540; d.ellipse([*T(fx - 70, fy - 70), *T(fx + 70, fy + 70)], outline=255, width=5)
            for b in range(4):
                a = t * 14 * (1 if var == "spark" or u > .3 else 0) + b * math.pi / 2; c_, s_ = math.cos(a), math.sin(a)
                d.polygon([T(fx, fy), T(fx + 62 * c_ - 18 * s_, fy + 62 * s_ * .45 + 18 * c_ * .45), T(fx + 62 * c_ + 18 * s_, fy + 62 * s_ * .45 - 18 * c_ * .45)], fill=255)
        d.line([T(560, 520), T(620, 640), T(600, 700), T(560, 700)], fill=255, width=int(6 * zoom)); d.line([T(560, 520), T(640, 720), T(640, 990), T(560, 1020)], fill=255, width=int(6 * zoom))
        for k in range(5): q = T(624 + k * 4, 830 + k * 26); d.line([q[0] - 10 * zoom, q[1], q[0] + 10 * zoom, q[1] + 6], fill=255, width=3)
        on = var == "spark" or u > .45
        if on:
            sx, sy = T(640, 880); fl = abs(math.sin(t * 31)) * (.5 + .5 * abs(math.sin(t * 7)))
            for k in range(9):
                a = k * .7 + t * 5; rr = (30 + 50 * fl) * zoom * (.6 + .4 * ((k * 37) % 5) / 4)
                dr.line([sx, sy, sx + rr * math.cos(a), sy + rr * math.sin(a)], fill=255, width=int(4 * zoom))
            dr.ellipse([sx - 14 * zoom * fl - 4, sy - 14 * zoom * fl - 4, sx + 14 * zoom * fl + 4, sy + 14 * zoom * fl + 4], fill=255)
        if var == "tank":
            d.text((W / 2, 400), "OXYGEN TANK 2", font=F("ob", 64), fill=255, anchor="mm"); d.text(T(860, 700), "FAN", font=F("ob", 40), fill=255); d.text(T(860, 1020), "FAN", font=F("ob", 40), fill=255)
            d.text((W / 2, 1290), "LIQUID OXYGEN, ABOUT −180 °C", font=F("oi", 38), fill=255, anchor="mm")
        else:
            d.text((W / 2, 330), "DAMAGED INSULATION ON THE FAN WIRES", font=F("ob", 46), fill=255, anchor="mm")
        img = ink_layer(img, L); img = ink_layer(img, R, np.array([.85, .30, .06], np.float32), .95); return img
    if var == "vent":                         # the stack in space, oxygen venting from the service module
        lines_ = ((yy % 5) < 1).astype(np.float32)[..., None]; img = INK * .85 * (1 - lines_) + (INK * .6 + PAPER * .4) * lines_
        for x, y, b, s_ in STARS:
            x2 = int((x - t * 14 * b) % W); y2 = int(y) % (H - 3); r_ = 1 + int(b * 2); img[y2:y2 + r_, x2:x2 + r_] = PAPER[y2, min(x2, W - 1)] * (.6 + .4 * b)
        cx, cy = 500 + 16 * math.sin(t * .3), 860; ang = math.radians(-16 + 3 * math.sin(t * .25)); ca, sa_ = math.cos(ang), math.sin(ang); kk = 1.05
        Rr = lambda x, y: (cx + kk * (x * ca - y * sa_), cy + kk * (x * sa_ + y * ca))
        vent = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(vent)
        for k in range(200):
            ph = (k / 200 + t * .35) % 1; a = 1.9 + .55 * math.sin(k * 2.1) + .25 * math.sin(k * .37); r0 = 30 + ph * 620; bx, by = Rr(-120, 70)
            px, py = bx + r0 * math.cos(a), by + r0 * math.sin(a); rr = 6 + ph * 52; dv.ellipse([px - rr, py - rr, px + rr, py + rr], fill=int(235 * (1 - ph) ** 1.3))
        va = np.clip(cv2.GaussianBlur(np.asarray(vent).astype(np.float32), (0, 0), 13) / 255 * 1.3, 0, .92) * (.75 + .25 * HATCH45); img = img * (1 - va[..., None]) + PAPER * va[..., None]
        S = Image.new("L", (W, H), 0); ds = ImageDraw.Draw(S)
        polys = ([Rr(-300, -70), Rr(60, -70), Rr(60, 70), Rr(-300, 70)], [Rr(-300, -40), Rr(-380, -64), Rr(-380, 64), Rr(-300, 40)], [Rr(60, -70), Rr(200, -26), Rr(200, 26), Rr(60, 70)], [Rr(200, -60), Rr(330, -80), Rr(370, 0), Rr(330, 80), Rr(200, 60)])
        for poly in polys: ds.polygon(poly, fill=255)
        for lg in (-1, 1): ds.line([Rr(320, 70 * lg), Rr(410, 150 * lg)], fill=255, width=8)
        Sa = np.asarray(S).astype(np.float32) / 255; shade = 1 - .55 * HATCH45 * (((xx - cx) * sa_ - (yy - cy) * ca) > 0)
        img = img * (1 - Sa[..., None]) + PAPER * shade[..., None] * Sa[..., None]
        L2 = Image.new("L", (W, H), 0); d2 = ImageDraw.Draw(L2)
        for poly in polys: d2.line(poly + [poly[0]], fill=255, width=3)
        d2.line([Rr(-150, -70), Rr(-150, 70)], fill=255, width=3); d2.line([Rr(-60, -70), Rr(-60, 70)], fill=255, width=3)
        img = ink_layer(img, L2, INK, .8)
        lab = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lab); pc = (236, 226, 200, 255)
        dl.text((Rr(-120, -150)[0], Rr(-120, -150)[1]), "SERVICE MODULE", font=F("ob", 36), fill=pc, anchor="mm")
        dl.text((Rr(130, -150)[0], Rr(130, -150)[1] - 30), "COMMAND MODULE", font=F("ob", 36), fill=pc, anchor="mm")
        dl.text((W - 60, Rr(330, 200)[1] + 20), "AQUARIUS (LUNAR MODULE)", font=F("ob", 36), fill=pc, anchor="ra")
        dl.text((W / 2, 1330), "OXYGEN VENTING INTO SPACE", font=F("ob", 46), fill=pc, anchor="mm")
        return comp(img, lab)
    if var == "splash":                       # capsule under three parachutes, swaying down to a moving sea
        sky_lines(d, 160, 1180, 9, 3, 60); hz = 1180
        for k, yv in enumerate(range(hz, H, 13)):
            off = int((t * 40 + k * 37) % 80)
            for x0 in range(-80 + off, W, 80): d.line([x0, yv + 3 * math.sin(x0 * .02 + t * 2 + k), x0 + 52, yv + 3 * math.sin((x0 + 52) * .02 + t * 2 + k)], fill=200, width=2)
        sw = math.sin(t * 1.3) * 18 * (1 - sm(u)); cy = 1000 + 110 * sm(u); cx = W / 2 + sw
        for j, (ox, oy) in enumerate(((-230, -470), (0, -540), (230, -470))):
            px, py = cx + ox + math.sin(t * 1.1 + j) * 10, cy + oy; d.chord([px - 150, py - 110, px + 150, py + 110], 180, 360, fill=255)
            for g_ in range(-150, 151, 50): d.line([px + g_, py, cx, cy - 70], fill=255, width=2)
            for g_ in range(-120, 121, 60): dr.line([px + g_, py - math.sqrt(max(0, 1 - (g_ / 150) ** 2)) * 110 + 4, px + g_ * .97, py - 4], fill=255, width=10)
        d.polygon([(cx - 90, cy + 40), (cx + 90, cy + 40), (cx + 30, cy - 70), (cx - 30, cy - 70)], fill=255); d.chord([cx - 92, cy + 10, cx + 92, cy + 70], 0, 180, fill=255)
        d.text((W / 2, 330), "SPLASHDOWN · SOUTH PACIFIC", font=F("ob", 48), fill=255, anchor="mm")
        img = ink_layer(img, L); img = ink_layer(img, R, REDN, .85); return img
# ------------------------------------------------ frame
def frame(n):
    t = n / FPS; si = max([k for k in range(len(SHOTS)) if t >= SHOTS[k][0]] or [0]); t0, kind, p = SHOTS[si]; t1 = SHOTS[si + 1][0] if si + 1 < len(SHOTS) else DUR; lt = t - t0; dur = t1 - t0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if kind == "slam": img = slam(p, lt)
    elif kind == "word": img = word(p, lt)
    elif kind == "clock": img = clock_img(p["v"]); d.text((W / 2, 600), p["lab"], font=F("b6", 40), fill=(170, 210, 190, 255), anchor="mm"); d.text((W / 2, 960), "SWIGERT: “OKAY, HOUSTON, WE'VE HAD A PROBLEM HERE.”", font=F("b6", 34), fill=(255, 255, 255, 200), anchor="mm")
    elif kind == "rewind":
        u = sm(lt / 1.0); sec = p["a"] + (p["b"] - p["a"]) * u; img = clock_img(sec, AMB if u < 1 else GRN); d.text((W / 2, 600), p["lab"], font=F("b6", 44), fill=AMB + (255,), anchor="mm")
        if u < 1: img = cv2.filter2D(img, -1, np.ones((9, 1), np.float32) / 9)
    elif kind == "traj": img = traj(lt, dur, t)
    elif kind == "km": img = km(lt)
    elif kind == "tr": img = tr(p, lt)
    elif kind == "gauge": img = gauge(lt, t)
    elif kind == "flash":
        img = DARK.copy(); f_ = max(0, 1 - lt / .45); img = img * (1 - f_) + f_
        if lt > .35: d.text((W / 2, 820), "055:54:53", font=F("m5", 110), fill=(255, 255, 255, int(255 * ease((lt - .35) / .2))), anchor="mm"); d.text((W / 2, 930), "THE CREW HEARS A BANG", font=F("b7", 56), fill=AMB + (int(255 * ease((lt - .45) / .2)),), anchor="mm")
        if lt < .5: k = (1 - lt / .5) * 30; img = cv2.warpAffine(img, np.float32([[1, 0, k * math.sin(lt * 90)], [0, 1, k * math.cos(lt * 70)]]), (W, H))
    elif kind == "caution": img = caution(lt, t)
    elif kind == "date": img = date(lt)
    elif kind == "photo":
        img = photo(p, lt, dur); a8 = int(255 * ease((lt - .25) / .35))
        d.rounded_rectangle([60, 1250, W - 60, 1380], 18, fill=(0, 0, 0, int(a8 * .65))); d.text((W / 2, 1296), p["cap"], font=F("b7", 48), fill=AMB + (a8,), anchor="mm"); d.text((W / 2, 1348), "PHOTOGRAPH · " + p["src"], font=F("b6", 28), fill=(255, 255, 255, int(a8 * .75)), anchor="mm")
    elif kind == "illus":
        img = illus(p["var"], np.clip(lt / max(dur, .1), 0, 1), t, lt); d.rounded_rectangle([W - 330, 200, W - 50, 260], 12, fill=(20, 18, 16, 200)); d.text((W - 190, 230), "ILLUSTRATION", font=F("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    else:
        img = DARK.copy() * .6; a8 = int(255 * ease((lt - .3) / .5))
        d.text((W / 2, 820), "ELAPSED", font=F("bb", 190), fill=(255, 255, 255, a8), anchor="mm"); d.text((W / 2, 950), "EVERY SECOND IS ON THE RECORD", font=F("b6", 40), fill=(255, 255, 255, int(a8 * .85)), anchor="mm")
        d.text((W / 2, 1010), "ILLUSTRATIONS AND DIAGRAMS ARE RECONSTRUCTIONS · PHOTOS: NASA", font=F("b6", 24), fill=(255, 255, 255, int(a8 * .55)), anchor="mm")
    if kind not in ("photo", "end", "flash"):          # constant slow camera push, so no frame is ever static
        zz = 1.0 + .07 * sm(np.clip(lt / max(dur, .1), 0, 1)) + .012 * math.sin(t * 1.7); cy_ = 860
        img = cv2.warpAffine(img, np.float32([[zz, 0, W / 2 * (1 - zz)], [0, zz, cy_ * (1 - zz)]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if kind != "end": d.text((W - 56, 92), "ELAPSED", font=F("bb", 64), fill=(255, 255, 255, 235), anchor="ra")
    if si > 0 and lt < 2 / FPS and kind in ("slam", "word", "date"): img = img * .6 + .4
    elif si > 0 and lt < .12 and kind not in ("flash",): kk = int(50 * (1 - lt / .12)) | 1; img = cv2.filter2D(img, -1, np.ones((1, kk), np.float32) / kk)
    for k_ in range(NB):
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
