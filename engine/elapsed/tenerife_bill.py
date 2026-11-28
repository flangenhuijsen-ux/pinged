import json, sys, subprocess, os, math, numpy as np, cv2, soundfile as sf, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont
O = "/home/claude/ten/out/"; W, H, FPS = 1080, 1920, 30; P = "/home/claude/paper/"
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
exec(open("/home/claude/slogan/endcard.py").read()); TX.append(""); D[14] = SLG_SPEECH
NB = len(TX); GAP = {0: .2, 1: .25, 2: .3, 3: .25, 4: .3, 5: .2, 6: .35, 7: .3, 8: .25, 9: .45, 10: .45, 11: .4, 12: .35, 13: .6}
V = []; t = 0.0
for i in range(NB): V.append(t); t += D[i] + GAP.get(i, .2)
DUR = V[14] + SLG_TOTAL + .4; T_SLOGAN = V[14]; T_BANG = 0; G = lambda h, m, s: h * 3600 + m * 60 + s
REDS = (255, 70, 52); END_NOTE = "ILLUSTRATIONS, SCREENS AND DIAGRAMS ARE RECONSTRUCTIONS · SOURCE: SPANISH CIAIAC REPORT, CVR TRANSCRIPTS (1978)"
S_ = [(0, 0, "slam", dict(lines=[("HE TOOK", 250), ("OFF.", 330)], kicker="KLM 4805 · TENERIFE · 27 MARCH 1977", stamp=None)),
      (0, 1.12, "screen", dict(w="NO CLEARANCE", sub="THE TOWER NEVER SAID: CLEARED FOR TAKEOFF")),
      (0, 2.05, "illus", dict(var="roll")),
      (1, 0, "canary", {}),
      (1, 4.2, "word", dict(w="1 RUNWAY", sub="LOS RODEOS · FULL OF DIVERTED JETS")),
      (2, 0, "illus", dict(var="fog")),
      (3, 0, "taxi", dict(stage=1)),
      (4, 0, "taxi", dict(stage=2)),
      (4, 3.3, "slam", dict(lines=[("FULL", 260), ("POWER", 300)], kicker="17:06 LOCAL TIME · RUNWAY 30", stamp=None)),
      (5, 0, "radio", dict(who="KLM 4805 · CO-PILOT", txt="...and we are now at takeoff.", col="amb")),
      (6, 0, "radio", dict(who="TENERIFE TOWER", txt="OK... Stand by for takeoff, I will call you.", col="grn")),
      (7, 0, "clash", {}),
      (7, 5.4, "word", dict(w="\"OK\"", sub="ALL THAT CAME THROUGH")),
      (8, 0, "quote", dict(who="KLM FLIGHT ENGINEER · COCKPIT RECORDER, 17:06:34", txt="Is he not clear, that Pan American?", head="ONE QUESTION")),
      (9, 0, "slam", dict(lines=[("\"JAWEL.\"", 300)], kicker="THE CAPTAIN · DUTCH FOR: OH, YES", stamp=None)),
      (10, 0, "illus", dict(var="lights")),
      (11, 0, "slam", dict(lines=[("583", 400)], kicker="27 MARCH 1977 · LOS RODEOS", stamp="DEADLIEST EVER")),
      (12, 0, "screen", dict(w="TAKEOFF", sub="NOW SAID ONLY IN A CLEARANCE · OTHERWISE: DEPARTURE", green=True, big=True, over="SINCE 1977")),
      (14, -.15, "end", {})]
