import json, sys, subprocess, os, math, numpy as np, cv2, soundfile as sf, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont
O = "/home/claude/tit4/out/"; W, H, FPS = 1080, 1920, 30
exec(open("/home/claude/elapsed/brand.py").read().split("# ------------------------------------------------ logo")[0])
SEG.update({"1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgecd", "7": "abc", "9": "abfgcd", "-": "g"})
FD2 = "/home/claude/bon2/fonts/"; _fc = {}
def F2(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(FD2 + {"b6": "barlow-condensed-600.ttf", "b7": "barlow-condensed-700.ttf", "m5": "ibm-plex-mono-500.ttf", "bb": "bebas.ttf"}[n], int(s))
    return _fc[(n, s)]
C = lambda h, m, s=0: h * 3600 + m * 60 + s
GRN, AMB, RED, WHT = (125, 242, 180), (255, 196, 96), (255, 104, 84), (240, 244, 240)
T0, TA = C(22, 55), C(23, 40)
B = [
 dict(t="Less than an hour before the iceberg, Titanic gets one last warning.", c=C(22, 55), z=(1.0, 540, 800)),
 dict(t="A ship nearby has stopped for the night. Its operator taps out why.", c=C(22, 55, 4), z=(1.05, 540, 640), msg=("22:55", "SS CALIFORNIAN  ·  C. EVANS", "Say, old man, we are stopped and surrounded by ice.")),
 dict(t="Stopped, and surrounded by ice.", c=C(22, 55, 10), z=(1.2, 540, 640), slam=("SURROUNDED", "BY ICE", AMB), gap=.5),
 dict(t="Titanic's operator is busy, sending passengers' telegrams.", c=C(22, 55, 14), z=(1.05, 540, 1000)),
 dict(t="Shut up. Shut up. I am busy.", c=C(22, 55, 20), z=(1.0, 540, 800), msg=("22:55", "RMS TITANIC  ·  OPERATOR", "Shut up, shut up, I am busy; I am working Cape Race."), slam=("SHUT UP", "I AM BUSY", AMB), gap=1.2),
 dict(t="The warning is cut off.", c=C(22, 56), z=(1.05, 540, 1150), run=30),
 dict(t="At eleven thirty-five, the other operator goes to bed. Nobody is listening now.", c=C(23, 30), z=(1.055, 540, 640), run=115, msg2=("23:35", "SS CALIFORNIAN  ·  SUMMARY", "Operator turns in for the night.")),
 dict(t="At eleven forty, the lookout rings the bell.", c=C(23, 40), z=(1.0, 540, 800), slam=("23:40", "ICEBERG, RIGHT AHEAD", RED), gap=1.3),
 dict(t="Follow, and read what came next.", c=C(23, 40, 6), z=(1.0, 540, 800), end=True)]
MORSE = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()))
UNIT = .05
def keying(txt):                                   # on/off per millisecond, and which letter is being sent
    on, let = [], []
    for ch in txt.upper():
        if ch == " ": on += [0] * int(UNIT * 4000); let += [" "] * int(UNIT * 4000); continue
        if ch not in MORSE: continue
        for sym in MORSE[ch]: k = int(UNIT * 1000 * (3 if sym == "-" else 1)); on += [1] * k + [0] * int(UNIT * 1000); let += [ch] * (k + int(UNIT * 1000))
        on += [0] * int(UNIT * 2000); let += [ch] * int(UNIT * 2000)
    return np.array(on, np.float32), let
NB = len(B)
if sys.argv[1] == "vo":
    from kokoro_onnx import Kokoro
    M = "/mnt/user-data/uploads/research--morpheus/model/"; k = Kokoro(M + "kokoro-v1.0.int8.onnx", M + "voices-v1.0.bin"); st = 0.6 * k.voices["bm_george"] + 0.4 * k.voices["bm_lewis"]; D = {}
    for i, b in enumerate(B):
        x, sr = k.create(b["t"], voice=st, speed=1.12, lang="en-gb"); sf.write(f"{O}v{i}.wav", x, sr); D[i] = round(len(x) / sr, 3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{O}v{i}.wav", "-af", "aresample=44100,highpass=f=70", "-ac", "1", f"{O}w{i}.wav"], check=True)
    json.dump(D, open(O + "d.json", "w")); print(round(sum(D.values()), 1)); sys.exit()
D = {int(k): v for k, v in json.load(open(O + "d.json")).items()}
V = []; t = .35
for i, b in enumerate(B): V.append(t); t += D[i] + b.get("gap", .28)
CPS = 34
F = F2
exec(open("/home/claude/slogan/endcard.py").read()); END_NOTE = "ILLUSTRATIONS AND DRAWN SIGNAL ARE RECONSTRUCTIONS"
T_SLOGAN = t + .3; DUR = T_SLOGAN + SLG_TOTAL + .4
ILL = [(V[1] - .1, V[2] - .1, "californian"), (V[3] - .1, V[4] - .1, "titanic"), (V[7] - .1, V[7] + D[7] * .45, "iceberg")]
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else 1 - (1 - u) ** 3
sm = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)
def beat(t): return max([i for i in range(NB) if t >= V[i]] or [0])
def clock(t):                                                  # seconds since midnight, Hawaii time
    i = beat(t); b = B[i]; n = V[i + 1] if i + 1 < NB else DUR; c0 = b["c"]; rate = b.get("run", 1); c = c0 + max(0, t - V[i]) * rate
    if i + 1 < NB and t > n - .3: c = c + (B[i + 1]["c"] - c) * sm((t - (n - .3)) / .3)
    return c
