# AI Agent News Hub — Product Requirements Document (PRD)

**Document Version:** 1.3  
**Last Updated:** 2025-03-08  
**Status:** Draft

---

## Design Principles

- **단순성 우선**: 구현은 최대한 단순하게 유지한다. 불필요한 추상화·미들웨어·의존성을 지양한다.
- **AI 요약 확장성**: v1.1에서 AI 요약을 도입할 수 있도록, MVP 단계부터 데이터 구조에 `summary` 필드를 확장 가능하게 설계한다. (MVP에서는 원문 메타데이터만 사용)

---

## Open Questions (Discovery)

다음 항목들은 추가 확인이 필요합니다. PRD 반복 시 업데이트 예정입니다.

- **데드라인**: MVP 출시 목표일이 있나요?

---

## 1. Executive Summary

### Problem Statement

AI Agent 도구 생태계가 빠르게 성장하면서, 개발자와 PM은 Cursor, Claude Code, Gemini CLI, Antigravity, Cline 등 다양한 도구의 최신 소식·업데이트·비교 정보를 한곳에서 파악하기 어렵다. 여러 블로그, X(Twitter), 공식 문서를 직접 돌아다니며 정보를 모으는 데 시간이 많이 소요된다.

### Proposed Solution

AI Agent 도구 관련 최신 뉴스를 **신뢰할 수 있는 출처**(공식 홈페이지, 공식 블로그, 뉴스)에서 수집·정리하여 웹에서 한눈에 볼 수 있는 뉴스 허브를 구축한다. Python + uv로 단순하게 구현하고, GitHub Pages로 배포한다. 사용자는 카테고리, 날짜, 도구별로 필터링하여 필요한 정보만 빠르게 확인할 수 있다.

### Success Criteria

| KPI | 목표 | 측정 방법 |
|-----|------|-----------|
| **뉴스 커버리지** | 주당 최소 20건 이상의 신규 뉴스 수집 | 수집 파이프라인 로그 |
| **페이지 로드 시간** | LCP(Largest Contentful Paint) ≤ 2.5초 | Lighthouse 성능 점수 |
| **접근성** | Lighthouse Accessibility 점수 ≥ 90 | Lighthouse 접근성 점수 |
| **일일 방문자** | MVP 출시 후 4주 내 DAU 100명 이상 | 분석 도구 (GA, Plausible 등) |
| **이탈률** | 세션당 2페이지 이상 조회 비율 ≥ 40% | 세션 분석 |

---

## 2. User Experience & Functionality

### User Personas

| Persona | 설명 | 주요 니즈 |
|---------|------|------------|
| **개발자 (Developer)** | AI 코딩 도구를 일상적으로 사용하는 개발자 | 새 도구 출시, API 변경, 베스트 프랙티스 소식 |
| **PM/기획자 (Product Manager)** | AI 제품 기획·도입 검토 담당자 | 시장 동향, 경쟁사/유사 도구 비교 |
| **AI 관심자 (AI Enthusiast)** | AI 에이전트 생태계를 넓게 관찰하는 사용자 | 트렌드, 인기 도구, 커뮤니티 논의 |

### User Stories

#### US-1: 뉴스 목록 조회
**As a** 개발자, **I want to** AI Agent 도구 관련 최신 뉴스 목록을 날짜순으로 볼 수 있어야 **so that** 최신 동향을 빠르게 파악할 수 있다.

**Acceptance Criteria:**
- [ ] 뉴스 목록이 최신순(날짜 내림차순)으로 표시된다.
- [ ] 각 뉴스 항목에 제목, 출처, 날짜, 요약(선택)이 표시된다. — *MVP: 원문 메타데이터(제목, description) 사용. `summary` 필드는 v1.1 AI 요약 확장을 위해 스키마에 포함.*
- [ ] 클릭 시 원문 링크로 이동한다.
- [ ] 1페이지당 20~30건 표시, 페이지네이션 또는 무한 스크롤 지원.

#### US-2: 카테고리/도구별 필터링
**As a** PM, **I want to** 특정 AI 도구(Cursor, Claude Code, Gemini CLI, Antigravity, Cline) 또는 카테고리(예: 출시, 업데이트)별로 뉴스를 필터링할 수 있어야 **so that** 관심 영역만 집중해서 볼 수 있다.

**Acceptance Criteria:**
- [ ] 도구별 필터(Cursor, Claude Code, Gemini CLI, Antigravity, Cline)가 제공된다.
- [ ] 카테고리별 필터(예: 출시, 업데이트, 튜토리얼, 비교)가 제공된다.
- [ ] 필터 적용 시 URL 쿼리 파라미터로 상태가 반영되어 공유 가능하다.

