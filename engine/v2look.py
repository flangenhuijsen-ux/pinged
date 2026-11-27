"""PINGED look v2 — applied on top of a generated lock.py (gen.py calls apply_file).
Frosted-glass cards with shadow and rim light, drawn app icons, glowing numbers,
a hook card inside the first half second, a ticking clock, word-by-word captions,
and the source line moved out of YouTube's bottom overlay. Timing, voice and music stay as built."""
import json


def apply(s, cfg):
    def R(a, b, cnt=1):
        nonlocal s
        assert s.count(a) >= 1, "v2look: missing " + a[:70]
        s = s.replace(a, b) if cnt == 0 else s.replace(a, b, cnt)

    hook = cfg.get("hook")
    hl = cfg.get("hl", [None] * len(cfg["vo"]))
    # ---- hook (standard since 27 Nov): the hook card is fully visible from frame 0 (feed shows frame 0);
    #      its sound lands at 0.35 s with a small shake, and it pulses again at its original moment
    R("T_Q = VSTART[7]; T_H = VSTART[8]\n",
      "T_Q = VSTART[7]; T_H = VSTART[8]\n"
      f"HOOK = {repr(hook)}; T_PULSE = None\n"
      "if HOOK: T_PULSE = globals()['T_' + HOOK]; globals()['T_' + HOOK] = -0.3\n")
    # ---- timeline for the sound: the hook card is on screen from frame 0, its sound still lands at 0.35 s
    import re as _re
    m_ = _re.search(r'json\.dump\((\{"VSTART": VSTART, "DUR": DUR, "T": dict\(.*?\)\}), open\(O \+ "tl\.json", "w"\)\)\n', s)
    assert m_, "v2look: tl.json dump not found"
    s = s[:m_.start()] + "_TL = " + m_.group(1) + "\nif HOOK: _TL['T'][HOOK] = 0.35\njson.dump(_TL, open(O + \"tl.json\", \"w\"))\n" + s[m_.end():]
    # ---- clock ticks through every minute instead of jumping near each key
    a = s.index("def clock_at(t):"); b = s.index("MOOD = ")
    s = s[:a] + '''def clock_at(t):
    for (t0, m0), (t1, m1) in zip(CLOCK, CLOCK[1:]):
        if t <= t1:
            return m0 + (m1 - m0) * (t - t0) / max(1e-6, t1 - t0)
    return CLOCK[-1][1]


def clock_rate(t):
    for (t0, m0), (t1, m1) in zip(CLOCK, CLOCK[1:]):
        if t <= t1: return (m1 - m0) / max(1e-6, t1 - t0)
    return 0.0


''' + s[b:]
    # ---- wallpaper a touch darker so glass and type carry the contrast
    R("    return cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)",
      "    return cv2.resize(img * 0.88, (W, H), interpolation=cv2.INTER_CUBIC)")
    # ---- glass card body
    a = s.index("def card_base("); b = s.index("def icon(")
    s = s[:a] + '''def card_base(h, tint=(255, 255, 255), fill_a=30, border_a=70, radius=46):
    g = np.linspace(1.0, 0.42, h)[:, None]
    body = np.zeros((h, CW, 4), np.uint8); body[..., :3] = tint; body[..., 3] = np.clip((fill_a * 0.9 + 14) * g, 0, 255)
    m = Image.new("L", (CW, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, CW - 1, h - 1], radius=radius, fill=255)
    im = Image.fromarray(body, "RGBA"); im.putalpha(Image.fromarray((np.asarray(im.getchannel("A")).astype(np.float32) * np.asarray(m) / 255).astype(np.uint8)))
    rim = Image.new("RGBA", (CW, h), (0, 0, 0, 0)); ImageDraw.Draw(rim).rounded_rectangle([1, 1, CW - 2, h - 2], radius=radius, outline=tint + (min(255, border_a + 70),), width=3)
    ra = np.asarray(rim.getchannel("A")).astype(np.float32) * np.linspace(1.0, 0.22, h)[:, None]
    rim.putalpha(Image.fromarray(ra.astype(np.uint8))); im.alpha_composite(rim)
    return im, ImageDraw.Draw(im)


''' + s[b:]
    # ---- drawn icons
    a = s.index("def icon("); b = s.index("def std_card(")
    s = s[:a] + '''def icon(d, x, y, letter, col):
    s_ = 104; gr = np.linspace(1.16, 0.78, s_)[:, None, None] * np.array(col, np.float32)
    body = Image.fromarray(np.clip(np.broadcast_to(gr, (s_, s_, 3)), 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (s_, s_), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s_ - 1, s_ - 1], 28, fill=255); body.putalpha(m)
    e = ImageDraw.Draw(body); ink = (12, 16, 22, 240)
    if letter == "M":
        pts = [(22, 70), (40, 54), (55, 62), (82, 32)] if col[1] > col[0] else [(22, 34), (40, 50), (55, 42), (82, 72)]
        e.line(pts, fill=ink, width=9, joint="curve"); e.ellipse([pts[-1][0] - 9, pts[-1][1] - 9, pts[-1][0] + 9, pts[-1][1] + 9], fill=ink)
    elif letter == "N":
        e.rounded_rectangle([22, 26, 82, 42], 4, fill=ink); e.rounded_rectangle([22, 52, 82, 60], 4, fill=ink); e.rounded_rectangle([22, 70, 62, 78], 4, fill=ink)
    else:
        e.text((52, 54), letter, font=F("b7", 80), fill=ink, anchor="mm")
    e.rounded_rectangle([1, 1, s_ - 2, s_ - 2], 28, outline=(255, 255, 255, 80), width=2)
    d._image.alpha_composite(body, (int(x), int(y)))


''' + s[b:]
    # ---- glow behind the big number
    R("        d.text((CW - 40, 186), big, font=fb, fill=bigcol + (255,), anchor=\"rm\")",
      "        gl_ = Image.new(\"RGBA\", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl_).text((CW - 40, 186), big, font=fb, fill=bigcol + (150,), anchor=\"rm\")\n"
      "        im.alpha_composite(gl_.filter(ImageFilter.GaussianBlur(16))); d = ImageDraw.Draw(im)\n"
      "        d.text((CW - 40, 186), big, font=fb, fill=bigcol + (255,), anchor=\"rm\")")
    # ---- glass blit: blurred, lifted background under the card plus a soft drop shadow
    R("def blit(img, card, x, y, sc, alpha):", '''_gm = {}


def glass_mask(w, h, r):
    k = (w, h, r)
    if k not in _gm:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
        sh = Image.new("L", (w + 160, h + 160), 0); ImageDraw.Draw(sh).rounded_rectangle([88, 104, w + 72, h + 96], radius=r, fill=255)
        _gm[k] = (np.asarray(m).astype(np.float32)[..., None] / 255, np.asarray(sh.filter(ImageFilter.GaussianBlur(30))).astype(np.float32)[..., None] / 255)
        if len(_gm) > 300: _gm.pop(next(iter(_gm)))
    return _gm[k]


def glass(img, x, y, w, h, r, alpha):
    m, sh = glass_mask(w, h, r); x, y = int(round(x)), int(round(y))
    X0, Y0 = x - 80, y - 80
    a0, b0, a1, b1 = max(0, X0), max(0, Y0), min(W, X0 + w + 160), min(H, Y0 + h + 160)
    if a1 > a0 and b1 > b0: img[b0:b1, a0:a1] *= 1 - 0.5 * alpha * sh[b0 - Y0:b1 - Y0, a0 - X0:a1 - X0]
    a0, b0, a1, b1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if a1 <= a0 or b1 <= b0: return
    reg = img[b0:b1, a0:a1]; hh, ww = reg.shape[:2]
    bl = cv2.resize(cv2.GaussianBlur(cv2.resize(reg, (max(2, ww // 8), max(2, hh // 8)), interpolation=cv2.INTER_AREA), (0, 0), 2.2), (ww, hh), interpolation=cv2.INTER_LINEAR)
    bl = bl * 1.14 + 0.045 + np.linspace(0.05, -0.01, hh)[:, None, None]
    mm = m[b0 - y:b1 - y, a0 - x:a1 - x] * alpha
    img[b0:b1, a0:a1] = reg * (1 - mm) + bl * mm


def blit(img, card, x, y, sc, alpha):''')
    R("    x, y = int(round(x)), int(round(y))\n    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)",
      "    x, y = int(round(x)), int(round(y))\n    if GLASS_R: glass(img, x, y, w, h, int(GLASS_R * sc), alpha)\n    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)")
    R("STACK_Y = 640", "GLASS_R = 0\nCS = 0.84          # cards drawn at 84%: room for captions above YouTube's overlay\nSTACK_LIMIT = 1330\nSTACK_Y = 640")
    # ---- extra buzz for the pulse; captions setup
    R("\n\ndef frame(i):", f'''
if HOOK: BUZZ.append((T_PULSE, 7)); BUZZ.append((0.35, 9))
VO = {json.dumps(cfg["vo"])}
HL = json.loads({json.dumps(json.dumps(hl))})
FCAP = F("b7", 76)


def captions(t):
    for i in range(len(VO)):
        if VSTART[i] <= t < VSTART[i] + VD[i] + 0.3:
            ws = VO[i].split(); L = [len(w) + 1 for w in ws]; tot = sum(L)
            starts = [VSTART[i] + VD[i] * sum(L[:k]) / tot for k in range(len(ws))]
            lay = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); rows = [[]]
            for k, w in enumerate(ws):
                if d.textlength(" ".join(x for x, _ in rows[-1] + [(w, k)]), font=FCAP) > 920: rows.append([])
                rows[-1].append((w, k))
            if len(rows) > 1 and len(rows[-1]) == 1 and len(rows[-2]) > 2: rows[-1].insert(0, rows[-2].pop())       # no lonely last word
            last = max([k for k in range(len(ws)) if t >= starts[k]] or [0])
            pg = [rows[j:j + 2] for j in range(0, len(rows), 2)]
            rows = next((p for p in pg if any(k == last for r in p for _, k in r)), pg[-1])
            hw = (HL[i] or [None, None])
            for r, row in enumerate(rows):
                x = (W - d.textlength(" ".join(w for w, _ in row), font=FCAP)) / 2
                for w, k in row:
                    u = t - starts[k]
                    if u >= 0:
                        p = float(ease(u / 0.12)); col = tuple(hw[1]) if hw[0] and w.strip(".,?!") == hw[0] else (255, 255, 255)
                        d.text((x, 34 + r * 92 + 12 * (1 - p)), w, font=FCAP, fill=col + (int(255 * (0.35 + 0.65 * p)),))
                    x += d.textlength(w + " ", font=FCAP)
            a = np.asarray(lay).astype(np.float32) / 255
            return a, cv2.GaussianBlur(a[..., 3], (0, 0), 9)[..., None]
    return None


def frame(i):''')
    # ---- no fade from black: frame 0 is the cover in the Shorts feed
    R("fade_in = float(smooth(t / 0.8))", "fade_in = 1.0")
    # ---- clock: per-digit drop on each minute change + glow in the mood colour
    R('''    cw = 150; x = W / 2 - (4 * cw + 70) / 2
    for ch in s:
        wd = 70 if ch == ":" else cw
        d.text((x + wd / 2, 400), ch, font=FCL, fill=(255, 255, 255, a8), anchor="mm"); x += wd''',
      '''    s = f"{hh_ % 24:02d}:{mm_:02d}"      # clocks that run past midnight keep counting forward
    rate = clock_rate(t); prev = int(mins) - 1; sp = f"{prev // 60 % 24:02d}:{prev % 60:02d}"
    since = (mins - int(mins)) / rate if rate > 0 else 9
    if t < 0.2: since = 9           # settled clock in frame 0
    cl = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); cd = ImageDraw.Draw(cl)
    cw = 150; x = W / 2 - (4 * cw + 70) / 2
    for j, ch in enumerate(s):
        wd = 70 if ch == ":" else cw
        p = float(ease(since / 0.16)) if (rate < 5 and ch != sp[j]) else 1.0
        cd.text((x + wd / 2, 400 - 34 * (1 - p)), ch, font=FCL, fill=(255, 255, 255, int(a8 * (0.25 + 0.75 * p))), anchor="mm"); x += wd
    m_ = key(MOOD, t); g_ = key(GOLD, t); pal_ = ((CALM * (1 - m_) + RED * m_) * (1 - g_) + GLD * g_).mean(0); pal_ = pal_ / pal_.max()
    ca = np.asarray(cl).astype(np.float32) / 255
    glow_ = cv2.resize(cv2.GaussianBlur(cv2.resize(ca[..., 3], (W // 4, 140)), (0, 0), 9), (W, 560))[..., None]
    ui.alpha_composite(cl)''')
    R('''    tracked(d, W / 2, H - 128, ''', '''    d.ellipse([W / 2 - 330, 603, W / 2 - 318, 615], fill=tuple(int(255 * c) for c in pal_) + (a8,))
    tracked(d, W / 2 - 306, 594, "PINGED", F("b7", 30), 6, "l", fill=(255, 255, 255, int(a8 * 0.85)))
    if False: tracked(d, W / 2, H - 128, ''')
    R('''F("m5", 27), 2, "m", fill=(255, 255, 255, int(a8 * 0.45)))''',
      '''F("m5", 27), 2, "m", fill=(255, 255, 255, int(a8 * 0.45)))
    fs_ = 22
    while fs_ > 14 and sum(d.textlength(c, font=F("m5", fs_)) + 1 for c in SRC_) > W - 40 - (W / 2 - 160): fs_ -= 1
    tracked(d, W / 2 - 160, 596 + (22 - fs_) // 2, SRC_, F("m5", fs_), 1, "l", fill=(255, 255, 255, int(a8 * 0.5)))''')
    R("    img = img * (1 - uia[..., 3:4]) + uia[..., :3] * uia[..., 3:4]",
      "    img = img * (1 - uia[..., 3:4]) + uia[..., :3] * uia[..., 3:4]\n    img[:560] += glow_ * pal_ * 0.42 * fade_in")
    # ---- stack: chronological order, scaled cards, glass, limit above captions, hook pulse
    R("    active = [k for k in ORDERC if t >= TIN[k]]", "    active = sorted([k for k in ORDERC if t >= TIN[k]], key=lambda k: TIN[k])")
    R("        fade = float(np.clip((1750 - (y + HGT[k])) / 130 + 1, 0, 1))\n        sc = 0.86 + 0.14 * min(ent, 1.08)\n        blit(img, card, CX0 + dx, y - 70 * (1 - min(ent, 1.0)) + dy, sc, float(smooth(age / 0.22)) * dim * fade)\n        y += (HGT[k] + GAP) * float(ease(age / 0.38))",
      "        fade = float(np.clip((STACK_LIMIT - (y + HGT[k] * CS)) / 110 + 1, 0, 1))\n"
      "        sc = (0.86 + 0.14 * min(ent, 1.08)) * CS\n"
      "        if HOOK and k == HOOK and 0 <= t - T_PULSE < 0.7: sc *= 1 + 0.06 * np.sin(np.pi * (t - T_PULSE) / 0.7)\n"
      "        globals()['GLASS_R'] = 56 if k == 'H' else 46\n"
      "        blit(img, card, CX0 + dx, y - HGT[k] * (1 - CS) / 2 - 70 * (1 - min(ent, 1.0)) + dy, sc, float(smooth(age / 0.22)) * dim * fade)\n"
      "        globals()['GLASS_R'] = 0\n"
      "        y += (HGT[k] * CS + GAP) * float(ease(age / 0.38))")
    R("msk = ((yy > STACK_Y) & (yy < STACK_Y + HH) & (xx > CX0) & (xx < CX0 + CW))[..., None]",
      "msk = ((yy > STACK_Y) & (yy < STACK_Y + HH * CS) & (xx > W / 2 - CW * CS / 2) & (xx < W / 2 + CW * CS / 2))[..., None]")
    # ---- captions on top of everything, before bloom
    R("    br = cv2.resize(np.clip(img - 0.78, 0, 1), (W // 4, H // 4))",
      "    cp = captions(t)\n"
      "    if cp is not None:\n"
      "        a_, s_ = cp; y0c = 1352\n"
      "        img[y0c:y0c + 330] *= 1 - 0.75 * s_\n"
      "        img[y0c:y0c + 330] = img[y0c:y0c + 330] * (1 - a_[..., 3:4]) + a_[..., :3] * a_[..., 3:4]\n"
      "    br = cv2.resize(np.clip(img - 0.78, 0, 1), (W // 4, H // 4))")
    # source text for the new line
    R("# ---------------- timeline ----------------", "SRC_ = " + json.dumps(cfg["src"]) + "\n# ---------------- timeline ----------------")
    return s


def apply_file(path, cfg, out=None):
    s = apply(open(path).read(), cfg)
    open(out or path, "w").write(s)
    return out or path
