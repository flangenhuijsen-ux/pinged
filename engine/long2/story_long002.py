import sys
sys.path.insert(0, "/home/claude/eng"); from builder import R, G, A, Wh, N, B
sys.path.insert(0, "/home/claude/long2"); import script as old
CLOCK0 = "04:00"; HIDLAB = "KEEP WATCHING"; SPK = {}
LINES = []
def s(text, **k): k["text"] = text; LINES.append(k)
g = .32
# ---------------- cold open
s("Friday morning. A routine security update goes out.", gap=g, date="FRIDAY, JULY 19 · 2024 · UTC", clk=("04:09", "slow", .5), cards=[(.5, 0, ("SECURITY", "S", G, "Security update installed", "", Wh))], log=(.5, "04:09 UTC", "A ROUTINE UPDATE GOES OUT", G), meter=(0, "CROWDSTRIKE FALCON", "ONE UPDATE", Wh, "04:09 UTC · JULY 19, 2024", None), acc=G)
s("Then the screens turn blue.", gap=g, acc=B, acc_u=.3, cards=[(.35, 0, ("SYSTEM", "S", B, "Windows has crashed", "", Wh))], glitch=[(.35, .4)], log=(.35, "04:09 UTC", "WINDOWS MACHINES CRASH", B), meter=(.35, "WINDOWS", "CRASH", B, "RESTART · CRASH · RESTART", None))
s("Eight and a half million computers. Down.", gap=g, slam=(.25, "8,500,000", B, "WINDOWS DEVICES DOWN", (8.5e6, "{:,.0f}", .9)), log=(.3, "JULY 19", "8.5 MILLION DEVICES DOWN", B))
s("Flights cancelled. Surgeries delayed. Billions of dollars lost.", gap=g, acc=R, cards=[(.05, 0, ("FLIGHTS", "F", B, "Flights cancelled", "5,078", R)), (.38, 0, ("NEWS", "N", N, "Hospitals delay procedures", "", Wh)), (.68, 0, ("DAMAGE", "$", A, "Estimated cost", "$5.4B", A))], glitch=[(.05, .2)], log=(.68, "JULY 19", "ESTIMATED DAMAGE: $5.4 BILLION", R), meter=(.05, "FLIGHTS CANCELLED · JULY 19", "5,078", R, "WORLDWIDE · CIRIUM", None))
s("And it was not an attack.", gap=g, slam=(.15, "NOT AN ATTACK", Wh, "NOBODY BROKE IN", None))
s("Three years earlier, the same kind of mistake.", gap=g, clear=True, acc=N, clk=("11:40", "back"), roll=(.6, "3 YEARS EARLIER", A), date="MONDAY, OCTOBER 4 · 2021", date_u=.6, log=(.6, "OCT 2021", "THE SAME KIND OF MISTAKE", N), meter=(.6, "OCTOBER 4, 2021", "?", A, "ONE COMMAND", None))
s("It took Facebook, Instagram and WhatsApp off the internet.", gap=g, acc=R, acc_u=.2, cards=[(.2, 0, ("STATUS", "S", N, "Facebook", "DOWN", R)), (.45, 0, ("STATUS", "S", N, "Instagram", "DOWN", R)), (.7, 0, ("STATUS", "S", N, "WhatsApp", "DOWN", R))], glitch=[(.2, .5)], log=(.7, "OCT 4, 2021", "FACEBOOK · INSTAGRAM · WHATSAPP: GONE", R), meter=(.2, "ALL SERVICES", "DOWN", R, "FOR ALMOST SIX HOURS", None))
s("For three and a half billion people.", gap=g, slam=(.1, "3,500,000,000", R, "USERS CUT OFF", (3.5e9, "{:,.0f}", .9)))
s("And both times, the people who could fix it were locked out.", gap=g, acc=A, hidden=("show", .3), slam=(.55, "LOCKED OUT", A, "THE PEOPLE WHO COULD FIX IT", None), log=(.5, "BOTH DAYS", "THE FIXERS WERE LOCKED OUT", A))
s("Let me back up.", gap=.5, clear=True, acc=N, rewind=True, clk=("04:00", "back"), date="FRIDAY, JULY 19 · 2024 · UTC", date_u=.8, hidden=("hide", .05))
# ---------------- body, converted from the verified script
CM = {old.R: R, old.G: G, old.A: A, old.W: Wh, old.N: N, old.B: B}
PARTS = {7: "JULY 19, 2024", 26: "WHY A RESTART DID NOT HELP", 35: "OCTOBER 4, 2021", 56: "THE SAME MISTAKE, TWICE", 64: "WHAT CHANGED"}
HOOK = {26: "But the update is only half the story.", 35: "And this had happened before.", 56: "Now look at what the two days share.", 64: "So did anything change?"}
X = lambda t, head, big, sub, bc=Wh: dict(text=t, head=head, big=big, sub=sub, bc=bc)
EXTRA = {8: [X("And by forty-three of the fifty American states.", "ALSO USED BY", "43 OF 50", "US STATES")],
         14: [X("Mac and Linux machines are not affected. Only Windows.", "NOT AFFECTED", "MAC · LINUX", "ONLY WINDOWS MACHINES CRASH")],
         25: [X("About twenty-five billion dollars of market value, gone.", "CROWDSTRIKE MARKET VALUE", "-$25 BILLION", "IN TWELVE DAYS", R), X("Its own shareholders sue. And in October, so does Delta.", "IN COURT", "SUED", "BY SHAREHOLDERS · AND BY DELTA", A), X("The company cuts its revenue forecast, and says the damage will last about a year.", "CROWDSTRIKE", "FORECAST CUT", "A CHALLENGING YEAR AHEAD", R)],
         52: [X("One point seven million of them from the United States alone.", "FROM THE UNITED STATES", "1.7 MILLION", "PROBLEM REPORTS", R)],
         54: [X("More than forty-seven billion dollars of market value, in a single day.", "FACEBOOK MARKET VALUE", "-$47 BILLION", "IN ONE DAY", R), X("Its founder's own fortune drops by about six billion.", "MARK ZUCKERBERG", "-$6 BILLION", "PERSONAL WEALTH · THAT DAY", R), X("One estimate puts the lost advertising at sixty million dollars.", "LOST ADVERTISING", "$60 MILLION", "ONE ESTIMATE", A)],
         55: [X("Back then, a bug kept it offline for about a day. But it had eighty million users. Not three and a half billion.", "IN 2008", "80 MILLION", "USERS BACK THEN", A)]}
