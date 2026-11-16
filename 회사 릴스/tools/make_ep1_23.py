"""1-2화 「나무읍?」, 1-3화 「로드뷰」 가편집 영상(애니매틱) 생성기.

정지 그림에 확대·이동·흔들림과 자막만 얹어 흐름을 미리 본다.
사용: python3 make_ep1_23.py <2|3> <그림 폴더> <출력.mp4> [미리보기 시각(초)...]
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
part, src_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
random.seed(7)


def font(size):
    return ImageFont.truetype(FONT, size)


def load(name):
    return Image.open(f"{src_dir}/{name}.png").convert("RGB")


def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def mix(a, b, k):
    return a + (b - a) * k


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
    d.text(((W - (box[2] - box[0])) / 2, H * y), text, font=f, fill=color, stroke_width=6, stroke_fill="black")


def tag(frame, text):
    d = ImageDraw.Draw(frame)
    f = font(56)
    box = d.textbbox((0, 0), text, font=f)
    d.rounded_rectangle((60, 250, 60 + box[2] - box[0] + 64, 354), 26, fill=(0, 0, 0))
    d.text((92, 270), text, font=f, fill="white")


def flash(frame, strength):
    if strength <= 0:
        return frame
    return Image.blend(frame, Image.new("RGB", (W, H), "white"), min(strength, 1))


def card(lines):
    fr = Image.new("RGB", (W, H), "black")
    for text, y, size, color in lines:
        subtitle(fr, text, y=y, size=size, color=color)
    return fr


def mosaic(img, box, block=26):
    iw, ih = img.size
    x0, y0, x1, y1 = (int(box[0] * iw), int(box[1] * ih), int(box[2] * iw), int(box[3] * ih))
    piece = img.crop((x0, y0, x1, y1))
    small = piece.resize((max(1, (x1 - x0) // block), max(1, (y1 - y0) // block)), Image.BILINEAR)
    out = img.copy()
    out.paste(small.resize(piece.size, Image.NEAREST), (x0, y0))
    return out


GRAY = (150, 150, 150)

if part == "2":
    img5, img6, img7, img8, img9, img10, img10b = (load(n) for n in ("5", "6", "7", "8", "9", "10", "10-1"))
    img5_hidden = mosaic(img5, (0.44, 0.584, 0.905, 0.637))
    QUERY = "한국자연공사 나무읍 지사"

    def typed(n):
        """검색창의 안내 문구를 지우고 QUERY의 앞 n글자를 찍은 그림."""
        im = img8.copy()
        d = ImageDraw.Draw(im)
        d.rectangle((236, 44, 880, 100), fill=(255, 255, 255))
        f = font(38)
        text = QUERY[:n]
        d.text((246, 52), text, font=f, fill=(30, 30, 30))
        end = 246 + d.textlength(text, font=f)
        d.rectangle((end + 4, 50, end + 7, 94), fill=(255, 90, 0))
        return im

    typed_cache = {}

    def c1(t, d):  # 지난 이야기: 모자이크가 걷히며 근무지 공개
        k = ease((t - 1.3) / 0.5)
        fr = view(Image.blend(img5_hidden, img5, k), mix(0.40, 0.50, ease(t / 2.4)), 0.61, 1.8)
        tag(fr, "지난 이야기")
        if t < 1.3:
            subtitle(fr, "근무지가…")
        return flash(fr, 0.5 - abs(t - 1.5) * 3)

    def c2(t, d):  # 굳은 얼굴
        fr = view(img6, 0.5, 0.40, 1.0 + 0.05 * ease(t / d))
        if 0.9 < t < 2.6:
            subtitle(fr, "…나무읍?")
        elif 3.0 < t < 4.8:
            subtitle(fr, "거기가… 어디야?")
        return fr

    def c3(t, d):  # 타자
        return view(img7, 0.5, 0.42, 1.12, random.uniform(-9, 9), random.uniform(-9, 9))

    def c4(t, d):  # 검색어가 한 글자씩 찍힘
        n = min(len(QUERY), int(t / 2.2 * len(QUERY)) + 1)
        if n not in typed_cache:
            typed_cache[n] = typed(n)
        return view(typed_cache[n], 0.50, 0.10, 1.6)

    def c5(t, d):  # 5시간 20분 → 하루 6대
        if t < 1.0:
            k = ease(t / 1.0)
            fr = view(img9, mix(0.5, 0.36, k), mix(0.40, 0.47, k), mix(1.0, 2.3, k))
        else:
            fr = view(img9, mix(0.36, 0.76, ease((t - 3.0) / 0.7)), 0.47, 2.3)
        if 1.0 < t < 3.0:
            subtitle(fr, "다섯 시간… 이십 분?")
        elif 3.6 < t < 5.8:
            subtitle(fr, "버스가… 하루 여섯 대?")
        return fr

    def c6(t, d):  # 번듯한 건물 사진 → 로드뷰 버튼
        if t < 0.8:
            k = ease(t / 0.8)
            fr = view(img10, mix(0.5, 0.80, k), mix(0.45, 0.48, k), mix(1.0, 2.4, k))
        else:
            k = ease((t - 3.4) / 0.9)
            fr = view(img10, mix(0.80, 0.64, k), mix(0.48, 0.585, k), 2.4)
        if 0.8 < t < 2.2:
            subtitle(fr, "어? 그래도 건물은 좋네!")
        elif 2.3 < t < 3.5:
            subtitle(fr, "신축인가 봐.")
        return fr

    def c7(t, d):  # 클릭
        return flash(view(img10b, 0.64, 0.585, 2.4 + 0.12 * ease(t / d)), (t - 0.5) * 2.5)

    def c8(t, d):
        if t < 0.4:
            return Image.new("RGB", (W, H), "black")
        return card([("로드뷰는 3편에서", 0.44, 84, "white"), ("흙수저 김토토  1-2", 0.52, 44, GRAY)])

    CUTS = [(c1, 3), (c2, 5), (c3, 3), (c4, 3), (c5, 6), (c6, 5), (c7, 1), (c8, 2)]
    # (시각, 종류) 자리 표시용 효과음
    SOUNDS = [(1.3, "thud")] + [(8.0 + 0.11 * i, "key") for i in range(26)] + [(10.9, "enter")] + \
             [(11.05 + 2.2 * i / 13, "key") for i in range(13)] + [(25.4, "click")]
else:
    img10b, img11, img12 = load("10-1"), load("11"), load("12")

    def c1(t, d):  # 지난 이야기: 로드뷰 클릭
        fr = view(img10b, 0.64, 0.585, 2.4 + 0.15 * ease(t / d))
        tag(fr, "지난 이야기")
        if t < 1.4:
            subtitle(fr, "신축인가 봐.")
        return flash(fr, (t - 1.5) * 2.2)

    def c2(t, d):  # 로드뷰 속 낡은 건물로 다가감
        k = ease(t / d)
        fr = view(img11, mix(0.5, 0.70, k), mix(0.5, 0.52, k), mix(1.0, 1.9, k))
        if 4.2 < t < 6.8:
            subtitle(fr, "…사진이랑 다른데.")
        return flash(fr, 1 - t * 2.5)

    def c3(t, d):  # 억지 미소
        fr = view(img12, 0.5, 0.36, 1.0 + 0.10 * ease(t / d))
        if 1.0 < t < 4.4:
            subtitle(fr, "설마… 가보면 다르겠지.")
        elif 5.0 < t < 8.6:
            subtitle(fr, "처음부터 겁먹지 말자.")
        return fr

    def c4(t, d):  # 타이틀
        if t < 0.5:
            return Image.new("RGB", (W, H), "black")
        lines = [("흙수저 김토토", 0.40, 110, "white")]
        if t > 1.5:
            lines.append(("입사 D-14", 0.49, 64, (255, 200, 60)))
        if t > 2.6:
            lines.append(("다음 화: 연수원 2주", 0.55, 52, GRAY))
        return card(lines)

    def c5(t, d):
        return card([("팔로우하면 2화 알림", 0.46, 72, "white")])

    CUTS = [(c1, 2), (c2, 7), (c3, 9), (c4, 5), (c5, 2)]
    SOUNDS = [(1.5, "click"), (2.0, "wind"), (18.5, "tone")]

TOTAL = sum(d for _, d in CUTS)


def make_audio(path):
    rate = 44100
    n = int(TOTAL * rate)
    buf = [0.0] * n

    def add(start, dur, fn):
        s = int(start * rate)
        for i in range(int(dur * rate)):
            if s + i < n:
                buf[s + i] += fn(i / rate)

    for at, kind in SOUNDS:
        if kind == "key":
            add(at, 0.03, lambda t: 0.35 * random.uniform(-1, 1) * (1 - t / 0.03))
        elif kind == "enter":
            add(at, 0.08, lambda t: 0.7 * random.uniform(-1, 1) * (1 - t / 0.08))
        elif kind == "click":
            add(at, 0.05, lambda t: 0.6 * random.uniform(-1, 1) * (1 - t / 0.05))
        elif kind == "thud":
            add(at, 0.9, lambda t: 0.7 * math.sin(2 * math.pi * 60 * t) * math.exp(-5 * t))
        elif kind == "wind":
            state = [0.0]

            def wind(t, state=state):
                state[0] = 0.995 * state[0] + 0.005 * random.uniform(-1, 1)
                return 6.0 * state[0] * min(t, 1) * min(7 - t, 1)

            add(at, 7.0, wind)
        elif kind == "tone":
            for f in (262, 330, 392):
                add(at, 4.0, lambda t, f=f: 0.12 * math.sin(2 * math.pi * f * t) * math.exp(-0.8 * t))
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in buf))


if len(sys.argv) > 4:  # 미리보기: 지정한 시각(초)의 화면만 저장
    for stamp in sys.argv[4:]:
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
