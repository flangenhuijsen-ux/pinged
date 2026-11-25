import numpy as np, soundfile as sf, scipy.signal as sg, json
O="/home/claude/lock2/out/"; LO="/home/claude/lock/out/"; tl=json.load(open(O+"tl.json")); DUR=tl["DUR"]; VS={int(k):v for k,v in tl["VSTART"].items()}
T=tl["T"]; T_A,T_B,T_BL,T_C1,T_C2,T_C3,T_D,T_F,T_G,T_E,T_Q,T_H,T_P=[T[k] for k in "A B BL C1 C2 C3 D F G E Q H P".split()]
SR=44100; n=int(SR*DUR); rng=np.random.default_rng(11)
def lp(x,fc,o=2): b,a=sg.butter(o,fc/(SR/2)); return sg.lfilter(b,a,x,axis=0)
def hp(x,fc,o=2): b,a=sg.butter(o,fc/(SR/2),'high'); return sg.lfilter(b,a,x,axis=0)
def place(buf,x,at,pan=0.0):
    k=int(at*SR)
    if k<0: x=x[-k:]; k=0
    x=x[:max(0,n-k)]
    if x.ndim==1: x=np.stack([x*np.sqrt((1-pan)/2)*1.414,x*np.sqrt((1+pan)/2)*1.414],1)
    buf[k:k+len(x)]+=x
def reverb(x,rt=1.8,mix=0.3):
    m=int(SR*rt); out=np.zeros_like(x)
    for c in range(2):
        ir=rng.standard_normal(m)*np.exp(-np.arange(m)/(SR*rt/5)); ir=lp(ir,7000); ir/=np.sqrt((ir**2).sum())
        out[:,c]=x[:,c]*(1-mix)+sg.fftconvolve(x[:,c],ir)[:len(x)]*mix
    return out
def peak(m,a,b):
    h=int(SR*0.01); e=np.array([np.abs(m[i:i+h]).max() for i in range(int(a*SR),int(b*SR),h)])
    # first moment env reaches 70% of local max
    return a+np.argmax(e>=0.7*e.max())*0.01
# ---------- voice
v=np.zeros(n)
for i,s in VS.items():
    a,_=sf.read(f"{O}vo44_{i}.wav"); k=int(s*SR); a=a[:n-k]; v[k:k+len(a)]+=a
v=v/np.abs(v).max()*0.92
# gentle presence + tiny room so the voice sits in the music
b_,a_=sg.iirpeak(3200/(SR/2),1.2); v=v+0.25*sg.lfilter(b_,a_,v)
V=np.stack([v,v],1); V=V+0.06*(reverb(V,0.7,1.0))
# ---------- Lyria A (tension) under 0 -> question
A,_=sf.read(LO+"lyria_in.wav"); B,_=sf.read(LO+"lyria_b.wav")
mA=A.mean(1); mB=B.mean(1)
pA=peak(mA,46.0,46.7); pB=peak(mB,2.0,2.7)
mus=np.zeros((n,2))
st=T_BL-pA                                   # big entry of the track lands on "turn blue"
src0=max(0,-st); seg=A[int(src0*SR):int((T_Q+0.9-st)*SR)].copy()
k=int(2.0*SR); seg[:k]*=np.linspace(0,1,k)[:,None]**1.5
k=int(1.3*SR); seg[-k:]*=(np.cos(np.linspace(0,np.pi/2,k))**2)[:,None]
place(mus,seg,st+src0)
print("A src",round(src0,2),"->",round(T_Q+0.9-st,2),"entry at",T_BL)
# reveal: Lyria B, its hit on the word "DeepSeek"
stB=T_H-pB; segB=B[:int((DUR-stB)*SR)+1].copy(); segB=0.75*lp(segB,2600)+0.25*segB; gB=np.interp(np.arange(len(segB))/SR,[0,pB-0.5,pB,pB+0.25,pB+1.2,60],[0.75,0.75,0.42,0.42,0.6,0.6]); segB*=gB[:,None]
place(mus,segB,stB)
print("B starts",round(stB,2))
# ---------- sound design
fx=np.zeros((n,2)); low=np.zeros((n,2))
def chime(f,amp=0.11,d=1.4):
    tt=np.arange(int(d*SR))/SR; x=np.zeros(len(tt))
    for r,am,dec in ((1,1,4.5),(2.76,0.35,7),(5.4,0.18,11),(8.9,0.07,16)):
        x+=np.sin(2*np.pi*f*r*tt)*am*np.exp(-tt*dec)
    x*=np.minimum(1,tt/0.003); return x*amp
