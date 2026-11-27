import json, sys, subprocess, os, math, numpy as np, cv2, soundfile as sf, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
O = "/home/claude/hal2/out/"; W, H, FPS = 1080, 1920, 30; P = "/home/claude/paper/"
exec(open("/home/claude/elapsed/brand.py").read().split("# ------------------------------------------------ logo")[0])
SEG.update({"1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgecd", "7": "abc", "9": "abfgcd", "-": "g"})
FB = "/home/claude/bon2/fonts/"; FP = P + "fonts/"; _fc = {}
def F(n, s, w=None):
    key = (n, int(s), w)
    if key not in _fc:
        path = {"b6": FB + "barlow-condensed-600.ttf", "b7": FB + "barlow-condensed-700.ttf", "m5": FB + "ibm-plex-mono-500.ttf", "bb": FB + "bebas.ttf",
                "go": FP + "Oswald%5Bwght%5D.ttf", "os": FP + "OldStandard-Regular.ttf", "ob": FP + "OldStandard-Bold.ttf", "oi": FP + "OldStandard-Italic.ttf", "bl": FP + "UnifrakturMaguntia-Book.ttf"}[n]
        f = ImageFont.truetype(path, int(s))
        if w: f.set_variation_by_axes([w])
        _fc[key] = f
    return _fc[key]
INK = np.array([.09, .08, .07], np.float32); REDI = (176, 30, 22); AMB, GRN = (255, 196, 96), (125, 242, 180)
ease = lambda u: 0 if u <= 0 else 1 if u >= 1 else 1 - (1 - u) ** 3
sm = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)
D = {int(k): v for k, v in json.load(open(O + "d.json")).items()}
TX = ["At four minutes past nine one morning in 1917, a single ship flattened a whole district of Halifax.", "An hour and a half earlier, two ships set off toward the same narrow channel.", "One of them was French, and loaded with explosives.", "Around a quarter to nine, they collided. The French ship caught fire.", "Her crew rowed for the far shore. And people gathered to watch.", "For twenty minutes, the burning ship drifted toward the city.", "Nine oh four, and thirty-five seconds.", "Almost everything within half a mile was flattened.", "That afternoon, the first reports reached Washington. Hundreds killed, on an American ship.", "The ship was French. And at least seventeen hundred and eighty-two people died.", "The next day, snow fell on the ruins.", "Follow, and read what came next."]
NB = len(TX); GAP = {0: .3, 5: .1, 6: .5, 8: .3, 9: .3, 10: .35}
V = []; t = 0.0
for i in range(NB): V.append(t); t += D[i] + GAP.get(i, .2)
DUR = t + 1.6; T_FLASH = V[6] + D[6] * .55
# ------------------------------------------------ shot list: (line, offset, kind, params)
S_ = [(0, 0, "slam_paper", dict(lines=[("HALIFAX", "go", 330, 700), ("SHATTERED", "go", 250, 700)], kicker="THE ELAPSED RECORD · EXTRA · 6 DEC 1917", stamp="EXTRA")),
      (0, 1.5, "clock", dict(v=9 * 3600 + 4 * 60 + 35, lab="HALIFAX, NOVA SCOTIA · 6 DECEMBER 1917")),
      (0, 2.9, "photo", dict(k="ruins_harbour", z0=1.25, z1=1.4, c=(.55, .72), cap="THE NORTH END, DECEMBER 1917", src="NOVA SCOTIA ARCHIVES")),
      (0, 4.6, "page", dict(k="e3", c0=(.5, .18, 1700, -2), c1=(.47, .22, 1350, -1))),
      (1, 0, "rewind", dict(a=9 * 3600 + 4 * 60 + 35, b=7 * 3600 + 30 * 60, lab="90 MINUTES EARLIER")),
      (1, 1.7, "map", dict(mode="ships", c0=(.48, .45, 1.05), c1=(.49, .40, 1.25))),
      (2, 0, "cards", {}),
      (2, 1.55, "cargo", {}),
      (3, 0, "clock", dict(v=8 * 3600 + 45 * 60, lab="ABOUT A QUARTER TO NINE")),
      (3, .9, "map", dict(mode="collide", c0=(.50, .40, 1.6), c1=(.50, .40, 2.1))),
      (3, 2.4, "page", dict(k="e2", c0=(.5, .16, 1500, 2), c1=(.48, .19, 1300, 1))),
      (4, 0, "illus", dict(var="crew")),
      (4, 1.8, "illus", dict(var="crowd")),
      (5, 0, "map", dict(mode="drift", c0=(.46, .42, 1.7), c1=(.43, .43, 2.0))),
      (6, 0, "clock_tick", dict(a=9 * 3600 + 4 * 60 + 31, lab="HALIFAX · 6 DECEMBER 1917")),
      (6, T_FLASH - V[6], "photo", dict(k="blast_cloud", z0=1.05, z1=1.18, c=(.5, .45), cap="THE BLAST · 6 DECEMBER 1917", src="LIBRARY AND ARCHIVES CANADA", shake=True)),
      (7, 0, "map", dict(mode="blast", c0=(.42, .45, 1.0), c1=(.42, .45, 1.15))),
      (7, 1.9, "slam_paper", dict(lines=[("NORTH END", "go", 240, 700), ("LEVELLED", "go", 260, 700)], kicker="HALF A MILE AROUND PIER 6")),
      (8, 0, "ticker", {}),
      (8, 2.6, "star", dict(c0=(.22, .14, 2.3), c1=(.20, .16, 2.6), mark=False)),
      (8, 4.1, "star", dict(c0=(.17, .26, 3.4), c1=(.17, .26, 3.6), mark=True)),
      (9, 0, "star", dict(c0=(.17, .26, 3.6), c1=(.17, .26, 3.7), mark=True, stamp=True)),
      (9, 1.6, "counter", {}),
      (10, 0, "photo", dict(k="ruins_harbour", z0=1.0, z1=1.12, c=(.5, .6), cap="THE NEXT DAY · DECEMBER 1917", src="NOVA SCOTIA ARCHIVES")),
      (11, 0, "end", {})]
