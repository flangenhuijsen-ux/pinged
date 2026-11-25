CFG=dict(
vo=["Monday, October fourth, twenty twenty-one.","Just before noon, the messages stop arriving.","Facebook. Instagram. WhatsApp.","Three and a half billion users, cut off.","It lasts almost six hours.","Inside the company, it is even worse.","Door badges stop working. Internal tools go dark.","Why did it take so long?","They had locked themselves out.","Engineers had to go to the data centers in person."],
cues='''W3 = json.load(open(O + "w3.json"))
T_A = 1.6
T_B = V[1] + 1.9
T_C1, T_C2, T_C3 = [V[2] + w for w in W3]
T_BL = T_C3 + 0.75
T_F = V[3] + 0.15
T_G = V[3] + 2.2
T_E = V[4] + 0.9
T_D = V[6] + 0.3
T_P = V[9] + 0.6''',
clock="[(0.0, 11*60+36), (T_A, 11*60+38), (T_B, 11*60+40), (T_F, 13*60), (T_E, 17*60+40), (DUR, 17*60+40)]",
mood="[(0, 0.0), (T_B, 0.15), (T_C3, 0.6), (T_BL + 0.3, 1.0), (T_Q, 0.9), (T_H, 0.35), (DUR, 0.25)]",
pal="[[0.20, 0.22, 0.27], [0.14, 0.15, 0.19], [0.26, 0.28, 0.34], [0.10, 0.11, 0.14], [0.22, 0.23, 0.30], [0.08, 0.09, 0.12], [0.18, 0.20, 0.26]]",
cards='''CARDS = {
    "A": (T_A, std_card("MESSAGES", "M", GRN, "11:38", "1 new message", "", WHT)),
    "B": (T_B, std_card("NEWS", "N", NWS, "11:40 ET", "Facebook, Instagram and WhatsApp are down", "", WHT)),
    "C1": (T_C1, std_card("STATUS", "S", NWS, "NOW", "Facebook", "DOWN", RED8)),
    "C2": (T_C2, std_card("STATUS", "S", NWS, "NOW", "Instagram", "DOWN", RED8)),
    "C3": (T_C3, std_card("STATUS", "S", NWS, "NOW", "WhatsApp", "DOWN", RED8)),
    "E": (T_E, std_card("STATUS", "S", NWS, "UNTIL EVENING", "Offline for almost", "6 HRS", AMB8)),
    "D": (T_D, std_card("NEWS", "N", NWS, "INSIDE FACEBOOK", "Staff door badges stop working", "", WHT)),
}''',
count='''CNT_MAX = 3.5e9; CNT_STEP = 1e6; CNT_TINT = (150, 160, 185); CNT_ICON = ("S", (200, 205, 220)); CNT_APP = "STATUS"; CNT_WHEN = "WORLDWIDE"
CNT_LABEL = "USERS CUT OFF"; CNT_SUB = "LARGEST OUTAGE DOWNDETECTOR HAD TRACKED"
CNT_FMT = lambda v: f"{v:,.0f}"''',
h=("!","WHY IT TOOK SO LONG","THEY HAD LOCKED THEMSELVES","OUT","ENGINEERS SENT IN PERSON",54),
order='["A", "B", "C1", "C2", "C3", "F", "E", "D", "H"]',
tin='{"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}',
gl="[(T_BL, 0.9), (T_D, 0.4)]",
buzz="[(T_A, 4), (T_B, 6), (T_C1, 7), (T_C2, 7), (T_C3, 8), (T_F, 14), (T_E, 8), (T_D, 8), (T_H, 12), (T_P, 10)]",
flash="((T_BL, 0.0), (T_F, 0.0))", fch=0,
date="MONDAY, OCTOBER 4  ·  NEW YORK", src="SOURCES: FACEBOOK ENGINEERING · REUTERS · 4 OCT 2021")