SHOTS = sorted([(max(0, V[l] + off - (.1 if off == 0 and l else 0)), k, p) for l, off, k, p in S_], key=lambda x: x[0])
CNT = None; CODE_A = [0, 0, 0, 0]; F60, F30 = 0, 0
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
    hb = (.5 + .5 * np.sin(2 * np.pi * (1.0 + .8 * np.clip((tt - V[3]) / (V[10] - V[3]), 0, 1)) * tt)) ** 6 * (tt > V[3]) * (tt < V[10])
    pad += .45 * np.sin(2 * np.pi * 49 * TU * tt) * hb; pad *= np.where(tt < V[11], 1.0, .7)
    bq, aq = sg.butter(2, [30 / (SR / 2), 1800 / (SR / 2)], "band"); pad = sg.lfilter(bq, aq, pad); pad *= rms(v[np.abs(v) > .02]) * 10 ** (-12 / 20) / rms(pad); pad *= np.clip((T_SLOGAN - .15 - tt) / .5, 0, 1)
    if os.path.exists(O + "music432.wav"):
        mu, _ = sf.read(O + "music432.wav"); mu = mu.mean(1) if mu.ndim > 1 else mu; mu = np.pad(mu, (0, max(0, n - len(mu))))[:n]
        mu *= np.clip(tt / .15, 0, 1); body = mu[:int(T_SLOGAN * SR)]; mu *= rms(v[np.abs(v) > .02]) * 10 ** (-9 / 20) / rms(body)
        env = np.convolve(np.abs(v), np.ones(int(SR * .12)) / int(SR * .12), "same"); duck = 10 ** (-3.5 * np.clip(env / .05, 0, 1) / 20)
        pad = mu * duck * np.clip((T_SLOGAN - .15 - tt) / .9, 0, 1)
    fx = np.zeros(n)
    def put(x, t0, g=1.0):
        k = int(t0 * SR); m = min(len(x), n - k)
        if m > 0 and k >= 0: fx[k:k + m] += x[:m] * g
    e = np.arange(int(SR * .3)) / SR; whoosh = sg.lfilter(*sg.butter(2, [400 / (SR / 2), 4000 / (SR / 2)], "band"), rng.normal(0, 1, len(e))) * np.sin(np.pi * e / e[-1]) ** 2 * .05
    e2 = np.arange(int(SR * .5)) / SR; thump = .2 * np.sin(2 * np.pi * 55 * e2) * np.exp(-e2 * 9)
    e3 = np.arange(int(SR * 1.2)) / SR; siren = .06 * np.sign(np.sin(2 * np.pi * 1000 * e3)) * (np.sin(2 * np.pi * 2.5 * e3) > 0) * np.minimum(1, (1.2 - e3) / .2); siren = sg.lfilter(*sg.butter(2, 3000 / (SR / 2)), siren)
    for t0, k, p in SHOTS[1:]:
        if k in ("slam", "word", "count", "fuel", "radio"): put(thump, t0)
        elif k == "screen": (put(siren, t0, 1.0) if p.get("amber") else None); put(thump, t0, 1.2)
        elif k not in ("end",): put(whoosh, t0 - .08)
    put(siren, 0.0, .9)
    put(thump, 0.0, 1.8); put(whoosh, V[2] - .1, 1.2)
    nz_ = rng.normal(0, 1, int(SR * 2.2)); nz_ = sg.lfilter(*sg.butter(2, [900 / (SR / 2), 3500 / (SR / 2)], 'band'), nz_) * .05 * np.sin(np.pi * np.arange(len(nz_)) / len(nz_)); sq = .03 * np.sin(2 * np.pi * 2400 * np.arange(len(nz_)) / SR) * np.sin(np.pi * np.arange(len(nz_)) / len(nz_))
    put(nz_ + sq, V[7] + 1.6)
    e4 = np.arange(int(SR * .9)) / SR; ring = .05 * np.sin(2 * np.pi * 900 * e4) * (np.sin(2 * np.pi * 20 * e4) > 0) * (e4 < .9)
    tick = np.sin(2 * np.pi * 1700 * np.arange(int(SR * .012)) / SR) * .06
    for kk in np.arange(0, 0, 1): put(tick, kk)
    key = rng.normal(0, 1, int(SR * .025)) * np.exp(-np.arange(int(SR * .025)) / SR * 200) * .07
    for kk in np.concatenate([np.arange(V[q] + .25, V[q] + .25 + len(TX[q]) / 30, 1 / 30) for q in (5, 6, 8)]): put(key * (.7 + .5 * rng.random()), kk)
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
    green = p.get("green"); amb = p.get("amber"); col = (110, 240, 170) if green else (255, 176, 60) if amb else REDS
    img = (DARK.copy() * .5 if green or amb else REDBG.copy()); fl = .75 + .25 * abs(math.sin(t * (2 if green else 7)))
    pw, ph_ = (980, 520) if p.get("big") else (900, 420); x0, y0 = (W - pw) / 2, 560
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0 - 26, y0 - 26, x0 + pw + 26, y0 + ph_ + 26], 30, fill=(28, 26, 26, 255), outline=(80, 74, 70, 255), width=6)
    d.rectangle([x0, y0, x0 + pw, y0 + ph_], fill=tuple(int(c * .25 * fl) for c in col) + (255,))
    for yy_ in range(int(y0), int(y0 + ph_), 6): d.line([x0, yy_, x0 + pw, yy_], fill=(0, 0, 0, 60))
    u = ease(lt / .15); fs = 260 if len(p["w"]) < 8 else 170
    while d.textlength(p["w"], font=F("bb", fs)) > pw - 80: fs -= 10
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); gd.text((W / 2, y0 + ph_ / 2 + (40 if p.get("over") else 0)), p["w"], font=F("bb", int(fs * (1.15 - .15 * u))), fill=col + (int(255 * fl),), anchor="mm")
    ga = np.asarray(gl).astype(np.float32) / 255; img = img + cv2.GaussianBlur(ga[..., :3] * ga[..., 3:], (0, 0), 30) * .9
    lay.alpha_composite(gl); d = ImageDraw.Draw(lay)
    d.text((W / 2, y0 + ph_ + 90), p["sub"], font=F("b6", 40 if p.get("top") else 36), fill=(255, 255, 255, 220 if p.get("top") else 190), anchor="mm")
    if p.get("over"): d.text((W / 2, y0 + 62), p["over"], font=F("b7", 52), fill=col + (int(230 * fl),), anchor="mm")
    if p.get("top"):
        d.text((W / 2, 330), p["top"][0], font=F("bb", 150), fill=(255, 255, 255, 255), anchor="mm"); d.text((W / 2, 440), p["top"][1], font=F("b7", 52), fill=(255, 220, 170, 255), anchor="mm")
    if not green and not amb:
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
    d.text((W / 2, 420), p.get("head", "IN HIS OWN WORDS"), font=F("ob", 52), fill=255, anchor="mm"); d.rectangle([110, 470, W - 110, 474], fill=255)
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

