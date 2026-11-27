import numpy as np, soundfile as sf, librosa, json
exec(open("make.py").read().split('TX = "Elapsed.')[0])
PH = ["Elapsed.", "Every second.", "Is on the record."]; GAPS = [.55, .25]
res = {}
for nm, st, semis in (("A", Vv["am_onyx"], 0), ("B", Vv["am_onyx"], -2)):
    clips = []
    for p in PH:
        x = tts(p, st, "en-us", .78); iv = librosa.effects.split(x, top_db=35); x = x[iv[0][0]:iv[-1][1]]; clips.append(x)
    raw = []; on = []; t = 0
    for i, c in enumerate(clips):
        on.append(round(t / SR, 3)); raw.append(c); t += len(c)
        if i < len(GAPS): raw.append(np.zeros(int(GAPS[i] * SR), np.float32)); t += int(GAPS[i] * SR)
    raw = np.concatenate(raw); y = trailer(raw, semis); sf.write(f"tr2_{nm}.wav", y, SR)
    f0, _, _ = librosa.pyin(librosa.resample(y[:len(raw)], orig_sr=SR, target_sr=16000), fmin=40, fmax=300, sr=16000)
    res[nm] = dict(onsets=on, speech=round(len(raw) / SR, 2), total=round(len(y) / SR, 2), f0=round(float(np.nanmedian(f0)), 1)); print(nm, res[nm])
json.dump(res, open("seg2.json", "w"))
h, _ = sf.read("hit.wav"); parts = []
for nm in "AB":
    y, _ = sf.read(f"tr2_{nm}.wav"); L = max(len(y), len(h)) + SR // 2; buf = np.zeros(L); buf[:len(h)] += .45 * h; buf[int(.05 * SR):int(.05 * SR) + len(y)] += y; parts += [buf, np.zeros(SR // 2)]
a = np.concatenate(parts); a = a / np.abs(a).max() * .95; sf.write("audition.wav", np.stack([a, a], 1), SR)
