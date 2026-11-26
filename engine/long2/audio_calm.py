import json, sys, os, glob, numpy as np, soundfile as sf, scipy.signal as sg
story=sys.argv[1]; O=f"/home/claude/{story}/out/"; tl=json.load(open(O+"tl.json")); DUR=tl["DUR"]; V_=tl["V"]; SR=44100; n=int(DUR*SR); rng=np.random.default_rng(4)
def lp(x,fc): b,a=sg.butter(2,fc/(SR/2)); return sg.lfilter(b,a,x,axis=0)
def hp(x,fc): b,a=sg.butter(2,fc/(SR/2),"high"); return sg.lfilter(b,a,x,axis=0)
def rms(x): return np.sqrt((x**2).mean())
v=np.zeros(n)
for i,t0 in enumerate(V_):
    if not tl["has"][i]: continue
    a,_=sf.read(f"{O}w{i}.wav"); k=int((t0+0.02)*SR); a=a[:n-k]; v[k:k+len(a)]+=a
v=v/np.abs(v).max()*0.92; b_,a_=sg.iirpeak(3200/(SR/2),1.2); v=v+0.22*sg.lfilter(b_,a_,v); V=np.stack([v,v],1)
CH=[0.0]+[V_[i] for i in range(len(V_)) if not tl["has"][i]]+[DUR]          # chapter starts = title cards
# ---- bed: one calm piece per chapter. Real tracks in /home/claude/music/long_*.wav are used when present; otherwise a soft synthesised pad (placeholder)
tracks=sorted(glob.glob("/home/claude/music/long_*.wav"))
PROG=[[(146.83,174.61,220.0,329.63),(130.81,164.81,196.0,293.66),(116.54,146.83,174.61,261.63),(110.0,146.83,164.81,246.94)],
      [(110.0,130.81,164.81,246.94),(98.0,123.47,146.83,220.0),(87.31,110.0,130.81,196.0),(98.0,123.47,146.83,246.94)],
      [(130.81,155.56,196.0,293.66),(116.54,146.83,174.61,261.63),(103.83,130.81,155.56,233.08),(116.54,146.83,174.61,293.66)]]
TUNE=432/440          # concert pitch A = 432 Hz
PROG=[[tuple(f*TUNE for f in ch) for ch in pr] for pr in PROG]
def pad(d,prog,seed):
    r=np.random.default_rng(seed); m=int(d*SR); out=np.zeros((m,2)); step=9.0; k=0; t=0.0
    while t<d:
        ch=prog[k%len(prog)]; L=int((step+4)*SR); tt=np.arange(L)/SR; env=np.clip(tt/3.5,0,1)*np.clip((step+4-tt)/4,0,1); env=env**1.5; x=np.zeros((L,2))
        for f in ch:
            for det,pan in ((-0.25,-.6),(0.2,.6),(0,0)):
                ph=r.uniform(0,6.28); s_=np.sin(2*np.pi*f*(1+det/100)*tt+ph)+0.45*np.sin(2*np.pi*2*f*(1+det/140)*tt+ph*1.3)+0.22*np.sin(2*np.pi*4*f*tt+ph*.7); s_*=(0.75+0.25*np.sin(2*np.pi*r.uniform(.05,.12)*tt+ph))
                x[:,0]+=s_*(1-pan)*.5; x[:,1]+=s_*(1+pan)*.5
        a=int(t*SR); x=x[:max(0,m-a)]; out[a:a+len(x)]+=x*env[:len(x),None]; t+=step; k+=1
    return lp(hp(out,150),3200)