def load(lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, 330), "GUIDANCE COMPUTER · WORKLOAD", font=F("b7", 52), fill=(255, 200, 120, 255), anchor="mm")
    v = min(1.15, ease(lt / .9) * 1.15); fl = int(t * 6) % 2 == 0 and v > 1
    for k in range(20):
        on = k / 20 < v; c = (255, 176, 60, 255) if k < 15 else (255, 70, 52, 255); y = 1180 - k * 32
        d.rectangle([340, y, 740, y + 22], fill=c if on else (40, 36, 32, 255))
    if v > 1: d.text((W / 2, 460), "OVERLOAD", font=F("bb", 150), fill=(255, 70, 52, 255 if not fl else 140), anchor="mm")
    d.text((W / 2, 1290), "MORE TASKS THAN IT HAD TIME FOR · SCHEMATIC", font=F("b6", 32), fill=(255, 255, 255, 150), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def codes(lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    L_ = [("1201", (255, 176, 60)), ("1202", (255, 176, 60)), ("GO", (110, 240, 170)), ("GO", (110, 240, 170))]
    k = max([q for q in range(4) if t >= CODE_A[q] - .05] or [-1])
    for q in range(k + 1):
        u = ease((t - (CODE_A[q] - .05)) / .12); y = 560 + q * 220; tx, c = L_[q]
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, y), tx, font=F("bb", int(220 * (1.25 - .25 * u))), fill=c + (255,), anchor="mm")
        ga = np.asarray(gl).astype(np.float32) / 255; img = img + cv2.GaussianBlur(ga[..., :3] * ga[..., 3:], (0, 0), 25) * .6; lay.alpha_composite(gl)
    d.text((W / 2, 330), "MORE ALARMS · EACH ONE CLEARED", font=F("b7", 46), fill=(255, 255, 255, 200), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def track(lt, t, dur):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    cx, cy, cr = 470, 820, 190
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=255, width=6); d.ellipse([cx - cr + 30, cy - cr + 30, cx + cr - 30, cy + cr - 30], outline=140, width=2)
    rr = np.random.default_rng(4)
    for k in range(40):
        a = rr.uniform(0, 2 * math.pi); r = rr.uniform(cr + 10, cr + 120); x, y = cx + r * math.cos(a), cy + r * math.sin(a); s_ = rr.uniform(6, 18); d.ellipse([x - s_, y - s_ * .7, x + s_, y + s_ * .7], fill=255)
    d.text((cx, cy - 50), "WEST CRATER", font=F("ob", 40), fill=255, anchor="mm")
    p0 = (180, 1300); auto = [(p0[0] + (cx - p0[0]) * u, p0[1] + (cy - p0[1]) * u) for u in np.linspace(0, 1, 30)]
    for k in range(0, 29, 2): d.line([auto[k], auto[k + 1]], fill=170, width=5)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=255); d.text((cx, cy + 50), "COMPUTER'S TARGET", font=F("b7", 32), fill=255, anchor="mm")
    u = ease(lt / max(dur * .8, .1)); man = [(p0[0] + 720 * v + 260 * math.sin(math.pi * v), p0[1] - 880 * v) for v in np.linspace(0, u + .001, 50)]
    if len(man) > 1: dr.line(man, fill=255, width=9)
    mx, my = man[-1]; dr.polygon([(mx, my - 22), (mx - 18, my + 14), (mx + 18, my + 14)], fill=255)
    if u > .95: dr.text((min(mx, 860), my - 60), "WHERE EAGLE LANDED", font=F("b7", 40), fill=255, anchor="mm")
    d.text((W / 2, 300), "ARMSTRONG FLIES PAST IT", font=F("b7", 56), fill=255, anchor="mm")
    d.text((W / 2, 1390), "DIAGRAM, NOT TO SCALE", font=F("b6", 30), fill=200, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def fuel(lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    v = "30" if t >= F30 - .05 else "60" if t >= F60 - .05 else "--"; c = (255, 70, 52) if v == "30" else (255, 176, 60)
    d.text((W / 2, 420), "FUEL LEFT, HOUSTON CALLS", font=F("b7", 54), fill=(255, 220, 170, 255), anchor="mm")
    if v == "--": d.text((W / 2, 780), "--", font=F("bb", 560), fill=(70, 60, 50, 255), anchor="mm")
    if v != "--":
        u = ease((t - ((F30 if v == "30" else F60) - .05)) / .12)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, 780), v, font=F("bb", int(560 * (1.2 - .2 * u))), fill=c + (255,), anchor="mm")
        ga = np.asarray(gl).astype(np.float32) / 255; img = img + cv2.GaussianBlur(ga[..., :3] * ga[..., 3:], (0, 0), 40) * .8; lay.alpha_composite(gl)
        d.text((W / 2, 1100), "SECONDS", font=F("b7", 70), fill=c + (255,), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def illus_a11(var, u, t):
    img = PAPER.copy() * .97; L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    if var == "lm":
        sky = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sky)
        for yv in range(0, 1120, 5): sd.line([0, yv, W, yv], fill=255, width=4)
        sa = np.asarray(sky).astype(np.float32) / 255 * .85; img = img * (1 - sa[..., None] * .85) + INK * sa[..., None] * .85
        d.chord([-700, 1060, W + 700, 2700], 180, 360, fill=190)
        for k in range(14):
            x = (k * 173) % W; y = 1150 + (k * 37) % 160; r = 20 + (k * 13) % 40; d.ellipse([x - r, y - r * .35, x + r, y + r * .35], outline=255, width=3)
        lx, ly = 540 + 30 * math.sin(t * .7), 560 + 120 * u; k_ = 1.6
        P = lambda x, y: (lx + x * k_, ly + y * k_)
        d.polygon([P(-110, -60), P(110, -60), P(130, 40), P(-130, 40)], fill=255)
        d.polygon([P(-70, -160), P(70, -160), P(100, -60), P(-100, -60)], fill=230); d.polygon([P(-30, -140), P(30, -140), P(40, -100), P(-40, -100)], fill=60)
        for sx in (-1, 1):
            d.line([P(sx * 120, 30), P(sx * 190, 170)], fill=255, width=12); d.line([P(sx * 175, 175), P(sx * 215, 175)], fill=255, width=12)
        fl = 60 + 20 * math.sin(t * 25); dr.polygon([P(-40, 40), P(40, 40), P(0, 40 + fl * 2)], fill=255)
        lab = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lab)
        dl.text((W / 2, 260), "EAGLE · POWERED DESCENT", font=F("b7", 54), fill=(236, 226, 200, 255), anchor="mm")
        img = ink_layer(img, L, np.array([.93, .90, .82], np.float32), .9); img = ink_layer(img, R, np.array([1.0, .78, .4], np.float32), .9)
        A = np.asarray(lab).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    if var == "mcc":
        for yv in range(160, 1360, 8): d.line([0, yv, W, yv], fill=55, width=1)
        for row in range(2):
            y0 = 760 + row * 300
            for k in range(4):
                x0 = 60 + k * 250; d.rectangle([x0, y0, x0 + 220, y0 + 140], fill=255); dr.rectangle([x0 + 20, y0 + 18, x0 + 200, y0 + 90], fill=int(200 + 55 * math.sin(t * 5 + k + row)))
                hx = x0 + 110; d.ellipse([hx - 34, y0 - 120, hx + 34, y0 - 52], fill=255); d.polygon([(hx - 80, y0), (hx + 80, y0), (hx + 55, y0 - 60), (hx - 55, y0 - 60)], fill=255)
        d.rectangle([80, 330, 1000, 640], outline=255, width=6)
        for k in range(1, 6): d.line([80 + k * 153, 330, 80 + k * 153, 640], fill=120, width=2)
        mc = [(100 + q * 30, 600 - 260 * (q / 30) ** 1.6) for q in range(31)]; dr.line(mc, fill=255, width=6)
        d.text((W / 2, 230), "MISSION CONTROL · HOUSTON", font=F("b7", 54), fill=255, anchor="mm")
        img = ink_layer(img, L); img = ink_layer(img, R, REDN, .9); return img
    # boulders, from above
    for yv in range(160, 1400, 6): d.line([0, yv, W, yv], fill=70, width=1)
    rr = np.random.default_rng(7); cx, cy, cr = 560, 820, 230
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255); d.ellipse([cx - cr + 26, cy - cr + 26, cx + cr - 26, cy + cr - 26], fill=0)
    for yv in range(int(cy - cr + 30), int(cy + cr - 30), 9): d.line([cx - cr + 30, yv, cx + cr - 30, yv], fill=150, width=2)
    for k in range(70):
        a = rr.uniform(0, 2 * math.pi); r = rr.uniform(cr, cr + 260); x, y = cx + r * math.cos(a), cy + r * math.sin(a); s_ = rr.uniform(8, 34)
        if 250 < y < 1360: d.ellipse([x - s_, y - s_ * .7, x + s_, y + s_ * .7], fill=255); d.ellipse([x - s_ + 4, y - s_ * .7 + 6, x + s_ + 6, y + s_ * .7 + 8], outline=200, width=2)
    sx, sy = 560 + 40 * math.sin(t), 820 - 260 * u + 260; dr.polygon([(sx, sy - 40), (sx - 36, sy + 26), (sx + 36, sy + 26)], outline=255, width=5)
    dr.text((sx + 60, sy), "EAGLE'S TARGET", font=F("b7", 36), fill=255, anchor="lm")
    d.text((W / 2, 230), "BOULDERS NEAR WEST CRATER", font=F("b7", 54), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN, .9); return img

