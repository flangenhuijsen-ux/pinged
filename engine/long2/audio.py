import json, sys, numpy as np, soundfile as sf, scipy.signal as sg
story=sys.argv[1]; O=f"/home/claude/{story}/out/"; tl=json.load(open(O+"tl.json")); DUR=tl["DUR"]; V_=tl["V"]; SR=44100; n=int(DUR*SR); rng=np.random.default_rng(4)
def lp(x,fc): b,a=sg.butter(2,fc/(SR/2)); return sg.lfilter(b,a,x,axis=0)
v=np.zeros(n)
for i,t0 in enumerate(V_):
    if not tl["has"][i]: continue
    a,_=sf.read(f"{O}w{i}.wav"); k=int((t0+0.02)*SR); a=a[:n-k]; v[k:k+len(a)]+=a
v=v/np.abs(v).max()*0.92; b_,a_=sg.iirpeak(3200/(SR/2),1.2); v=v+0.22*sg.lfilter(b_,a_,v); V=np.stack([v,v],1)
A,_=sf.read("/home/claude/lock/out/lyria_in.wav"); Bq,_=sf.read("/home/claude/lock/out/lyria_b.wav")
seg=A[int(1*SR):int(90*SR)]; xf=int(4*SR); bed=np.zeros((n,2)); pos=0; first=True
while pos<n:
    s_=seg.copy()
    if not first: s_[:xf]*=np.linspace(0,1,xf)[:,None]
    s_[-xf:]*=np.linspace(1,0,xf)[:,None]; m=min(len(s_),n-pos); bed[pos:pos+m]+=s_[:m]; pos+=len(seg)-xf; first=False
bed=lp(bed,6000)
def rms(x): return np.sqrt((x**2).mean())
bed*=0.095/max(rms(bed),1e-6)
for u0 in tl["unlock"]:                      # the hidden notification opens: soft reveal track, hit aligned with the unlock
    k=int(max(0,u0-2.4)*SR); rb=lp(Bq,3000)[:min(len(Bq),int(26*SR),n-k)]*0.42; f=int(5*SR); rb[-f:]*=np.linspace(1,0,f)[:,None]; rb*=0.11/max(rms(rb),1e-6); bed[k:k+len(rb)]*=0.45; bed[k:k+len(rb)]+=rb
b_,a_=sg.butter(1,6/(SR/2)); env=sg.filtfilt(b_,a_,np.abs(v)); env/=env.max(); duck=(1-0.55*np.clip(env*4,0,1))[:,None]
fx=np.zeros((n,2))
def put(x,at,pan=0.0):
    k=int(max(0,at)*SR); x=x[:max(0,n-k)]; fx[k:k+len(x),0]+=x*(1-pan)*0.7; fx[k:k+len(x),1]+=x*(1+pan)*0.7
def chime(f,amp,d=1.2):
    tt=np.arange(int(d*SR))/SR; return sum(np.sin(2*np.pi*f*r*tt)*am*np.exp(-tt*dc) for r,am,dc in ((1,1,5.5),(2.76,.35,8),(5.4,.18,12)))*amp
def buzz(amp=0.16):
    tt=np.arange(int(0.34*SR))/SR; e=(np.clip(np.sin(2*np.pi*tt/0.17),0,1)**.5)*((tt%0.17)<0.11); x=np.sign(np.sin(2*np.pi*155*tt))*e; return lp(x,420)*amp
def boom(amp=0.36):
    tt=np.arange(int(2.2*SR))/SR; f=34+(110-34)*np.exp(-tt*7); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.2)*amp
def riser(d=0.7,amp=0.09):
    tt=np.arange(int(d*SR))/SR; x=rng.standard_normal(len(tt)+4096); out=np.zeros(len(tt)); st=2048
    for k in range(0,len(tt),st):
        fc=400+5200*(k/len(tt))**2; b,a=sg.butter(2,[fc*.7/(SR/2),min(.95,fc*1.4/(SR/2))],"band"); m=len(out[k:k+st]); out[k:k+st]=sg.lfilter(b,a,x[k:k+st])[:m]
    return out*(tt/d)**2*amp
def tick(f=1500,amp=0.035):
    tt=np.arange(int(0.02*SR))/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*240)*amp
def noise(d,amp,lo=800,hi=6000):
    x=rng.standard_normal(int(d*SR)); b,a=sg.butter(2,[lo/(SR/2),hi/(SR/2)],"band"); return sg.lfilter(b,a,x)*amp
BZ=buzz(); C1=chime(987.8,0.045); C2=chime(1318.5,0.035); BM=boom(); RS=riser()
for c in tl["cards"]: put(BZ,c,-0.1); put(C1,c+0.02,-0.2); put(C2,c+0.11,-0.2)
for t0,cd in tl["slam"]:
    land=t0+cd
    if cd:
        for j in range(26): u=j/26; put(tick(1000+1500*u),t0+cd*(1-(1-u)**2),0.2)
    put(RS,land-0.7); put(BM,land); put(noise(0.25,0.06,200,2500)*np.linspace(1,0,int(0.25*SR)),land)
for g0,gd in tl["glitch"]:
    x=noise(gd,0.045,1500,9000); st=int(0.03*SR)
    for k in range(0,len(x),st*2): x[k:k+st]*=0.15
    put(x,g0)
for r0,r1 in tl["rew"]:
    d=r1-r0; tt=np.arange(int(d*SR))/SR; f=1800*np.exp(-tt*1.6)+200; put(np.sin(2*np.pi*np.cumsum(f)/SR)*0.05*np.sin(np.pi*tt/d)**.5+noise(d,0.03,400,3000)*np.sin(np.pi*tt/d),r0)
for a,b in tl["spin"]:
    k=0
    while a+k*0.045<b: put(tick(2100,0.022),a+k*0.045,0.3); k+=1
for t0 in tl["clear"]: put(noise(0.3,0.035,900,5000)*np.linspace(0,1,int(0.3*SR))**2,t0-0.25)
for t0 in tl["hidden"]: put(chime(440,0.05,2.0),t0); put(chime(554.4,0.035,2.0),t0+0.08)
for t0 in tl["unlock"]: put(chime(440,0.06,2.5),t0); put(chime(554.4,0.05,2.5),t0+0.1); put(chime(659.3,0.05,2.5),t0+0.2)
for t0 in tl["dates"]: put(tick(700,0.05),t0)
mix=V*0.95+bed*duck+fx; mix=np.tanh(mix*1.15)/1.15
k=int(0.8*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]; mix=mix/np.abs(mix).max()*0.89
sf.write(O+"mix.wav",mix,SR); sp=env>0.25; M=(bed*duck).mean(1)
print("voice",round(20*np.log10(rms(v[sp])),1),"music under voice",round(20*np.log10(rms(M[sp])),1),"fx peak",round(20*np.log10(np.abs(fx.mean(1)).max()),1),"dur",round(DUR,1))
