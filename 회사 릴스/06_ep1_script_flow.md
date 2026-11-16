# 1화 「합격」 — 확정 씬 대본 + Google Flow 프롬프트

확정 그림은 `assets/ep1/` 의 13장 (01~12, 10-1). 예상 길이 약 90초.

## 1. 씬 대본 (순서대로)

| 컷 | 그림 | 초 | 화면 | 대사·자막·소리 | 만드는 곳 |
|---|---|---|---|---|---|
| 1 | 01 | 6 | 어두운 방, 화면을 노려보는 토토. 침을 삼키고 마우스를 누름 | 자막: 수험 생활 3년 / 토토(속삭임): "제발… 제발…" / 클릭음 | Flow |
| 2 | 02 | 4 | 합격 화면. 천천히 확대 | 효과음: 띠링 | 편집 앱 |
| 3 | 03 | 5 | 벌떡 일어나 두 주먹을 치켜들고 환호. 삐친 머리가 쫙 섬 | 토토: "됐다!!! 붙었다!!!" | Flow |
| 4 | 04 | 8 | 울면서 웃으며 통화 | 토토: "엄마! 나 붙었어! 응, 공기업! 정년 보장!" | Flow |
| 5 | 05 | 7 | 안내 표. 아래로 훑다가 "나무읍 지사" 칸으로 천천히 확대 | 토토(목소리만): "어디 보자… 근무지가…" / 낮게 깔리는 음 | 편집 앱 |
| 6 | 06 | 5 | 웃는 얼굴 그대로 굳음. 눈만 커지고 삐친 머리가 꺾임 | 토토: "…나무읍?" (한 박자 뒤) "거기가… 어디야?" | Flow |
| 7 | 07 | 3 | 키보드를 급하게 두드리는 손 | 타자 소리, 마지막에 엔터 "탁" | Flow |
| 8 | 08 | 3 | 네이놈 지도. 검색창에 글자가 한 자씩 찍힘 | 자막 효과: 한국자연공사 나무읍 지사 | 편집 앱 |
| 9 | 09 | 6 | 길찾기 결과. "5시간 20분"으로 확대 → "버스 운행 하루 6대"로 이동 | 토토(목소리만): "다섯 시간… 이십 분? …버스가 하루 여섯 대?" | 편집 앱 |
| 10 | 10 | 5 | 장소 정보. 번듯한 유리 건물 사진으로 확대 → 로드뷰 버튼으로 이동 | 토토(목소리만): "어? 그래도 건물은 좋네! 신축인가 봐." | 편집 앱 |
| 10-1 | 10-1 | 1 | 로드뷰 버튼 클릭 | 효과음: 딸깍 | 편집 앱 |
| 11 | 11 | 7 | 로드뷰. 젖은 도로 끝의 낡은 건물로 천천히 다가감 | (3초 정적) 까마귀 / 토토(목소리만): "…사진이랑 다른데." | Flow |
| 12 | 12 | 9 | 스탠드 불빛 아래 억지로 웃는 토토. 심호흡 | 토토: "설마… 가보면 다르겠지. 처음부터 겁먹지 말자." | Flow |
| 13 | — | 5 | 검은 화면 + 타이틀 「흙수저 김토토」 / 입사 D-14 / 다음 화: 연수원 2주 | 잔잔한 피아노 | 편집 앱 |

컷 10의 "사진은 신축, 로드뷰는 폐건물" 대비는 확정 그림에 이미 들어 있어서 대사로 살렸다.

## 2. Flow로 만드는 컷과 편집 앱으로 만드는 컷

- **Flow (7컷)**: 01, 03, 04, 06, 07, 11, 12 — 인물과 풍경이 움직이는 컷
- **편집 앱 (6컷)**: 02, 05, 08, 09, 10, 10-1 — 모니터·지도 화면. 영상 모델에 넣으면 한글이 뭉개지므로 그림 그대로 넣고 확대·이동(키프레임)만 준다
- 10 → 10-1은 건물 사진 속 글자가 서로 달라서, 로드뷰 버튼 쪽으로 확대한 상태에서 바꿔 끼워야 티가 안 난다

## 3. Flow 설정과 순서

1. 새 프로젝트를 만들고 설정에서 화면 비율을 **세로(9:16)** 로 고른다. 비율은 프롬프트에 쓰지 않고 설정에서 정한다
2. 모드를 **프레임을 동영상으로(Frames to Video)** 로 바꾸고, 해당 컷의 그림을 **시작 프레임**으로 올린다
3. 아래 프롬프트를 붙여 넣고 생성한다. 시험은 빠른 모델로, 확정본은 품질 모델로
4. 마음에 드는 결과를 내려받는다. 클립은 최대 8초이므로 한 컷에 한 가지 동작만 시킨다
5. 내려받은 클립을 편집 앱에서 대본 순서대로 잇는다

## 4. Flow 프롬프트 (컷별, 그대로 붙여넣기)

### 컷 1 — 그림 01

