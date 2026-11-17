"""1-1화 「합격」 완성본: Flow 클립 4개 + 근무지 표 컷 + 끝 카드.

사용: python3 make_ep1_1_final.py <클립 폴더> <그림 폴더> <출력.mp4>
클립 폴더: c1.mp4(그림1 마우스) c2.mp4(그림2 합격 화면) c3.mp4(그림3 환호) c4.mp4(그림4 통화)
그림 폴더: 5.png (근무지 표)
"""
import math
import random
import struct
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS, RATE = 1080, 1920, 24, 44100  # Flow 클립과 같은 초당 24장
FONT = "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf"
clips, pics, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
voice_file = Path(sys.argv[4]) if len(sys.argv) > 4 else None  # ElevenLabs 등으로 만든 1-1화 대사 한 파일
work = out.parent / "_work"
work.mkdir(parents=True, exist_ok=True)


def font(size):
    return ImageFont.truetype(FONT, size)


def subtitle(fr, text, y=0.70, size=76, color="white"):
    d = ImageDraw.Draw(fr)
    f = font(size)
    box = d.textbbox((0, 0), text, font=f, stroke_width=6)
    d.text(((W - (box[2] - box[0])) / 2, H * y), text, font=f, fill=color, stroke_width=6, stroke_fill="black")


def tag(fr, text):
    d = ImageDraw.Draw(fr)
    f = font(56)
    box = d.textbbox((0, 0), text, font=f)
    d.rounded_rectangle((60, 250, 60 + box[2] - box[0] + 64, 354), 26, fill=(0, 0, 0))
    d.text((92, 270), text, font=f, fill="white")


def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def view(img, cx, cy, zoom):
    iw, ih = img.size
    base = max(W / iw, H / ih)
    vw, vh = W / (base * zoom), H / (base * zoom)
    x0 = min(max(cx * iw - vw / 2, 0), iw - vw)
    y0 = min(max(cy * ih - vh / 2, 0), ih - vh)
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))


