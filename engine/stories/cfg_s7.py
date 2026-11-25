CFG=dict(
vo=["Tuesday, March twenty-third, twenty twenty-one.","At seven forty in the morning, a ship turns sideways in the Suez Canal.","It is four hundred meters long. And it is stuck.","Day two. Day four. Day six.","More than four hundred ships are waiting.","Nine point six billion dollars of trade, held up. Every single day.","Diggers and tugboats pull for six days.","What finally frees it?","The moon.","A full moon brought an unusually high tide."],
cues='''W3 = json.load(open(O + "w3.json"))
T_A = V[1] + 2.6
T_B = V[2] + 0.8
T_BL = V[2] + 3.0
T_C1, T_C2, T_C3 = [V[3] + w for w in W3]
T_D = V[4] + 1.0
T_F = V[5] + 0.15
T_G = V[5] + 3.4
T_E = V[6] + 0.6
T_P = V[9] + 0.6''',
clock="[(0.0, 7*60+38), (T_A, 7*60+40), (T_C1, 12*60), (T_C2, 18*60), (T_C3, 6*60), (T_E + 1.0, 15*60+5), (DUR, 15*60+5)]",
mood="[(0, 0.0), (T_B, 0.2), (T_BL, 0.6), (T_F + 2.0, 1.0), (T_Q, 0.85), (T_H, 0.35), (DUR, 0.25)]",
pal="[[0.55, 0.33, 0.10], [0.42, 0.22, 0.06], [0.65, 0.42, 0.14], [0.30, 0.16, 0.05], [0.50, 0.30, 0.14], [0.24, 0.12, 0.04], [0.60, 0.36, 0.08]]",
cards='''CARDS = {
    "A": (T_A, std_card("NEWS", "N", NWS, "07:40", "Container ship blocks the Suez Canal", "", WHT)),
    "B": (T_B, std_card("SHIPPING", "S", BLU, "EVER GIVEN", "Ship length", "400 M", WHT)),
    "C1": (T_C1, std_card("SHIPPING", "S", BLU, "STILL STUCK", "The canal is closed", "DAY 2", AMB8)),
    "C2": (T_C2, std_card("SHIPPING", "S", BLU, "STILL STUCK", "The canal is closed", "DAY 4", AMB8)),
    "C3": (T_C3, std_card("SHIPPING", "S", BLU, "STILL STUCK", "The canal is closed", "DAY 6", RED8)),
    "D": (T_D, std_card("SHIPPING", "S", BLU, "CANAL AUTHORITY", "Ships waiting in line", "422", RED8)),
    "E": (T_E, std_card("NEWS", "N", NWS, "DAY AND NIGHT", "Tugboats and dredgers keep pulling", "", WHT)),
}''',
count='''CNT_MAX = 9.6e9; CNT_STEP = 1e6; CNT_TINT = (235, 170, 90); CNT_ICON = ("$", (255, 190, 80)); CNT_APP = "TRADE"; CNT_WHEN = "LLOYD'S LIST EST."
CNT_LABEL = "TRADE HELD UP, EVERY DAY"; CNT_SUB = "ABOUT $400 MILLION EVERY HOUR"
CNT_FMT = lambda v: f"${v:,.0f}"''',
h=("*","WHAT FREED IT","IN THE END IT WAS","THE MOON","FULL MOON  ·  HIGH TIDE",60),
order='["A", "B", "C1", "C2", "C3", "D", "F", "E", "H"]',
tin='{"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}',
gl="[(T_BL, 0.5)]",
buzz="[(T_A, 5), (T_B, 6), (T_BL, 14), (T_C1, 6), (T_C2, 7), (T_C3, 8), (T_D, 8), (T_F, 14), (T_E, 6), (T_H, 10), (T_P, 8)]",
flash="((T_BL, 0.08), (T_F, 0.08))", fch=0,
date="MARCH 23 – 29, 2021  ·  SUEZ CANAL", src="SOURCES: SUEZ CANAL AUTHORITY · LLOYD'S LIST · AP · BBC", notif_only=True)