def echo_mi(c): return 134 - (134 - 22) * np.clip((c - T0) / (C(7, 39) - T0), 0, 1)   # drawn, not measured, after 07:02
if sys.argv[1] == "info": print(round(DUR, 1), int(DUR * FPS)); sys.exit()
SL = [(V[i] + D[i] * (.0 if i in (2, 4) else .45), V[i] + D[i] + b.get("gap", .28) - .05, b["slam"]) for i, b in enumerate(B) if "slam" in b]
MS = [(V[i] + .15, *b["msg"]) for i, b in enumerate(B) if "msg" in b] + [(V[i] + D[i] * .62, *b["msg2"]) for i, b in enumerate(B) if "msg2" in b]; MS.sort()
T_LOST = [m[0] for m in MS if m[1] == "23:35"][0]; T_RED = V[7]; T_AMB = V[4]
KEY = [(0.0, V[3] - .1, *keying(B[1]["msg"][2])), (V[4] + .15, V[5] + D[5], *keying(B[4]["msg"][2]))]
if sys.argv[1] == "audio":
    SR = 44100; n = int(DUR * SR); v = np.zeros(n); rms = lambda x: np.sqrt((x ** 2).mean())
    for i, t0 in enumerate(V):
        a, _ = sf.read(f"{O}w{i}.wav"); k = int(t0 * SR); v[k:k + len(a)] += a[:n - k]
    v = v / np.abs(v).max() * .9; tt = np.arange(n) / SR; TU = 432 / 440; pad = np.zeros(n)
    for f, a in ((73.42, .5), (110, .45), (146.83, .3), (220, .2), (293.66, .1)): pad += a * np.sin(2 * np.pi * f * TU * tt + 2.5 * np.sin(2 * np.pi * .09 * tt + f))
    pad *= .6 + .4 * np.clip(tt / DUR * 1.4, 0, 1); pulse = (.5 + .5 * np.sin(2 * np.pi * (1.0 + 1.2 * np.clip((tt - T_AMB) / (T_RED - T_AMB), 0, 1)) * tt)) ** 4     # heartbeat that speeds up
    pad += .35 * np.sin(2 * np.pi * 55 * TU * tt) * pulse * (tt > V[2]); pad += (tt > T_RED) * .3 * np.sin(2 * np.pi * 77.78 * TU * tt)
    bq, aq = sg.butter(2, [45 / (SR / 2), 2600 / (SR / 2)], "band"); pad = sg.lfilter(bq, aq, pad); pad *= rms(v[np.abs(v) > .02]) * 10 ** (-12 / 20) / rms(pad)
    if os.path.exists(O + "music432.wav"):
        mu, _ = sf.read(O + "music432.wav"); mu = mu.mean(1) if mu.ndim > 1 else mu; mu = np.pad(mu, (0, max(0, n - len(mu))))[:n]
        mu *= np.clip(tt / .15, 0, 1); body = mu[:int(T_SLOGAN * SR)]; mu *= rms(v[np.abs(v) > .02]) * 10 ** (-9 / 20) / rms(body)
        env = np.convolve(np.abs(v), np.ones(int(SR * .12)) / int(SR * .12), "same"); duck = 10 ** (-3.5 * np.clip(env / .05, 0, 1) / 20)
        pad = mu * duck
    fx = np.zeros(n); rng = np.random.default_rng(2)
    def put(x, t0, g=1.0):
        k = int(t0 * SR); m = min(len(x), n - k)
        if m > 0 and k >= 0: fx[k:k + m] += x[:m] * g
    e = np.arange(SR * 2) / SR; low = .22 * np.sin(2 * np.pi * 49 * TU * e) * np.exp(-e * 2.4) + .05 * rng.normal(0, 1, len(e)) * np.exp(-e * 30)
    ek = np.arange(int(SR * .03)) / SR; key = rng.normal(0, 1, len(ek)) * np.exp(-ek * 220) * .05; eb = np.arange(int(SR * .25)) / SR; blip = .09 * np.sin(2 * np.pi * 864 * eb) * np.exp(-eb * 16)
    put(blip, .35, 1.4)
    for a_, b2, on, let in KEY:
        m_ = min(int((b2 - a_) * SR), n - int(a_ * SR)); idx = np.minimum((np.arange(m_) / SR * 1000).astype(int), len(on) - 1); env = sg.lfilter([.02], [1, -.98], on[idx] * (np.arange(m_) / SR * 1000 < len(on))); put(.07 * env * np.sin(2 * np.pi * 648 * np.arange(m_) / SR), a_)
    for a, b_, s in SL: put(low, a, 1.5)
    for m in MS:
        for j in range(0, len(m[3]), 2): put(key * (.8 + .4 * rng.random()), m[0] + j / CPS)
    for i in range(1, NB): put(blip, V[i] - .28, .5)
    pad *= np.clip((T_SLOGAN - .15 - tt) / (.9 if os.path.exists(O + 'music432.wav') else .5), 0, 1)
    ew = np.arange(int(SR * .3)) / SR; whoosh = sg.lfilter(*sg.butter(2, [400 / (SR / 2), 4000 / (SR / 2)], 'band'), rng.normal(0, 1, len(ew))) * np.sin(np.pi * ew / ew[-1]) ** 2 * .05
    for a_, b2_, _v in ILL: put(whoosh, a_ - .08); put(whoosh, b2_ - .08)
    fx += add_slogan(rms(v[np.abs(v) > .02]), n, SR, T_SLOGAN)
    fade = np.clip(np.minimum(tt / .15, (DUR - tt) / .6), 0, 1); mix = (v + pad + fx) * fade; mix = np.stack([mix, mix], 1) / max(1, np.abs(mix).max() / .97)
    sf.write(O + "mix.wav", mix, SR); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", O + "mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "44100", O + "mixn.wav"], check=True); print("voice", round(20 * np.log10(rms(v[np.abs(v) > .02])), 1), "pad", round(20 * np.log10(rms(pad)), 1)); sys.exit()