#### US-3: 검색
**As a** AI 관심자, **I want to** 키워드로 뉴스를 검색할 수 있어야 **so that** 특정 주제(예: "RAG", "agent") 관련 기사만 찾을 수 있다.

**Acceptance Criteria:**
- [ ] 검색어 입력 시 제목·요약·태그에서 매칭되는 뉴스만 표시된다.
- [ ] 검색 결과가 500ms 이내에 표시된다 (클라이언트 사이드 필터 기준).

#### US-4: 반응형 웹
**As a** 모바일 사용자, **I want to** 스마트폰에서도 편하게 뉴스를 읽을 수 있어야 **so that** 이동 중에도 최신 소식을 확인할 수 있다.

**Acceptance Criteria:**
- [ ] 320px ~ 1920px 뷰포트에서 레이아웃이 깨지지 않는다.
- [ ] 터치 타겟은 최소 44x44px을 유지한다.

### User Flow

```
[방문] → [목록 조회] → [필터/검색 (선택)] → [뉴스 클릭] → [원문 이동]
                ↓
         [북마크/공유 (v1.1)]
```

### Non-Goals

| 항목 | 이유 |
|------|------|
| **실시간 푸시 알림** | MVP 범위 외, v1.1 이후 검토 |
| **사용자 계정·로그인** | MVP는 익명 조회만 지원 |
| **뉴스 큐레이션/편집 UI** | MVP는 수집 파이프라인 기반 자동 수집만 |
| **댓글·소셜 기능** | 범위 확대 시 검토 |
| **AI 요약 생성** | v1.1에서 구현. MVP는 데이터 스키마만 확장 가능하게 설계 |

---

## 3. AI System Requirements (If Applicable)

### 적용 범위

- **뉴스 수집**: MVP에서는 RSS/수동 큐레이션만 사용. AI 기반 수집(예: LLM으로 관련성 판별)은 v1.1에서 검토.
- **요약/태깅**: MVP에서는 원문 메타데이터(제목, description)만 사용. **AI 요약은 v1.1에서 구현** — 데이터 스키마에 `summary` 필드(optional)를 두어 확장 가능하게 설계.

### v1.1 AI 요약 확장을 위한 설계

- **데이터 스키마**: `summary` 필드 nullable, MVP에서는 비워두거나 원문 description 사용
- **파이프라인**: 수집 → 저장 단계에 v1.1에서 "AI 요약 추론" 단계 삽입 가능하도록 모듈화

### Tool Requirements (v1.1 시)

- **LLM API**: 요약 생성 시 OpenAI/Anthropic/기타 API
- **임베딩**: 검색 품질 향상 시 벡터 DB + 임베딩 API

### Evaluation Strategy (AI 도입 시)

- 요약 품질: 5점 척도로 샘플 20건 수동 평가, 평균 ≥ 4.0
- 관련성 필터: 수집된 뉴스 중 "AI Agent 도구 관련" 비율 ≥ 85%

---

## 4. Technical Specifications

### Architecture Overview

```
[신뢰 소스] → [수집 파이프라인] → [저장소] → [정적 빌드] → [GitHub Pages] → [사용자]
   (RSS 등)   (Python + uv)     (JSON/파일)   (정적 HTML)   (배포)
```

- **수집**: Python + uv 기반 스크립트. GitHub Actions Cron으로 주기적 수집 (예: 6시간마다)
- **저장**: 구조화된 뉴스 메타데이터 (제목, URL, 출처, 날짜, 도구 태그, 카테고리, `summary` 필드)
- **웹**: 정적 사이트(HTML/JS) 생성 후 GitHub Pages 배포. **구현은 최대한 단순하게** 유지

### 대상 도구 (뉴스 수집 대상)

다음 AI Agent 도구들의 최신 소식을 수집·표시한다.

| 도구 | 비고 |
|------|------|
| Cursor | |
| Claude Code | |
| Gemini CLI | |
| Antigravity | |
| Cline | |

- **필터**: 사용자는 위 도구별로 뉴스를 필터링할 수 있다.
- **확장**: 추후 도구 추가 시 설정/설정 파일로 관리 가능하도록 설계.

### 뉴스 소스 (신뢰할 수 있는 출처만)

| 유형 | 예시 | 비고 |
|------|------|------|
| **공식 홈페이지** | Cursor, Claude, Gemini, Antigravity, Cline 등 대상 도구 공식 사이트 | RSS, 공식 블로그 링크 |
| **공식 블로그** | Anthropic Blog, Google AI Blog 등 | RSS 피드 |
| **뉴스/미디어** | TechCrunch, The Verge, Hacker News 등 검증된 뉴스 | RSS/API |

