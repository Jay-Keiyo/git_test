# 1화 「합격」 — 30초 3부작 대본 + Google Flow 프롬프트

확정 그림은 `assets/ep1/` 의 13장 (01~12, 10-1). 1화를 1-1, 1-2, 1-3 세 편으로 나눠 올린다.

- **Flow로 만드는 컷**: 그림 1, 3, 4, 6, 7, 11, 12 (인물과 풍경이 움직이는 컷)
- **편집 앱으로 만드는 컷**: 그림 2, 5, 8, 9, 10, 10-1 (모니터·지도 화면. 영상 모델에 넣으면 한글이 뭉개지므로 그림 그대로 넣고 확대·이동만 준다)

## Flow 공통 설정

1. 새 프로젝트 설정에서 화면 비율을 **세로(9:16)** 로 고른다 (프롬프트에 쓰지 않는다)
2. 모드를 **프레임을 동영상으로** 바꾸고, 그 컷의 그림을 **시작 프레임**으로 올린다
3. 프롬프트를 붙여 넣고 생성한다. 한 클립은 최대 8초, 동작은 하나만
4. 내려받은 클립에서 동작이 좋은 구간만 잘라 편집 앱에서 잇는다

---

## 1-1화 「합격」 (약 30초)

| 순서 | 그림 | 초 | 화면 | 대사·자막·소리 | 만드는 곳 |
|---|---|---|---|---|---|
| 1 | 1 | 5 | 어두운 방, 화면을 노려보다 마우스를 누름 | 자막: 수험 생활 3년 / 토토: "제발… 제발…" / 클릭음 | Flow |
| 2 | 2 | 4 | 합격 화면, 천천히 확대 | 효과음: 띠링 | 편집 앱 |
| 3 | 3 | 5 | 벌떡 일어나 두 주먹 치켜들고 환호 | 토토: "됐다!!! 붙었다!!!" | Flow |
| 4 | 4 | 7 | 울면서 웃으며 통화 | 토토: "엄마! 나 붙었어! 응, 공기업! 정년 보장!" | Flow |
| 5 | 5 | 6 | 안내 표를 위에서 아래로 훑다가 "근무 예정지" 칸 제목으로 확대. **오른쪽 칸의 값은 화면 밖** | 토토(목소리만): "어디 보자… 근무지가…" / 낮게 깔리는 음 | 편집 앱 |
| 6 | — | 3 | 암전 + 자막 "근무지는 2편에서" | 음악 뚝 끊김 | 편집 앱 |

끊는 지점: "나무읍 지사" 글자가 읽히기 직전. 이 편만 보면 그냥 기분 좋은 합격 영상이라, 마지막 3초의 불길한 음이 다음 편을 누르게 만든다.

**컷 1 (그림 1) — Flow 프롬프트**

```
Stylized 3D animated film. The young man stares at the laptop screen, tense. He swallows hard, his finger trembles on the mouse. He whispers in Korean, "제발… 제발…", then clicks the mouse once. The single cowlick on top of his hair quivers.
Camera: very slow push-in on his face. Lighting stays the same: dark room, blue screen glow.
Audio: quiet room tone, one mouse click. A soft, slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

**컷 3 (그림 3) — Flow 프롬프트**

```
Stylized 3D animated film. The young man pumps both fists in the air and jumps up and down with joy, eyes squeezed shut, laughing. He shouts in Korean, "됐다! 붙었다!". The cowlick on top of his hair stands straight up.
Camera: slight handheld shake, energetic. Same dark room with blue screen glow.
Audio: his excited shout, a soft slightly high young male voice, chair wheels rolling. No music.
No subtitles, no on-screen text, no captions.
```

**컷 4 (그림 4) — Flow 프롬프트**

```
Stylized 3D animated film. The young man holds the phone to his ear, crying happy tears and laughing, wiping his eye with the back of his hand. He says in Korean, "엄마! 나 붙었어! 응, 공기업! 정년 보장!". He nods quickly while talking.
Camera: gentle handheld, slow drift to the right. Same dark room.
Audio: his tearful happy voice, a soft slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

---

## 1-2화 「나무읍?」 (약 28초)

| 순서 | 그림 | 초 | 화면 | 대사·자막·소리 | 만드는 곳 |
|---|---|---|---|---|---|
| 1 | 5 | 3 | (지난 이야기) 표의 "근무 예정지" 칸에서 시작해 오른쪽으로 이동, **"나무읍 지사"가 드러남** | 자막: 지난 이야기 / 토토(목소리만): "근무지가…" | 편집 앱 |
| 2 | 6 | 5 | 웃는 얼굴 그대로 굳음. 눈만 커지고 삐친 머리가 꺾임 | 토토: "…나무읍?" (한 박자 뒤) "거기가… 어디야?" | Flow |
| 3 | 7 | 3 | 키보드를 급하게 두드리는 손 | 타자 소리, 마지막에 엔터 "탁" | Flow |
| 4 | 8 | 3 | 네이놈 지도 검색창에 글자가 한 자씩 찍힘 | 타자 효과: 한국자연공사 나무읍 지사 | 편집 앱 |
| 5 | 9 | 6 | 길찾기 결과. "5시간 20분"으로 확대 → "버스 운행 하루 6대"로 이동 | 토토(목소리만): "다섯 시간… 이십 분? …버스가 하루 여섯 대?" | 편집 앱 |
| 6 | 10 | 5 | 장소 정보. 번듯한 유리 건물 사진으로 확대 → 로드뷰 버튼으로 이동 | 토토(목소리만): "어? 그래도 건물은 좋네! 신축인가 봐." | 편집 앱 |
| 7 | 10-1 | 1 | 로드뷰 버튼 클릭 | 효과음: 딸깍 | 편집 앱 |
| 8 | — | 2 | 암전 + 자막 "로드뷰는 3편에서" | 정적 | 편집 앱 |

