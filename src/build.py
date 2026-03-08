"""정적 사이트 빌드 스크립트.

data/news.json + index.html + style.css → dist/ 로 복사·생성한다.
GitHub Pages 배포 대상 디렉터리는 dist/ 이다.

GitHub Actions 에서는 아래 순서로 실행한다:
  uv run python src/collect.py   # 뉴스 수집
  uv run python src/build.py     # 정적 사이트 빌드
  → dist/ 를 GitHub Pages 에 배포
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "news.json"
DIST_DIR = ROOT / "dist"


def load_news() -> list[dict]:
    if not DATA_FILE.exists():
        print(f"ERROR: {DATA_FILE} 없음. collect.py 를 먼저 실행하세요.", file=sys.stderr)
        sys.exit(1)
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def build_meta(news: list[dict]) -> dict:
    """빌드 메타데이터를 반환한다."""
    now = datetime.now(tz=timezone.utc).isoformat()
    latest = news[0]["published_at"] if news else now
    tools: list[str] = sorted({item["tool"] for item in news})
    return {
        "built_at": now,
        "latest_news_at": latest,
        "total": len(news),
        "tools": tools,
    }


def prepare_dist(dist: Path) -> None:
    """dist/ 를 초기화하고 필요한 디렉터리를 생성한다."""
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)
    (dist / "data").mkdir()


def copy_static(dist: Path) -> None:
    """index.html, style.css 를 dist/ 에 복사한다."""
    for filename in ("index.html", "style.css"):
        src = ROOT / filename
        if not src.exists():
            print(f"WARN: {src} 없음 — 건너뜀")
            continue
        shutil.copy2(src, dist / filename)
        print(f"  복사: {filename}")


def write_news_json(dist: Path, news: list[dict]) -> None:
    """data/news.json 을 dist/data/news.json 에 기록한다."""
    out = dist / "data" / "news.json"
    out.write_text(json.dumps(news, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  생성: data/news.json ({len(news)}건)")


def write_meta_json(dist: Path, meta: dict) -> None:
    """빌드 메타데이터를 dist/data/meta.json 에 기록한다."""
    out = dist / "data" / "meta.json"
    out.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  생성: data/meta.json")


def main() -> None:
    """data/news.json 을 읽어 dist/ 에 정적 사이트를 생성한다."""
    print("=== AI Agent News Hub - 정적 사이트 빌드 ===\n")

    news = load_news()
    meta = build_meta(news)

    print(f"뉴스 {meta['total']}건 | 도구: {', '.join(meta['tools'])}")
    print(f"빌드 시각: {meta['built_at']}\n")

    prepare_dist(DIST_DIR)
    copy_static(DIST_DIR)
    write_news_json(DIST_DIR, news)
    write_meta_json(DIST_DIR, meta)

    print(f"\n빌드 완료 → {DIST_DIR}")


if __name__ == "__main__":
    main()