REPL = {18: "That is less than one percent of all Windows machines. But they include the ones that run airlines, hospitals and some of the world's largest companies.",
        65: "Facebook published its own account the next day. One command. And one safety tool that failed to stop it."}
REPLF = {18: ("LESS THAN 1% OF WINDOWS", "THE 1%", "AIRLINES · HOSPITALS · LARGE COMPANIES"), 65: ("FACEBOOK · OCTOBER 5, 2021", "ITS OWN ACCOUNT", "ONE COMMAND · ONE TOOL THAT FAILED")}
KEEP = {"crowdstrike": "CrowdStrike", "windows": "Windows", "us": "US", "facebook": "Facebook", "delta": "Delta", "whatsapp": "WhatsApp", "instagram": "Instagram", "mac": "Mac", "linux": "Linux", "utc": "UTC", "microsoft's": "Microsoft's", "parametrix": "Parametrix", "cirium": "Cirium", "july": "July", "york": "York", "new": "New", "pm": "PM", "fortune": "Fortune", "telegram": "Telegram", "downdetector": "Downdetector"}
def case(x):
    w = [KEEP.get(a, KEEP.get(a.strip(":,."), a.strip(":,.")) + a[len(a.rstrip(":,.")):] if a.strip(":,.") in KEEP else a) for a in x.lower().split()]; o = " ".join(w); return o[0].upper() + o[1:] if o else o
