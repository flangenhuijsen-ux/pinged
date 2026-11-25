CFG=dict(
vo=["Wednesday, February eighth, twenty twenty-three.","Google is showing the world its new A.I. chatbot.","In the ad, a parent asks about a space telescope.","The A.I. answers. Confidently.","But the answer is wrong.","Astronomers notice. Reporters notice. Then the market does.","One hundred billion dollars. Gone in a day.","And the question?","It was meant for a nine-year-old.","And it was in Google's own ad."],
cues='''T_A = V[1] + 1.0
T_B = V[2] + 0.9
T_C1 = V[3] + 0.5
T_C2 = V[4] + 0.6
T_C3 = V[5] + 0.1
T_D = V[5] + 1.6
T_BL = V[5] + 3.1
T_F = V[6] + 0.15
T_G = V[6] + 2.3
T_E = V[6] + 2.9
T_P = V[9] + 0.5''',
clock="[(0.0, 8*60+58), (T_A, 9*60), (T_C1, 10*60+30), (T_D, 13*60), (T_F + 2.0, 16*60), (DUR, 16*60)]",
mood="[(0, 0.0), (T_C2, 0.1), (T_D, 0.35), (T_BL, 0.7), (T_F + 2.0, 1.0), (T_Q, 0.8), (T_H, 0.35), (DUR, 0.25)]",
pal="[[0.75, 0.06, 0.05], [0.55, 0.03, 0.10], [0.90, 0.20, 0.05], [0.45, 0.02, 0.04], [0.70, 0.10, 0.18], [0.35, 0.02, 0.06], [0.85, 0.12, 0.04]]",
cards='''CARDS = {
    "A": (T_A, std_card("NEWS", "N", NWS, "MONDAY", "Google unveils its AI chatbot, Bard", "", WHT)),
    "B": (T_B, std_card("THE AD", "?", BLU, "QUESTION", "A parent asks about the James Webb telescope", "", WHT)),
    "C1": (T_C1, std_card("THE AD", "A", BLU, "AI ANSWER", "It took the very first photo of an exoplanet", "", WHT)),
    "C2": (T_C2, std_card("FACT CHECK", "!", RED8, "NASA", "The first exoplanet photo was taken in 2004", "", WHT)),
    "C3": (T_C3, std_card("NEWS", "N", NWS, "TODAY", "Astronomers spot the error in the ad", "", WHT)),
    "D": (T_D, std_card("NEWS", "N", NWS, "REUTERS", "Reuters reports the mistake", "", WHT)),
    "E": (T_E, std_card("MARKETS", "M", (255, 110, 96), "AT THE CLOSE", "Alphabet shares", "-8%", RED8)),
}''',
count='''CNT_MAX = 100e9; CNT_STEP = 1e6; CNT_TINT = (255, 90, 70); CNT_ICON = ("M", (255, 110, 96)); CNT_APP = "MARKETS"; CNT_WHEN = "TODAY"
CNT_LABEL = "ALPHABET MARKET VALUE LOST"; CNT_SUB = "AFTER ONE WRONG ANSWER"
CNT_FMT = lambda v: f"-${v:,.0f}"''',
h=("?","THE QUESTION","THE QUESTION WAS MEANT FOR","A 9-YEAR-OLD","IN GOOGLE'S OWN AD",70),
order='["A", "B", "C1", "C2", "C3", "D", "F", "E", "H"]',
tin='{"A": T_A, "B": T_B, "C1": T_C1, "C2": T_C2, "C3": T_C3, "D": T_D, "E": T_E, "F": T_F, "H": T_H}',
gl="[(T_C2, 0.6), (T_F, 0.5)]",
buzz="[(T_A, 4), (T_B, 5), (T_C1, 5), (T_C2, 12), (T_C3, 6), (T_D, 7), (T_F, 16), (T_E, 9), (T_H, 12), (T_P, 10)]",
flash="((T_C2, 0.10), (T_F, 0.16))", fch=0,
date="WEDNESDAY, FEBRUARY 8  ·  2023", src="SOURCES: REUTERS · NPR · FORTUNE · NASA · 8 FEB 2023", notif_only=True)
