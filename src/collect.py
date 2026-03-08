"""RSS 기반 뉴스 수집 스크립트.

대상 도구의 공식 RSS 피드를 수집하여 data/news.json에 저장한다.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser

DATA_DIR = Path(__file__).parent.parent / "data"
NEWS_FILE = DATA_DIR / "news.json"

# 대상 도구 및 RSS 소스 목록
SOURCES: list[dict] = [
    # Cursor
    {
        "tool": "Cursor",
        "name": "Cursor Changelog",
        "url": "https://cursor.com/changelog/rss.xml",
    },
    # Claude Code (Anthropic)
    {
        "tool": "Claude Code",
        "name": "Claude Code Changelog",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_changelog_claude_code.xml",
    },
    {
        "tool": "Claude Code",
        "name": "Claude Code Releases",
        "url": "https://github.com/anthropics/claude-code/releases.atom",
    },
    # Gemini CLI (Google)
    {
        "tool": "Gemini CLI",
        "name": "Google Developers Blog",
        "url": "https://developers.googleblog.com/feeds/posts/default",
        "filter_keywords": ["gemini cli", "gemini-cli"],
    },
    {
        "tool": "Gemini CLI",
        "name": "Gemini CLI Releases",
        "url": "https://github.com/google-gemini/gemini-cli/releases.atom",
    },
    # Antigravity (Google)
    {
        "tool": "Antigravity",
        "name": "Google Developers Blog",
        "url": "https://developers.googleblog.com/feeds/posts/default",
        "filter_keywords": ["antigravity"],
    },
    # Cline
    {
        "tool": "Cline",
        "name": "Cline Releases",
        "url": "https://github.com/cline/cline/releases.atom",
    },
]


def parse_date(entry: feedparser.FeedParserDict) -> str:
    """피드 항목에서 날짜를 ISO 8601 문자열로 반환한다."""
    for field in ("published_parsed", "updated_parsed"):
        t = getattr(entry, field, None)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc).isoformat()
    return datetime.now(tz=timezone.utc).isoformat()


def matches_keywords(entry: feedparser.FeedParserDict, keywords: list[str]) -> bool:
    """제목·요약이 키워드 중 하나라도 포함하면 True를 반환한다."""
    text = " ".join([
        getattr(entry, "title", ""),
        getattr(entry, "summary", ""),
    ]).lower()
    return any(kw.lower() in text for kw in keywords)


def strip_html(text: str) -> str:
    """HTML 태그를 제거한 순수 텍스트를 반환한다."""
    return re.sub(r"<[^>]+>", "", text).strip()


def collect_source(source: dict) -> list[dict]:
    """단일 소스에서 뉴스를 수집한다."""
    print(f"  Fetching: {source['name']} ({source['url']})", flush=True)
    try:
        feed = feedparser.parse(source["url"])
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return []

    if feed.bozo and not feed.entries:
        print(f"  WARN: 피드 파싱 오류 - {feed.bozo_exception}", file=sys.stderr)
        return []

    keywords: list[str] = source.get("filter_keywords", [])
    items: list[dict] = []

    for entry in feed.entries:
        if keywords and not matches_keywords(entry, keywords):
            continue

        raw_summary = getattr(entry, "summary", "") or ""
        items.append({
            "id": getattr(entry, "id", None) or entry.get("link", ""),
            "title": getattr(entry, "title", ""),
            "url": getattr(entry, "link", ""),
            "source": source["name"],
            "tool": source["tool"],
            "published_at": parse_date(entry),
            "summary": strip_html(raw_summary)[:500] or None,  # v1.1: AI 요약으로 교체 예정
        })

    print(f"  -> {len(items)}건 수집")
    return items


def load_existing() -> list[dict]:
    """기존 news.json을 불러온다."""
    if NEWS_FILE.exists():
        return json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    return []


def merge(existing: list[dict], new_items: list[dict]) -> list[dict]:
    """기존 데이터에 새 항목을 병합한다. URL 기준 중복 제거 후 최신순 정렬."""
    seen: set[str] = {item["url"] for item in existing}
    added = 0
    for item in new_items:
        if item["url"] and item["url"] not in seen:
            existing.append(item)
            seen.add(item["url"])
            added += 1
    print(f"\n신규 {added}건 추가 (전체 {len(existing)}건)")
    return sorted(existing, key=lambda x: x["published_at"], reverse=True)


def main() -> None:
    """뉴스를 수집하여 data/news.json에 저장한다."""
    DATA_DIR.mkdir(exist_ok=True)

    print("=== AI Agent News Hub - 뉴스 수집 시작 ===\n")
    all_new: list[dict] = []
    for source in SOURCES:
        print(f"[{source['tool']}] {source['name']}")
        all_new.extend(collect_source(source))

    existing = load_existing()
    merged = merge(existing, all_new)

    NEWS_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n저장 완료: {NEWS_FILE}")


if __name__ == "__main__":
    main()