끊는 지점: 버튼을 누른 직후. "건물은 좋네"라는 기대를 깔아 놓고 결과를 안 보여 준다.

그림 10과 10-1은 건물 사진 속 글자가 서로 달라서, 로드뷰 버튼 쪽으로 확대한 상태에서 바꿔 끼워야 티가 안 난다.

**컷 6 (그림 6) — Flow 프롬프트**

```
Stylized 3D animated film. The young man's wide smile stays frozen on his face while his eyes slowly grow wider. A drop of sweat runs down his temple. The cowlick on top of his hair slowly bends and flops to the side. After a pause he says quietly in Korean, "…나무읍?", then, "거기가… 어디야?". He blinks twice.
Camera: locked-off close-up, no movement. Blue screen glow on his face.
Audio: dead silence, then his small confused voice, a soft slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

**컷 7 (그림 7) — Flow 프롬프트**

```
Stylized 3D animated film. Close-up of two hands typing very fast on the black keyboard, frantic and a little clumsy, ending with one hard press of the Enter key.
Camera: locked-off, no movement.
Audio: loud rapid keyboard clacking, one heavy final key press. No voice, no music.
No subtitles, no on-screen text, no captions.
```

---

## 1-3화 「로드뷰」 (약 25초)

| 순서 | 그림 | 초 | 화면 | 대사·자막·소리 | 만드는 곳 |
|---|---|---|---|---|---|
| 1 | 10-1 | 2 | (지난 이야기) 로드뷰 버튼 클릭 → 화면이 하얗게 번쩍 | 자막: 지난 이야기 / 토토(목소리만): "신축인가 봐." / 딸깍 | 편집 앱 |
| 2 | 11 | 7 | 젖은 도로 끝의 낡은 건물로 천천히 다가감 | (3초 정적) 까마귀 / 토토(목소리만): "…사진이랑 다른데." | Flow |
| 3 | 12 | 9 | 스탠드 불빛 아래 억지로 웃는 토토. 심호흡 | 토토: "설마… 가보면 다르겠지. 처음부터 겁먹지 말자." | Flow |
| 4 | — | 5 | 검은 화면 + 타이틀 「흙수저 김토토」 / 입사 D-14 / 다음 화: 연수원 2주 | 잔잔한 피아노 | 편집 앱 |
| 5 | — | 2 | 자막 "팔로우하면 2화 알림" | — | 편집 앱 |

끊는 지점: 억지 미소. 시청자는 "가보면 다르지 않다"는 걸 이미 알기 때문에 2화가 궁금해진다.

**컷 11 (그림 11) — Flow 프롬프트**

```
Realistic footage, overcast day. Slow, eerie push-in along the wet road toward the old two-story office building. Rice plants sway in the wind, power lines swing slightly, a single crow flies across the gray sky. Nothing else moves. The building sign stays unchanged.
Camera: slow steady forward dolly, like a street-view image coming to life.
Audio: wind, distant crow caw, faint hum. No voice, no music.
No subtitles, no on-screen text, no captions.
```

**컷 12 (그림 12) — Flow 프롬프트**

```
Stylized 3D animated film. The young man sits stiffly in his chair under the warm desk lamp. He takes a long deep breath, forces an awkward smile and nods to himself. He says in Korean, slowly, "설마… 가보면 다르겠지. 처음부터 겁먹지 말자.". The bent cowlick on his hair tries to stand up, then droops again.
Camera: locked-off, very slow push-in.
Audio: his quiet unsure voice, a soft slightly high young male voice, a soft hopeful piano note at the end.
No subtitles, no on-screen text, no captions.
```

---

## 올릴 때

- 하루 간격으로 올린다. 설명글 첫 줄과 고정 댓글에 다음 편 위치를 적는다
- 표지에 "1-1", "1-2", "1-3"을 크게 넣어 프로필에서 순서가 보이게 한다
- 2편과 3편은 첫 2~3초의 "지난 이야기"가 있어 중간부터 본 사람도 따라올 수 있다

## 주의

- **목소리**: 영상 모델은 클립마다 목소리를 새로 만들어서 토토 목소리가 컷마다 달라질 수 있다. 모든 프롬프트에 같은 목소리 설명을 넣었지만 보장은 안 된다. 다르게 나오면 목소리만 직접 녹음하거나 TTS 하나로 덧입힌다. "목소리만" 대사는 처음부터 녹음이나 TTS로 넣는다
- **대사 길이**: 8초 클립에 대사가 길면 말이 빨라지거나 잘린다. 통화 컷과 마지막 컷이 가장 길어서, 어색하면 문장을 하나 줄인다
- **자막**: 모델이 화면에 자막을 멋대로 박는 경우가 있어 모든 프롬프트 끝에 금지 문장을 넣었다