SHOTS = sorted([(V[l] + off - (.1 if off == 0 and l else 0), k, p) for l, off, k, p in S_], key=lambda x: x[0])
if sys.argv[1] == "info": print(round(DUR, 1), int(DUR * FPS), len(SHOTS)); sys.exit()
if sys.argv[1] == "audio":
    SR = 44100; n = int(DUR * SR); v = np.zeros(n); rms = lambda x: np.sqrt((x ** 2).mean()); rng = np.random.default_rng(2)
    for i, t0 in enumerate(V):
        a, _ = sf.read(f"{O}w{i}.wav"); k = int(t0 * SR); v[k:k + len(a)] += a[:n - k]
    v = v / np.abs(v).max() * .9; tt = np.arange(n) / SR; TU = 432 / 440; pad = np.zeros(n)
    for f, a in ((65.41, .5), (98.0, .4), (130.81, .3), (196.0, .18)): pad += a * np.sin(2 * np.pi * f * TU * tt + 2.5 * np.sin(2 * np.pi * .08 * tt + f))
    pulse = (.5 + .5 * np.sin(2 * np.pi * (1.0 + 1.4 * np.clip((tt - V[3]) / (T_FLASH - V[3]), 0, 1)) * tt)) ** 5 * (tt > V[3]) * (tt < T_FLASH)
    pad += .5 * np.sin(2 * np.pi * 49 * TU * tt) * pulse; pad *= np.where(tt < T_FLASH, .6 + .6 * np.clip((tt - V[1]) / (T_FLASH - V[1]), 0, 1), .8)
    bq, aq = sg.butter(2, [35 / (SR / 2), 2000 / (SR / 2)], "band"); pad = sg.lfilter(bq, aq, pad); pad *= rms(v[np.abs(v) > .02]) * 10 ** (-12 / 20) / rms(pad)
    fx = np.zeros(n)
    def put(x, t0, g=1.0):
        k = int(t0 * SR); m = min(len(x), n - k)
        if m > 0 and k >= 0: fx[k:k + m] += x[:m] * g
    e = np.arange(int(SR * .3)) / SR; whoosh = sg.lfilter(*sg.butter(2, [400 / (SR / 2), 4000 / (SR / 2)], "band"), rng.normal(0, 1, len(e))) * np.sin(np.pi * e / e[-1]) ** 2 * .05
    e2 = np.arange(int(SR * .5)) / SR; thump = .2 * np.sin(2 * np.pi * 55 * e2) * np.exp(-e2 * 9)
    for t0, k, p in SHOTS[1:]:
        if k in ("slam_paper", "cargo", "cards", "counter"): put(thump, t0, 1.0)
        else: put(whoosh, t0 - .08)
    e = np.arange(SR * 4) / SR; boom = .75 * np.sin(2 * np.pi * 36 * e) * np.exp(-e * 1.0) + .4 * sg.lfilter(*sg.butter(2, 160 / (SR / 2)), rng.normal(0, 1, len(e))) * np.exp(-e * 1.5)
    put(boom, T_FLASH - .02, 1.0)
    tick = np.sin(2 * np.pi * 1800 * np.arange(int(SR * .012)) / SR) * .07
    for kk in np.arange(V[5] - .1, T_FLASH - 1.3, .125): put(tick, kk)
    for kk in (0, 1, 2, 3): put(tick * 2.2, T_FLASH - 1.25 + kk * .42 - .4)
    key = rng.normal(0, 1, int(SR * .025)) * np.exp(-np.arange(int(SR * .025)) / SR * 200) * .08
    for kk in np.arange(V[8] - .1, V[8] + 2.4, .055): put(key * (.7 + .5 * rng.random()), kk)
    fade = np.clip(np.minimum(tt / .03, (DUR - tt) / 1.2), 0, 1); mix = (v + pad + fx) * fade
    mix = np.stack([mix, mix], 1) / max(1, np.abs(mix).max() / .97); sf.write(O + "mix.wav", mix, SR)
    print("voice", round(20 * np.log10(rms(v[np.abs(v) > .02])), 1), "pad", round(20 * np.log10(rms(pad)), 1)); sys.exit()