since = 9; pn = 0; tag = "JULY 19"; clockv = "04:00"
def conv(l, i, part=False):
    global since, tag, clockv
    k = {}; p = l.get("phone", {}); bc = CM.get(l["bc"], l["bc"]); card = None
    if p.get("clear") or part: k["clear"] = True
    if "date" in p:
        dt = p["date"]; k["date"] = dt.replace("JULY 19 · UTC", "JULY 19 · 2024 · UTC").replace("OCTOBER 4", "OCTOBER 4 · 2021") if "," in dt else dt; tag = {"FRIDAY, JULY 19 · UTC": "JULY 19", "MONDAY, OCTOBER 4": "OCT 4, 2021", "SEPTEMBER 24, 2024": "SEPT 2024"}.get(dt, dt)
    if "clock" in p and p["clock"][:2].isdigit(): k["clk"] = (p["clock"], "fwd"); clockv = p["clock"]
    elif "clock" in p: k["clocktxt"] = "--:--"
    if p.get("card"):
        c = p["card"]; card = (c[0], c[1], CM[c[2]], c[3], c[4], CM[c[5]]); k["cards"] = [(.45, 0, card)]
        if card[5] == R or card[2] == B: k["glitch"] = [(.45, .22)]
    if bc in (R, G, A, B) and l["head"]: k["acc"] = bc
    cnt = l.get("count")
    if l["head"]:
        big = l["big"] or ""; sub = l["sub"] or ""
        val = big or (card[4] if card else "")
        if cnt: val = f"{cnt[0] / 1e6:.1f}M" if cnt[0] < 1e9 else f"{cnt[0] / 1e9:.1f}B"
        k["meter"] = (.12, l["head"], val or "·", bc, sub, None)
        k["log"] = (.72, tag, (big if len(big) >= 9 or not sub else f"{big} · {sub}") or sub or l["head"] if not cnt else f"{val} · {sub}", bc if bc != Wh else N)
        if cnt: k["slam"] = (.30, cnt[1].format(cnt[0]), bc, l["sub"], (cnt[0], cnt[1], .9)); since = 0
        elif big and not card and len(big) <= 18 and since >= 3 and (bc != Wh or since >= 5): k["slam"] = (.45, big, bc, sub or None, None); since = 0
        else:
            since += 1
            if not card: k["cards"] = [(.45, 0, ("PINGED", "P", A, case(sub or l["head"]) if len(big) <= 9 else case(f"{big}: {sub}" if sub else big), big if len(big) <= 9 else "", bc))]
    else: since += 1
    if l["head"] and l["big"] and len(l["big"]) <= 18 and "slam" not in k: k["emph"] = (l["big"], bc, l["sub"] or None)
    return k
for i, l in enumerate(old.L):
    if i < 7: continue
    if i in HOOK: s(HOOK[i], cut=True, acc=A, cards=[(.3, 0, ("PINGED", "P", A, HOOK[i], "", Wh))]); since += 1
    if i in PARTS:
        pn += 1; s("", dur=2.0, gap=.3, clear=True, acc=A, slam=(0, PARTS[i], Wh, f"PART {pn} OF {len(PARTS)}", None)); since = 0
    l = dict(l)
    if i in REPL: l["text"] = REPL[i]; l["head"], l["big"], l["sub"] = REPLF[i]
    if i == 74: l["head"] = None
    k = conv(l, i, i in PARTS)
    if i in PARTS and "acc" not in k: k["acc"] = B
    if i == 7: k["hidden"] = ("show", .1)
    if i == 69: tag = "BOTH DAYS"
    if i == 27: k["cards"] = [(.35, 0, ("PINGED", "P", A, "Where the software lives", "", Wh))]
    if i == 60: k["hidden"] = ("unlock", .40); k.pop("slam", None); k["cards"] = [(.42, 0, ("PINGED", "P", A, "The fix: a human, at the machine", "", Wh))]; k["acc"] = A
    if i == 74: k["cards"] = [(.3, 0, ("PINGED", "P", A, "New story tomorrow", "", Wh))]; k["clear"] = True; k["date"] = "PINGED"
    s(l["text"], **k)
    for e in EXTRA.get(i, []): s(e["text"], **conv(dict(e, phone={}, count=None), i))