- **원칙**: 소스는 공식 홈페이지·공식 블로그·검증된 뉴스 사이트에 한정. 신뢰도가 낮은 소스는 제외.

### Integration Points

| 구분 | 항목 | 비고 |
|------|------|------|
| **뉴스 소스** | 공식 홈페이지 RSS, 공식 블로그, 뉴스 사이트 RSS | 신뢰할 수 있는 출처만 |
| **저장** | JSON 파일 또는 SQLite | 최소 의존성, 단순 구조 |
| **배포** | GitHub Pages | 정적 사이트만 지원 |
| **Auth** | MVP 없음 | v1.1 이후 검토 |

### Security & Privacy

- **데이터 수집**: 공개된 RSS/API만 사용, 크롤링 시 robots.txt 준수
- **개인정보**: MVP에서 수집·저장하지 않음
- **HTTPS**: GitHub Pages 기본 HTTPS 적용

### Tech Stack

| 레이어 | 기술 | 비고 |
|--------|------|------|
| **실행 환경** | Python + uv | 패키지 관리·실행 |
| **수집** | Python (feedparser, requests 등) | 최소 의존성 |
| **저장** | JSON 파일 또는 SQLite | 단순 구조 |
| **웹** | 정적 HTML/CSS/JS | 또는 단순 정적 생성기 |
| **배포** | GitHub Pages | 정적 호스팅 |

### 추천 스택 (최소 복잡도)

단순성 우선 원칙에 따라, 아래 조합을 권장한다.

| 구분 | 선택 | 이유 |
|------|------|------|
| **실행 환경** | Python 3.11+ / uv | PRD 지정, 의존성 최소화 |
| **수집** | feedparser, httpx | RSS 파싱·HTTP 표준 라이브러리, 의존성 2개 |
| **저장** | JSON 파일 | DB 없음, Git 추적 가능, 설정 불필요 |
| **웹** | 정적 HTML + Vanilla JS + Vanilla CSS | 빌드 도구 없음, 프레임워크 없음 |
| **배포** | GitHub Pages | 정적 호스팅, 비용 없음 |
| **CI** | GitHub Actions | 수집 Cron, 배포 자동화 |

**데이터 흐름:**
```
RSS 소스 → collect.py (feedparser) → news.json → index.html (fetch + 렌더)
                                                    ↓
                                            GitHub Pages 배포
```

**의존성 (수집 스크립트):**
- `feedparser` — RSS/Atom 파싱
- `httpx` — HTTP 요청 (requests 대안, 현대적 API)

**프로젝트 구조 (권장):**
```
/
├── pyproject.toml      # uv 프로젝트
├── src/
│   └── collect.py      # 수집 스크립트
├── data/
│   └── news.json       # 수집 결과 (생성)
├── index.html          # 정적 페이지
├── style.css           # 스타일
├── .github/
│   └── workflows/
│       └── collect.yml # 6시간마다 수집 + 배포
└── docs/               # PRD 등
```

**비선택 (복잡도 증가):**
- SQLite — JSON으로 충분, DB 설정 불필요
- React/Vue/Svelte — Vanilla JS로 필터·검색 구현 가능
- Tailwind/Vite — 빌드 단계 추가, Vanilla CSS로 충분
- Jinja2/템플릿 엔진 — 클라이언트 fetch로 대체 가능

---

## 5. Risks & Roadmap

### Phased Rollout

| 단계 | 범위 | 예상 기간 |
|------|------|-----------|
| **MVP** | 뉴스 목록, 기본 필터, 반응형 UI, 수동/반자동 수집 | 4~6주 |
| **v1.1** | **AI 요약** 도입, 검색 고도화, 알림(이메일) | +4주 |
| **v2.0** | 사용자 계정, 북마크, 맞춤 피드 | +6주 |

### Technical Risks

| 리스크 | 영향 | 완화 방안 |
|--------|------|-----------|
| **뉴스 소스 API 제한** | 수집량 감소 | 다중 소스, 캐시, 폴백 소스 |
| **수집 파이프라인 장애** | 신규 뉴스 누락 | 모니터링, 재시도, 알림 |
| **GitHub Pages 제한** | 빌드/대역폭 제한 | 정적 사이트 유지로 최소화 |

---

## Appendix: PRD 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-03-08 | 초안 작성 |
| 1.1 | 2025-03-08 | Python+uv, GitHub Pages, 신뢰 소스, 단순성 원칙, AI 요약 v1.1 확장성 반영 |
| 1.2 | 2025-03-08 | 대상 도구 목록 확정 (Cursor, Claude Code, Gemini CLI, Antigravity, Cline) |
| 1.3 | 2025-03-08 | 추천 스택 (최소 복잡도) 정리 |