# ------------------------------------------------ assets
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); rng0 = np.random.default_rng(7)
def nz(sh, s, a): return cv2.GaussianBlur(rng0.normal(0, 1, sh).astype(np.float32), (0, 0), s) * a
mott = cv2.resize(nz((H // 8, W // 8), 5, 20), (W, H)) * .012 + nz((H, W), .8, 2) * .01
PAPER = (np.array([228, 216, 189], np.float32) / 255)[None, None] * (1 + mott[..., None]) * np.clip(1.1 - (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * .9, .6, 1)[..., None]
DARK = np.zeros((H, W, 3), np.float32) + np.array([.035, .04, .04], np.float32); DARK += np.exp(-(((xx - W / 2) / 700) ** 2 + ((yy - 820) / 900) ** 2))[..., None] * np.array([.03, .05, .045], np.float32)
VIG = np.clip(1.15 - (((xx - W / 2) / W) ** 2 * 1.2 + ((yy - H * .45) / H) ** 2 * 1.4), .45, 1)[..., None].astype(np.float32)
INKN = np.clip(.82 + nz((H, W), 1.2, 2.4) * .08, .55, 1).astype(np.float32)
def ink_layer(img, L, col=INK, k=1.0):     # composite a PIL L mask as rough ink
    a = np.asarray(L).astype(np.float32) / 255
    a = np.clip((cv2.GaussianBlur(a, (0, 0), 1.0) - .3 + (INKN - .82)) * 1.8, 0, 1) * k
    return img * (1 - a[..., None]) + np.asarray(col, np.float32)[None, None] * a[..., None]
PAGES = {k: np.load(f"{P}page_{k}.npy") for k in ("e2", "e3")}
star = cv2.imread(f"{P}img/fp-1.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
STAR = (np.clip(star[..., None] * np.array([.95, .90, .79], np.float32) * 1.03, 0, 1) * 255).astype(np.uint8)
PH_ = {k: cv2.imread(f"{P}img/{k}.jpg", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255 for k in ("blast_cloud", "ruins_harbour")}
g = cv2.resize(cv2.GaussianBlur(rng0.normal(0, 1, (H // 4, 30)).astype(np.float32), (0, 0), sigmaX=1.2, sigmaY=5), (W, H))
DESK = np.stack([.10 + g * .02, .075 + g * .016, .055 + g * .012], -1).astype(np.float32)
LAMP = (.42 + .78 * np.exp(-(((xx - 520) / 760) ** 2 + ((yy - 640) / 980) ** 2)))[..., None] * np.array([1.06, 1.0, .9], np.float32)
ANCH = (540, 760)
def place(src, u, v, scale, ang):
    sh_, sw_ = src.shape[:2]; c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    A = np.float32([[scale * c, -scale * sn, 0], [scale * sn, scale * c, 0]]); tx, ty = u * sw_, v * sh_
    A[0, 2] = ANCH[0] - (A[0, 0] * tx + A[0, 1] * ty); A[1, 2] = ANCH[1] - (A[1, 0] * tx + A[1, 1] * ty); return A
def on_desk(src, A):
    sh_, sw_ = src.shape[:2]
    warped = cv2.warpAffine(src, A, (W, H), flags=cv2.INTER_AREA if A[0, 0] < 1 else cv2.INTER_LINEAR, borderValue=(0, 0, 0)).astype(np.float32) / 255
    m = cv2.warpAffine(np.ones((sh_ // 8, sw_ // 8), np.float32), np.float32([[A[0, 0] * 8, A[0, 1] * 8, A[0, 2]], [A[1, 0] * 8, A[1, 1] * 8, A[1, 2]]]), (W, H))
    shm = np.roll(np.roll(cv2.resize(cv2.GaussianBlur(cv2.resize(m, (W // 4, H // 4)), (0, 0), 8), (W, H)), 30, 0), 18, 1)
    out = DESK * (1 - .75 * shm[..., None]); out = out * (1 - m[..., None]) + warped * m[..., None]; out *= LAMP
    k = np.clip((np.abs(yy - ANCH[1]) - 360) / 900, 0, 1) ** 1.3; return out * (1 - k[..., None]) + cv2.GaussianBlur(out, (0, 0), 6) * k[..., None]
# ------------------------------------------------ the map (engraved, landscape canvas, filmed by a camera)
MW, MH = 2400, 1832
def mU(x, y): return (x * MW, y * MH)
def smooth(pts, n=14):
    Pp = np.array(pts, np.float32); out = []
    for i in range(len(Pp)):
        p0, p1, p2, p3 = Pp[i - 1], Pp[i], Pp[(i + 1) % len(Pp)], Pp[(i + 2) % len(Pp)]
        for tq in np.linspace(0, 1, n, endpoint=False): out.append(tuple(.5 * ((2 * p1) + (-p0 + p2) * tq + (2 * p0 - 5 * p1 + 4 * p2 - p3) * tq * tq + (-p0 + 3 * p1 - 3 * p2 + p3) * tq ** 3)))
    return out
WATER = smooth([mU(*p) for p in [(-.02, -.02), (.50, -.02), (.58, .10), (.52, .24), (.45, .32), (.47, .38), (.53, .45), (.60, .55), (.66, .68), (.76, .84), (.86, 1.02), (.40, 1.02), (.44, .86), (.46, .72), (.43, .60), (.36, .50), (.30, .43), (.27, .35), (.14, .30), (-.02, .24)]])
def build_map():
    yyy, xxx = np.mgrid[0:MH, 0:MW].astype(np.float32)
    base = (np.array([228, 216, 189], np.float32) / 255)[None, None] * (1 + cv2.resize(nz((MH // 8, MW // 8), 5, 20), (MW, MH))[..., None] * .012)
    L = Image.new("L", (MW, MH), 0); d = ImageDraw.Draw(L)
    wm = Image.new("L", (MW, MH), 0); ImageDraw.Draw(wm).polygon(WATER, fill=255); wa = np.asarray(wm) > 0
    lines = np.zeros((MH, MW), np.uint8); lines[(yyy.astype(int) % 11) < 3] = 255; lines[~wa] = 0
    L = Image.fromarray(np.maximum(np.asarray(L), lines)); d = ImageDraw.Draw(L)
    d.line(WATER + [WATER[0]], fill=255, width=6); d.line([(x + 12, y) for x, y in WATER], fill=255, width=2)
    for x0 in range(0, MW, 140): d.line([x0, 0, x0, MH], fill=60, width=1)
    for y0 in range(0, MH, 140): d.line([0, y0, MW, y0], fill=60, width=1)
    def lab(t, x, y, f):
        bb = d.textbbox((0, 0), t, font=f); w_, h_ = bb[2] - bb[0], bb[3] - bb[1]; X, Y = x * MW - w_ / 2, y * MH - h_ / 2
        d.rectangle([X - 14, Y - 6, X + w_ + 14, Y + h_ + 14], fill=0); d.text((X, Y - bb[1]), t, font=f, fill=255)
    lab("BEDFORD BASIN", .25, .10, F("ob", 64)); lab("THE NARROWS", .66, .29, F("oi", 56)); lab("HALIFAX", .15, .78, F("ob", 92)); lab("DARTMOUTH", .80, .55, F("ob", 76))
    lab("RICHMOND", .17, .50, F("os", 52)); lab("PIER 6", .37, .395, F("ob", 44)); lab("HARBOUR", .64, .93, F("oi", 56))
    img = ink_map(base, L); return img
def ink_map(base, L):
    a = np.asarray(L).astype(np.float32) / 255; a = np.clip(cv2.GaussianBlur(a, (0, 0), 1.0) * 1.25, 0, 1)
    return base * (1 - a[..., None] * .92) + INK[None, None] * a[..., None] * .92
MAPB = build_map()
P_IMO = [(.28, .12), (.40, .22), (.47, .33), (.50, .40)]; P_MB = [(.74, .92), (.64, .70), (.57, .52), (.50, .40)]; P_DRIFT = [(.50, .40), (.46, .42), (.40, .44)]
def along(path, u):
    pts = np.array(path); seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)]); s = u * cum[-1]
    i = min(np.searchsorted(cum, s) - 1, len(seg) - 1); i = max(i, 0); f = (s - cum[i]) / max(seg[i], 1e-6); p = pts[i] + (pts[i + 1] - pts[i]) * f
    ang = math.degrees(math.atan2((pts[i + 1][1] - pts[i][1]) * MH, (pts[i + 1][0] - pts[i][0]) * MW)); return p, ang
def ship(d, p, ang, col, fill, lab=None):
    x, y = p[0] * MW, p[1] * MH; c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(-46, -14), (30, -14), (58, 0), (30, 14), (-46, 14)]; d.polygon([(x + px * c - py * s, y + px * s + py * c) for px, py in pts], fill=fill, outline=col, width=5)
    if lab: d.text((x + 40, y - 80), lab, font=F("b7", 46), fill=col)
def burst(d, x, y, r, col, t):
    for k in range(16):
        a0 = k * math.pi / 8 + t * 2; rr = r * (1 + .25 * math.sin(t * 25 + k)); d.line([x + r * .35 * math.cos(a0), y + r * .35 * math.sin(a0), x + rr * math.cos(a0), y + rr * math.sin(a0)], fill=col, width=8)
    d.ellipse([x - r * .3, y - r * .3, x + r * .3, y + r * .3], fill=col)
def map_frame(mode, u, t):
    over = Image.new("RGBA", (MW, MH), (0, 0, 0, 0)); d = ImageDraw.Draw(over); red = REDI + (255,); ink = (22, 20, 18, 255)
    if mode == "ships":
        uu = ease(u) * .82
        for path, lab in ((P_IMO, "IMO"), (P_MB, "MONT-BLANC")):
            pts = [along(path, k / 40 * uu)[0] for k in range(41)]
            for k in range(0, 40, 2): d.line([mU(*pts[k]), mU(*pts[k + 1])], fill=ink, width=5)
            p, a = along(path, uu); ship(d, p, a, ink if lab == "IMO" else red, (240, 232, 210, 255) if lab == "IMO" else red, lab)
    elif mode == "collide":
        p = mU(.50, .40); ship(d, (.475, .375), 50, ink, (240, 232, 210, 255)); ship(d, (.51, .425), -130, red, red)
        if u < .25: f_ = 1 - u / .25; d.ellipse([p[0] - 260 * f_, p[1] - 260 * f_, p[0] + 260 * f_, p[1] + 260 * f_], outline=red, width=10)
        burst(d, p[0] + 20, p[1] + 20, 70, (230, 90, 20, 255), t); d.text((p[0] + 120, p[1] - 30), "COLLISION · c. 8.45", font=F("b7", 52), fill=red)
    elif mode == "drift":
        uu = sm(u); pp, a = along(P_DRIFT, uu)
        for k in range(0, 20, 2): q0 = along(P_DRIFT, k / 20)[0]; q1 = along(P_DRIFT, (k + 1) / 20)[0]; d.line([mU(*q0), mU(*q1)], fill=red, width=5)
        ship(d, pp, 160, red, red); x, y = mU(*pp); burst(d, x, y - 10, 60, (230, 90, 20, 255), t)
        for k in range(14):                                     # crowd on the hillside
            cx, cy = mU(.30 + (k % 7) * .012, .47 + (k // 7) * .02); d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=ink)
        d.text(mU(.24, .53), "CROWDS WATCH", font=F("b7", 46), fill=ink)
    elif mode == "blast":
        p = mU(.40, .44); R = .25 * MW * ease(u * 1.3)
        for k in range(3):
            rr = R * (1 - k * .12)
            if rr > 0: d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], outline=red, width=12 - k * 3)
        if u > .5:
            a8 = int(255 * ease((u - .5) / .3)); d.text((p[0] - 200, p[1] + .25 * MW + 30), "800 METRES", font=F("b7", 72), fill=REDI + (a8,))
        d.line([p[0] - 30, p[1] - 30, p[0] + 30, p[1] + 30], fill=red, width=12); d.line([p[0] - 30, p[1] + 30, p[0] + 30, p[1] - 30], fill=red, width=12)
    base = (MAPB * 255).astype(np.uint8); ov = np.asarray(over).astype(np.float32) / 255
    img = base.astype(np.float32) / 255 * (1 - ov[..., 3:]) + ov[..., :3] * ov[..., 3:]
    if mode == "blast" and u < .12: img = img * (1 - (1 - u / .12)) + (1 - u / .12)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)
# ------------------------------------------------ the moving illustration (engraving style)
def illus(var, u, t):
    img = PAPER.copy() * .97
    L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    hz = 1020
    for yv in range(160, hz, 9):                       # sky: sparse horizontal engraving lines, denser low
        if (yv // 9) % (2 if yv > 700 else 3) == 0: d.line([0, yv, W, yv], fill=70, width=1)
    for k, yv in enumerate(range(hz, H, 13)):          # sea: moving wave strokes
        off = int((t * 40 + k * 37) % 80)
        for x0 in range(-80 + off, W, 80): d.line([x0, yv + 3 * math.sin(x0 * .02 + t * 2 + k), x0 + 52, yv + 3 * math.sin((x0 + 52) * .02 + t * 2 + k)], fill=200, width=2)
    # far shore: Halifax hill with houses and a watching crowd
    shore = [(0, 860), (180, 850), (360, 880), (520, 910), (700, 930), (1080, 950), (1080, hz), (0, hz)]
    d.polygon(shore, fill=150)
    for k in range(26):
        x0 = 20 + k * 41; hgt = 26 + (k * 7) % 22; y0 = 860 + int(k * 3.2)
        d.rectangle([x0, y0 - hgt, x0 + 30, y0], fill=235); d.polygon([(x0 - 3, y0 - hgt), (x0 + 15, y0 - hgt - 16), (x0 + 33, y0 - hgt)], fill=235)
    if var == "crowd":
        for k in range(60):
            x0 = 60 + k * 15 + (k % 3) * 4; y0 = 905 + (k % 4) * 4 + int(k * .9); d.ellipse([x0 - 4, y0 - 22, x0 + 4, y0 - 14], fill=255); d.rectangle([x0 - 4, y0 - 14, x0 + 4, y0], fill=255)
    # the ship, drifting slowly
    sx = 620 - 60 * u if var == "crew" else 520 - 90 * u; sy = 1120
    hull = [(sx - 330, sy - 55), (sx + 320, sy - 55), (sx + 270, sy + 50), (sx - 290, sy + 50)]; d.polygon(hull, fill=255)
    d.rectangle([sx - 150, sy - 140, sx + 50, sy - 55], fill=255); d.rectangle([sx - 40, sy - 240, sx + 5, sy - 140], fill=255)
    for mx_ in (sx - 240, sx + 190): d.line([mx_, sy - 55, mx_, sy - 420], fill=255, width=9)
    for mx_ in (sx - 240, sx + 190): d.line([mx_, sy - 400, mx_ + 150, sy - 55], fill=255, width=2); d.line([mx_, sy - 400, mx_ - 150, sy - 55], fill=255, width=2)
    # smoke: a rising, drifting column of soft blobs, drawn as dark ink
    sm_ = Image.new("L", (W, H), 0); ds = ImageDraw.Draw(sm_); rs = np.random.default_rng(3)
    for k in range(260):
        ph = (k / 260 + t * .10) % 1.0; r = 40 + ph * 230; x0 = sx + 100 + ph * 300 + 60 * math.sin(k * 1.7 + t * .8) + 40 * math.sin(k * .37); y0 = sy - 70 - ph * 980
        ds.ellipse([x0 - r, y0 - r * .8, x0 + r, y0 + r * .8], fill=int(170 * (1 - ph) + 60))
    sma = np.maximum.reduce([cv2.GaussianBlur(np.asarray(sm_).astype(np.float32), (0, 0), 10)]); hatch = ((xx + yy * .6) % 7 < 3).astype(np.float32)
    smoke = np.clip(sma / 255 * 1.35 * (.72 + .28 * hatch), 0, .96)
    # flames on deck: red spot colour, flickering
    for k in range(9):
        fx = sx + 60 + k * 26; fh = 70 + 60 * abs(math.sin(t * 13 + k * 1.3)); dr.polygon([(fx - 16, sy - 55), (fx + 4 * math.sin(t * 9 + k), sy - 55 - fh), (fx + 16, sy - 55)], fill=255)
    if var == "crew":                                  # lifeboat pulling away toward the viewer's left
        bx = sx - 330 - 260 * ease(u); by = 1250 + 40 * u; d.polygon([(bx - 70, by - 12), (bx + 70, by - 12), (bx + 50, by + 14), (bx - 50, by + 14)], fill=255)
        for k in range(4):
            ox = bx - 45 + k * 30; ang = math.sin(t * 6 + k) * .5; d.line([ox, by - 10, ox - 60 * math.cos(ang), by + 30], fill=255, width=4); d.ellipse([ox - 7, by - 34, ox + 7, by - 20], fill=255)
    img = img * (1 - smoke[..., None] * .92) + INK[None, None] * smoke[..., None] * .92
    img = ink_layer(img, L); img = ink_layer(img, R, np.array([.80, .26, .07], np.float32), .95)
    return img
# ------------------------------------------------ the other shot types
def slam_paper(p, lt, t):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); u = ease(lt / .16); sc = 1.12 - .12 * u
    y = 640
    if p.get("kicker"): tw = d.textlength(p["kicker"], font=F("ob", 34)); d.text(((W - tw) / 2, 520), p["kicker"], font=F("ob", 34), fill=255); d.rectangle([90, 580, W - 90, 584], fill=255)
    for txt, fn, sz, wgt in p["lines"]:
        f = F(fn, int(sz * sc), wgt)
        while d.textlength(txt, font=f) > W - 110: sz -= 8; f = F(fn, int(sz * sc), wgt)
        bb = d.textbbox((0, 0), txt, font=f); d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y - bb[1]), txt, font=f, fill=255); y += (bb[3] - bb[1]) + 34
    d.rectangle([90, y + 6, W - 90, y + 10], fill=255)
    img = ink_layer(img, L)
    if p.get("stamp") and lt > .35:
        uu = ease((lt - .35) / .12); st = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(st); f = F("go", int(150 * (1.3 - .3 * uu)), 700); tw = sd.textlength(p["stamp"], font=f)
        sd.rounded_rectangle([(W - tw) / 2 - 40, 1180, (W + tw) / 2 + 40, 1400], 20, outline=255, width=14); sd.text(((W - tw) / 2, 1190), p["stamp"], font=f, fill=255)
        st = st.rotate(-8, center=(W / 2, 1290)); img = ink_layer(img, st, np.array([.70, .12, .09], np.float32), .9 * uu)
    if lt < .2: k = (1 - lt / .2) * 18; img = cv2.warpAffine(img, np.float32([[1, 0, k * math.sin(lt * 80)], [0, 1, k * math.cos(lt * 70)]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return img
def clock_img(sec, lab, glow_col=GRN, flick=1.0):
    img = DARK.copy(); s_ = f"{int(sec) // 3600:02d}:{int(sec) % 3600 // 60:02d}:{int(sec) % 60:02d}"
    w, h, th, gap, cw = 104, 196, 26, 22, 40; tw = width(s_, w, gap, cw); x0 = (W - tw) / 2
    gl, _ = word((W, H), "88:88:88", x0, 680, w, h, th, gap, cw); _, lt = word((W, H), s_, x0, 680, w, h, th, gap, cw)
    a = np.asarray(lt).astype(np.float32) / 255; m = a[..., 3:]
    g = np.asarray(gl).astype(np.float32) / 255; img = img * (1 - g[..., 3:] * .5) + g[..., :3] * g[..., 3:] * .5
    col = np.array(glow_col, np.float32) / 255 * flick; img = img * (1 - m) + col * m
    bl = cv2.GaussianBlur(m * col, (0, 0), 18) * 1.2 + cv2.GaussianBlur(m * col, (0, 0), 50) * .8; img = img + bl
    return img, s_
def photo_full(p, lt, dur):
    im = PH_[p["k"]]; ih, iw = im.shape; u = np.clip(lt / max(dur, .1), 0, 1); z = p["z0"] + (p["z1"] - p["z0"]) * sm(u)
    s = max(W / iw, H * .78 / ih) * z; cx, cy = p["c"]; Mx = np.float32([[s, 0, W / 2 - cx * iw * s], [0, s, H * .42 - cy * ih * s]])
    if p.get("shake") and lt < .5: k = (1 - lt / .5) * 30; Mx[0, 2] += k * math.sin(lt * 90); Mx[1, 2] += k * math.cos(lt * 70)
    g = cv2.warpAffine(im, Mx, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    img = np.clip((g - .03) * 1.08, 0, 1)[..., None] * np.array([.97, .94, .86], np.float32)
    img *= np.clip(1.0 - ((yy - H * .42) / (H * .75)) ** 2 * .9, .2, 1)[..., None]
    if p.get("shake"): f_ = max(0, 1 - lt / .35); img = img * (1 - f_) + f_
    return img
def cards(lt):
    img = DARK.copy(); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k, (nm, ctry, lines, flag) in enumerate((("IMO", "NORWAY", ["OUTBOUND FOR NEW YORK", "BELGIAN RELIEF CHARTER"], "no"), ("MONT-BLANC", "FRANCE", ["INBOUND TO BEDFORD BASIN", "CARGO: EXPLOSIVES"], "fr"))):
        u = ease((lt - k * .25) / .3); y0 = 330 + k * 640; x0 = (-W if k == 0 else W) * (1 - u) + 70
        col = (240, 232, 210, 255) if k == 0 else REDI + (255,)
        d.rounded_rectangle([x0, y0, x0 + W - 140, y0 + 560], 30, fill=(20, 22, 22, 240), outline=col, width=4)
        fx, fy = x0 + 50, y0 + 50
        if flag == "fr":
            for j, c_ in enumerate(((0, 50, 140), (240, 240, 240), (200, 20, 30))): d.rectangle([fx + j * 70, fy, fx + j * 70 + 70, fy + 140], fill=c_ + (255,))
        else:
            d.rectangle([fx, fy, fx + 210, fy + 140], fill=(186, 12, 47, 255)); d.rectangle([fx + 56, fy, fx + 86, fy + 140], fill=(255, 255, 255, 255)); d.rectangle([fx, fy + 55, fx + 210, fy + 85], fill=(255, 255, 255, 255))
            d.rectangle([fx + 63, fy, fx + 79, fy + 140], fill=(0, 32, 91, 255)); d.rectangle([fx, fy + 62, fx + 210, fy + 78], fill=(0, 32, 91, 255))
        d.text((fx + 250, fy - 6), nm, font=F("bb", 150), fill=col); d.text((fx + 254, fy + 140), ctry, font=F("b6", 44), fill=(255, 255, 255, 200))
        for j, ln in enumerate(lines): d.text((fx, fy + 250 + j * 80), ln, font=F("b7", 64), fill=(255, 255, 255, 235) if not ln.startswith("CARGO") else REDI + (255,))
    a = np.asarray(lay).astype(np.float32) / 255; return img * (1 - a[..., 3:]) + a[..., :3] * a[..., 3:]
def cargo(lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    d.text((W / 2, 300), "ABOARD MONT-BLANC", font=F("ob", 56), fill=255, anchor="mm"); d.rectangle([140, 350, W - 140, 354], fill=255)
    for k, w_ in enumerate(("PICRIC ACID", "TNT", "GUNCOTTON", "BENZOL")):
        tk = k * .32
        if lt >= tk:
            u = ease((lt - tk) / .1); f = F("go", int(170 * (1.25 - .25 * u)), 700); (dr if w_ == "BENZOL" else d).text((W / 2, 500 + k * 230), w_, font=f, fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, np.array([.70, .12, .09], np.float32))
    if lt >= 1.28: d2 = ImageDraw.Draw(L)
    return img
def ticker(lt):
    img = DESK * LAMP * 1.1; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    msg = "HALIFAX N.S. DEC 6 VIA HAVANA -- HUNDREDS OF PERSONS WERE KILLED AND A THOUSAND OTHERS INJURED"
    k = int(lt * 34); shown = msg[:k]; f = F("m5", 70); tw = d.textlength(shown, font=f)
    x0 = min(80, W - 160 - tw); d.rectangle([-10, 760, W + 10, 900], fill=(232, 222, 196, 255)); d.line([-10, 760, W + 10, 760], fill=(160, 150, 130, 255), width=3); d.line([-10, 900, W + 10, 900], fill=(160, 150, 130, 255), width=3)
    for j in range(0, W + 60, 34): d.ellipse([j - 5, 775, j + 5, 785], fill=(190, 180, 158, 255))
    d.text((x0, 800), shown + ("_" if int(lt * 6) % 2 == 0 else ""), font=f, fill=(28, 24, 20, 255))
    d.text((W / 2, 640), "WIRE · 6 DECEMBER 1917", font=F("b6", 40), fill=AMB + (255,), anchor="mm")
    d.text((W / 2, 980), "As printed by The Evening Star, Washington, that afternoon", font=F("b6", 32), fill=(255, 255, 255, 170), anchor="mm")
    a = np.asarray(lay).astype(np.float32) / 255; return img * (1 - a[..., 3:]) + a[..., :3] * a[..., 3:]
SB = (236, 817, 627, 851)       # "Said to Be on American Vessel" on the real page (pixels)
def star_frame(p, lt, dur):
    u = sm(np.clip(lt / max(dur, .1), 0, 1)); c0, c1 = p["c0"], p["c1"]; cam = [c0[k] + (c1[k] - c0[k]) * u for k in range(3)]
    sh_, sw_ = STAR.shape[:2]; A = place(STAR, cam[0], cam[1], cam[2] * W / sw_, -1.0); img = on_desk(STAR, A)
    if p.get("mark"):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        pts = np.array([[SB[0] - 30, SB[1] - 24], [SB[2] + 30, SB[3] + 24]], np.float32); q = (A[:, :2] @ pts.T).T + A[:, 2]
        (x0, y0), (x1, y1) = q; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 30, (y1 - y0) / 2 + 30
        prog = 1.0 if p.get("stamp") else ease(lt / .7); n = int(80 * prog)
        pts_ = [(cx + rx * math.cos(-2.6 + k / 80 * 2 * math.pi * 1.08), cy + ry * math.sin(-2.6 + k / 80 * 2 * math.pi * 1.08)) for k in range(n + 1)]
        if len(pts_) > 1: d.line(pts_, fill=(200, 30, 24, 235), width=14, joint="curve")
        if p.get("stamp") and lt > .15:
            uu = ease((lt - .15) / .12); f = F("go", int(190 * (1.3 - .3 * uu)), 700); st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); tw = sd.textlength("FRENCH.", font=f)
            sd.rounded_rectangle([(W - tw) / 2 - 40, 1060, (W + tw) / 2 + 40, 1310], 22, outline=(200, 30, 24, int(240 * uu)), width=16); sd.text(((W - tw) / 2, 1070), "FRENCH.", font=f, fill=(200, 30, 24, int(240 * uu)))
            lay.alpha_composite(st.rotate(-7, center=(W / 2, 1185)))
        a = np.asarray(lay).astype(np.float32) / 255; img = img * (1 - a[..., 3:]) + a[..., :3] * a[..., 3:]
    return img
def counter(lt):
    img = PAPER.copy(); L = Image.new("L", (W, H), 0); d = ImageDraw.Draw(L); R = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(R)
    v = int(1782 * ease(lt / 1.4)); dr.text((W / 2, 760), f"{v:,}", font=F("go", 330, 700), fill=255, anchor="mm")
    d.text((W / 2, 1000), "PEOPLE KILLED, AT LEAST", font=F("ob", 64), fill=255, anchor="mm"); d.text((W / 2, 1080), "As later counted. Estimates vary; 1,782 is the figure most often cited.", font=F("oi", 30), fill=255, anchor="mm")
    img = ink_layer(img, L); img = ink_layer(img, R, np.array([.70, .12, .09], np.float32)); return img
# ------------------------------------------------ frame
def frame(n):
    t = n / FPS; si = max([k for k in range(len(SHOTS)) if t >= SHOTS[k][0]] or [0]); t0, kind, p = SHOTS[si]; t1 = SHOTS[si + 1][0] if si + 1 < len(SHOTS) else DUR; lt = t - t0; dur = t1 - t0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); chip = None
    if kind == "slam_paper": img = slam_paper(p, lt, t)
    elif kind == "clock":
        img, s_ = clock_img(p["v"] + lt * 0, p["lab"]); d.text((W / 2, 600), p["lab"], font=F("b6", 40), fill=(170, 210, 190, 255), anchor="mm")
    elif kind == "rewind":
        u = sm(lt / 1.3); sec = p["a"] + (p["b"] - p["a"]) * u; img, s_ = clock_img(sec, "", AMB if u < 1 else GRN); d.text((W / 2, 600), p["lab"], font=F("b6", 44), fill=AMB + (255,), anchor="mm")
        if u < 1: img = cv2.filter2D(img, -1, np.ones((9, 1), np.float32) / 9)
    elif kind == "clock_tick":
        tt_ = T_FLASH - t; sec = 9 * 3600 + 4 * 60 + 35 - max(0, math.ceil(tt_ / .42 - 1e-6)); img, s_ = clock_img(sec, "", GRN if sec < 9 * 3600 + 4 * 60 + 35 else (255, 255, 255))
        d.text((W / 2, 600), p["lab"], font=F("b6", 40), fill=(170, 210, 190, 255), anchor="mm")
        k = (math.sin((T_FLASH - t) / .42 * math.pi * 2) * .5 + .5) ** 8; img = img * (1 + .25 * k)
    elif kind == "photo":
        img = photo_full(p, lt, dur); a8 = int(255 * ease((lt - .3) / .4))
        d.rounded_rectangle([60, 1250, W - 60, 1380], 18, fill=(0, 0, 0, int(a8 * .65))); d.text((W / 2, 1296), p["cap"], font=F("b7", 48), fill=AMB + (a8,), anchor="mm"); d.text((W / 2, 1348), "PHOTOGRAPH · " + p["src"], font=F("b6", 28), fill=(255, 255, 255, int(a8 * .75)), anchor="mm")
    elif kind == "page":
        u = sm(np.clip(lt / max(dur, .1), 0, 1)); c0, c1 = p["c0"], p["c1"]; cam = [c0[k] + (c1[k] - c0[k]) * u for k in range(4)]
        pg = PAGES[p["k"]]; img = on_desk(pg, place(pg, cam[0], cam[1], cam[2] / pg.shape[1], cam[3]))
    elif kind == "map":
        u = np.clip(lt / max(dur, .1), 0, 1); mp = map_frame(p["mode"], u, t).astype(np.float32) / 255; c0, c1 = p["c0"], p["c1"]; uu = sm(u); cu = [c0[k] + (c1[k] - c0[k]) * uu for k in range(3)]
        s = cu[2]; Mx = np.float32([[s, 0, W / 2 - cu[0] * MW * s], [0, s, 820 - cu[1] * MH * s]]); img = cv2.warpAffine(mp, Mx, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        lab = {"ships": "07:30 · TWO SHIPS, ONE CHANNEL", "collide": "c. 08:45 · COLLISION", "drift": "08:45 - 09:04 · ADRIFT AND BURNING", "blast": "09:04:35 · HALF A MILE"}[p["mode"]]
        d.rounded_rectangle([50, 230, 50 + d.textlength(lab, font=F("b7", 46)) + 50, 300], 14, fill=(20, 18, 16, 220)); d.text((75, 238), lab, font=F("b7", 46), fill=AMB + (255,))
        d.text((W - 60, 1230), "MAP: DIAGRAM, NOT TO SCALE", font=F("b6", 26), fill=(40, 34, 28, 200), anchor="ra")
        if p["mode"] == "drift":
            mins = 20 * (1 - sm(u)); txt = f"{int(mins):02d}:{int((mins % 1) * 60):02d}"; d.rounded_rectangle([W / 2 - 250, 1210, W / 2 + 250, 1380], 22, fill=(16, 14, 12, 230))
            d.text((W / 2, 1250), "MINUTES TO 9.04", font=F("b6", 34), fill=AMB + (255,), anchor="mm"); d.text((W / 2, 1325), txt, font=F("m5", 92), fill=(255, 110, 80, 255), anchor="mm")
    elif kind == "illus":
        img = illus(p["var"], np.clip(lt / max(dur, .1), 0, 1), t); d.rounded_rectangle([W - 330, 230, W - 50, 290], 12, fill=(20, 18, 16, 200)); d.text((W - 190, 260), "ILLUSTRATION", font=F("b7", 38), fill=(255, 255, 255, 230), anchor="mm")
    elif kind == "cards": img = cards(lt)
    elif kind == "cargo": img = cargo(lt)
    elif kind == "ticker": img = ticker(lt)
    elif kind == "star": img = star_frame(p, lt, dur)
    elif kind == "counter": img = counter(lt)
    else:
        img = DARK.copy() * .6; a8 = int(255 * ease((lt - D[11] * .4) / .5))
        d.text((W / 2, 820), "ELAPSED", font=F("bb", 190), fill=(255, 255, 255, a8), anchor="mm"); d.text((W / 2, 950), "EVERY SECOND IS ON THE RECORD", font=F("b6", 40), fill=(255, 255, 255, int(a8 * .85)), anchor="mm")
        d.text((W / 2, 1010), "THE ELAPSED RECORD AND ILLUSTRATIONS ARE RECONSTRUCTIONS", font=F("b6", 24), fill=(255, 255, 255, int(a8 * .55)), anchor="mm")
    # brand mark
    if kind != "end": d.text((W - 56, 92), "ELAPSED", font=F("bb", 64), fill=(255, 255, 255, 235), anchor="ra")
    # cut accents: 2-frame flash on hard cuts into slams; short whip on others
    if si > 0 and lt < 2 / FPS and kind in ("slam_paper", "cargo", "counter"): img = img * .6 + .4
    elif si > 0 and lt < .12: kk = int(50 * (1 - lt / .12)) | 1; img = cv2.filter2D(img, -1, np.ones((1, kk), np.float32) / kk)
    # captions
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
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", f"{O}{name}.part.mp4"], stdin=subprocess.PIPE)
    for n in range(a, b_): pr.stdin.write(frame(n).tobytes())
    pr.stdin.close(); pr.wait(); os.rename(f"{O}{name}.part.mp4", f"{O}{name}.mp4")