# ------------------------------------------------------------------ picture
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); SCX, SCY, SR_ = 540, 640, 300
RR = np.hypot(xx - SCX, yy - SCY); TUBE = (RR < SR_)[..., None].astype(np.float32); TSH = (np.clip(1 - RR / SR_, 0, 1) ** .5)[..., None]
VIG = np.clip(1.1 - (((xx - W / 2) / (W * .8)) ** 2 + ((yy - H * .45) / (H * .7)) ** 2), .3, 1)[..., None]
SCAN = (1 - .13 * ((yy % 4) < 1))[..., None]
def col_at(t):
    if t >= T_RED: return RED
    if t >= T_AMB: u = sm((t - T_AMB) / .5); return tuple(int(GRN[k] + (AMB[k] - GRN[k]) * u) for k in range(3))
    return GRN
def tintimg(im, col):
    a = np.asarray(im).copy(); m = a[..., 3] > 0
    for k in range(3): a[..., k] = np.where(m, col[k], a[..., k])
    return Image.fromarray(a, "RGBA")
def glow(img, lit, k=1.0, mask=None):
    L = np.asarray(lit).astype(np.float32) / 255; al = L[..., 3:]; rgb = L[..., :3] * al
    s_ = cv2.resize(rgb, (W // 4, H // 4), interpolation=cv2.INTER_AREA); bl = cv2.resize(cv2.GaussianBlur(s_, (0, 0), 4), (W, H)) * .9 + cv2.resize(cv2.GaussianBlur(s_, (0, 0), 18), (W, H)) * .6
    return img * (1 - al) + rgb + bl * k
FM = F2("m5", 40)
def wrapf(d, tx, f, maxw):
    out, cur = [], ""
    for w_ in tx.split():
        if cur and d.textlength(cur + " " + w_, font=f) > maxw: out.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    return out + [cur]
def frame_radar(n):
    t = n / FPS; i = beat(t); b = B[i]; c = clock(t); col = col_at(t); rng = np.random.default_rng(n); red = t >= T_RED
    img = np.zeros((H, W, 3), np.float32) + np.array([7, 10, 9], np.float32) / 255
    if red: img += np.array([.05, .0, .0], np.float32) * (.6 + .4 * math.sin(t * 9))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); lit = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lit)
    # clock
    s_ = f"{int(c) // 3600:02d}:{int(c) % 3600 // 60:02d}:{int(c) % 60:02d}"; w, h, th, gap, cw = 62, 116, 15, 15, 26; tw = width(s_, w, gap, cw)
    gl, lt = word((W, H), "".join("8" if ch.isdigit() else ch for ch in s_), 70, 120, w, h, th, gap, cw); lay.alpha_composite(gl); _, lt = word((W, H), s_, 70, 120, w, h, th, gap, cw); lit.alpha_composite(tintimg(lt, col)); d = ImageDraw.Draw(lay); ld = ImageDraw.Draw(lit)
    tracked(d, 70 + tw + 40, 126, "14 APRIL 1912", F2("b6", 38), 7, AMB + (255,)); tracked(d, 70 + tw + 40, 178, "SHIP'S TIME", F2("b6", 30), 7, (255, 255, 255, 170)); tracked(d, 70, 62, "RMS TITANIC  ·  WIRELESS ROOM", F2("b6", 34), 7, (255, 255, 255, 235))
    # scope
    img += TUBE * np.array([.02, .09, .055], np.float32) * (.5 + .5 * TSH) * (np.array(col, np.float32) / np.array(GRN, np.float32)) ** .6
    d.ellipse([SCX - SR_ - 12, SCY - SR_ - 12, SCX + SR_ + 12, SCY + SR_ + 12], outline=(74, 84, 80, 255), width=12); d.ellipse([SCX - SR_ - 26, SCY - SR_ - 26, SCX + SR_ + 26, SCY + SR_ + 26], outline=(30, 36, 34, 255), width=9)
    x0, x1, yb = SCX - 255, SCX + 255, SCY + 90; lost = t >= T_LOST
    xs = np.arange(x0, x1, 2, dtype=np.float32); sig = np.zeros(len(xs), np.float32); cur = None
    for a_, b2, on, let in KEY:
        if a_ <= t < min(b2 + 2.2, V[6]):
            tau = (t - a_) - (x1 - xs) / 255.0; idx = (tau * 1000).astype(int); ok = (idx >= 0) & (idx < len(on)) & (tau < b2 - a_); sig = np.where(ok, on[np.clip(idx, 0, len(on) - 1)], 0)
            k0 = int((t - a_) * 1000)
            if 0 <= k0 < len(let) and t < b2: cur = let[k0]
    y = yb - np.abs(rng.normal(0, 3.5, len(xs))) - 170 * sig
    tr = np.zeros((H, W, 4), np.uint8); cv2.polylines(tr, [np.stack([xs, y], 1).astype(np.int32)], False, col + (255,), 4, cv2.LINE_AA); lit.alpha_composite(Image.fromarray(tr, "RGBA")); ld = ImageDraw.Draw(lit)
    if sig[-1] > 0: ld.ellipse([x1 + 4, yb - 190, x1 + 28, yb - 166], fill=WHT + (255,))
    tracked(d, SCX, yb + 30, "WIRELESS  ·  MORSE", F2("b6", 24), 7, col + (170,), "m")
    if cur and cur != " ": tracked(ld, SCX, SCY - 235, cur, F2("bb", 110), 0, AMB + (255,), "m")
    if lost: tracked(ld, SCX, SCY - 170, "NO ONE", F2("b7", 54), 8, RED + (int(255 * (.6 + .4 * math.sin(t * 8))),), "m"); tracked(ld, SCX, SCY - 105, "LISTENING", F2("b7", 54), 8, RED + (int(255 * (.6 + .4 * math.sin(t * 8))),), "m")
    tracked(d, SCX, SCY + 205, "MORSE DRAWN FROM THE FIRST WORDS OF EACH MESSAGE", F2("b6", 17), 3, (255, 255, 255, 95), "m")
    # countdown strip
    py = 990; d.rounded_rectangle([56, py, 1024, py + 170], 18, fill=(14, 18, 17, 240), outline=(60, 80, 76, 255), width=2); tracked(d, 84, py + 16, "MINUTES TO THE ICEBERG", F2("b6", 26), 7, (255, 255, 255, 160))
    left = max(0, (TA - c) / 60); s2 = f"{int(math.ceil(left - 1e-6)):02d}"; w2, h2, th2, g2, c2 = 46, 84, 11, 12, 20; tw2 = width(s2, w2, g2, c2); gg, _ = word((W, H), "88", 994 - tw2, py + 62, w2, h2, th2, g2, c2); lay.alpha_composite(gg); _, l2 = word((W, H), s2, 994 - tw2, py + 62, w2, h2, th2, g2, c2); lit.alpha_composite(tintimg(l2, RED if left <= 5 else col)); d = ImageDraw.Draw(lay); ld = ImageDraw.Draw(lit)
    px = lambda cc: 96 + 720 * np.clip((cc - T0) / (TA - T0), 0, 1); d.line([px(T0), py + 112, px(TA), py + 112], fill=(120, 130, 126, 160), width=3); d.line([px(T0), py + 112, px(c), py + 112], fill=col + (255,), width=5)
    for cc, lb in ((C(22, 55), "22:55"), (C(23, 35), "23:35"), (C(23, 40), "23:40")):
        on = c >= cc; x = px(cc); kc = (RED if cc == TA else col) if on else (120, 130, 126); d.ellipse([x - 10, py + 102, x + 10, py + 122], fill=kc + (255,) if on else (14, 18, 17, 255), outline=kc + (255,), width=3); tracked(d, x + (-40 if lb == "23:35" else 34 if lb == "23:40" else 0), py + 62, lb, F2("m5", 24), 0, kc + (255,), "m")
    xm = px(c); ld.ellipse([xm - 7, py + 105, xm + 7, py + 119], fill=WHT + (255,))
    # message card
    shown = [m for m in MS if t >= m[0]]; cy0 = 1180; d.rounded_rectangle([56, cy0, 1024, cy0 + 170], 18, fill=(9, 14, 12, 240), outline=(60, 80, 76, 255), width=2)
    if shown:
        m = shown[-1]; k = int((t - m[0]) * CPS); fl = max(0, 1 - (t - m[0]) / .3); d.rounded_rectangle([56, cy0, 1024, cy0 + 170], 18, outline=AMB + (int(255 * fl),), width=4)
        ld.text((84, cy0 + 16), m[1] + "   " + m[2], font=F2("b6", 30), fill=AMB + (255,)); f_ = F2("m5", 38 if len(m[3]) < 36 else 33); yq = cy0 + 62
        for ln in wrapf(d, m[3], f_, 890): ld.text((84, yq), ln[:max(0, k)] + ("_" if 0 <= k < len(ln) else ""), font=f_, fill=col + (255,)); k -= len(ln) + 1; yq += 46
    else: d.text((W / 2, cy0 + 108), "TITANIC", font=F2("bb", 100), fill=(255, 255, 255, 255), anchor="mm"); tracked(d, 84, cy0 + 16, "WIRELESS LOG", F2("b6", 26), 7, AMB + (255,))
    L0 = np.asarray(lay).astype(np.float32) / 255; img = img * (1 - L0[..., 3:]) + L0[..., :3] * L0[..., 3:]; img = glow(img, lit, 1.0); img = img * (1 - TUBE * (1 - SCAN))
    # camera: slow drift, punch-in per beat, shake on slams
    z1, cx1, cy1 = b["z"]; zp, cxp, cyp = B[i - 1]["z"] if i else b["z"]; u = ease((t - V[i]) / .22); z = zp + (z1 - zp) * u; cx = cxp + (cx1 - cxp) * u; cy = cyp + (cy1 - cyp) * u
    z *= 1 + .012 * (t - V[i]) / max(1, D[i]); shx = shy = 0
    for a, e_, s in SL:
        if a <= t < a + .35: k_ = (1 - (t - a) / .35) * 14; shx += k_ * math.sin(t * 90); shy += k_ * math.cos(t * 70)
    Mx = np.float32([[z, 0, W / 2 - cx * z + (cx - W / 2) * (1 - (z - 1) * 0) * 0 + (W / 2 - W / 2) + shx + (cx - W / 2) * 0], [0, z, H * .42 - cy * z + shy]]); Mx[0, 2] = W / 2 - (W / 2 + (cx - W / 2) * min(1, (z - 1) * 3)) * z + shx; Mx[1, 2] = 800 - (800 + (cy - 800) * min(1, (z - 1) * 3)) * z + shy
    img = cv2.warpAffine(img, Mx, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); cap = True
    for a, e_, (big, sub, sc) in SL:
        if a <= t < e_:
            u = ease((t - a) / .14); img = img * (1 - .88 * u); fs = 330
            while od.textlength(big, font=F2("bb", fs)) > 960: fs -= 10
            sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl); k_ = 1 + .25 * (1 - u); twb = sd.textlength(big, font=F2("bb", fs)); sd.text(((W - twb) / 2, 700 - fs * .6), big, font=F2("bb", fs), fill=sc + (int(255 * u),)); img = glow(img, sl, .6)
            fs2 = 120
            while od.textlength(sub, font=F2("bb", fs2)) + 6 * len(sub) > 960: fs2 -= 6
            od.line([W / 2 - 420 * u, 860, W / 2 + 420 * u, 860], fill=(255, 255, 255, 200), width=3); tracked(od, W / 2, 890, sub, F2("bb", fs2), 6, (255, 255, 255, int(255 * u)), "m")
    if False:
        u = ease((t - V[i] - D[i] * .55) / .4); img = img * (1 - u); w, h, th, gap, cw = 74, 128, 17, 17, 30; tw = width("EL:AP:SED", w, gap, cw); gl, _ = word((W, H), "88:88:888", (W - tw) / 2 + 6, 760, w, h, th, gap, cw); _, lt = word((W, H), "EL:AP:SED", (W - tw) / 2 + 6, 760, w, h, th, gap, cw)
        gl.putalpha(gl.getchannel("A").point(lambda v_: int(v_ * u))); lt.putalpha(lt.getchannel("A").point(lambda v_: int(v_ * u))); ov.alpha_composite(gl); img = glow(img, lt, 1.0); od = ImageDraw.Draw(ov)
        tracked(od, W / 2, 940, "EVERY SECOND IS ON THE RECORD", F2("b6", 36), 9, (255, 255, 255, int(220 * u)), "m"); cap = t < V[i] + D[i] + .1
    else: (tracked(od, W / 2, 1650, "SOURCE: US SENATE INQUIRY 1912  ·  TESTIMONY OF C. EVANS", F2("b6", 22), 5, (255, 255, 255, 120), "m"), tracked(od, W / 2, 1684, "TIMES AS TESTIFIED  ·  THE SHIPS' CLOCKS DIFFERED", F2("b6", 20), 5, (255, 255, 255, 95), "m"))
    if cap and any(V[k_] <= t < V[k_] + D[k_] + .2 for k_ in range(NB)):
        band = np.clip(1 - np.abs(yy - 1462) / 150, 0, 1)[..., None] ** .7 * .82; img = img * (1 - band)
    if cap:
        for k_ in range(NB):
            if V[k_] <= t < V[k_] + D[k_] + .2:
                f = F2("b7", 60); ws_ = B[k_]["t"].split(); L_ = [len(x) + 1 for x in ws_]; tot = sum(L_); ws = [(x, V[k_] + D[k_] * sum(L_[:q]) / tot) for q, x in enumerate(ws_)]; rows, cur = [], []
                for x, t_ in ws:
                    if cur and od.textlength(" ".join(q for q, _ in cur + [(x, t_)]), font=f) > 900: rows.append(cur); cur = []
                    cur.append((x, t_))
                rows.append(cur)
                if len(rows) > 1 and len(rows[-1]) == 1: rows[-1].insert(0, rows[-2].pop())
                pg = max([p for p in range(0, len(rows), 2) if t >= rows[p][0][1]] or [0])
                for r, row in enumerate(rows[pg:pg + 2]):
                    x_ = (W - od.textlength(" ".join(q for q, _ in row), font=f)) / 2
                    for x, t_ in row:
                        if t >= t_: p = ease((t - t_) / .1); od.text((x_ + 3, 1392 + r * 72 + 4), x, font=f, fill=(0, 0, 0, 220)); od.text((x_, 1392 + r * 72 + 8 * (1 - p)), x, font=f, fill=(AMB if t - t_ < .22 else (255, 255, 255)) + (255,))
                        x_ += od.textlength(x + " ", font=f)
    A = np.asarray(ov).astype(np.float32) / 255; img = img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
    img = img * VIG + rng.normal(0, .012, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1); img *= min(1, (DUR - t) / .5)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)
