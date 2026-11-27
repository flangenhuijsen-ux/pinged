# Shared ELAPSED end card + trailer-voice slogan. exec() into a renderer after F, ease, DARK, W, H exist.
import json as _j, soundfile as _sf
SLG = _j.load(open("/home/claude/slogan/seg5.json"))["B"]; SLG_ON = SLG["onsets"]; SLG_SPEECH = SLG["speech"]; SLG_TOTAL = SLG["total"]
_LOGO = None
def _logo(sz):
    global _LOGO
    if _LOGO is None or _LOGO.size[0] != sz:
        im = Image.open("/home/claude/elapsed/ELAPSED-logo.png").convert("RGBA").resize((sz, sz), Image.LANCZOS)
        m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse([sz * .03, sz * .03, sz * .97, sz * .97], fill=255); im.putalpha(m); _LOGO = im
    return _LOGO
def end_card(lt):
    img = DARK.copy() * .55; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if lt < SLG_ON[0]: return img, lay
    u = ease((lt - SLG_ON[0]) / .25); a8 = int(255 * min(1, (lt - SLG_ON[0]) / .08))
    sz = int(400 * (1.2 - .2 * u)); L_ = _logo(sz).copy(); L_.putalpha(L_.getchannel("A").point(lambda v_: int(v_ * a8 / 255)))
    # soft mint glow behind the logo
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse([W / 2 - sz * .5, 560 - sz * .5, W / 2 + sz * .5, 560 + sz * .5], fill=255)
    ga = cv2.GaussianBlur(np.asarray(g).astype(np.float32) / 255, (0, 0), 60) * .45 * (a8 / 255); img = img + ga[..., None] * np.array([.25, .9, .6], np.float32)
    lay.alpha_composite(L_, (int(W / 2 - sz / 2), int(560 - sz / 2)))
    # seven-segment wordmark EL:AP:SED, as on the banner
    bw = globals().get("word_") or word
    w_, h_, th_, gap_, cw_ = 74, 128, 17, 17, 30; tw_ = width("EL:AP:SED", w_, gap_, cw_); x0 = (W - tw_) / 2
    gl_, lt_ = bw((W, H), "EL:AP:SED", x0, 840, w_, h_, th_, gap_, cw_)
    gl_.putalpha(gl_.getchannel("A").point(lambda v_: int(v_ * a8 / 255 * .6))); lt_.putalpha(lt_.getchannel("A").point(lambda v_: int(v_ * a8 / 255)))
    la = np.asarray(lt_).astype(np.float32) / 255; img = img + cv2.GaussianBlur(la[..., :3] * la[..., 3:], (0, 0), 16) * .9
    lay.alpha_composite(gl_); lay.alpha_composite(lt_); d = ImageDraw.Draw(lay)
    if lt < SLG_ON[0] + .12: img = img + (1 - (lt - SLG_ON[0]) / .12) * .45
    if lt >= SLG_ON[1]:
        u2 = ease((lt - SLG_ON[1]) / .3); d.text((W / 2, 1075 + 20 * (1 - u2)), "EVERY SECOND", font=F("b7", 84), fill=(255, 255, 255, int(255 * u2)), anchor="mm")
    if lt >= SLG_ON[2]:
        u3 = ease((lt - SLG_ON[2]) / .3); d.text((W / 2, 1170 + 20 * (1 - u3)), "IS ON THE RECORD.", font=F("b7", 84), fill=(255, 196, 96, int(255 * u3)), anchor="mm")
    if lt >= SLG_ON[2] + 1.0:
        u4 = ease((lt - SLG_ON[2] - 1.0) / .5); d.text((W / 2, 1290), END_NOTE, font=F("b6", 26), fill=(255, 255, 255, int(150 * u4)), anchor="mm")
    return img, lay
def add_slogan(mix_voice_rms, n, SR, t0):
    tr, _ = _sf.read("/home/claude/slogan/tr5.wav"); hit, _ = _sf.read("/home/claude/slogan/hit.wav"); out = np.zeros(n)
    r = np.sqrt((tr[np.abs(tr) > .02] ** 2).mean()); tr = tr * mix_voice_rms * 10 ** (1.5 / 20) / r
    k = int(t0 * SR); m = min(len(tr), n - k); out[k:k + m] += tr[:m]
    k = int((t0 - .03) * SR); m = min(len(hit), n - k); out[k:k + m] += hit[:m] * mix_voice_rms * 2.2 / np.sqrt((hit ** 2).mean()) * .35
    return out
