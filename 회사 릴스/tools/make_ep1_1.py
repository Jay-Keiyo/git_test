"""1-1화 「합격」 가편집 영상(애니매틱) 생성기.

정지 그림에 확대·이동·흔들림과 자막만 얹어 흐름을 미리 본다.
사용: python3 make_ep1_1.py <그림 폴더> <출력.mp4>
"""
import math
import random
import struct
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf"
src_dir, out_path = sys.argv[1], sys.argv[2]


def font(size):
    return ImageFont.truetype(FONT, size)


def load(name):
    return Image.open(f"{src_dir}/{name}").convert("RGB")


def ease(t):
    return t * t * (3 - 2 * t)


def view(img, cx, cy, zoom, dx=0, dy=0):
    """(cx, cy)를 중심으로 zoom배 확대한 화면. 좌표는 원본 그림 기준 0~1."""
    iw, ih = img.size
    base = max(W / iw, H / ih)
    vw, vh = W / (base * zoom), H / (base * zoom)
    x0 = min(max(cx * iw - vw / 2 + dx, 0), iw - vw)
    y0 = min(max(cy * ih - vh / 2 + dy, 0), ih - vh)
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))


def subtitle(frame, text, y=0.70, size=76, color="white"):
    d = ImageDraw.Draw(frame)
    f = font(size)
    box = d.textbbox((0, 0), text, font=f, stroke_width=6)
    x = (W - (box[2] - box[0])) / 2
    d.text((x, H * y), text, font=f, fill=color, stroke_width=6, stroke_fill="black")


def tag(frame, text):
    d = ImageDraw.Draw(frame)
    f = font(56)
    box = d.textbbox((0, 0), text, font=f)
    w = box[2] - box[0]
    d.rounded_rectangle((60, 250, 60 + w + 64, 250 + 104), 26, fill=(0, 0, 0))
    d.text((92, 270), text, font=f, fill="white")


def flash(frame, strength):
    if strength <= 0:
        return frame
    return Image.blend(frame, Image.new("RGB", (W, H), "white"), min(strength, 1))


def dim(frame, strength):
    return Image.blend(frame, Image.new("RGB", (W, H), "black"), min(max(strength, 0), 1))


img1, img2, img3, img4, img5 = (load(f"{n}.png") for n in "12345")
random.seed(7)


def cut1(t, d):  # 5초: 긴장
    fr = view(img1, 0.5, 0.36, 1.0 + 0.10 * ease(t / d))
    if t < 2.2:
        tag(fr, "수험 생활 3년")
    if 1.6 < t < 4.5:
        subtitle(fr, "제발… 제발…")
    return fr


def cut2(t, d):  # 4초: 합격 화면
    fr = view(img2, 0.5, 0.42, 1.0 + 0.16 * ease(t / d))
    return flash(fr, 0.9 - t * 3)


def cut3(t, d):  # 5초: 환호
    amp = 16 * max(0, 1 - t / 3.5)
    punch = 0.10 * max(0, 1 - t * 4)
    fr = view(img3, 0.5, 0.36, 1.06 + punch, random.uniform(-amp, amp), random.uniform(-amp, amp))
    if t < 2.0:
        subtitle(fr, "됐다!!!", size=96)
    elif t < 4.6:
        subtitle(fr, "붙었다!!!", size=96)
    return fr


def cut4(t, d):  # 7초: 통화
    k = ease(t / d)
    fr = view(img4, 0.46 + 0.08 * k, 0.36, 1.10 + 0.05 * k)
    if 0.4 < t < 3.0:
        subtitle(fr, "엄마! 나 붙었어!")
    elif 3.3 < t < 6.7:
        subtitle(fr, "응, 공기업! 정년 보장!")
    return fr


def mosaic(img, box, block=26):
    """box(원본 그림 기준 0~1 좌표) 안을 모자이크로 가린다."""
    iw, ih = img.size
    x0, y0, x1, y1 = (int(box[0] * iw), int(box[1] * ih), int(box[2] * iw), int(box[3] * ih))
    part = img.crop((x0, y0, x1, y1))
    small = part.resize((max(1, (x1 - x0) // block), max(1, (y1 - y0) // block)), Image.BILINEAR)
    out = img.copy()
    out.paste(small.resize(part.size, Image.NEAREST), (x0, y0))
    return out


img5 = mosaic(img5, (0.44, 0.584, 0.905, 0.637))  # '나무읍 지사' 칸은 2편에서 공개


def cut5(t, d):  # 6초: 표를 훑어 내려가 모자이크 된 '근무 예정지' 줄로 확대
    k = ease(min(t / 4.2, 1))
    fr = view(img5, 0.5 - 0.10 * k, 0.36 + 0.25 * k, 1.0 + 0.8 * k)
    if 0.6 < t < 2.6:
        subtitle(fr, "어디 보자…")
    elif 3.0 < t < 5.8:
        subtitle(fr, "근무지가…")
    return dim(fr, (t - 5.6) / 0.4)


def cut6(t, d):  # 3초: 암전 카드
    fr = Image.new("RGB", (W, H), "black")
    if t > 0.5:
        subtitle(fr, "근무지는 2편에서", y=0.44, size=84)
        subtitle(fr, "흙수저 김토토  1-1", y=0.52, size=44, color=(150, 150, 150))
    return fr


CUTS = [(cut1, 5), (cut2, 4), (cut3, 5), (cut4, 7), (cut5, 6), (cut6, 3)]
TOTAL = sum(d for _, d in CUTS)


def make_audio(path):
    """자리 표시용 효과음: 클릭, 합격 알림, 불길한 저음."""
    rate = 44100
    n = int(TOTAL * rate)
    buf = [0.0] * n

    def add(start, dur, fn):
        s = int(start * rate)
        for i in range(int(dur * rate)):
            if s + i < n:
                buf[s + i] += fn(i / rate)

    add(4.85, 0.05, lambda t: 0.6 * random.uniform(-1, 1) * (1 - t / 0.05))
    for k, freq in enumerate((880, 1109, 1319)):
        add(5.0 + 0.12 * k, 1.2, lambda t, f=freq: 0.25 * math.sin(2 * math.pi * f * t) * math.exp(-4 * t))
    add(21.0, 6.0, lambda t: 0.45 * (t / 6.0) * math.sin(2 * math.pi * (55 - 2 * t) * t))
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in buf))


if len(sys.argv) > 3:  # 미리보기: 지정한 시각(초)의 화면만 저장
    for stamp in sys.argv[3:]:
        t = float(stamp)
        for fn, d in CUTS:
            if t < d:
                fn(t, d).save(f"{out_path}_{stamp}.jpg", quality=85)
                break
            t -= d
    sys.exit()

audio = out_path + ".wav"
make_audio(audio)
enc = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
     "-r", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_path],
    stdin=subprocess.PIPE,
)
for fn, d in CUTS:
    for i in range(int(d * FPS)):
        enc.stdin.write(fn(i / FPS, d).tobytes())
enc.stdin.close()
enc.wait()