def notif(f1,f2):
    d=1.6; x=np.zeros(int(d*SR)); a=chime(f1); b=chime(f2,0.09); x[:len(a)]+=a; k=int(0.095*SR); x[k:k+len(b)]+=b[:len(x)-k]; return x
def haptic(amp=0.16):
    tt=np.arange(int(0.26*SR))/SR; env=np.hanning(len(tt))*(0.55+0.45*np.sign(np.sin(2*np.pi*7.5*tt+0.3)))
    return lp(np.sin(2*np.pi*152*tt)+0.3*np.sin(2*np.pi*304*tt),900)*env*amp
def whoosh(d=0.42,amp=0.07):
    tt=np.arange(int(d*SR))/SR; x=rng.standard_normal(len(tt)); fc=600+3200*np.sin(np.pi*tt/d)**2
    y=np.zeros(len(tt)); s=0.0
    for i in range(len(tt)):
        al=1-np.exp(-2*np.pi*fc[i]/SR); s+=al*(x[i]-s); y[i]=s
    return hp(y,300)*np.sin(np.pi*tt/d)**2*amp
W=whoosh()
def err(amp=0.10):
    tt=np.arange(int(0.34*SR))/SR; x=np.zeros(len(tt))
    for j,f in enumerate((392.0,277.2)):
        k=int(j*0.13*SR); sg_=np.sign(np.sin(2*np.pi*f*tt))*0.35+np.sin(2*np.pi*f*tt); x[k:]+=(lp(sg_,2200)*np.exp(-tt*9))[:len(tt)-k]
    return x*amp
def glitch(d=0.3,amp=0.09):
    m=int(d*SR); x=np.zeros(m)
    for _ in range(9):
        k=int(rng.integers(0,m-900)); L=int(rng.integers(200,900)); f=rng.uniform(300,5000); tt=np.arange(L)/SR
        x[k:k+L]+=np.sign(np.sin(2*np.pi*f*tt))*rng.uniform(0.3,1)
    return hp(x,400)*amp
place(fx,W,T_A-0.30); place(fx,notif(987.8,1318.5),T_A,-0.1); place(low,haptic(),T_A+0.02)
for at,pan in ((T_B,0.15),(T_C1,-0.3),(T_C2,0.3),(T_C3,-0.2),(T_D,0.2),(T_E,0.0)):
    place(fx,W,at-0.30,-pan); place(fx,err(),at,pan); place(fx,glitch(0.22,0.05),at,-pan); place(low,haptic(),at+0.02)
place(fx,glitch(0.45,0.13),T_BL); place(fx,glitch(0.3,0.08),T_F)
# clock spin ticks; fast rewind on the reveal
for tk in (T_A,T_C1,T_D,T_F,T_E):
    for j in range(16):
        tt=np.arange(int(0.012*SR))/SR; c=hp(rng.standard_normal(len(tt)),2500)*np.exp(-tt*500)*0.05+np.sin(2*np.pi*(2100+j*45)*tt)*np.exp(-tt*400)*0.03
        place(fx,c,tk-0.95+0.9*(j/16)**0.8,pan=-0.5+j/16)
for j in range(34):
    u=j/34; tt=np.arange(int(0.014*SR))/SR
    place(fx,np.sin(2*np.pi*(3200-1700*u)*tt)*np.exp(-tt*350)*0.045,T_H+0.05+0.88*u**0.7,pan=0.5-u)
