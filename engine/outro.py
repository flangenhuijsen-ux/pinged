import sys, subprocess, numpy as np, soundfile as sf, scipy.signal as sg, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, "/home/claude/brand")
FD = "/home/claude/bon2/fonts/"
def F(n, s): return ImageFont.truetype(FD + n, s)
W, H, FPS, CUT, SR = 1080, 1920, 30, 1.2, 44100
src, dst = sys.argv[1], sys.argv[2]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
t0 = dur - CUT
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", src, "-frames:v", "1", "/home/claude/outro/last.png"], check=True)
base = Image.open("/home/claude/outro/last.png").convert("RGB")
# ---- the PINGED notification card
CW, CH = 980, 300
def mark(S):
    s = S * 2; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], int(s * .22), fill=(10, 18, 32, 255))
    d.rounded_rectangle([s * .14, s * .24, s * .82, s * .80], int(s * .13), fill=(246, 248, 252, 255))
    d.text((s * .475, s * .55), "P", font=F("bebas.ttf", int(s * .58)), fill=(10, 14, 24, 255), anchor="mm")
    cx, cy, r = s * .80, s * .24, s * .135
    d.ellipse([cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2], fill=(10, 18, 32, 255)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 196, 90, 255))
    d.text((cx, cy + s * .008), "1", font=F("barlow-condensed-700.ttf", int(r * 1.55)), fill=(20, 16, 8, 255), anchor="mm")
    return im.resize((S, S), Image.LANCZOS)
card = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
d.rounded_rectangle([0, 0, CW - 1, CH - 1], 54, fill=(8, 14, 26, 236), outline=(255, 196, 90, 235), width=3)
card.alpha_composite(mark(150), (34, 34)); d = ImageDraw.Draw(card)
x = 214
for ch in "PINGED":
    d.text((x, 30), ch, font=F("barlow-condensed-600.ttf", 50), fill=(255, 255, 255, 215)); x += d.textlength(ch, font=F("barlow-condensed-600.ttf", 50)) + 5
d.text((CW - 40, 34), "NOW", font=F("ibm-plex-mono-600.ttf", 44), fill=(255, 196, 90, 235), anchor="ra")
d.text((214, 100), "New story tomorrow.", font=F("barlow-condensed-700.ttf", 84), fill=(255, 255, 255, 255))
d.text((214, 192), "Follow to get pinged.", font=F("barlow-condensed-600.ttf", 68), fill=(255, 196, 90, 255))
glow = Image.new("RGBA", (CW + 200, CH + 200), (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle([100, 100, CW + 100, CH + 100], 54, fill=(255, 196, 90, 120)); glow = glow.filter(ImageFilter.GaussianBlur(46))
vo, vsr = sf.read("/home/claude/outro/vo.wav"); vo = sg.resample_poly(vo, SR, vsr); vo = vo / np.abs(vo).max() * 0.9
LEN = 0.3 + len(vo) / SR + 0.5; n = int(LEN * FPS)
Y1 = 1500
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "/home/claude/outro/o.mp4"], stdin=subprocess.PIPE)
rng = np.random.default_rng(3)
for i in range(n):
    t = i / FPS; u = min(1, t / 0.5); e = 1 - (1 - u) ** 3; ov = 1 + 0.06 * np.sin(min(1, t / 0.7) * np.pi)   # ease-out with a small overshoot
    y = int(H + 40 - (H + 40 - Y1) * e * (1 + 0.02 * np.sin(min(1, t / 0.7) * np.pi)))
    fr = base.copy().convert("RGBA")
    dim = Image.new("RGBA", (W, H), (4, 6, 11, int(110 * e))); fr.alpha_composite(dim)
    pulse = 0.75 + 0.25 * np.sin(t * 5)
    g = glow.copy(); g.putalpha(g.getchannel("A").point(lambda a: int(a * e * pulse)))
    fr.alpha_composite(g, ((W - CW) // 2 - 100, y - 100)) if y - 100 < H else None
    if y < H: fr.alpha_composite(card.crop((0, 0, CW, min(CH, H - y))), ((W - CW) // 2, y))
    a = np.asarray(fr.convert("RGB")).astype(np.int16) + rng.normal(0, 3, (H, W, 1)).astype(np.int16)
    if t > LEN - 0.35: a = a * max(0, (LEN - t) / 0.35)
    p.stdin.write(np.clip(a, 0, 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
# ---- audio: original up to the cut (short fade), then chime + voice
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2", "-ar", str(SR), "/home/claude/outro/a.wav"], check=True)
A, _ = sf.read("/home/claude/outro/a.wav"); k = int(t0 * SR); head = A[:k].copy()
tail = A[k:k + int(LEN * SR)].copy(); tail = np.vstack([tail, np.zeros((int(LEN * SR) - len(tail), 2))]) * 0.5
o = np.zeros((int(LEN * SR), 2)) + tail
tt = np.arange(int(1.6 * SR)) / SR
for j, (f, at) in enumerate(((1174.66, 0.02), (1760.0, 0.12))):
    c = sum(np.sin(2 * np.pi * f * r * tt) * am * np.exp(-tt * dc) for r, am, dc in ((1, 1, 4.5), (2.76, .35, 7), (5.4, .18, 11))) * 0.07
    kk = int(at * SR); m = min(len(c), len(o) - kk); o[kk:kk + m] += c[:m, None]
pad = (np.sin(2 * np.pi * 146.83 * np.arange(len(o)) / SR) + 0.6 * np.sin(2 * np.pi * 220 * np.arange(len(o)) / SR)) * 0.018 * np.hanning(len(o)); o += pad[:, None]
kk = int(0.3 * SR); o[kk:kk + len(vo)] += vo[:, None] * 0.62
f = int(0.3 * SR); o[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write("/home/claude/outro/mix.wav", np.clip(np.vstack([head, o]), -0.98, 0.98), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", f"{t0:.3f}", "-i", src, "-i", "/home/claude/outro/o.mp4", "-i", "/home/claude/outro/mix.wav", "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst + ".tmp.mp4"], check=True)
import os; os.replace(dst + ".tmp.mp4", dst); print(dst, round(t0 + LEN, 2))
