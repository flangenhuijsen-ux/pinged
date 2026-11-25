import re, json, os, subprocess, sys
def build(name, cfg):
    root=f"/home/claude/{name}"; os.makedirs(root+"/src",exist_ok=True); os.makedirs(root+"/out",exist_ok=True)
    O=root+"/out/"
    # ---- voice
    v=open('/home/claude/lock2/src/vo.py').read().replace('/home/claude/lock2/out/',O)
    a=v.index('L=['); b=v.index('k=Kokoro'); v=v[:a]+"L="+json.dumps(cfg["vo"])+"\n"+v[b:]
    open(root+"/src/vo.py","w").write(v)
    # ---- renderer
    s=open('/home/claude/lock2/src/lock2.py').read()
    def R(a,b):
        nonlocal s
        assert a in s,a[:60]; s=s.replace(a,b)
    R('O = "/home/claude/lock2/out/"',f'O = "{O}"')
    a=s.index("# ---------------- timeline"); b=s.index("def clock_at")
    s=s[:a]+'''# ---------------- timeline ----------------
VD = json.load(open(O + "vo.json"))
VSTART = {}
t = 0.5
for i in range(10):
    VSTART[i] = round(t, 3); t += VD[i] + {6: 0.5, 7: 0.6, 8: 0.4}.get(i, 0.36)
DUR = round(t + 1.5, 2)
N = int(FPS * DUR)
V = VSTART
'''+cfg["cues"]+'''
T_Q = VSTART[7]; T_H = VSTART[8]
json.dump({"VSTART": VSTART, "DUR": DUR, "T": dict(A=T_A, B=T_B, BL=T_BL, C1=T_C1, C2=T_C2, C3=T_C3, D=T_D, F=T_F, G=T_G, E=T_E, Q=T_Q, H=T_H, P=T_P)}, open(O + "tl.json", "w"))
CLOCK = '''+cfg["clock"]+"\n\n\n"+s[b:]
    m=re.search(r"MOOD = \[.*?\]\n",s); s=s[:m.start()]+"MOOD = "+cfg["mood"]+"\n"+s[m.end():]
    m=re.search(r"RED = np.array\(.*?np.float32\)\n",s); s=s[:m.start()]+"RED = np.array("+cfg["pal"]+", np.float32)\n"+s[m.end():]
    a=s.index("CARDS = {"); b=s.index("FH = 520")
    s=s[:a]+cfg["cards"]+"\n"+s[b:]
    a=s.index("fnum = F(\"bebas\""); b=s.index("HH = 640")
    s=s[:a]+cfg["count"]+'''
fnum = F("bebas", 236)
_d = ImageDraw.Draw(Image.new("L", (8, 8)))
while _d.textlength(CNT_FMT(CNT_MAX), font=fnum) > CW - 90: fnum = F("bebas", fnum.size - 4)
_fc = {}


def card_F(t):
    v = CNT_MAX * float(ease((t - T_F - 0.25) / 2.0)); v = round(v / CNT_STEP) * CNT_STEP if v < CNT_MAX else CNT_MAX
    g = float(smooth((t - T_G) / 0.4))
    kkey = (int(v // CNT_STEP), round(g, 2))
    if kkey not in _fc:
        im, d = card_base(FH, tint=CNT_TINT, fill_a=46, border_a=170)
        icon(d, 34, 34, CNT_ICON[0], CNT_ICON[1])
        tracked(d, 164, 30, CNT_APP, F("b6", 50), 5, fill=(255, 255, 255, 200))
        d.text((CW - 40, 34), CNT_WHEN, font=F("m6", 44), fill=(255, 255, 255, 170), anchor="ra")
        tracked(d, 40, 150, CNT_LABEL, F("b6", 54), 6, fill=(255, 255, 255, 220))
        wfull = d.textlength(CNT_FMT(CNT_MAX), font=fnum)
        d.text((CW / 2 + wfull / 2, 330), CNT_FMT(v), font=fnum, fill=(255, 240, 234, 255), anchor="rm")
        if g > 0:
            fg = F("b7", 64)
            while d.textlength(CNT_SUB, font=fg) > CW - 70: fg = F("b7", fg.size - 2)
            d.text((CW / 2, 462), CNT_SUB, font=fg, fill=AMB8 + (int(255 * g),), anchor="mm")
        _fc[kkey] = np.asarray(im).copy()
        if len(_fc) > 400: _fc.pop(next(iter(_fc)))
    return _fc[kkey]


'''+s[b:]
    h=cfg["h"]
    R('icon(d, 34, 34, "S", (255, 196, 90))\n        tracked(d, 164, 30, "SECURITY  ·  UPDATE PULLED"',f'icon(d, 34, 34, "{h[0]}", (255, 196, 90))\n        tracked(d, 164, 30, "{h[1]}"')
    R('"THE FAULTY UPDATE WAS ONLINE FOR"',json.dumps(h[2])); s=s.replace('"78 MINUTES"',json.dumps(h[3]))
    R("wp, hp_ = int(800 * sc), int(150 * sc)","wp, hp_ = int(880 * sc), int(150 * sc)")
    m=re.search(r'd\.text\(\(CW / 2, 552\), ".*?", font=F\("m7", int\(74 \* sc\)\)',s); assert m
    s=s[:m.start()]+f'd.text((CW / 2, 552), {json.dumps(h[4])}, font=F("m7", int({h[5]} * sc))'+s[m.end():]
    m=re.search(r"ORDERC = \[.*?\]\n",s); s=s[:m.start()]+"ORDERC = "+cfg["order"]+"\n"+s[m.end():]
    m=re.search(r"TIN = \{.*?\}\n",s); s=s[:m.start()]+"TIN = "+cfg["tin"]+"\n"+s[m.end():]
    m=re.search(r"GL = \[.*?\]\n",s); s=s[:m.start()]+"GL = "+cfg["gl"]+"\n"+s[m.end():]
    m=re.search(r"BUZZ = \[.*?\]\n",s); s=s[:m.start()]+"BUZZ = "+cfg["buzz"]+"\n"+s[m.end():]
    R("if t >= T_BL: img = img + np.exp(-(t - T_BL) * 3.2) * np.array([0.0, 0.42, 0.80], np.float32)\n    for t0, amp in ((T_F, 0.14), (T_E, 0.08)):\n        if t >= t0: img[..., 2] += amp * np.exp(-(t - t0) * 2.5)",
      "for t0, amp in "+cfg["flash"]+":\n        if t >= t0: img[..., "+str(cfg["fch"])+"] += amp * np.exp(-(t - t0) * 2.5)")
    R('"FRIDAY, JULY 19  ·  UTC"',json.dumps(cfg["date"],ensure_ascii=False))
    R('"SOURCES: CROWDSTRIKE · MICROSOFT · CIRIUM · PARAMETRIX", F("m5", 27)',json.dumps(cfg["src"],ensure_ascii=False)+', F("m5", 27)')
    open(root+"/src/lock.py","w").write(s)
    # ---- audio
    a_=open('/home/claude/lock2/src/audio.py').read().replace('O="/home/claude/lock2/out/"',f'O="{O}"')
    x=a_.index('for j in range(34):\n    u=j/34; tt=np.arange(int(0.014*SR))/SR'); y=a_.index("# impacts: sub drop"); a_=a_[:x]+a_[y:]
    if cfg.get("notif_only"):
        a_=a_.replace("place(fx,W,at-0.30,-pan); place(fx,err(),at,pan); place(fx,glitch(0.22,0.05),at,-pan); place(low,haptic(),at+0.02)","place(fx,W,at-0.30,-pan); place(fx,notif(784,659.3),at,pan); place(low,haptic(),at+0.02)")
        a_=a_.replace("place(fx,glitch(0.45,0.13),T_BL); place(fx,glitch(0.3,0.08),T_F)","pass")
    open(root+"/src/audio.py","w").write(a_)
if __name__=="__main__":
    import importlib; name=sys.argv[1]; cfg=importlib.import_module("cfg_"+name).CFG; build(name,cfg)
