import numpy as np, soundfile as sf, librosa, scipy.signal as sg, json
from kokoro_onnx import Kokoro
SR = 44100; rng = np.random.default_rng(5)
M = "/mnt/user-data/uploads/research--morpheus/model/"; k = Kokoro(M + "kokoro-v1.0.int8.onnx", M + "voices-v1.0.bin"); Vv = k.voices
def tts(tx, st, lg, sp):
    x, sr = k.create(tx, voice=st, speed=sp, lang=lg); return librosa.resample(x.astype(np.float32), orig_sr=sr, target_sr=SR)
def trailer(x, semis):
    if semis: x = librosa.effects.pitch_shift(x, sr=SR, n_steps=semis, bins_per_octave=24)
    x = x / np.abs(x).max()
    for f, g, q in ((110, 5.0, .7), (320, -2.5, 1.0), (3200, 2.0, 1.0)):          # warm low end, less mud, a bit of presence
        A = 10 ** (g / 40); w0 = 2 * np.pi * f / SR; al = np.sin(w0) / (2 * q)
        b = [1 + al * A, -2 * np.cos(w0), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w0), 1 - al / A]; x = sg.lfilter(b, a, x)
    env = np.sqrt(sg.lfilter([1 - .999], [1, -.999], x ** 2)) + 1e-6; thr = .12; gain = np.where(env > thr, (thr / env) ** .6, 1.0); x = x * gain   # compression
    x = np.tanh(2.2 * x / np.abs(x).max()) / np.tanh(2.2)                            # warm saturation
    n = int(SR * 2.6); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 2.6); ir = sg.lfilter(*sg.butter(2, 3500 / (SR / 2)), ir); ir[:int(SR * .03)] *= np.linspace(0, 1, int(SR * .03))
    wet = sg.fftconvolve(x, ir); wet = np.pad(wet, (0, max(0, len(x) + n - len(wet))))[:len(x) + n]; wet = wet / np.abs(wet).max(); dry = np.concatenate([x, np.zeros(n)])
    y = dry + .22 * wet; return (y / np.abs(y).max() * .95).astype(np.float32)
def hit():
    n = int(SR * 3.2); t = np.arange(n) / SR; f0 = 41.2 * 432 / 440
    saw = sum(np.sin(2 * np.pi * f0 * h * t + .3 * h) / h for h in range(1, 18)); saw = sg.lfilter(*sg.butter(2, 900 / (SR / 2)), saw)
    braam = saw * np.minimum(1, t / .02) * np.exp(-t * 1.1)
    sub = np.sin(2 * np.pi * np.cumsum(30 + 30 * np.exp(-t * 4)) / SR) * np.exp(-t * 1.4)
    imp = sg.lfilter(*sg.butter(2, 2500 / (SR / 2)), rng.normal(0, 1, n)) * np.exp(-t * 18)
    y = .55 * braam / np.abs(braam).max() + .8 * sub + .35 * imp; return (y / np.abs(y).max() * .95).astype(np.float32)
TX = "Elapsed. ... Every second. ... Is on the record."
out = {}
for nm, st, lg, semis in (("A", Vv["am_onyx"], "en-us", 0), ("B", Vv["am_onyx"], "en-us", -2), ("C", .6 * Vv["am_onyx"] + .4 * Vv["bm_george"], "en-us", -3)):
    raw = tts(TX, st, lg, .80); y = trailer(raw, semis); sf.write(f"tr_{nm}.wav", y, SR)
    iv = librosa.effects.split(raw, top_db=32, frame_length=2048, hop_length=256); segs = [(round(a / SR, 2), round(b / SR, 2)) for a, b in iv if b - a > SR * .12]
    f0, _, _ = librosa.pyin(librosa.resample(y[:len(raw)], orig_sr=SR, target_sr=16000), fmin=40, fmax=300, sr=16000)
    out[nm] = dict(dur=round(len(raw) / SR, 2), segs=segs, f0=round(float(np.nanmedian(f0)), 1)); print(nm, out[nm])
sf.write("hit.wav", hit(), SR)
for lab, txt in (("follow_a13", "Follow, for the next story."),):
    sf.write(f"{lab}.wav", tts(txt, .6 * Vv["bm_george"] + .4 * Vv["bm_lewis"], "en-gb", 1.12), SR)
json.dump(out, open("seg.json", "w"))
# audition: A, B, C each with the hit, 1 s apart
h, _ = sf.read("hit.wav"); parts = []
for nm in "ABC":
    y, _ = sf.read(f"tr_{nm}.wav"); seg = out[nm]["segs"][0][0]; L = max(len(y), len(h)) + SR; buf = np.zeros(L)
    buf[:len(h)] += .5 * h; buf[int(seg * SR):int(seg * SR) + len(y)] += y[:L - int(seg * SR)]; parts.append(buf); parts.append(np.zeros(SR // 2))
a = np.concatenate(parts); a = a / np.abs(a).max() * .95; sf.write("audition.wav", np.stack([a, a], 1), SR)
