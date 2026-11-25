import json, soundfile as sf, subprocess
from kokoro_onnx import Kokoro
M="/mnt/user-data/uploads/research--morpheus/model/"; O="/home/claude/lock2/out/"
L=["Friday, July nineteenth, twenty twenty-four.",
"At four oh nine, universal time, a routine security update goes out.",
"Minutes later, screens around the world turn blue.",
"Airlines. Banks. Hospitals.",
"More than five thousand flights, cancelled.",
"Eight and a half million computers. Crashed.",
"The estimated bill: five point four billion dollars.",
"And the faulty update?",
"Seventy-eight minutes.",
"That's how long it was online."]
k=Kokoro(M+"kokoro-v1.0.int8.onnx",M+"voices-v1.0.bin")
style=0.5*k.voices["am_onyx"]+0.25*k.voices["am_echo"]+0.25*k.voices["am_michael"]
D=[]
for i,l in enumerate(L):
    s,sr=k.create(l,voice=style,speed=1.13,lang="en-us"); sr2=int(round(sr*0.86)); sf.write(f"{O}vo_{i}.wav",s,sr2); D.append(round(len(s)/sr2,3))
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{O}vo_{i}.wav","-af","aresample=44100,highpass=f=60","-ac","1",f"{O}vo44_{i}.wav"],check=True)
json.dump(D,open(O+"vo.json","w")); print(D,sum(D))