def canary(lt, t, dur):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    for yv in range(160, 1400, 9): d.line([0, yv, W, yv], fill=40, width=1)
    TF = [(250, 640), (330, 560), (470, 520), (560, 470), (600, 520), (520, 620), (420, 700), (300, 720)]
    GC = [(700, 860), (800, 820), (880, 880), (870, 990), (780, 1040), (690, 980)]
    d.polygon(TF, fill=255); d.polygon(GC, fill=255)
    d.text((410, 780), "TENERIFE", font=F("b7", 46), fill=255, anchor="mm"); d.text((790, 1110), "GRAN CANARIA", font=F("b7", 46), fill=255, anchor="mm")
    bx, by = 840, 900; u = ease(lt / .3)
    for k in range(10): a = k * math.pi / 5; r = 26 + 30 * u; dr.line([bx, by, bx + r * math.cos(a), by + r * math.sin(a)], fill=255, width=6)
    dr.text((bx + 40, by - 70), "BOMB · LAS PALMAS AIRPORT", font=F("b7", 34), fill=255, anchor="lm") if False else dr.text((W / 2, 1190), "A BOMB AT LAS PALMAS AIRPORT CLOSES IT", font=F("b7", 38), fill=255, anchor="mm")
    tx, ty = 470, 560
    for k in range(6):
        q = ease((lt - .5 - k * .18) / 1.2)
        if q > 0:
            sx, sy = 980 + (k % 3) * 20, 700 + k * 40; mx, my = (sx + tx) / 2 + 60, min(sy, ty) - 120
            pts = [((1 - v) ** 2 * sx + 2 * (1 - v) * v * mx + v * v * tx, (1 - v) ** 2 * sy + 2 * (1 - v) * v * my + v * v * ty) for v in np.linspace(0, q, 24)]
            dr.line(pts, fill=255, width=5); ex, ey = pts[-1]; dr.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=255)
    d.ellipse([tx - 16, ty - 16, tx + 16, ty + 16], outline=255, width=5); dr.text((tx - 40, ty - 150), "LOS RODEOS AIRPORT", font=F("b7", 40), fill=255, anchor="mm")
    d.text((W / 2, 300), "27 MARCH 1977 · CANARY ISLANDS", font=F("b7", 52), fill=255, anchor="mm"); d.text((W / 2, 1300), "DIAGRAM, NOT TO SCALE", font=F("b6", 30), fill=200, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN); return img
