#!/usr/bin/env python3
"""토목 관련 기사만 골라 data/news.json 으로 저장합니다.

Google 뉴스 RSS 검색을 분야별 검색어로 조회한 뒤, 제목에 토목 관련 용어가
들어 있는 기사만 남기고(분양·주가·교통정체 같은 잡음은 제외) 분야를 분류합니다.
표준 라이브러리만 사용하므로 별도 설치가 필요 없습니다.
"""
from __future__ import annotations

import email.utils
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "news.json"
KEEP_DAYS = 14
MAX_ITEMS = 200
RSS = "https://news.google.com/rss/search?q={q}+when:7d&hl=ko&gl=KR&ceid=KR:ko"

# 분야별 검색어(queries)와 분류용 키워드(keywords)
CATEGORIES: dict[str, dict] = {
    "bridge": {
        "label": "교량",
        "queries": ["교량 공사", "교량 건설", "대교 착공"],
        "keywords": ["교량", "대교", "사장교", "현수교", "교각", "상판", "육교"],
    },
    "tunnel": {
        "label": "터널·지하",
        "queries": ["터널 공사", "지하차도 공사", "대심도 터널"],
        "keywords": ["터널", "지하차도", "대심도", "TBM", "쉴드", "지하화"],
    },
    "road": {
        "label": "도로",
        "queries": ["고속도로 건설", "도로 확장 공사", "국도 개통"],
        "keywords": ["고속도로", "국도", "도로", "나들목", "IC", "우회도로", "포장"],
    },
    "rail": {
        "label": "철도",
        "queries": ["철도 건설 공사", "GTX 공사", "도시철도 착공"],
        "keywords": ["철도", "GTX", "도시철도", "지하철", "경전철", "트램", "복선"],
    },
    "port": {
        "label": "항만·공항",
        "queries": ["항만 공사", "신공항 건설", "방파제 공사"],
        "keywords": ["항만", "부두", "방파제", "신항", "신공항", "활주로", "매립", "준설"],
    },
    "water": {
        "label": "수자원",
        "queries": ["댐 건설", "하천 정비 사업", "상하수도 공사"],
        "keywords": ["댐", "하천", "제방", "상수도", "하수", "치수", "저수지", "배수", "홍수"],
    },
    "safety": {
        "label": "지반·안전",
        "queries": ["싱크홀", "지반침하", "건설현장 붕괴", "옹벽 붕괴"],
        "keywords": ["싱크홀", "지반", "침하", "붕괴", "안전점검", "옹벽", "사면", "균열", "땅꺼짐"],
    },
    "industry": {
        "label": "정책·업계",
        "queries": ["토목 수주", "SOC 예산", "토목 공사", "건설기술 토목"],
        "keywords": ["토목", "SOC", "수주", "입찰", "턴키", "건설기술", "인프라", "기술형입찰"],
    },
}

# 이 중 하나가 제목에 있으면 바로 토목 기사로 인정
STRONG = [
    "토목", "교량", "대교", "터널", "지하차도", "대심도", "항만", "방파제", "댐", "제방",
    "싱크홀", "땅꺼짐", "지반침하", "SOC", "GTX", "철도", "도시철도", "옹벽", "준설", "신공항",
]
# 약한 키워드(도로·하천 등)는 아래 공사 관련 단어와 함께 나올 때만 인정
WORKS = [
    "공사", "건설", "착공", "준공", "개통", "시공", "설계", "사업", "정비", "확장",
    "보강", "개량", "발주", "수주", "입찰", "완공", "복구", "점검",
]
# 토목과 무관한 잡음
EXCLUDE = [
    "분양", "청약", "특징주", "주가", "목표가", "급등", "급락", "정체", "귀성", "귀경",
    "음주", "교통사고", "날씨", "운세", "부고", "인사]", "[인사", "아파트값", "전세",
]

UA = "Mozilla/5.0 (compatible; civil-news-fetcher/1.0)"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def clean_title(title: str, source: str) -> str:
    title = title.strip()
    if source and title.endswith(" - " + source):
        title = title[: -len(source) - 3]
    else:
        title = re.sub(r"\s+-\s+[^-]{1,30}$", "", title)
    return re.sub(r"\s+", " ", title).strip()


def is_civil(title: str) -> bool:
    if any(word in title for word in EXCLUDE):
        return False
    if any(word in title for word in STRONG):
        return True
    weak = any(k in title for c in CATEGORIES.values() for k in c["keywords"])
    return weak and any(w in title for w in WORKS)


def classify(title: str, fallback: str) -> str:
    best, best_score = fallback, 0
    for key, cat in CATEGORIES.items():
        score = sum(len(k) for k in cat["keywords"] if k in title)
        if score > best_score:
            best, best_score = key, score
    return best


def parse_rss(xml_bytes: bytes, category: str) -> list[dict]:
    items = []
    root = ET.fromstring(xml_bytes)
    for node in root.iter("item"):
        source_el = node.find("source")
        source = (source_el.text or "").strip() if source_el is not None else ""
        title = clean_title(node.findtext("title", ""), source)
        link = (node.findtext("link") or "").strip()
        if not title or not link or not is_civil(title):
            continue
        published = None
        pub = node.findtext("pubDate")
        if pub:
            try:
                published = email.utils.parsedate_to_datetime(pub).astimezone(timezone.utc)
            except (TypeError, ValueError):
                published = None
        items.append({
            "id": hashlib.sha1(re.sub(r"\W", "", title).encode()).hexdigest()[:12],
            "title": title,
            "link": link,
            "source": source or "언론사 미상",
            "published": (published or datetime.now(timezone.utc)).isoformat(timespec="seconds"),
            "category": classify(title, category),
        })
    return items


def load_existing() -> list[dict]:
    try:
        return json.loads(OUT.read_text(encoding="utf-8")).get("items", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def main() -> int:
    collected: dict[str, dict] = {}
    for item in load_existing():
        collected[item["id"]] = item

    ok = 0
    for key, cat in CATEGORIES.items():
        for query in cat["queries"]:
            url = RSS.format(q=urllib.parse.quote(query))
            try:
                for item in parse_rss(fetch(url), key):
                    collected.setdefault(item["id"], item)
                ok += 1
            except Exception as exc:  # 한 검색어가 실패해도 나머지는 계속
                print(f"[warn] {query}: {exc}", file=sys.stderr)
            time.sleep(1)

    if ok == 0:
        print("[error] 모든 검색어 조회에 실패했습니다. 기존 파일을 유지합니다.", file=sys.stderr)
        return 1

    cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)
    items = [i for i in collected.values() if datetime.fromisoformat(i["published"]) >= cutoff]
    items.sort(key=lambda i: i["published"], reverse=True)
    items = items[:MAX_ITEMS]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "categories": {k: v["label"] for k, v in CATEGORIES.items()},
        "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)}건 저장 → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