bed=np.zeros((n,2)); xf=int(3*SR)
for c in range(len(CH)-1):
    a=int(max(0,CH[c]-1.5)*SR); b=min(n,int((CH[c+1]+1.5)*SR)); d=(b-a)/SR
    if tracks:
        x,_=sf.read(tracks[c%len(tracks)]); x=sg.resample_poly(x,55,54,axis=0) if "_432" not in tracks[c%len(tracks)] else x; x=x if x.ndim>1 else np.stack([x,x],1); reps=int(np.ceil((b-a)/len(x))); x=np.tile(x,(reps,1))[:b-a]
    else: x=pad(d,PROG[c%len(PROG)],c)
    x=x/max(rms(x),1e-9); f=min(xf,len(x)//3); x[:f]*=np.linspace(0,1,f)[:,None]; x[-f:]*=np.linspace(1,0,f)[:,None]; x=x[:b-a]; bed[a:a+len(x)]+=x
b_,a_=sg.butter(1,6/(SR/2)); env=sg.filtfilt(b_,a_,np.abs(v)); env/=env.max(); duck=(1-0.45*np.clip(env*4,0,1))[:,None]
bed*=10**(-12/20)*rms(v[env>0.25])/1.0/ (1-0.45)                      # -24 dB under the voice while speaking
BIG=[t for t,cd in tl["slam"] if cd]+tl["unlock"]                         # the few moments that get weight
for t0 in BIG:                                                              # music steps back 1.2 s before a big number
    a=int(max(0,t0-1.2)*SR); b=int((t0+0.6)*SR); g=np.ones(b-a); f=int(.5*SR); g[:f]=np.linspace(1,.25,f); g[f:-f]=.25; g[-f:]=np.linspace(.25,1,f); bed[a:b]*=g[:,None]
fx=np.zeros((n,2))
def put(x,at,pan=0.0):
    k=int(max(0,at)*SR); x=x[:max(0,n-k)]; fx[k:k+len(x),0]+=x*(1-pan)*0.7; fx[k:k+len(x),1]+=x*(1+pan)*0.7
def chime(f,amp,d=1.0):
    f=f*TUNE; tt=np.arange(int(d*SR))/SR; return sum(np.sin(2*np.pi*f*r*tt)*am*np.exp(-tt*dc) for r,am,dc in ((1,1,7),(2.76,.25,10)))*amp
def thud(amp):
    tt=np.arange(int(1.4*SR))/SR; f=40+(85-40)*np.exp(-tt*9); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*3.2)*amp
def tick(f=1500,amp=0.02):
    tt=np.arange(int(0.02*SR))/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*240)*amp
POP=chime(784,0.04,0.9); cold=V_[next(i for i in range(len(V_)) if not tl["has"][i])]
for c in tl["cards"]: put(POP,c,-0.15)                                     # one soft note per notification, no buzz
for t0,cd in tl["slam"]:
    land=t0+cd
    if cd:
        for j in range(18): u=j/18; put(tick(1000+900*u,0.015),t0+cd*(1-(1-u)**2),0.2)
        put(thud(0.26),land)
    else: put(thud(0.12),land)                                              # ordinary emphasis: barely there
for r0,r1 in tl["rew"]:
    d=r1-r0; tt=np.arange(int(d*SR))/SR; f=1200*np.exp(-tt*1.6)+200; put(np.sin(2*np.pi*np.cumsum(f)/SR)*0.03*np.sin(np.pi*tt/d)**.5,r0)
for t0 in tl["unlock"]: put(chime(440,0.05,2.5),t0); put(chime(554.4,0.04,2.5),t0+0.12); put(chime(659.3,0.04,2.5),t0+0.24); put(thud(0.2),t0)
for t0 in tl["hidden"]: put(chime(440,0.035,2.0),t0)
mix=V*0.95+bed*duck+fx; mix=np.tanh(mix*1.1)/1.1
k=int(0.8*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]; mix=mix/np.abs(mix).max()*0.89
sf.write(O+"mix_calm.wav",mix,SR); sp=env>0.25; M=(bed*duck).mean(1)
print("voice",round(20*np.log10(rms(v[sp])),1),"music under voice",round(20*np.log10(rms(M[sp])),1),"fx peak",round(20*np.log10(np.abs(fx.mean(1)).max()),1),"chapters",len(CH)-1,"tracks",len(tracks) or "synth pad","big moments",len(BIG))
sf.write(O+"bed_calm.wav",(bed/np.abs(bed).max()*0.5)[:int(96*SR)],SR)
