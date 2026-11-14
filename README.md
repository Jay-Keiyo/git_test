# 토목 데일리

교량 · 터널 · 도로 · 철도 · 항만 · 수자원 · 지반·안전 · 정책·업계 등 **토목 분야 기사만** 모아 보여주는 뉴스 홈페이지입니다.

## 구조

| 경로 | 역할 |
| --- | --- |
| `index.html`, `assets/` | 홈페이지 (빌드 없는 정적 HTML/CSS/JS) |
| `scripts/fetch_news.py` | Google 뉴스 RSS에서 분야별로 검색 → 토목 기사만 걸러 `data/news.json` 저장 |
| `data/sample.json` | `news.json`이 아직 없을 때 보여주는 예시 데이터 (화면에 "예시" 안내 표시) |

### 토목 기사 판별 방식
- 제목에 `토목`, `교량`, `터널`, `댐`, `싱크홀`, `SOC`, `GTX` 등 **핵심 용어**가 있으면 채택
- `도로`, `하천` 같은 일반 용어는 `공사`, `착공`, `준공`, `개통`, `수주` 등 **공사 관련 단어와 함께** 있을 때만 채택
- `분양`, `주가`, `특징주`, `정체`, `교통사고` 등 **무관한 기사는 제외**
- 키워드와 검색어는 `scripts/fetch_news.py` 맨 위 `CATEGORIES`, `STRONG`, `WORKS`, `EXCLUDE`에서 수정할 수 있습니다.

## 사용 방법

1. **기사 수집** — 자동 수집은 꺼져 있습니다. 필요할 때 `python3 scripts/fetch_news.py`를 직접 실행하세요.
2. **홈페이지 공개** — *Settings → Pages*에서 *Deploy from a branch*, 기본 브랜치의 `/ (root)`를 선택하면 `https://<계정>.github.io/<저장소>/`에서 볼 수 있습니다.

### 로컬에서 보기

```bash
python3 scripts/fetch_news.py
```

```bash
python3 -m http.server 8000
```

브라우저에서 http://localhost:8000 을 엽니다. (`file://`로 열면 JSON을 불러오지 못하므로 로컬 서버가 필요합니다.)
