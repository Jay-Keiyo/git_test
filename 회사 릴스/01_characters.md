# 인물 설정 + 이미지 프롬프트 (Higgsfield용)

드라마 가제: **「흙수저 김토토」** — 한국자연공사 거제지사 사업부 신입 기술직의 생존기

## 0. 공통 비주얼 규칙

| 규칙 | 내용 |
|---|---|
| 몸 | 얼굴·목·손 등 드러난 피부 전체가 **진짜 흙** (입자, 잔금, 잔자갈, 잔뿌리가 보이는 무광 질감). 사람 피부는 어디에도 없음 |
| 눈 | 크고 표정이 풍부한 만화 눈 (감정 연기가 여기서 나옴) |
| 머리 | 머리카락 없음. 정수리에서 **나무**가 자람 → 직급이 오를수록 커짐 |
| 옷 | 평범한 한국 공공기관 직장인 복장 + 사원증 목걸이 |
| 톤 | 3D 애니메이션풍 만화 캐릭터 (실사 X). 흙 질감은 살리되 얼굴은 단순하고 표정이 큰 만화 비율 |
| 흙 종류 | 인물마다 토질을 다르게 해서 한눈에 구분 |

### 직급별 머리 나무

| 직급 | 나무 |
|---|---|
| 사원 | 2~3cm짜리 뾰족뾰족한 새싹 몇 가닥 (삐죽 솟은 짧은 머리처럼) |
| 대리 | 한 뼘(10~15cm) 묘목, 잎 몇 장 |
| 과장 | 30cm 정도의 가지 뻗은 어린 나무 |
| 차장 | 50cm 정도, 수형이 잡힌 중간 나무 |
| 부장 | 머리보다 큰 풍성한 나무 (분재처럼 굵은 줄기) |
| 처장 | 어깨너비를 넘는 큰 나무, 굵은 뿌리가 이마까지 내려옴 |
| 본부장 | 화면 위를 뚫고 나가는 거목, 이끼·새 둥지 |

> **확정 규칙 (시안 반영)**: 직급은 정수리에서 **위로 솟은** 식물의 높이로만 구분한다. 여성 캐릭터는 아래로 늘어지는 잎사귀 머리를 가질 수 있고, 이는 직급과 무관하다. 이정원 대리 = 잎사귀 머리 + 위로 솟은 흰 꽃봉오리 하나.

> **확정 규칙 v2 (최종)**: 모든 인물은 **평범한 머리카락**이 있고, 식물은 정수리에서 머리카락 사이로 자란다. 민머리 설정은 폐기. 사원 = 새싹 **하나**. 아래 영문 프롬프트의 "No hair" 문구는 구버전이며, 실제 생성은 `03_gpt_prompts_ko.md`의 "머리카락 버전" 프롬프트를 쓴다.

> **최종 확정 인물 이미지**: `assets/characters/` 의 12장이 기준이다 (인물 6명, 취업 전 토토, 토토 표정 4종, 화난 부장, 사원증, 단체사진 2종). 확정된 모습은 "온몸이 흙 덩어리"가 아니라 **흙빛 피부의 3D 만화 캐릭터 + 평범한 머리카락 + 정수리의 식물**이다. 새 장면을 뽑을 때는 프롬프트 설명보다 이 이미지를 첨부해 기준으로 삼는다.

### 공통 프롬프트 블록 (모든 인물 프롬프트 맨 앞에 붙임)

```
Stylized 3D animated film still, high-quality character animation look, soft global illumination, 9:16 vertical.
A cartoon humanoid Korean office worker whose whole body is sculpted out of soil, like a living clay-and-dirt figure:
face, neck, ears and hands are all brown earth with visible soil grains, small cracks, tiny pebbles and thin root
fibers. Absolutely no human skin anywhere. Simplified appealing cartoon proportions: slightly large head, big
expressive eyes, simple nose and mouth. No hair at all; a living plant grows directly out of the bare soil scalp.
Clean shapes, readable silhouette, original character design, no text, no watermark.
```

---

## 1. 김토토 사원 (주인공, 20대 후반 남, 입사 1년차)

- 토질: **갓 퍼낸 밝은 갈색 표토** — 촉촉하고 부드러움 (에피소드가 진행될수록 점점 마르고 갈라짐 = 피폐도 표현)
- 나무: 뾰족뾰족 짧은 새싹
- 성격: 순하고 눈치 봄, "설마 가보면 다르겠지" 긍정 회로
- 옷: 살짝 큰 새 흰 셔츠, 남색 슬랙스, 새 사원증

```
[공통 블록]
Character: a man in his late 20s, soft slightly moist light-brown topsoil skin, round gentle face, big innocent eyes,
nervous but hopeful smile. On top of his head: a few very short spiky green sprouts, 2–3 cm tall, sticking straight up
like a short spiky haircut. Wearing a slightly oversized crisp white dress shirt, navy slacks, a brand-new employee ID
lanyard. Standing upright, waist-up portrait, plain light-gray studio background.
```

