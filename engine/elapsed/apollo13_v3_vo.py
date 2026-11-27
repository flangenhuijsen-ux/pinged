import json, soundfile as sf, subprocess
from kokoro_onnx import Kokoro
VO = ["Two minutes before Houston, we've had a problem, Apollo 13 sent one word.",
      "April thirteenth, 1970. Three men, more than two hundred thousand miles from Earth.",
      "Houston sends a routine request.",
      "Stir up your cryo tanks.",
      "The reply is one word. Okay.",
      "Inside oxygen tank two, a fan switches on. Its wiring is damaged.",
      "Ninety seconds later, the tank bursts.",
      "Okay, Houston, we've had a problem here.",
      "Houston's first answer? Say again, please.",
      "Their oxygen is pouring into space. The lunar module, Aquarius, becomes their lifeboat.",
      "More than three days later, they finally see the damage. A whole panel is gone.",
      "On April seventeenth, all three came home.",
      "Follow. Every second is on the record."]
M = "/mnt/user-data/uploads/research--morpheus/model/"; O = "/home/claude/a13v3/out/"
k = Kokoro(M + "kokoro-v1.0.int8.onnx", M + "voices-v1.0.bin"); st = 0.6 * k.voices["bm_george"] + 0.4 * k.voices["bm_lewis"]; D = {}
for i, tx in enumerate(VO):
    x, sr = k.create(tx, voice=st, speed=1.12, lang="en-gb"); sf.write(f"{O}v{i}.wav", x, sr); D[i] = round(len(x) / sr, 3)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{O}v{i}.wav", "-af", "aresample=44100,highpass=f=70", "-ac", "1", f"{O}w{i}.wav"], check=True)
json.dump(dict(D=D, VO=VO), open(O + "d.json", "w")); print(D, round(sum(D.values()), 1))