# ------------------------------------------------------------------ option 2: moving engravings + slogan end card
DARK = np.zeros((H, W, 3), np.float32) + np.array([.03, .035, .04], np.float32)
rng0 = np.random.default_rng(7)
def nz(sh, s_, a): return cv2.GaussianBlur(rng0.normal(0, 1, sh).astype(np.float32), (0, 0), s_) * a
mott = cv2.resize(nz((H // 8, W // 8), 5, 20), (W, H)) * .012
PAPER = (np.array([228, 216, 189], np.float32) / 255)[None, None] * (1 + mott[..., None]) * np.clip(1.1 - (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * .9, .6, 1)[..., None]
INKN = np.clip(.82 + nz((H, W), 1.2, 2.4) * .08, .55, 1).astype(np.float32); INK = np.array([.09, .08, .07], np.float32); REDN = np.array([.70, .12, .09], np.float32)
HATCH45 = ((xx + yy) % 7 < 3).astype(np.float32)
def ink_layer(img, L, col=INK, k=1.0):
    a = np.asarray(L).astype(np.float32) / 255; a = np.clip((cv2.GaussianBlur(a, (0, 0), 1.0) - .3 + (INKN - .82)) * 1.8, 0, 1) * k
    return img * (1 - a[..., None]) + np.asarray(col, np.float32)[None, None] * a[..., None]
def illus_ph(var, u, t):
    img = PAPER.copy() * .97; L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    sky = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sky)
    for yv in range(0, 1400, 5): sd.line([0, yv, W, yv], fill=255, width=4)                     # night sky: dense engraving lines
    sa = np.asarray(sky).astype(np.float32) / 255 * .8; img = img * (1 - sa[..., None] * .85) + INK * sa[..., None] * .85
    rs = np.random.default_rng(4)
    for k in range(120):                                                                        # stars
        x0, y0 = rs.uniform(0, W), rs.uniform(150, 1000); b = .5 + .5 * math.sin(t * 2 + k)
        img[int(y0):int(y0) + 3, int(x0):int(x0) + 3] = PAPER[int(y0), int(x0)] * (.6 + .4 * b)
    hz = 1100
    for k, yv in enumerate(range(hz, 1380, 11)):                                               # flat calm sea
        off = int((t * 18 + k * 37) % 90)
        for x0 in range(-90 + off, W, 90): d.line([x0, yv, x0 + 40, yv], fill=150, width=2)
    lab = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lab); pc = (236, 226, 200, 255)
    if var == "californian":
        for k in range(14):                                                                     # ice floes around a stopped ship
            fx_ = (k * 83) % W; fy = hz + 30 + (k * 47) % 220; fw = 60 + (k * 29) % 90
            d.polygon([(fx_, fy), (fx_ + fw, fy - 6), (fx_ + fw + 20, fy + 14), (fx_ + 10, fy + 20)], fill=255)
        sx, sy = 540, hz - 4
        d.polygon([(sx - 260, sy - 50), (sx + 240, sy - 50), (sx + 210, sy + 20), (sx - 230, sy + 20)], fill=255)
        d.rectangle([sx - 60, sy - 120, sx + 40, sy - 50], fill=255); d.rectangle([sx - 20, sy - 200, sx + 10, sy - 120], fill=255)
        d.line([sx - 200, sy - 50, sx - 200, sy - 260], fill=255, width=6); d.line([sx + 190, sy - 50, sx + 190, sy - 250], fill=255, width=6)
        d.line([sx - 200, sy - 250, sx + 190, sy - 240], fill=255, width=2)                      # wireless aerial
        for k in range(4):                                                                     # radio waves from the aerial
            r = ((t * 120 + k * 60) % 240) + 20; dr.arc([sx - r, sy - 250 - r * .6, sx + r, sy - 250 + r * .6], 200, 340, fill=255, width=4)
        dl.text((W / 2, 300), "SS CALIFORNIAN · STOPPED FOR THE NIGHT", font=F2("b7", 52), fill=pc, anchor="mm"); dl.text((W / 2, 362), "SINCE 22:21, AMONG FIELD ICE", font=F2("b6", 36), fill=pc, anchor="mm")
    elif var == "titanic":
        sx = 520 + 60 * u; sy = hz - 4
        d.polygon([(sx - 420, sy - 70), (sx + 400, sy - 70), (sx + 360, sy + 26), (sx - 380, sy + 26)], fill=255)
        d.rectangle([sx - 300, sy - 120, sx + 280, sy - 70], fill=255)
        for k in range(4): fx_ = sx - 220 + k * 140; d.polygon([(fx_ - 24, sy - 120), (fx_ + 24, sy - 120), (fx_ + 20, sy - 250), (fx_ - 18, sy - 250)], fill=255)
        for k in range(26):                                                                     # lit portholes, flickering
            px = sx - 380 + k * 29; on = (math.sin(t * 3 + k * 1.7) > -.6)
            if on: dr.ellipse([px - 5, sy - 40, px + 5, sy - 30], fill=255)
        for k in range(4):                                                                      # funnel smoke trailing back
            for j in range(6):
                ph_ = ((t * .4 + j / 6) % 1); r = 14 + ph_ * 60; cx_ = sx - 220 + k * 140 - ph_ * 300; cy_ = sy - 260 - ph_ * 90
                d.ellipse([cx_ - r, cy_ - r * .5, cx_ + r, cy_ + r * .5], fill=int(140 * (1 - ph_)))
        dl.text((W / 2, 300), "RMS TITANIC · FULL SPEED", font=F2("b7", 54), fill=pc, anchor="mm"); dl.text((W / 2, 362), "ABOUT 22 KNOTS, INTO THE ICE FIELD", font=F2("b6", 36), fill=pc, anchor="mm")
    else:
        sc = .55 + .7 * ease(u)                                                                # the iceberg looming out of the dark
        bx, by = 600, hz
        pts = [(bx - 260 * sc, by), (bx - 150 * sc, by - 260 * sc), (bx - 40 * sc, by - 330 * sc), (bx + 60 * sc, by - 250 * sc), (bx + 200 * sc, by - 290 * sc), (bx + 300 * sc, by)]
        ib = Image.new("L", (W, H), 0); ImageDraw.Draw(ib).polygon(pts, fill=255); ia = np.asarray(ib).astype(np.float32) / 255
        img = img * (1 - ia[..., None]) + PAPER * (.55 + .4 * HATCH45[..., None]) * ia[..., None]
        d.line(pts + [pts[0]], fill=255, width=3)
        cx_, cy_ = 180, 760; d.line([cx_, cy_, cx_, 1100], fill=255, width=10); d.rectangle([cx_ - 60, cy_ - 70, cx_ + 60, cy_], outline=255, width=8)   # crow's nest
        d.ellipse([cx_ - 14, cy_ - 108, cx_ + 14, cy_ - 80], fill=255)
        bl = abs(math.sin(t * 12)); dr.ellipse([cx_ + 70, cy_ - 60, cx_ + 96, cy_ - 34], fill=int(255 * bl))                                     # the bell
        for k in range(3): r = 30 + k * 26 + 10 * bl; dr.arc([cx_ + 83 - r, cy_ - 47 - r, cx_ + 83 + r, cy_ - 47 + r], -60, 60, fill=int(200 * bl), width=4)
        dl.text((W / 2, 300), "23:40 · THE CROW'S NEST", font=F2("b7", 54), fill=pc, anchor="mm"); dl.text((W / 2, 362), "THREE RINGS OF THE BELL", font=F2("b6", 36), fill=pc, anchor="mm")
    img = ink_layer(img, L, np.array([.93, .90, .82], np.float32), .9); img = ink_layer(img, R, np.array([1.0, .82, .45], np.float32), .95)
    A = np.asarray(lab).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def caps(img, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for k_ in range(NB):
        if V[k_] <= t < V[k_] + D[k_] + .2:
            band = np.clip(1 - np.abs(yy - 1462) / 150, 0, 1)[..., None] ** .7 * .82; img = img * (1 - band)
            f = F2("b7", 60); ws_ = B[k_]["t"].split(); L_ = [len(x) + 1 for x in ws_]; tot = sum(L_); ws = [(x, V[k_] + D[k_] * sum(L_[:q]) / tot) for q, x in enumerate(ws_)]; rows, cur = [], []
            for x, t_ in ws:
                if cur and od.textlength(" ".join(q for q, _ in cur + [(x, t_)]), font=f) > 900: rows.append(cur); cur = []
                cur.append((x, t_))
            rows.append(cur)
            if len(rows) > 1 and len(rows[-1]) == 1: rows[-1].insert(0, rows[-2].pop())
            pg = max([p for p in range(0, len(rows), 2) if t >= rows[p][0][1]] or [0])
            for r, row in enumerate(rows[pg:pg + 2]):
                x_ = (W - od.textlength(" ".join(q for q, _ in row), font=f)) / 2
                for x, t_ in row:
                    if t >= t_: p = ease((t - t_) / .1); od.text((x_, 1392 + r * 72 + 8 * (1 - p)), x, font=f, fill=(AMB if t - t_ < .22 else (255, 255, 255)) + (255,))
                    x_ += od.textlength(x + " ", font=f)
    od.rounded_rectangle([W - 330, 200, W - 50, 260], 12, fill=(20, 18, 16, 200)); od.text((W - 190, 230), "ILLUSTRATION", font=F2("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    A = np.asarray(ov).astype(np.float32) / 255; return img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
def frame(n):
    t = n / FPS
    if t >= T_SLOGAN - .15:
        img, lay_e = end_card(t - T_SLOGAN); A = np.asarray(lay_e).astype(np.float32) / 255; img = img * (1 - A[..., 3:]) + A[..., :3] * A[..., 3:]
        img *= min(1, (DUR - t) / .5); return (np.clip(img, 0, 1) * 255).astype(np.uint8)
    for a_, b_, var in ILL:
        if a_ <= t < b_:
            img = illus_ph(var, (t - a_) / (b_ - a_), t)
            if t - a_ < .12: kk = int(50 * (1 - (t - a_) / .12)) | 1; img = cv2.filter2D(img, -1, np.ones((1, kk), np.float32) / kk)
            img = caps(img, t) * VIG + np.random.default_rng(n).normal(0, .011, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1)
            return (np.clip(img, 0, 1) * 255).astype(np.uint8)
    return frame_radar(n)
if sys.argv[1] == "test":
    for x in sys.argv[2:]: Image.fromarray(frame(int(float(x) * FPS))).save(f"{O}t_{float(x):05.1f}.jpg", quality=88)
else:
    a, b_, name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", f"{O}{name}.part.mp4"], stdin=subprocess.PIPE)
    for n in range(a, b_): p.stdin.write(frame(n).tobytes())
    p.stdin.close(); p.wait(); os.rename(f"{O}{name}.part.mp4", f"{O}{name}.mp4")
