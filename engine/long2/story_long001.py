import sys
sys.path.insert(0, "/home/claude/eng"); from builder import R, G, A, Wh, N, B
sys.path.insert(0, "/home/claude/long"); import script as old
CLOCK0 = "06:40"; HIDLAB = "KEEP WATCHING"
SPK = {"jan": ([142.62, 126.36, 124.08, 118.42], R, "NVIDIA · JAN 27, 2025"), "nov": ([173.0, 125.5, 165.05, 155.38], G, "NVIDIA · NOV 11 – 24, 2026")}
MK = lambda t, b, c=R: ("MARKETS", "M", c, t, b, c)
LINES = []
def s(text, **k): k["text"] = text; LINES.append(k)
g = .32
# ---------------- cold open
s("Monday morning. A free app hits number one.", gap=g, date="MONDAY, JANUARY 27 · 2025", cards=[(.55, 0, ("APP STORE", "A", B, "DeepSeek, free apps", "#1", Wh))], log=(.55, "MON AM", "DEEPSEEK IS #1 ON THE APP STORE", B), meter=(0, "NVIDIA · SHARE PRICE", "$142.62", Wh, "FRIDAY'S CLOSE", None))
s("Eight sixteen. Nvidia is down eleven percent.", gap=g, clk=("08:16", "slow", 0), acc=R, acc_u=.4, cards=[(.45, 0, MK("Nvidia, pre-market", "-11.4%"))], glitch=[(.45, .3)], log=(.45, "08:16", "NVIDIA  -11.4%  PRE-MARKET", R), meter=(.45, "NVIDIA · PRE-MARKET", "-11.4%", R, "08:16 · BEFORE THE OPEN", None), spark=("jan", [(0, .45), (1, .58)]))
s("Four p.m. Five hundred eighty-nine billion dollars. Gone.", gap=g, clk=("16:00", "fwd"), cards=[(.05, 0, MK("Nvidia at the close", "-17%"))], glitch=[(.36, .22)], log=(.16, "16:00", "NVIDIA CLOSES  -17%", R), meter=(.16, "NVIDIA · THE CLOSE", "$118.42", R, "DOWN 17% ON THE DAY", None), spark=("jan", [(2, .0), (3, .2)]),
  slam=(.36, "-$589,000,000,000", R, "GONE IN ONE DAY", (589e9, "-${:,.0f}", .9)))