place(fx,chime(880,0.08,1.6),T_H+0.95)
# impacts: sub drop + air
def subdrop(d,f0,f1,amp):
    tt=np.arange(int(d*SR))/SR; f=f1+(f0-f1)*np.exp(-tt*5); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.9)
    x+=lp(rng.standard_normal(len(tt)),220)*np.exp(-tt*10)*0.6; x*=np.minimum(1,tt/0.004); return np.tanh(x*1.6)*amp
def revswell(d,amp):
    tt=np.arange(int(d*SR))/SR; x=hp(lp(rng.standard_normal(len(tt)),5000),700)*(tt/d)**3.2; return x*amp
place(low,subdrop(2.6,100,32,0.60),T_BL); place(low,subdrop(2.2,90,36,0.36),T_E)
place(fx,revswell(1.3,0.10),T_F-1.3); place(low,subdrop(3.0,110,30,0.62),T_F)
place(low,subdrop(2.6,70,40,0.13),T_H)
# counting ticks under the number, rising, ending in a stamp
for j in range(40):
    u=j/40; tt=np.arange(int(0.022*SR))/SR
    place(fx,np.sin(2*np.pi*(1100+1300*u)*tt)*np.exp(-tt*220)*0.055,T_F+0.25+2.0*(1-(1-u)**2),pan=0.4*np.sin(j))
place(fx,chime(440,0.10,1.8),T_F+2.27)
# reveal sparkle on the price pill
for j,f in enumerate((1174.66,1479.98,1760.0,2349.32,2959.96,3520.0)):
    place(fx,chime(f,0.02,2.4),T_P+0.02+j*0.06,pan=-0.6+0.24*j)
place(fx,chime(587.33,0.05,3.0),T_H+0.02)
fx=reverb(fx,2.0,0.30); low=reverb(low,1.2,0.12)
# ---------- mix: music ducks under the voice, breath of silence before the name
b_,a_=sg.butter(1,6/(SR/2)); env=sg.filtfilt(b_,a_,np.abs(v)); env/=env.max()
duck=(1-0.52*np.clip(env*4,0,1))[:,None]
def rms(x): return np.sqrt((x**2).mean())
mus*=0.20/max(rms(mus[int(14*SR):int(26*SR)]),1e-6)*0.62     # climax of A sits at a known level
gate=np.ones(n); k0,k1=int((T_H-0.20)*SR),int((T_H-0.015)*SR); r=int(0.03*SR)
gate[k0:k1]=0.3; gate=np.convolve(gate,np.ones(r)/r,'same')
auto=np.interp(np.arange(n)/SR,[0,T_BL-0.6,T_BL,T_F,T_Q,T_H-0.3,T_H,DUR],[0.8,0.85,1.05,1.1,1.0,1.0,0.8,0.8])
mix=V*0.98+mus*duck*(gate*auto)[:,None]+fx*0.9+low*(0.75+0.25*duck)
mix=np.tanh(mix*1.2)/1.2
k=int(1.0*SR); mix[-k:]*=(np.cos(np.linspace(0,np.pi/2,k))**1.5)[:,None]; mix=mix/np.abs(mix).max()*0.89
sf.write(O+"mix3.wav",mix,SR)
M=(mus*duck*(gate*auto)[:,None]).mean(1); sp=env>0.25; print("during speech: voice",round(20*np.log10(rms(v[sp])),1),"music",round(20*np.log10(rms(M[sp])),1)," gaps music",round(20*np.log10(rms(M[~sp])),1))
for nm,x in (("voice",V),("music",mus*duck*(gate*auto)[:,None]),("fx",fx),("low",low)): print(nm,round(20*np.log10(rms(x)+1e-9),1))
w=SR; mm=mix.mean(1); print(' '.join(f'{20*np.log10(rms(mm[i:i+w])+1e-9):.0f}' for i in range(0,n-w,w)))
