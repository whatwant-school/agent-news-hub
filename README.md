# AI Agent News Hub

AI Agent 도구들의 최신 뉴스를 공식 출처에서 자동 수집하여 웹으로 보여주는 사이트

[![Deploy](https://github.com/whatwant-school/agent-news-hub/actions/workflows/deploy.yml/badge.svg)](https://github.com/whatwant-school/agent-news-hub/actions/workflows/deploy.yml)

## 대상 도구

| 도구 | 설명 |
|------|------|
| [Cursor](https://cursor.com) | AI 코드 에디터 |
| [Claude Code](https://claude.ai/code) | Anthropic AI 코딩 에이전트 |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google Gemini 커맨드라인 에이전트 |
| [Antigravity](https://antigravity.codes) | Google 에이전트 개발 플랫폼 |
| [Cline](https://cline.bot) | VS Code AI 코딩 에이전트 |

## 기능

- 공식 RSS 피드 기반 자동 수집 (6시간마다)
- 도구별 필터 및 키워드 검색
- 반응형 UI, 다크모드 지원
- GitHub Pages 정적 배포

## 프로젝트 구조

```
agent-news-hub/
├── src/
│   ├── collect.py        # RSS 뉴스 수집
│   └── build.py          # 정적 사이트 빌드 (→ dist/)
├── data/
│   └── news.json         # 수집된 뉴스 데이터
├── index.html            # 웹 페이지 템플릿
├── style.css             # 스타일
├── dist/                 # 빌드 결과물 (GitHub Pages 배포 대상, gitignore)
├── docs/
│   └── PRD.md            # 제품 요구사항 문서
├── pyproject.toml        # uv 프로젝트 설정
└── .github/
    └── workflows/
        └── deploy.yml    # 수집 → 빌드 → GitHub Pages 배포
```

## 로컬 실행

**요구사항:** Python 3.11+, [uv](https://docs.astral.sh/uv/)

```bash
# 의존성 설치
uv sync

# 뉴스 수집
uv run python src/collect.py

# 정적 사이트 빌드 → dist/
uv run python src/build.py
```

빌드 후 `dist/index.html`을 브라우저에서 열거나 로컬 서버로 확인:

```bash
cd dist && python -m http.server 8000
```

## 자동 배포

GitHub Actions가 6시간마다 자동으로 실행합니다:

1. 뉴스 수집 (`collect.py`)
2. 변경된 `data/news.json` 커밋
3. 정적 사이트 빌드 (`build.py`)
4. GitHub Pages 배포

수동 실행: GitHub → Actions → **뉴스 수집 & 배포** → Run workflow

> GitHub Pages 첫 설정: Settings → Pages → Source를 **GitHub Actions**로 변경

## 기술 스택

| 레이어 | 기술 |
|--------|------|
| 실행 환경 | Python 3.11+ / uv |
| 수집 | feedparser, httpx |
| 저장 | JSON 파일 |
| 웹 | 정적 HTML / Vanilla CSS / Vanilla JS |
| 배포 | GitHub Pages |
| CI | GitHub Actions |
