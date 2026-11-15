# EP1 「합격」 제작 시트 (약 110초, 9:16)

화면 톤: **단체샷과 같은 방식** — 배경은 실사에 가까운 한국 일상 공간, 인물만 3D 애니메이션 흙 캐릭터.

작업 흐름: ① ChatGPT로 장면 이미지(스틸) 생성 → ② Higgsfield에 스틸을 시작 이미지로 넣고 영상 생성 → ③ 편집 앱에서 자막·효과음·타이틀.

## 1. 장면 이미지 (ChatGPT, 매번 김토토 프로필 이미지 첨부)

모든 프롬프트 맨 앞에 붙이는 문장:

```
첨부한 캐릭터(김토토)를 얼굴, 흙 색, 머리 위 새싹까지 똑같이 유지해서 그려줘. 캐릭터는 같은 3D 애니메이션 그림체, 배경은 사실적인 한국의 일상 공간. 세로 9:16. 워터마크 없이.
```

| 스틸 | 쓰는 컷 | 프롬프트 (위 문장 뒤에 붙임) |
|---|---|---|
| S1 | 1 | `밤, 불 꺼진 좁은 원룸 책상. 모니터 불빛만 얼굴을 비춰. 회색 후드티를 입은 토토가 마우스에 손을 올리고 침을 삼키며 화면을 노려봐. 책상에는 수험서 더미와 컵라면 용기. 정면 상반신, 모니터는 뒷모습만 보여.` |
| S2 | 2 | `(캐릭터 없이) 모니터 화면 클로즈업. 깔끔한 공공기관 채용 사이트 화면이고 가운데에 큰 글씨로 "최종 합격을 축하드립니다", 그 위에 "한국자연공사 신입사원 공개채용", 아래에 "김토토 님 / 기술직(토목)"이라고 정확한 한글로 적혀 있어. 다른 글자는 넣지 마.` |
| S3 | 3 | `S1과 같은 방, 같은 옷. 토토가 의자에서 벌떡 일어나 두 주먹을 치켜들고 입을 크게 벌려 환호해. 머리 위 새싹이 곧게 쫙 서 있어. 의자가 뒤로 밀려나 있어.` |
| S4 | 4 | `S1과 같은 방, 같은 옷. 토토가 휴대폰을 귀에 대고 통화하며 눈물이 글썽한 채 활짝 웃어. 다른 손으로 눈가를 훔쳐.` |
| S5 | 5–6 | `(캐릭터 없이) 모니터 화면 클로즈업. 같은 채용 사이트의 안내 페이지. 제목 "합격자 등록 일정 및 장소 안내". 아래에 단순한 표가 있고 행은 "등록 기간 / 연수원 입소 / 근무 예정지" 세 개. 근무 예정지 칸에 "거제지사"라고 정확한 한글로 적혀 있어. 다른 글자는 넣지 마.` |
| S6 | 7 | `S1과 같은 방, 같은 옷. 얼굴 클로즈업. 웃던 입이 그대로 굳고 눈이 동그래졌어. 머리 위 새싹 한 가닥이 꺾여서 옆으로 누웠어. 모니터 불빛이 얼굴에 푸르게 비쳐.` |
| S7 | 9 | `(캐릭터 없이, 가로 사진을 세로로 크롭한 느낌) 한국 시골의 허름한 2층 사무소 건물. 얼룩진 외벽, 글자 없는 빈 간판, 텅 빈 주차장, 뒤에는 야산, 양옆은 논밭. 흐린 날, 지도 앱 거리뷰처럼 살짝 광각.` (단체샷 이미지를 첨부해 "이 건물과 같은 건물로"라고 덧붙이면 건물이 통일됨) |
| S8 | 10 | `S1과 같은 방, 같은 옷. 토토가 노트북을 반쯤 덮고 두 손을 그 위에 올린 채 억지로 입꼬리를 올려 웃어. 눈은 불안해. 새싹 한 가닥은 여전히 꺾여 있어.` |

컷 8(지도 앱 화면)은 이미지 생성보다 **실제 지도 앱에서 집→거제 경로를 화면 녹화**하는 편이 빠르고 진짜 같음.

## 2. 영상 프롬프트 (Higgsfield)

- 모델: `Seedance 2.0` (9:16, 720p, genre: comedy). 스틸을 start image로 넣음
- 대사는 영상 생성 음성에 맡기지 말고, 편집 단계에서 더빙/TTS + 자막으로 넣는 것을 기본으로 함 (한국어 대사 품질은 먼저 컷 3 하나로 시험해 볼 것)

| 컷 | 초 | 스틸 | 영상 프롬프트 | 자막·대사 |
|---|---|---|---|---|
| 1 | 6 | S1 | `Slow push-in on the character's tense face lit by the monitor. He swallows, his finger trembles on the mouse, then clicks. The sprouts on his head quiver. Quiet room tone, a single mouse click.` | 자막: 수험 생활 3년 |
| 2 | 5 | S2 | `Static shot of the monitor. The page finishes loading with a subtle screen flicker. No change to the text.` | 효과음: 띠링 |
| 3 | 8 | S3 | `He jumps up from the chair, pumps both fists, spins once and shouts with joy. The sprouts on his head pop straight up. Handheld energetic camera. The chair rolls back and hits the bed.` | "됐다!!! 엄마!!!" |
| 4 | 8 | S4 | `He paces in a small circle while on the phone, nodding fast, wiping a tear, laughing. Gentle handheld camera following him.` | "네, 공기업이요. 네, 정년 보장이요." |
| 5 | 6 | S5 | `Slow vertical scroll down the web page, stopping on the table.` | — |
| 6 | 8 | S5 | `Very slow dramatic zoom into the bottom row of the table until the last cell fills the screen. Everything else blurs. Low ominous hum.` | (정적) |
| 7 | 8 | S6 | `Extreme close-up. His smile stays frozen while his eyes slowly widen. One sprout on his head snaps and falls sideways. He blinks twice. Silence, then a tiny comedic crack sound.` | "…거제?" |
| 8 | 10 | 화면 녹화 | (실제 지도 앱 녹화: 경로가 남쪽으로 끝없이 이어지고 "5시간 20분" 표시) | "…도?" |
| 9 | 8 | S7 | `Slow creeping push-in toward the shabby building, like a street-view image coming alive. Grass sways, a crow flies across, an old air conditioner rattles. Overcast, lonely.` | 효과음: 까마귀 |
| 10 | 12 | S8 | `He slowly closes the laptop, takes a long deep breath, forces a smile and nods to himself. The bent sprout tries to stand up and droops again. Soft hopeful piano starts.` | "설마… 가보면 다르겠지. 처음부터 겁먹지 말자." |
| 11 | 8 | 편집 | 검은 화면 + 타이틀 「흙수저 김토토」 / 입사 D-14 / 다음 화: 연수원 2주 | — |

합계 약 87초 + 컷 사이 여백과 대사 호흡 = 100~110초.

## 3. 체크

- 컷 1·3·4·6·8·10은 같은 방·같은 옷이어야 함 → S1을 먼저 확정하고, 이후 스틸은 **S1 이미지도 함께 첨부**해서 "같은 방"으로 요청
- 한글이 들어가는 S2·S5는 글자가 틀리면 다시 뽑기. 계속 틀리면 글자 없이 뽑고 편집 앱에서 텍스트를 얹음