```
Stylized 3D animated film. The young man stares at the laptop screen, tense. He swallows hard, his finger trembles on the mouse. He whispers in Korean, "제발… 제발…", then clicks the mouse once. The single cowlick on top of his hair quivers.
Camera: very slow push-in on his face. Lighting stays the same: dark room, blue screen glow.
Audio: quiet room tone, one mouse click. A soft, slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

### 컷 3 — 그림 03

```
Stylized 3D animated film. The young man pumps both fists in the air and jumps up and down with joy, eyes squeezed shut, laughing. He shouts in Korean, "됐다! 붙었다!". The cowlick on top of his hair stands straight up.
Camera: slight handheld shake, energetic. Same dark room with blue screen glow.
Audio: his excited shout, a soft slightly high young male voice, chair wheels rolling. No music.
No subtitles, no on-screen text, no captions.
```

### 컷 4 — 그림 04

```
Stylized 3D animated film. The young man holds the phone to his ear, crying happy tears and laughing, wiping his eye with the back of his hand. He says in Korean, "엄마! 나 붙었어! 응, 공기업! 정년 보장!". He nods quickly while talking.
Camera: gentle handheld, slow drift to the right. Same dark room.
Audio: his tearful happy voice, a soft slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

### 컷 6 — 그림 06

```
Stylized 3D animated film. The young man's wide smile stays frozen on his face while his eyes slowly grow wider. A drop of sweat runs down his temple. The cowlick on top of his hair slowly bends and flops to the side. After a pause he says quietly in Korean, "…나무읍?", then, "거기가… 어디야?". He blinks twice.
Camera: locked-off close-up, no movement. Blue screen glow on his face.
Audio: dead silence, then his small confused voice, a soft slightly high young male voice. No music.
No subtitles, no on-screen text, no captions.
```

### 컷 7 — 그림 07

```
Stylized 3D animated film. Close-up of two hands typing very fast on the black keyboard, frantic and a little clumsy, ending with one hard press of the Enter key.
Camera: locked-off, no movement.
Audio: loud rapid keyboard clacking, one heavy final key press. No voice, no music.
No subtitles, no on-screen text, no captions.
```

### 컷 11 — 그림 11

```
Realistic footage, overcast day. Slow, eerie push-in along the wet road toward the old two-story office building. Rice plants sway in the wind, power lines swing slightly, a single crow flies across the gray sky. Nothing else moves. The building sign stays unchanged.
Camera: slow steady forward dolly, like a street-view image coming to life.
Audio: wind, distant crow caw, faint hum. No voice, no music.
No subtitles, no on-screen text, no captions.
```

### 컷 12 — 그림 12

```
Stylized 3D animated film. The young man sits stiffly in his chair under the warm desk lamp. He takes a long deep breath, forces an awkward smile and nods to himself. He says in Korean, slowly, "설마… 가보면 다르겠지. 처음부터 겁먹지 말자.". The bent cowlick on his hair tries to stand up, then droops again.
Camera: locked-off, very slow push-in.
Audio: his quiet unsure voice, a soft slightly high young male voice, a soft hopeful piano note at the end.
No subtitles, no on-screen text, no captions.
```

## 5. 주의

- **목소리**: 영상 모델은 클립마다 목소리를 새로 만들어서 토토 목소리가 컷마다 달라질 수 있다. 모든 프롬프트에 같은 목소리 설명을 넣었지만 보장은 안 된다. 다르게 나오면 목소리만 직접 녹음하거나 TTS 하나로 덧입힌다
- **대사 길이**: 8초 클립에 대사가 길면 말이 빨라지거나 잘린다. 컷 4와 12가 가장 길어서, 어색하면 문장을 하나 줄인다
- **자막**: 모델이 화면에 자막을 멋대로 박는 경우가 있어 모든 프롬프트 끝에 금지 문장을 넣었다
- **컷 9, 10, 11의 목소리만 나오는 대사**: 컷 6이나 12와 같은 목소리여야 하므로 녹음이나 TTS로 넣는다

## 6. 30초 3부작으로 쪼개기

한 편을 통으로 올리지 않고 세 편으로 나눈다. 각 편은 **궁금한 순간에서 끊고**, 다음 편은 그 순간을 2초 되풀이하며 시작한다.

| 편 | 제목 | 컷 | 길이 | 끊는 지점 |
|---|---|---|---|---|
| 1-1 | 합격 | 1 → 2 → 3 → 4 → 5 | 약 30초 | "근무지가…" 하며 표가 확대되다가, 칸의 글자가 읽히기 직전에 암전. 자막 "근무지는 다음 편에" |
| 1-2 | 나무읍? | (5 끝 2초) → 6 → 7 → 8 → 9 → 10 → 10-1 | 약 27초 | "건물은 좋네!" 하고 로드뷰 버튼을 누르는 순간 암전. 자막 "로드뷰는 다음 편에" |
| 1-3 | 로드뷰 | (10-1 클릭 1초) → 11 → 12 → 13 | 약 24초 | 억지 미소와 "가보면 다르겠지" 뒤에 "입사 D-14 / 다음 화: 연수원 2주" |

- 1-1은 컷 5에서 "나무읍 지사" 글자가 보이기 전에 끊어야 한다. 확대를 표의 "근무 예정지" 칸 제목까지만 하고 값은 화면 밖에 둔다
- 각 편 첫 2초에 그 편에서 가장 센 장면을 먼저 보여 준다 (1-2는 굳은 얼굴, 1-3은 낡은 건물이 나오기 직전의 흰 화면)
- 설명글 첫 줄과 고정 댓글에 "2편은 프로필에"처럼 다음 편 위치를 적는다
- 세 편을 같은 날 몰아 올리지 말고 하루 간격으로 올리면 다음 편을 기다리게 된다