**캐릭터 시트 (위 이미지 완성 후, 그 이미지를 레퍼런스로 넣고 생성)**

```
Character reference sheet of the exact same character from the reference image, same soil texture, same sprouts,
same outfit: front view, 3/4 view, side profile, back view, plus four facial expressions — overjoyed, confused,
exhausted, dead-inside. Neutral gray background, even lighting, consistent proportions.
```

**피폐 버전 (EP7 이후용)**

```
The same character from the reference image, but the soil skin is now dry, pale and deeply cracked, small crumbs of
dirt falling from the cheeks, dark hollow under-eyes, the sprouts on his head wilted and drooping. Wrinkled shirt,
loosened lanyard, slumped shoulders, empty stare. Fluorescent office light at night.
```

## 2. 박토양 대리 (30대 초반 남, 입사 4년차)

- 토질: **검고 기름진 양토** — 믿음직한 색
- 나무: 한 뼘 묘목, 잎이 튼튼함
- 성격: 일 잘하고 토토에게 잘 알려줌. 다만 늘 바빠서 길게 못 챙김 (설명하다 전화 받으러 감)
- 옷: 소매 걷은 하늘색 셔츠, 한 손엔 늘 서류철이나 휴대폰

```
[공통 블록]
Character: a man in his early 30s, dark rich fertile loam soil skin, calm reliable face, kind but busy eyes.
On top of his head: a healthy sapling about 12 cm tall with several sturdy green leaves. Wearing a light-blue dress
shirt with sleeves rolled up, charcoal slacks, ID lanyard, holding a thick document folder in one hand and a phone
in the other. Waist-up portrait, plain light-gray studio background.
```

## 3. 이정원 대리 (20대 후반 여, 입사 2년차·경력직)

- 토질: **매끈한 붉은 점토** — 단단하고 정돈됨
- 나무: 한 뼘 묘목, 깔끔하게 다듬어진 모양
- 성격: 일잘러, 주변의 신뢰. 토토와 사이 좋고 힘들어 보이면 슬쩍 도와줌 (회식 장소 같이 찾아줌). 박 대리와 같은 인사발령으로 거제에 옴
- 옷: 베이지 블라우스, 검정 슬랙스, 깔끔한 사원증
- ※ 성별은 임의로 여성으로 잡았음. 남성으로 바꾸려면 `a woman` → `a man`, 블라우스 → 셔츠

```
[공통 블록]
Character: a woman in her late 20s, smooth reddish-brown clay soil skin with a fine polished surface, sharp
intelligent eyes, confident relaxed half-smile. On top of her head: a neat sapling about 12 cm tall, tidy symmetrical
leaves. Wearing a beige blouse, black slacks, ID lanyard, holding a tablet. Waist-up portrait, plain light-gray
studio background.
```

## 4. 최태산 과장 (40대 후반 남)

- 토질: **자갈 섞인 단단한 회갈색 암반토** — 거칠고 깊게 갈라짐
- 나무: 30cm, 가지가 뻣뻣하고 가시 돋은 어린 나무
- 성격: 일은 잘하지만 부서 최고 꼰대. "막내가 당연히 해야지". 시공사·감리단 쥐잡듯 잡음. 회식 때 건배사 시키고 술 먹이고 2차 장소 안 알아놓으면 "아직도 이러네". 차장보다 나이가 많아 술 마시면 차장에게도 말실수
- 옷: 회사 로고 없는 남색 현장 점퍼 + 셔츠, 팔짱

```
[공통 블록]
Character: a man in his late 40s, hard gray-brown rocky soil skin full of gravel and deep cracks like bedrock,
square jaw, narrowed judging eyes, one eyebrow raised, mouth pressed in disapproval. On top of his head: a stiff
30 cm young tree with rigid thorny branches and sparse dark leaves. Wearing a plain navy field work jacket over a
white dress shirt, ID lanyard, arms crossed. Waist-up portrait, plain light-gray studio background.
```

## 5. 이난초 차장 (40대 초반 남)

- 토질: **연한 모래빛 사질토** — 부슬부슬, 살짝 흘러내림
- 나무: 50cm, 한쪽으로 살짝 기운 수수한 나무 (가지에 작은 피규어 키링 하나)
- 성격: 최고 명문대 출신, 사회성 부족, 모태솔로 순애보. 일은 나름 잘하지만 권위 없음, 혼자 묵묵히 일함. 마이너 애니·게임 덕후, 유머 감각 없음
- 옷: 체크무늬 셔츠 단추 끝까지 채움, 무테 안경, 낡은 백팩