def mosaic(img, box, block=26):
    iw, ih = img.size
    x0, y0, x1, y1 = (int(box[0] * iw), int(box[1] * ih), int(box[2] * iw), int(box[3] * ih))
    piece = img.crop((x0, y0, x1, y1))
    small = piece.resize((max(1, (x1 - x0) // block), max(1, (y1 - y0) // block)), Image.BILINEAR)
    res = img.copy()
    res.paste(small.resize(piece.size, Image.NEAREST), (x0, y0))
    return res


def clip_frames(path):
    """클립을 1080x1920, 30fps 프레임으로 읽는다."""
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(path), "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    size = W * H * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield Image.frombytes("RGB", (W, H), buf)
    p.wait()


def clip_audio(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(RATE), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return [s / 32768 for s in struct.unpack(f"<{len(raw) // 2}h", raw)]


# 대사 파일 속 각 줄의 위치(초)와 컷 안에서 시작할 시각(초)
LINES = {  # 줄: (파일에서 시작, 끝)
    1: (0.15, 3.25), 2: (3.50, 5.18), 3: (5.22, 7.38), 4: (7.40, 9.52), 5: (10.02, 11.32), 6: (11.34, 12.90)}
PLACE = {"c1.mp4": [(1, 0.6)], "c3.mp4": [(2, 0.45)], "c4.mp4": [(3, 0.35), (4, 3.4)], "table": [(5, 0.6), (6, 2.9)]}
voice = clip_audio(voice_file) if voice_file else None


def with_voice(key, base):
    """voice가 있으면 그 컷의 원래 목소리를 빼고 대사 줄을 얹는다."""
    if voice is None or key not in PLACE:
        return base
    if key != "table":  # 원래 클립 소리(Flow 목소리)를 빼고 아주 작은 방 소음만 깐다
        rnd, lp, mixed = random.Random(7), 0.0, []
        for _ in base:
            lp = 0.985 * lp + 0.015 * rnd.uniform(-1, 1)
            mixed.append(lp * 0.05)
    else:
        mixed = list(base)
    for line, at in PLACE[key]:
        a, b = LINES[line]
        piece = voice[int(a * RATE):int(b * RATE)]
        fade = int(0.03 * RATE)
        for i, v in enumerate(piece):
            g = min(1, i / fade, (len(piece) - i) / fade)
            j = int(at * RATE) + i
            if j < len(mixed):
                mixed[j] += v * g
    return mixed


def say(line, key):
    """대사 줄이 그 컷 안에서 나오는 구간 (자막 시간)."""
    if voice is None:
        return None
    for ln, at in PLACE.get(key, []):
        if ln == line:
            a, b = LINES[line]
            return at, at + (b - a) + 0.15
    return None


def show(t, line, key, default):
    rng = say(line, key) or default
    return rng[0] <= t < rng[1]


# 컷 목록: (클립 경로 또는 None, 길이(초), 자막 함수)
def subs_c1(fr, t):
    if t < 2.0:
        tag(fr, "수험 생활 3년")
    if show(t, 1, "c1.mp4", (2.2, 3.95)):
        subtitle(fr, "제발… 제발…")


def subs_c3(fr, t):
    a, b = say(2, "c3.mp4") or (0.6, 3.6)
    mid = a + (b - a) * 0.45
    if a < t < mid:
        subtitle(fr, "됐다!!!", size=96)
    elif mid <= t < b:
        subtitle(fr, "붙었다!!!", size=96)


def subs_c4(fr, t):
    if show(t, 3, "c4.mp4", (0, 2.3)):
        subtitle(fr, "엄마! 나 붙었어!")
    elif show(t, 4, "c4.mp4", (2.4, 6.9)):
        subtitle(fr, "응, 공기업! 정년 보장!")


img5 = mosaic(Image.open(pics / "5.png").convert("RGB"), (0.44, 0.584, 0.905, 0.637))


def table(t, d=6.0):  # 표를 훑어 내려가 모자이크 된 근무지 줄로 확대
    k = ease(t / 4.2)
    fr = view(img5, 0.5 - 0.10 * k, 0.36 + 0.25 * k, 1.0 + 0.8 * k)
    if show(t, 5, "table", (0.6, 2.6)):
        subtitle(fr, "어디 보자…", y=0.75)
    elif show(t, 6, "table", (3.0, 5.6)):
        subtitle(fr, "근무지가…", y=0.75)
    return Image.blend(fr, Image.new("RGB", (W, H), "black"), min(max((t - 5.6) / 0.4, 0), 1))


def end_card(t):
    fr = Image.new("RGB", (W, H), "black")
    if t > 0.5:
        subtitle(fr, "근무지는 2편에서", y=0.44, size=84)
        subtitle(fr, "흙수저 김토토  1-1", y=0.52, size=44, color=(150, 150, 150))
    return fr


def encode(path, frames, audio):
    """프레임과 소리로 구간 하나를 만든다."""
    wav = path.with_suffix(".wav")
    with wave.open(str(wav), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in audio))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-shortest", str(path)], stdin=subprocess.PIPE)
    n = 0
    for fr in frames:
        enc.stdin.write(fr.tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    return n / FPS


segments = []  # (파일, 길이)
for idx, (name, subs) in enumerate((("c1.mp4", subs_c1), ("c2.mp4", None), ("c3.mp4", subs_c3), ("c4.mp4", subs_c4))):
    def frames(name=name, subs=subs):
        for n, fr in enumerate(clip_frames(clips / name)):
            if subs:
                subs(fr, n / FPS)
            yield fr
    seg = work / f"seg{idx}.mov"
    segments.append((seg, encode(seg, frames(), with_voice(name, clip_audio(clips / name)))))

random.seed(3)
drone = [0.06 * (i / RATE / 5.6) * math.sin(2 * math.pi * (55 - 2 * i / RATE) * i / RATE) if i < 5.6 * RATE else 0.0
         for i in range(6 * RATE)]
seg = work / "seg4.mov"
segments.append((seg, encode(seg, (table(i / FPS) for i in range(6 * FPS)), with_voice("table", drone))))
seg = work / "seg5.mov"
segments.append((seg, encode(seg, (end_card(i / FPS) for i in range(3 * FPS)), [0.0] * (3 * RATE))))

# 컷 사이 장면 전환 (그림 1→2→3→4는 짧은 디졸브, 표 컷 앞은 흰 번쩍임 대신 디졸브, 끝 카드는 페이드)
XF = [0.25, 0.25, 0.25, 0.35, 0.3]
inputs, vf, af = [], [], []
for f, _ in segments:
    inputs += ["-i", str(f)]
prev_v, prev_a, offset = "0:v", "0:a", segments[0][1]
for k in range(1, len(segments)):
    d = XF[k - 1]
    offset -= d
    vf.append(f"[{prev_v}][{k}:v]xfade=transition=fade:duration={d}:offset={offset:.3f}[v{k}]")
    af.append(f"[{prev_a}][{k}:a]acrossfade=d={d}:c1=tri:c2=tri[a{k}]")
    prev_v, prev_a = f"v{k}", f"a{k}"
    offset += segments[k][1]
last = len(segments) - 1
# 소리 다듬기: 저음 웅웅거림 제거, 목소리 크기 고르게, 인스타 기준 음량(-14 LUFS)
af.append(f"[a{last}]highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(vf + af),
                "-map", f"[v{last}]", "-map", "[aout]", "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
for f, _ in segments:
    f.unlink(missing_ok=True); f.with_suffix(".wav").unlink(missing_ok=True)
work.rmdir()
print("완성:", out)
