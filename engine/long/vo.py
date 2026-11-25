import sys, json, soundfile as sf, subprocess
sys.path.insert(0,"/home/claude/long"); from script import L
from kokoro_onnx import Kokoro
M="/mnt/user-data/uploads/research--morpheus/model/"; O="/home/claude/long/out/"
a,b=int(sys.argv[1]),int(sys.argv[2])
k=Kokoro(M+"kokoro-v1.0.int8.onnx",M+"voices-v1.0.bin")
style=0.5*k.voices["am_onyx"]+0.25*k.voices["am_echo"]+0.25*k.voices["am_michael"]
D={}
for i in range(a,b):
    x,sr=k.create(L[i]["text"],voice=style,speed=1.13,lang="en-us"); sr2=int(round(sr*0.86)); sf.write(f"{O}v{i}.wav",x,sr2); D[i]=round(len(x)/sr2,3)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{O}v{i}.wav","-af","aresample=44100,highpass=f=60","-ac","1",f"{O}w{i}.wav"],check=True)
json.dump(D,open(f"{O}d_{a}.json","w")); print(a,b,round(sum(D.values()),1))