```
[공통 블록]
Character: a man in his early 40s, pale sandy loose soil skin with fine grains slightly crumbling at the edges,
thin face, rimless glasses, shy averted gaze, awkward tight-lipped expression. On top of his head: a modest 50 cm
tree leaning slightly to one side, with a tiny generic anime-style keychain hanging from one branch. Wearing a plaid
shirt buttoned all the way to the top, khaki pants, an old backpack, ID lanyard. Waist-up portrait, plain light-gray
studio background.
```

## 6. 조궁화 부장 (50대 중반 남)

- 토질: **누런 풍화토(마사토)** — 겉은 번지르르한데 만지면 바스러짐
- 나무: 머리보다 큰 풍성한 나무. **기분 좋을 땐 꽃이 피고, 기분 나쁠 땐 잎이 붉게 시들어 떨어짐** (기분파 연출 장치)
- 성격: 극단적 기분파. 결재를 엉뚱한 걸로 꼬투리. 술 좋아해서 퇴근 후 회식 강제 소집, 계산은 엔빵·부서비 무임승차. 엉뚱한 아이디어로 일을 꼬고 잘못되면 실무자 탓. 타 부서엔 착한 사람이고 싶어 일을 진공청소기처럼 빨아옴 → 실무자가 반대하면 "요즘 MZ들은 이래서 안 돼", 정작 다른 부서가 거절하면 바로 "안 되는구나" 하고 돌아섬
- 옷: 배 나온 체형, 살짝 번들거리는 회색 정장, 금색 넥타이핀

**기분 좋은 버전**

```
[공통 블록]
Character: a man in his mid 50s, yellowish weathered granite soil skin that looks smooth but flakes at the edges,
pot belly, wide overly friendly grin, eyes squeezed in laughter. On top of his head: a large lush tree bigger than
his head with a thick bonsai-like trunk, full of small pink blossoms. Wearing a slightly shiny gray suit, gold tie
pin, ID lanyard, giving a thumbs up. Waist-up portrait, plain light-gray studio background.
```

**기분 나쁜 버전** (기분 좋은 버전을 레퍼런스로 넣고 생성)

```
The same character from the reference image, same suit and same tree shape, but now in a foul mood: deep frown,
cold glare over his glasses, lips curled. The blossoms are gone, the leaves have turned red-brown and are falling,
soil skin dry and flaking. Holding a printed document with a red pen, tapping it irritably. Office background, harsh
fluorescent light.
```

## 7. 부서 단체샷 (프로필 6장 완성 후, 6장 모두 레퍼런스로)

```
Group photo of the six characters from the reference images standing in a row in front of a shabby two-story rural
branch office building in the Korean countryside, tile facade, faded signboard, parking lot with one small van,
green hills behind. Left to right ordered by tree height on their heads, shortest (spiky sprouts) to tallest (large
tree). Each keeps their own soil color and outfit. Overcast summer daylight, documentary photo, 16:9.
```

---

## 8. Higgsfield 작업 순서

1. **김토토 프로필** 먼저 여러 장 뽑아서 마음에 드는 1장 확정 → 이게 시리즈 전체의 질감 기준
   - 모델: `Nano Banana Pro` (2K, 9:16) 추천 — 프롬프트 재현력이 좋고 레퍼런스 이미지를 14장까지 받음
2. 확정한 토토 이미지를 레퍼런스로 넣고 **캐릭터 시트** 생성
3. 나머지 5명은 **토토 이미지를 스타일 레퍼런스로 함께 넣고** 생성 (프롬프트 끝에 `same photographic style and soil-body concept as the reference image, but a different person` 추가) → 질감·조명이 통일됨
4. 단체샷 + 장소 이미지(지사 외관, 사무실, 논밭 버스정류장, 연수원, 감사실, 회식 고깃집, 노래방, 원룸) 생성
   - 올려주신 지사 사진은 장소 레퍼런스로 쓰되, **간판은 가상의 "한국자연공사 거제지사"로 교체** (실제 기관명 노출 방지). 한글 간판은 `GPT Image 2`나 `Nano Banana Pro`가 가장 정확함
5. 영상: `Seedance 2.0` / `Seedance 2.5` (9:16) — 캐릭터 시트를 image_references에 넣으면 컷마다 얼굴이 유지됨. 장면 이미지를 start_image로, 컷당 8~15초 × 10~14컷 = 2분 내외

## 9. 다음 직급용 (추후 승진 에피소드)

토토 이미지를 레퍼런스로 넣고 나무만 교체:

```
The same character from the reference image, older and more tired, same soil skin. The plant on his head has grown
into [a 12 cm sapling / a 30 cm young tree / a 50 cm tree / a large lush tree / a wide heavy tree with roots reaching
his forehead / a towering old tree with moss and a bird nest, extending out of frame]. Outfit upgraded accordingly.
```
