import json, os, sys, importlib.util
R = (255, 92, 78); G = (96, 235, 140); A = (255, 196, 90); Wh = (255, 255, 255); N = (200, 205, 220); B = (110, 185, 255)
HM = lambda s: int(s[:2]) * 60 + int(s[3:])
def build(story):
    O = f"/home/claude/{story}/out/"; sp = importlib.util.spec_from_file_location("story", f"/home/claude/{story}/story.py"); st = importlib.util.module_from_spec(sp); sp.loader.exec_module(st)
    LINES = st.LINES; D = {}
    if os.path.exists(O + "d.json"): D = {int(k): v for k, v in json.load(open(O + "d.json")).items()}
    for i, l in enumerate(LINES):
        if not l["text"]: D[i] = l.get("dur", 2.0)
    V = []; t = 0.5
    for i, l in enumerate(LINES): V.append(t); t += D.get(i, 2.0) + l.get("gap", 0.55)
    DUR = round(t + 1.0, 2); D = {i: D.get(i, 2.0) for i in range(len(LINES))}
    o = dict(O=O, VO=[l["text"] for l in LINES], D=D, V=V, DUR=DUR, CARDS=[], CLEAR=[], DIMC=[], HID=[], UNLOCK=[], CLOCK=[], DATES=[], ROLL=[], ACC=[(0, B)], SLAM=[], REWS=[], GLITCH=[], LOG=[], LOGCLR=[], METER=[], SPARK=[], CUTS=[0], SPIN=[], FLIP=[], CLKTXT=[(0, None)])
    m = HM(st.CLOCK0); o["CLOCK"].append((0, m)); hid = None; spk = {}
    for i, l in enumerate(LINES):
        t0, d = V[i], D[i]; nx = V[i + 1] if i + 1 < len(LINES) else DUR
        if "acc" in l: o["ACC"].append((t0 + d * l.get("acc_u", 0), l["acc"]))
        for u, off, c in l.get("cards", []): o["CARDS"].append((t0 + d * u + off,) + tuple(c))
        if l.get("clear"): o["CLEAR"].append(t0 + .05)
        if l.get("cut") or l.get("clear"): o["CUTS"].append(t0)
        if "slam" not in l and l.get("emph") and d > 5.0: l["slam"] = (.66,) + tuple(l["emph"]) + (None,)
        if "slam" in l:
            u, tx, col, sub, cnt = l["slam"]; o["SLAM"].append((t0 + d * u, nx - .08, tx, col, sub, cnt))
        if "meter" in l:
            u, lab, val, col, sub, cnt = l["meter"]; o["METER"].append((t0 + d * u, lab, val, col, sub, cnt))
        if "log" in l:
            u, tag, tx, col = l["log"]; o["LOG"].append((t0 + d * u, tag, tx, col))
        for u, gd in l.get("glitch", []): o["GLITCH"].append((t0 + d * u, gd))
        if l.get("dim"): o["DIMC"].append((t0 + .1 * d, nx))
        if l.get("rewind"): o["REWS"].append((t0, t0 + d + .25)); o["LOGCLR"].append(t0 + .3); o["GLITCH"].append((t0, .35))
        if "roll" in l: o["ROLL"].append((t0 + .2, t0 + d * l["roll"][0], l["roll"][1], l["roll"][2]))
        h = l.get("hidden")
        if h:
            if h[0] == "show": hid = t0 + d * h[1]
            else:
                if hid is not None: o["HID"].append((hid, t0 + d * h[1])); hid = None
                if h[0] == "unlock": o["UNLOCK"].append(t0 + d * h[1])
        if "date" in l: o["DATES"].append((t0 + d * l.get("date_u", 0), l["date"]))
        for u, off, tx in l.get("dates", []): o["DATES"].append((t0 + d * u + off, tx)); o["FLIP"].append(t0 + d * u + off)
        if "clocktxt" in l: o["CLKTXT"].append((t0, l["clocktxt"]))
        if "clk" in l:
            o["CLKTXT"].append((t0, None))
            c = l["clk"]; tg = HM(c[0]); mode = c[1]; ue = c[2] if len(c) > 2 else 0; bk = c[3] if len(c) > 3 else 0
            if mode == "back":
                m2 = m - 3 * 1440; m2 -= (m2 - tg) % 1440; o["CLOCK"] += [(t0, m), (t0 + d, m2)]; o["SPIN"].append((t0, t0 + d))
            else:
                m2 = m + (2 * 1440 if mode == "long" else 0); m2 += (tg - m2) % 1440
                if mode == "fwd": o["CLOCK"] += [(t0, m), (t0 + .5, m2)]; o["SPIN"].append((t0, t0 + .5))
                elif mode == "slow": o["CLOCK"] += [(t0 + d * ue, m2)]
                elif mode == "long": ts = V[i - bk]; o["CLOCK"] += [(ts, m), (t0 + d * ue, m2)]; o["SPIN"].append((ts, t0 + d * ue))
            m = m2
        if "spark" in l:
            key, pts = l["spark"]; e = spk.setdefault(key, dict(ts=[], t0=t0))
            for j, (k, u) in enumerate(pts): e["ts"].append(t0 + d * u)
            e["last"] = i
    if hid is not None: o["HID"].append((hid, DUR + 9))
    for key, e in spk.items():
        vals, col, lab = st.SPK[key]; t1 = min([c for c in o["CLEAR"] if c > e["ts"][-1]] + [DUR]); o["SPARK"].append((e["t0"], t1, vals, e["ts"], col, lab))
    o["CLOCK"].append((DUR + 1, m)); o["CLOCK"].sort(key=lambda x: x[0]); o["DATES"].sort(); o["ACC"].sort(key=lambda x: x[0]); o["CARDS"].sort(key=lambda x: x[0]); o["CUTS"] = sorted(set(o["CUTS"])); o["METER"].sort(key=lambda x: x[0])
    for k_ in ("DATES", "METER"):
        if o[k_]: o[k_][0] = (0,) + tuple(o[k_][0][1:])
    o["HIDLAB"] = getattr(st, "HIDLAB", "KEEP WATCHING")
    json.dump(dict(DUR=DUR, V=V, n=len(LINES), has=[bool(l["text"]) for l in LINES], cards=[c[0] for c in o["CARDS"]], slam=[(s[0], s[5][2] if s[5] else 0) for s in o["SLAM"]], rew=o["REWS"], glitch=o["GLITCH"], clear=o["CLEAR"], hidden=[h[0] for h in o["HID"]], unlock=o["UNLOCK"], spin=o["SPIN"], dates=o["FLIP"]), open(O + "tl.json", "w"))
    return o
