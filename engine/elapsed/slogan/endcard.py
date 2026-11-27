# Shared ELAPSED end card + trailer-voice slogan. exec() into a renderer after F, ease, DARK, W, H exist.
import json as _j, soundfile as _sf
SLG = _j.load(open("/home/claude/slogan/seg2.json"))["B"]; SLG_ON = SLG["onsets"]; SLG_SPEECH = SLG["speech"]; SLG_TOTAL = SLG["total"]
def end_card(lt):
    img = DARK.copy() * .55; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if lt < SLG_ON[0]: return img, lay
    u = ease((lt - SLG_ON[0]) / .22); f = F("bb", int(250 * (1.25 - .25 * u))); a8 = int(255 * min(1, (lt - SLG_ON[0]) / .08))
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).text((W / 2, 800), "ELAPSED", font=f, fill=255, anchor="mm")
    ga = np.asarray(g).astype(np.float32) / 255; glow = cv2.GaussianBlur(ga, (0, 0), 28) * .55 + cv2.GaussianBlur(ga, (0, 0), 80) * .35
    img = img + glow[..., None] * np.array([1.0, .85, .6], np.float32) * (a8 / 255)
    d.text((W / 2, 800), "ELAPSED", font=f, fill=(255, 255, 255, a8), anchor="mm")
    if lt < SLG_ON[0] + .12: img = img + (1 - (lt - SLG_ON[0]) / .12) * .5
    if lt >= SLG_ON[1]:
        u2 = ease((lt - SLG_ON[1]) / .3); d.text((W / 2, 990 + 20 * (1 - u2)), "EVERY SECOND", font=F("b7", 84), fill=(255, 255, 255, int(255 * u2)), anchor="mm")
    if lt >= SLG_ON[2]:
        u3 = ease((lt - SLG_ON[2]) / .3); d.text((W / 2, 1090 + 20 * (1 - u3)), "IS ON THE RECORD.", font=F("b7", 84), fill=AMB + (int(255 * u3),), anchor="mm")
    if lt >= SLG_ON[2] + 1.0:
        u4 = ease((lt - SLG_ON[2] - 1.0) / .5); d.text((W / 2, 1220), END_NOTE, font=F("b6", 26), fill=(255, 255, 255, int(150 * u4)), anchor="mm")
    return img, lay
def add_slogan(mix_voice_rms, n, SR, t0):
    tr, _ = _sf.read("/home/claude/slogan/tr2_B.wav"); hit, _ = _sf.read("/home/claude/slogan/hit.wav"); out = np.zeros(n)
    r = np.sqrt((tr[np.abs(tr) > .02] ** 2).mean()); tr = tr * mix_voice_rms * 10 ** (1.5 / 20) / r
    k = int(t0 * SR); m = min(len(tr), n - k); out[k:k + m] += tr[:m]
    k = int((t0 - .03) * SR); m = min(len(hit), n - k); out[k:k + m] += hit[:m] * mix_voice_rms * 2.2 / np.sqrt((hit ** 2).mean()) * .35
    return out
