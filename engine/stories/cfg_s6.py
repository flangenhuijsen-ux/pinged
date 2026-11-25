CFG=dict(
vo=["Wednesday, August first, twenty twelve.","At nine thirty, the stock market opens.","One trading firm starts buying. And it cannot stop.","More than a thousand orders. Every second.","Four million trades in forty-five minutes.","By the time it stops, the damage is done.","Four hundred forty million dollars. Gone.","The cause?","One server out of eight.","It was still running old code."],
cues='''T_A = V[1] + 1.2
T_B = V[2] + 0.5
T_BL = V[2] + 2.5
T_C1 = V[3] + 0.3
T_F = V[4] + 0.15
T_G = V[4] + 2.3
T_C2 = V[5] + 0.4
T_C3 = V[5] + 1.9
T_D = V[6] + 0.2
T_E = V[6] + 2.4
T_P = V[9] + 0.5''',
clock="[(0.0, 9*60+28), (T_A, 9*60+30), (T_C1, 9*60+38), (T_F + 2.0, 10*60+10), (T_C2, 10*60+15), (DUR, 10*60+15)]",
mood="[(0, 0.0), (T_B, 0.15), (T_BL, 0.5), (T_F + 2.0, 0.85), (T_D + 0.5, 1.0), (T_Q, 0.8), (T_H, 0.35), (DUR, 0.25)]",
pal="[[0.75, 0.06, 0.05], [0.55, 0.03, 0.10], [0.90, 0.20, 0.05], [0.45, 0.02, 0.04], [0.70, 0.10, 0.18], [0.35, 0.02, 0.06], [0.85, 0.12, 0.04]]",
cards='''CARDS = {
    "A": (T_A, std_card("MARKETS", "M", GRN, "09:30", "The opening bell rings", "", WHT)),
    "B": (T_B, std_card("NEWS", "N", NWS, "MINUTES LATER", "Strange trading hits 154 stocks", "", WHT)),
    "C1": (T_C1, std_card("MARKETS", "M", (255, 110, 96), "LIVE", "Orders per second", "1,000+", RED8)),
    "C2": (T_C2, std_card("NEWS", "N", NWS, "10:15", "The trading finally stops", "", WHT)),
    "C3": (T_C3, std_card("MARKETS", "M", (255, 110, 96), "TOTAL", "Shares traded", "397M", AMB8)),
    "D": (T_D, std_card("MARKETS", "M", (255, 110, 96), "KNIGHT CAPITAL", "Trading loss", "$440M", RED8)),
    "E": (T_E, std_card("MARKETS", "M", (255, 110, 96), "DAYS LATER", "Knight's own stock", "-70%", RED8)),
}''',
count='''CNT_MAX = 4e6; CNT_STEP = 1e3; CNT_TINT = (255, 90, 70); CNT_ICON = ("M", (255, 110, 96)); CNT_APP = "MARKETS"; CNT_WHEN = "45 MINUTES"
CNT_LABEL = "TRADES EXECUTED BY ONE FIRM"; CNT_SUB = "FROM JUST 212 CUSTOMER ORDERS"
CNT_FMT = lambda v: f"{v:,.0f}"''',
h=("!","THE CAUSE","EIGHT SERVERS. ONE WAS MISSED.","ONE SERVER","STILL RUNNING OLD CODE",58),
order='["A", "B", "C1", "F", "C2", "C3", "D", "E", "H"]',
tin='{"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}',
gl="[(T_BL, 0.7), (T_F, 0.5), (T_D, 0.5)]",
buzz="[(T_A, 4), (T_B, 6), (T_BL, 12), (T_C1, 8), (T_F, 14), (T_C2, 6), (T_C3, 7), (T_D, 16), (T_E, 9), (T_H, 12), (T_P, 10)]",
flash="((T_BL, 0.10), (T_D, 0.16))", fch=0,
date="WEDNESDAY, AUGUST 1  ·  2012", src="SOURCES: SEC ORDER (2013) · FORTUNE · 1 AUG 2012")
