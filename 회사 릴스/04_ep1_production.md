# EP1 「합격」 제작 시트 (약 110초, 9:16)

화면 톤: **단체샷과 같은 방식** — 배경은 실사에 가까운 한국 일상 공간, 인물만 3D 애니메이션 흙 캐릭터.

작업 흐름: ① ChatGPT로 장면 이미지(스틸) 생성 → ② Higgsfield에 스틸을 시작 이미지로 넣고 영상 생성 → ③ 편집 앱에서 자막·효과음·타이틀.

> 1~2화의 토토는 아직 입사 전이라 **머리카락이 있는 버전**이다. 새싹은 2화 엔딩에서 사원증을 받는 순간 처음 돋는다. 새싹으로 하던 감정 표현은 정수리의 삐친 머리 한 가닥이 대신한다.

## 1. 장면 이미지

씬별 완성 프롬프트는 [05_ep1_gpt_scenes.md](05_ep1_gpt_scenes.md)에 있다 (S1~S8).

## 2. 영상 프롬프트 (Higgsfield)

- 모델: `Seedance 2.0` (9:16, 720p, genre: comedy). 스틸을 start image로 넣음
- 대사는 영상 생성 음성에 맡기지 말고, 편집 단계에서 더빙/TTS + 자막으로 넣는 것을 기본으로 함 (한국어 대사 품질은 먼저 컷 3 하나로 시험해 볼 것)

| 컷 | 초 | 스틸 | 영상 프롬프트 | 자막·대사 |
|---|---|---|---|---|
| 1 | 6 | S1 | `Slow push-in on the character's tense face lit by the monitor. He swallows, his finger trembles on the mouse, then clicks. The single cowlick on top of his hair quivers. Quiet room tone, a single mouse click.` | 자막: 수험 생활 3년 |
| 2 | 5 | S2 | `Static shot of the monitor. The page finishes loading with a subtle screen flicker. No change to the text.` | 효과음: 띠링 |
| 3 | 8 | S3 | `He jumps up from the chair, pumps both fists, spins once and shouts with joy. The cowlick on top of his hair pops straight up. Handheld energetic camera. The chair rolls back and hits the bed.` | "됐다!!! 엄마!!!" |
| 4 | 8 | S4 | `He paces in a small circle while on the phone, nodding fast, wiping a tear, laughing. Gentle handheld camera following him.` | "네, 공기업이요. 네, 정년 보장이요." |
| 5 | 6 | S5 | `Slow vertical scroll down the web page, stopping on the table.` | — |
| 6 | 8 | S5 | `Very slow dramatic zoom into the bottom row of the table until the last cell fills the screen. Everything else blurs. Low ominous hum.` | (정적) |
| 7 | 8 | S6 | `Extreme close-up. His smile stays frozen while his eyes slowly widen. The cowlick on top of his hair bends and flops sideways. He blinks twice. Silence, then a tiny comedic crack sound.` | "…나무읍?" |
| 8 | 10 | S9 | `The route line draws itself slowly from the top pin down to the bottom pin. The camera drifts down following the line, then settles on the travel-time card. Subtle map zoom-out. Comedic falling whistle sound.` | "…읍?" |
| 8-1 | 3 | S10 | `Close-up of hands typing fast on the keyboard, frantic and slightly clumsy. Loud mechanical key clacks, ending with a hard hit on the Enter key.` | 효과음: 타자, 엔터 |
| 8-2 | 4 | S11 | `Static shot of the monitor, the cursor blinks in the empty search box.` (편집에서 "한국자연공사 나무읍지사"를 한 글자씩 타이핑 효과로 얹음) | — |
| 8-3 | 5 | S12 | `The mouse cursor trembles, hesitates above the button, then clicks it. The button presses in. The screen flashes white.` | 효과음: 딸깍 |
| 9 | 8 | S7 | `Slow creeping push-in toward the shabby building, like a street-view image coming alive. Grass sways, a crow flies across, an old air conditioner rattles. Overcast, lonely.` | 효과음: 까마귀 |
| 10 | 12 | S8 | `The monitor is off. He takes a long deep breath, forces a smile and nods to himself. The bent cowlick tries to stand up and droops again. Soft hopeful piano starts.` | "설마… 가보면 다르겠지. 처음부터 겁먹지 말자." |
| 11 | 8 | 편집 | 검은 화면 + 타이틀 「흙수저 김토토」 / 입사 D-14 / 다음 화: 연수원 2주 | — |

합계 약 99초 + 컷 사이 여백과 대사 호흡 = 110~120초.

## 3. 체크

- 컷 1·3·4·6·8·10은 같은 방·같은 옷이어야 함 → S1을 먼저 확정하고, 이후 스틸은 **S1 이미지도 함께 첨부**해서 "같은 방"으로 요청
- 한글이 들어가는 S2·S5는 글자가 틀리면 다시 뽑기. 계속 틀리면 글자 없이 뽑고 편집 앱에서 텍스트를 얹음