s("The biggest one-day loss in history.", gap=g, slam=(0, "BIGGEST ONE-DAY LOSS", Wh, "ANY COMPANY · EVER", None), log=(0, "16:00", "-$589 BILLION IN ONE DAY", R))
s("Twenty-two months later, one more notification.", gap=g, clear=True, acc=A, clk=("09:25", "long", .55, 0), roll=(.5, "22 MONTHS LATER", A), date="MONDAY, NOVEMBER 23 · 2026", date_u=.5, hidden=("show", .62), log=(.62, "NOV 2026", "ONE MORE NOTIFICATION", A), meter=(.5, "NVIDIA · NOVEMBER 23, 2026", "?", A, "ONE ANNOUNCEMENT", None))
s("And this time, it went the other way.", gap=g, acc=G, slam=(.30, "+$952,000,000,000", G, "IN ONE DAY", (952e9, "+${:,.0f}", .8)), log=(.3, "NOV 2026", "+$952 BILLION IN ONE DAY", G), meter=(.3, "NVIDIA · ONE DAY", "+31.5%", G, "ITS BEST DAY SINCE 2003", None))
s("But let me back up.", gap=g, clear=True, acc=N, rewind=True, clk=("16:00", "back"), date="FRIDAY, JANUARY 24 · 2025", date_u=.8, hidden=("hide", .05))
s("January twenty twenty-five. Nvidia is the most valuable company on earth.", gap=g, cut=True, acc=G, hidden=("show", .1), cards=[(.5, 0, ("MARKETS", "M", G, "Nvidia: world's No. 1", "$3.5T", Wh))], log=(.5, "JAN 24", "NVIDIA IS WORTH $3.5 TRILLION", G), meter=(0, "NVIDIA · MARKET VALUE", "$3.5 TRILLION", G, "WORLD'S MOST VALUABLE COMPANY", (3.5, "${:.1f} TRILLION", 1.6)))
s("Its chips power artificial intelligence.", gap=g, cards=[(.15, 0, ("PINGED", "P", A, "Its chips power AI", "", Wh))])
s("And the whole market believes one thing.", gap=g, cut=True, acc=A, log=(.3, "JAN 24", "THE BELIEF: MORE CHIPS", A))
s("A.I. needs more chips. Always more.", gap=g, cards=[(.02, 0, ("PINGED", "P", A, "The belief: AI needs more chips", "", Wh))], slam=(.55, "ALWAYS MORE", A, "THE WHOLE MARKET BELIEVED IT", None))
s("Then a Chinese startup releases a model called Deep Seek.", gap=g, clear=True, acc=N, date="MONDAY, JANUARY 20 · 2025", cards=[(.5, 0, ("NEWS", "N", N, "DeepSeek releases its R1 model", "", Wh))], log=(.5, "JAN 20", "DEEPSEEK RELEASES R1", N), meter=(.5, "WALL STREET REACTION", "QUIET", N, "JANUARY 20 – 26", None))
s("Almost nobody notices.", gap=g, dim=True, dates=[(0, j * .33, f"{d}, JANUARY {21 + j} · 2025") for j, d in enumerate(["TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"])], log=(.3, "JAN 20-26", "WALL STREET BARELY REACTS", N))
fl = [("APP STORE", "A", B, "DeepSeek, free apps", "#1", Wh), MK("Nvidia, pre-market", "-11.4%"), MK("Broadcom", "-17.4%"), MK("Chip stock index", "-9.2%"), MK("Nasdaq", "-3.1%")]
s("One week later, everybody does.", gap=.5, clear=True, cut=True, acc=R, acc_u=.28, date="MONDAY, JANUARY 27 · 2025", date_u=.22, clk=("08:16", "long", .25, 2), cards=[(.30, j * .24, c) for j, c in enumerate(fl)], glitch=[(.30, 1.2)], log=(.3, "JAN 27", "EVERYBODY NOTICES", R), meter=(.3, "NVIDIA · PRE-MARKET", "-11.4%", R, "MONDAY, JANUARY 27", None))
# ---------------- the rest: converted from the verified first version
CM = {old.R: R, old.G: G, old.A: A, old.W: Wh, old.N: N, old.B: B}
PARTS = {11: "JANUARY 27, 2025", 29: "WHY IT HAPPENED", 39: "THE COMEBACK", 47: "NOVEMBER 23, 2026", 64: "WHAT IT MEANS"}
HOOK = {29: "But the strangest part is why.", 39: "And here is where the story turns.", 64: "Two days. Opposite directions. The same cause."}
SKIP = {40}; YEAR = {1: " · 2025", 2: " · 2025", 3: " · 2025", 4: " · 2026"}
KEEP = {"nvidia": "Nvidia", "chatgpt": "ChatGPT", "ai": "AI", "us": "US", "s&p": "S&P", "dow": "Dow", "nasdaq": "Nasdaq", "apple": "Apple", "microsoft": "Microsoft", "asml": "ASML", "asml,": "ASML,", "amsterdam": "Amsterdam", "september": "September", "march": "March", "april": "April", "europe": "Europe", "deepseek": "DeepSeek", "ceo": "CEO", "$3t": "$3T", "$4t": "$4T", "$5t": "$5T", "no.": "No.", "january": "January", "november": "November", "october": "October", "july": "July", "friday": "Friday", "monday": "Monday", "broadcom": "Broadcom"}
def case(x):
    w = x.lower().split(); w = [KEEP.get(a, a) for a in w]; o = " ".join(w); return o[0].upper() + o[1:] if o else o
