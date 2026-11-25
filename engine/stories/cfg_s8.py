CFG=dict(
vo=["Monday, November twenty-third, twenty twenty-six.","On Friday, the stock market closes in a correction.","Nvidia has lost more than a quarter of its value in eleven days.","Then, just before the opening bell, one announcement.","The stock opens thirty percent higher.","Nine hundred fifty-two billion dollars. Added in a single day.","The Nasdaq has its best day since April twenty twenty-five.","What changed over one weekend?","One person came back.","The C.E.O. who had resigned eleven days earlier."],
cues='''T_A = V[1] + 1.4
T_B = V[2] + 1.2
T_C1 = V[3] + 1.6
T_C2 = V[4] + 0.6
T_BL = V[4] + 1.0
T_F = V[5] + 0.15
T_G = V[5] + 2.6
T_C3 = V[6] + 0.2
T_D = V[6] + 1.2
T_E = V[6] + 2.6
T_P = V[9] + 0.6''',
clock="[(0.0, 8*60+58), (T_A, 9*60), (T_C1, 9*60+25), (T_C2, 9*60+30), (T_F + 2.0, 15*60+59), (T_C3, 16*60), (DUR, 16*60)]",
mood="[(0, 0.0), (T_C1, 0.05), (T_BL, 0.55), (T_F + 2.0, 1.0), (T_Q, 0.85), (T_H, 0.35), (DUR, 0.25)]",
pal="[[0.05, 0.55, 0.25], [0.03, 0.40, 0.20], [0.10, 0.70, 0.30], [0.02, 0.30, 0.15], [0.08, 0.50, 0.35], [0.02, 0.22, 0.12], [0.06, 0.62, 0.22]]",
cards='''UP = (120, 235, 150)
CARDS = {
    "A": (T_A, std_card("MARKETS", "M", (255, 110, 96), "FRIDAY", "All three indexes end in a correction", "", WHT)),
    "B": (T_B, std_card("MARKETS", "M", (255, 110, 96), "IN 11 DAYS", "Nvidia since its CEO left", "-27%", RED8)),
    "C1": (T_C1, std_card("NEWS", "N", NWS, "BEFORE THE BELL", "Nvidia's board brings its CEO back", "", WHT)),
    "C2": (T_C2, std_card("MARKETS", "M", GRN, "09:30", "Nvidia at the open", "+30%", UP)),
    "C3": (T_C3, std_card("MARKETS", "M", GRN, "CLOSE: $165.05", "Nvidia", "+31%", UP)),
    "D": (T_D, std_card("MARKETS", "M", GRN, "BEST SINCE APR 2025", "Nasdaq", "+6.5%", UP)),
    "E": (T_E, std_card("MARKETS", "M", GRN, "TODAY", "S&P 500", "+4.7%", UP)),
}''',
count='''CNT_MAX = 952e9; CNT_STEP = 1e6; CNT_TINT = (90, 220, 130); CNT_ICON = ("M", (120, 225, 150)); CNT_APP = "MARKETS"; CNT_WHEN = "TODAY"
CNT_LABEL = "NVIDIA MARKET VALUE ADDED"; CNT_SUB = "ITS BEST DAY SINCE 2003"
CNT_FMT = lambda v: f"+${v:,.0f}"''',
h=("!","WHAT CHANGED","OVER ONE WEEKEND","ONE PERSON","THE CEO CAME BACK",64),
order='["A", "B", "C1", "C2", "F", "C3", "D", "E", "H"]',
tin='{"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}',
gl="[(T_BL, 0.5)]",
buzz="[(T_A, 5), (T_B, 6), (T_C1, 6), (T_C2, 12), (T_BL, 14), (T_F, 16), (T_C3, 7), (T_D, 7), (T_E, 7), (T_H, 12), (T_P, 10)]",
flash="((T_BL, 0.12), (T_F, 0.14))", fch=1,
date="MONDAY, NOVEMBER 23  ·  2026", src="SOURCES: CNBC · CNN · FORTUNE · 23 NOV 2026", notif_only=True)
