import json, numpy as np, soundfile as sf, scipy.signal as sg
O="/home/claude/long/out/"; tl=json.load(open(O+"tl.json")); DUR=tl["DUR"]; EV=tl["EV"]; SR=44100; n=int(DUR*SR); rng=np.random.default_rng(4)
def lp(x,fc): b,a=sg.butter(2,fc/(SR/2)); return sg.lfilter(b,a,x,axis=0)
v=np.zeros(n)
for e in EV:
    if e["kind"]!="line": continue
    a,_=sf.read(f"{O}w{e['i']}.wav"); k=int(e["vo"]*SR); a=a[:n-k]; v[k:k+len(a)]+=a
v=v/np.abs(v).max()*0.92; b_,a_=sg.iirpeak(3200/(SR/2),1.2); v=v+0.22*sg.lfilter(b_,a_,v); V=np.stack([v,v],1)
# music bed: Lyria tension track looped with long crossfades, reveal track under the final chapter
A,_=sf.read("/home/claude/lock/out/lyria_in.wav"); B,_=sf.read("/home/claude/lock/out/lyria_b.wav")
seg=A[int(1*SR):int(90*SR)]; xf=int(4*SR); bed=np.zeros((n,2)); pos=0
while pos<n:
    s_=seg.copy(); s_[:xf]*=np.linspace(0,1,xf)[:,None]; s_[-xf:]*=np.linspace(1,0,xf)[:,None]
    m=min(len(s_),n-pos); bed[pos:pos+m]+=s_[:m]; pos+=len(seg)-xf
t5=next(e["t0"] for e in EV if e["ch"]==5); k5=int(t5*SR); fade=int(3*SR)
bed[k5:k5+fade]*=np.linspace(1,0.35,fade)[:,None]; bed[k5+fade:]*=0.35
rb=lp(B,3000)[:n-k5]*0.5; bed[k5:k5+len(rb)]+=rb
bed=lp(bed,5200)
b_,a_=sg.butter(1,6/(SR/2)); env=sg.filtfilt(b_,a_,np.abs(v)); env/=env.max(); duck=(1-0.6*np.clip(env*4,0,1))[:,None]
def rms(x): return np.sqrt((x**2).mean())
bed*=0.075/max(rms(bed),1e-6)
fx=np.zeros((n,2))
def chime(f,amp,d=1.4):
    tt=np.arange(int(d*SR))/SR; return sum(np.sin(2*np.pi*f*r*tt)*am*np.exp(-tt*dc) for r,am,dc in ((1,1,4.5),(2.76,.35,7),(5.4,.18,11)))*amp
def put(x,at,pan=0.0):
    k=int(at*SR); x=x[:max(0,n-k)]; fx[k:k+len(x),0]+=x*(1-pan)*0.7; fx[k:k+len(x),1]+=x*(1+pan)*0.7
for e in EV:
    if e["kind"]=="title":
        tt=np.arange(int(2.4*SR))/SR; f=38+(90-38)*np.exp(-tt*5); boom=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.8)*0.32; put(boom,e["t0"]+0.05); put(chime(293.66,0.05,2.4),e["t0"]+0.05)
    elif e["card"]: put(chime(987.8,0.05),e["t0"]+0.02,-0.5); put(chime(1318.5,0.04),e["t0"]+0.12,-0.5)
    if e["kind"]=="line" and e["count"]:
        for j in range(36):
            u=j/36; tt=np.arange(int(0.02*SR))/SR; put(np.sin(2*np.pi*(1100+1200*u)*tt)*np.exp(-tt*220)*0.04,e["t0"]+0.3+2.2*(1-(1-u)**2),0.3)
mix=V*0.95+bed*duck+fx; mix=np.tanh(mix*1.15)/1.15
k=int(1.0*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]; mix=mix/np.abs(mix).max()*0.89
sf.write(O+"mix.wav",mix,SR); sp=env>0.25; M=(bed*duck).mean(1)
print("voice",round(20*np.log10(rms(v[sp])),1),"music under voice",round(20*np.log10(rms(M[sp])),1),"dur",round(DUR,1))