NOHEAD = {13: "An uncomfortable question", 30: "What it seemed to prove", 45: "The record loss: now a footnote", 72: "One share price can move your savings"}
since = 9; pn = 0; tag = "JAN 27"
for i, l in enumerate(old.L):
    if i < 11 or i in SKIP: continue
    if i in HOOK: s(HOOK[i], cut=True, acc=A, cards=[(.3, 0, ("PINGED", "P", A, HOOK[i], "", Wh))]); since += 1
    if i in PARTS:
        pn += 1; s("", dur=2.0, gap=.3, clear=True, acc=A, slam=(0, PARTS[i], Wh, f"PART {pn} OF {len(PARTS)}", None)); since = 0
    k = {}; p = l["phone"]; bc = CM[l["bc"]]; card = None
    if p.get("clear") or i in PARTS: k["clear"] = True
    if "date" in p:
        dt = p["date"]; k["date"] = dt + (YEAR.get(l["ch"], "") if "," in dt else "")
        tag = dt.split(", ")[-1][:3] + dt.split(", ")[-1][3:].replace("UARY", "").replace("EMBER", "").replace("OBER", "") if "," in dt else dt
    if "clock" in p and i != 11: k["clk"] = (p["clock"], "fwd")
    if i == 11: k["clk"] = ("06:40", "fwd"); k["date"] = "MONDAY, JANUARY 27 · 2025"
    if i == 15: k["clk"] = ("08:16", "slow", 0)
    if p.get("card"):
        c = p["card"]; card = (c[0], c[1], CM[c[2]], c[3], c[4], CM[c[5]]); k["cards"] = [(.45, 0, card)]
        if card[2] == R: k["glitch"] = [(.45, .22)]
        if card[2] in (R, G): k["acc"] = card[2]; k["acc_u"] = .4
    if bc in (R, G, A) and l["head"]: k["acc"] = bc
    cnt = l["count"]
    if l["head"]:
        val = l["big"] or (card[4] if card else "") or ""
        if cnt: val = ("-" if "-" in cnt[1] else "+") + f"${cnt[0] / 1e9:.0f}B"
        k["meter"] = (.12, l["head"], val or "·", bc, l["sub"] or "", None)
        tg = p.get("clock") if ("clock" in p and l["ch"] in (1, 4) and i != 11) else tag
        big_ = l["big"] or ""; sub_ = l["sub"] or ""
        k["log"] = (.2, tg, ((big_ if len(big_) >= 9 or not sub_ else f"{big_} · {sub_}") or sub_ or l["head"]) if not cnt else f"{val} IN ONE DAY", bc if bc != Wh else N)
    if cnt: k["slam"] = (.30, cnt[1].format(cnt[0]), bc, l["sub"], (cnt[0], cnt[1], .9)); since = 0
    elif l["big"] and not card and len(l["big"]) <= 18 and since >= 3 and (bc != Wh or since >= 5) and i not in (78, 79): k["slam"] = (.45, l["big"], bc, l["sub"] or None, None); since = 0
    else: since += 1
    if l["chart"]:
        key, upto = l["chart"]; done = {"jan": 0, "nov": 0}
        prev = max([x["chart"][1] for x in old.L[:i] if x["chart"] and x["chart"][0] == key], default=0); new = list(range(prev, upto)); k["spark"] = (key, [(j, .15 + .6 * n / max(1, len(new))) for n, j in enumerate(new)])
    if l["head"] and not card and "slam" not in k and i not in (78,):
        big = l["big"] or ""; sub = l["sub"] or l["head"]
        k["cards"] = [(.45, 0, ("PINGED", "P", A, case(sub) if len(big) <= 9 else case(f"{big}: {sub}" if l["sub"] else big), big if len(big) <= 9 else "", bc))]
    if "log" in k: k["log"] = (.72,) + k["log"][1:]
    if l["head"] and l["big"] and len(l["big"]) <= 18 and "slam" not in k and i not in (78, 79): k["emph"] = (l["big"], bc, l["sub"] or None)
    if i in PARTS and "acc" not in k: k["acc"] = B
    if i in NOHEAD: k["cards"] = [(.35, 0, ("PINGED", "P", A, NOHEAD[i], "", Wh))]
    if i == 55: k["hidden"] = ("unlock", .30); k["cards"] = [(.32, 0, card)]; k["acc"] = A
    if i == 12: k["text_override"] = None
    s(l["text"], **k)