def jet(d, x, y, s, ang, fill=255):
    P = [(0, -1.0), (.09, -.85), (.1, -.2), (.62, .15), (.62, .25), (.1, .12), (.08, .62), (.28, .8), (.28, .88), (0, .82)]
    P = P + [(-a, b) for a, b in reversed(P[1:-1])]; ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(x + (a * ca - b * sa) * s, y + (a * sa + b * ca) * s) for a, b in P], fill=fill)
def taxi(p, lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, x1 = 120, 960; yr = 760
    d.rectangle([x0, yr - 34, x1, yr + 34], fill=(70, 74, 78, 255)); [d.line([x, yr, x + 30, yr], fill=(220, 220, 210, 255), width=4) for x in range(x0 + 20, x1 - 20, 60)]
    d.rectangle([x0, 1000 - 14, x1, 1000 + 14], fill=(50, 54, 58, 255)); d.text((x0, 1050), "PARALLEL TAXIWAY", font=F("b6", 28), fill=(200, 200, 200, 200), anchor="lm")
    EX = [(260, "C1"), (430, "C2"), (600, "C3"), (780, "C4")]
    for i, (ex, lb) in enumerate(EX):
        if lb == "C3": d.line([ex, yr + 34, ex - 90, 986], fill=(50, 54, 58, 255), width=24)
        else: d.line([ex, yr + 34, ex + (60 if i < 2 else 90), 986], fill=(50, 54, 58, 255), width=24)
        c = (255, 196, 96, 255) if lb == "C3" else (200, 200, 200, 220); d.text((ex, yr + 90), lb, font=F("b7", 40), fill=c, anchor="mm")
    if lt % .8 < .5: d.text((600 - 60, yr + 150), "?", font=F("bb", 90), fill=(255, 196, 96, 255), anchor="mm")
    fogA = np.clip(.35 + .1 * math.sin(t * .8), 0, 1)
    if p["stage"] == 1: px = x0 + 40 + 560 * ease(lt / max(dur, .1)); kx, ka = x1 - 40, 0
    else: px = 640 + 50 * ease(lt / max(dur, .1)); kx = x1 - 40; ka = math.pi * ease((lt - .3) / 1.6)
    gl = Image.new("L", (W, H), 0); jet(ImageDraw.Draw(gl), px, yr, 70, math.pi / 2); jet(ImageDraw.Draw(gl), kx, yr, 70, -math.pi / 2 + ka)
    g = np.asarray(gl).astype(np.float32)[..., None] / 255; img = img * (1 - g) + g * np.array([.92, .92, .9], np.float32)
    d.text((px, yr - 100), "PAN AM", font=F("b7", 36), fill=(120, 190, 255, 255), anchor="mm"); d.text((kx - 10, yr - 100), "KLM", font=F("b7", 36), fill=(255, 196, 96, 255), anchor="mm")
    d.text((W / 2, 300), "RUNWAY 30 · LOS RODEOS" if p["stage"] == 1 else "KLM TURNS AT THE END", font=F("b7", 54), fill=(255, 255, 255, 240), anchor="mm")
    d.text((W / 2, 400), "PAN AM WAS TOLD: LEAVE AT THE THIRD EXIT" if p["stage"] == 1 else "PAN AM STILL ON THE RUNWAY", font=F("b6", 36), fill=(255, 196, 96, 230), anchor="mm")
    d.text((W / 2, 1300), "DIAGRAM, NOT TO SCALE · DIRECTIONS SIMPLIFIED", font=F("b6", 30), fill=(255, 255, 255, 140), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; img = img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    fog = cv2.GaussianBlur(np.random.default_rng(int(t * 2)).random((H // 16, W // 16)).astype(np.float32), (0, 0), 3); fog = cv2.resize(fog, (W, H))[..., None]
    return img * (1 - fogA * .5) + fogA * .5 * (.5 + .3 * fog)
def radio(p, lt, t):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = (255, 196, 96) if p["col"] == "amb" else (125, 242, 180)
    d.rounded_rectangle([70, 380, W - 70, 1260], 28, fill=(14, 18, 20, 245), outline=c + (180,), width=3)
    d.text((110, 430), "RADIO · 119.7 MHz · RECONSTRUCTION", font=F("b6", 30), fill=(255, 255, 255, 150))
    d.text((110, 500), p["who"], font=F("b7", 56), fill=c + (255,))
    for k in range(60):
        x = 110 + k * 14; a = (abs(math.sin(t * 9 + k * .7)) * 60 + 6) * (1 if lt < len(p["txt"]) / 30 + .4 else .15)
        d.rectangle([x, 640 - a, x + 7, 640 + a], fill=c + (200,))
    n = int(max(0, lt - .25) * 30); f = F("m5", 58); y = 800; words = p["txt"].split(" "); lines, cur = [], ""
    for w_ in words:
        if d.textlength((cur + " " + w_).strip(), font=f) > W - 260: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur)
    for ln in lines: d.text((110, y), ln[:max(0, n)] + ("_" if 0 <= n < len(ln) else ""), font=f, fill=(255, 255, 255, 255)); n -= len(ln) + 1; y += 80
    A = np.asarray(lay).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def clash(lt, t, dur):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hit = lt > 1.55; u = ease((lt - .2) / 1.3)
    d.text((W / 2, 330), "TWO TRANSMISSIONS · SAME SECOND", font=F("b7", 50), fill=(255, 255, 255, 235), anchor="mm")
    for row, (lb, c, y) in enumerate((("TOWER: STAND BY FOR TAKEOFF", (125, 242, 180), 600), ("PAN AM: WE'RE STILL TAXIING", (120, 190, 255), 900))):
        d.text((110, y - 120), lb, font=F("b6", 36), fill=c + (255,))
        for k in range(70):
            x = 110 + k * 12; jit = (np.random.default_rng(int(t * 30) + k).random() * 2 - 1) if hit else 0
            a = (abs(math.sin(t * (7 + row * 4) + k * .5)) * 55 + 5) * (1 + 1.5 * hit) + 40 * jit * hit
            if not hit: x = x * u + (W / 2) * (1 - u) * 0 if True else x
            d.rectangle([x, y - abs(a), x + 6, y + abs(a)], fill=(255, 70, 52, 230) if hit else c + (220,))
    if hit: d.text((W / 2, 1120), "HETERODYNE · THE SIGNALS CANCEL OUT", font=F("b7", 44), fill=(255, 70, 52, 255), anchor="mm")
    A = np.asarray(lay).astype(np.float32) / 255; img = img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    if hit and int(t * 20) % 3 == 0: img = img + .06
    return img
def illus_ten(var, u, t):
    img = PAPER.copy() * .97; L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    hz = 900
    for yv in range(160, hz, 7): d.line([0, yv, W, yv], fill=50, width=1)
    d.polygon([(W / 2 - 40, hz), (W / 2 + 40, hz), (W + 400, 1500), (-400, 1500)], fill=150)
    for k in range(12): z = ((k / 12) + t * (.9 if var == "roll" else .15)) % 1; yy_ = hz + (1500 - hz) * z ** 2; ww = 6 + 30 * z ** 2; d.rectangle([W / 2 - ww / 2, yy_, W / 2 + ww / 2, yy_ + 8 + 40 * z ** 2], fill=255)
    if var == "roll":
        jet(d, W / 2, 1180, 330, 0); dr.text((W / 2, 260), "KLM 4805 · TAKEOFF ROLL", font=F("b7", 52), fill=255, anchor="mm")
    elif var == "fog":
        jet(d, W / 2 - 40, hz + 20, 60, 0); jet(d, W / 2 + 120, 1220, 200, math.pi)
        d.text((W / 2, 260), "FOG · VISIBILITY FALLING", font=F("b7", 52), fill=255, anchor="mm")
    else:
        f_ = ease(u * 1.6)
        d.text((W / 2, 260), "OUT OF THE FOG", font=F("b7", 52), fill=255, anchor="mm"); dr.text((W / 2, 700), "PAN AM 1736 · STILL ON THE RUNWAY", font=F("b7", 40), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, REDN, .95)
    fogA = {"roll": .25, "fog": .55, "lights": .5}[var]; fog = cv2.resize(cv2.GaussianBlur(np.random.default_rng(int(t * 3)).random((H // 20, W // 20)).astype(np.float32), (0, 0), 2.5), (W, H))[..., None]
    img = img * (1 - fogA) + fogA * (.78 + .15 * fog)
    if var == "lights":
        f_ = ease(u * 1.6); Lg = np.zeros((H, W), np.float32)
        for sx in (-1, 1): cv2.circle(Lg, (int(W / 2 + sx * (90 + 60 * f_)), int(hz + 40 + 40 * f_)), int(18 + 40 * f_), 1.0, -1)
        img = img + (cv2.GaussianBlur(Lg, (0, 0), 30 + 30 * f_) * 1.6 + Lg * .6)[..., None] * np.array([1.0, .95, .8], np.float32)
    return img
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
    elif kind == "canary": img = canary(lt, t, dur)
    elif kind == "taxi": img = taxi(p, lt, t, dur)
    elif kind == "radio": img = radio(p, lt, t)
    elif kind == "clash": img = clash(lt, t, dur)
    elif kind == "load": img = load(lt, t, dur)
    elif kind == "codes": img = codes(lt, t, dur)
    elif kind == "track": img = track(lt, t, dur)
    elif kind == "fuel": img = fuel(lt, t, dur)
    elif kind == "illus":
        img = illus_ten(p["var"], np.clip(lt / max(dur, .1), 0, 1), t); d.rounded_rectangle([50, 120, 330, 180], 12, fill=(20, 18, 16, 200)); d.text((190, 150), "ILLUSTRATION", font=F("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    else:
        img, lay_e = end_card(t - T_SLOGAN); lay.alpha_composite(lay_e)
    if kind not in ("end",):
        zz = 1.0 + .06 * sm(np.clip(lt / max(dur, .1), 0, 1)) + .01 * math.sin(t * 1.7)
        img = cv2.warpAffine(img, np.float32([[zz, 0, W / 2 * (1 - zz)], [0, zz, 860 * (1 - zz)]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        d.text((W - 56, 92), "ELAPSED", font=F("bb", 64), fill=(255, 255, 255, 235), anchor="ra")
    if si > 0 and lt < 2 / FPS and kind in ("slam", "word", "screen", "count", "codes", "fuel", "radio"): img = img * .6 + .4
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
