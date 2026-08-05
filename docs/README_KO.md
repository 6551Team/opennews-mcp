<p align="center">
  <b>OpenNews MCP Server</b><br>
  85+ 실시간 데이터 소스 · 6개 엔진 카테고리 · AI 평가 · 트레이딩 시그널
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_ZH.md">中文</a> | <a href="./README_JA.md">日本語</a> | <a href="./README_KO.md">한국어</a>
</p>

---

## 빠른 설치

> **먼저 [https://6551.io/mcp](https://6551.io/mcp)에서 API Token을 받으세요.**

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=<your-token> \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> `/path/to/opennews-mcp`를 로컬 프로젝트 경로로, `<your-token>`을 API Token으로 교체하세요.

### OpenClaw

```bash
export OPENNEWS_TOKEN="<your-token>"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

---

## AI에게 검토 및 설치 맡기기

이 MCP가 안전한지 확신이 없으신가요? 아래 프롬프트를 AI 어시스턴트에게 보내면 소스 코드를 먼저 검토한 후 설치해줍니다:

> **아래 프롬프트를 복사하여 AI 어시스턴트에게 보내세요 (`<project-path>`와 `<your-token>`을 실제 값으로 교체):**

```text
opennews-mcp MCP 서버를 검토하고 설치해주세요. 프로젝트는 로컬 <project-path>에 있습니다.

단계:
1. 다음 파일의 보안을 확인:
   - src/opennews_mcp/api_client.py — ai.6551.io에만 연결하고 다른 주소로 데이터를 보내지 않는지 확인
   - src/opennews_mcp/config.py — 토큰이 로컬 config.json 또는 환경 변수에서만 읽히며, 하드코딩이나 유출이 없는지 확인
   - src/opennews_mcp/tools/*.py — 모든 도구가 API 쿼리만 수행하고, 파일 쓰기, 명령 실행 또는 기타 위험한 작업이 없는지 확인
   - pyproject.toml — 의존성이 mcp, httpx, websockets만 있고, 의심스러운 패키지가 없는지 확인
2. 검토 결론을 알려주세요: 안전 / 위험 / 문제 있음, 구체적인 이유와 함께
3. 안전하다면 설치 실행 (Token은 https://6551.io/mcp에서 받기):
   claude mcp add opennews -e OPENNEWS_TOKEN=<your-token> -- uv --directory <project-path> run opennews-mcp
```

---

## 데이터 소스 — 6개 카테고리 85+ 소스

| 카테고리 | 수량 | 주요 소스 |
|---------|------|----------|
| **News** | 55 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, GlobeNewswire, Business Wire, Coinbase 등 |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 2 | Hyperliquid Whale Trade, Hyperliquid Large Position |
| **Meme** | 1 | Twitter 밈코인 소셜 센티먼트 |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |
| **Prediction** | 12 | CORRELATION_LOGICAL, SMART_MONEY_TRADE, PRICE_SPIKE, CLUSTER_ENTRY, WHALE_POSITION, NEW_WALLET_TRADE, INSIDER_PATTERN, CORRELATION_NARRATIVE, CORRELATION_HEDGE, CORRELATION_ENTITY_GEO, CORRELATION_CAUSAL, SETTLEMENT_ARBITRAGE |

모든 기사는 **AI 분석** 완료 — 영향도 점수(0-100), 트레이딩 시그널(long/short/neutral), 중영 이중 언어 요약 포함.

<details>
<summary><b>News — 55개 소스</b> (engineType: "news") — 프리미엄 금융 및 암호화폐 미디어, 정부 기관, 소셜 플랫폼</summary>

| 소스 코드 | 설명 |
|----------|------|
| Bloomberg | 블룸버그 — 최상위 금융 뉴스 |
| Reuters | 로이터 — 글로벌 통신사 |
| Financial Times | 파이낸셜 타임스 — 프리미엄 비즈니스 뉴스 |
| CNBC | CNBC — 금융 방송 |
| CNN | CNN — 미국 뉴스 네트워크 |
| BBC | BBC — 영국 방송 공사 |
| Fox Business | Fox Business — 미국 금융 뉴스 |
| CoinDesk | CoinDesk — 선도적 암호화폐 미디어 |
| Cointelegraph | Cointelegraph — 암호화폐 미디어 |
| The Block | The Block — 암호화폐 데이터 및 저널리즘 |
| Blockworks | Blockworks — 암호화폐 네이티브 미디어 |
| Decrypt | Decrypt — 암호화폐 및 Web3 미디어 |
| DlNews | DL News — 암호화폐 탐사 보도 |
| A16Z | a16z (Andreessen Horowitz) — 선도적 암호화폐 VC |
| TechCrunch | TechCrunch — 테크 및 스타트업 뉴스 |
| Wired | Wired — 테크 저널리즘 |
| Politico | Politico — 미국 및 EU 정치 뉴스 |
| Business Insider | Business Insider |
| Twitter/X | Twitter/X 암호화폐 인플루언서 게시물 |
| X / Twitter Profile | Twitter/X 프로필 변경 (이름, 자기소개 업데이트) |
| Telegram | Telegram 채널 |
| Weibo | Weibo (微博) — 중국 소셜 미디어 |
| Truth Social | Truth Social — 트럼프 소셜 플랫폼 |
| U.S. Treasury | 미국 재무부 — 공식 성명 |
| U.S. Trade Representative | USTR — 무역 정책 발표 |
| ECB | 유럽중앙은행 — 공식 커뮤니케이션 |
| TASS | TASS — 러시아 국영 통신사 |
| Interfax | Interfax — 러시아 통신사 |
| Handelsblatt | Handelsblatt — 독일 비즈니스 신문 |
| Hadelsblatt | Hadelsblatt — 독일 비즈니스 |
| Welt | Welt — 독일 신문 |
| Telegraph | 텔레그래프 — 영국 뉴스 |
| MS NOW | 모건 스탠리 NOW — 기관 리서치 |
| Ambrey | Ambrey — 해양 및 지정학 인텔리전스 |
| PR Newswire | PR Newswire — 보도자료 |
| GlobeNewswire | GlobeNewswire — 보도자료 |
| Business Wire | Business Wire — 보도자료 |
| Coinbase | Coinbase 공지 및 블로그 |
| Binance | Binance 공지 및 블로그 |
| jin10 | 진스 데이터 — 중국 금융 속보 |
| The Big Whale | The Big Whale — 유럽 암호화폐 미디어 |
| The Verge | The Verge — 테크 미디어 |
| Techinasia | Tech in Asia — 아시아 테크 뉴스 |
| Medium | Medium 블로그 |
| Chainwire | Chainwire — 암호화폐 보도자료 |
| Token Relations | 토큰 관계 및 파트너십 |
| Crypto Narratives | 암호화폐 내러티브 추적 |
| Crypto in America | 미국 암호화폐 산업 보도 |
| 6551News | 6551 플랫폼 오리지널 분석 |
| BWEnews | BWE 뉴스 와이어 |
| AGGRNEWS | 통합 뉴스 피드 |
| Velo | Velo 데이터 인텔리전스 |

</details>

<details>
<summary><b>Listing — 9개 소스</b> (engineType: "listing") — 주요 거래소 토큰 상장 공지</summary>

| 소스 코드 | 설명 |
|----------|------|
| Binance | Binance 신규 토큰 상장 |
| Coinbase | Coinbase 신규 토큰 상장 |
| OKX | OKX 신규 토큰 상장 |
| Bybit | Bybit 신규 토큰 상장 |
| Upbit | Upbit (한국 거래소) 상장 |
| Bithumb | Bithumb (한국 거래소) 상장 |
| Robinhood | Robinhood 암호화폐 상장 |
| Hyperliquid | Hyperliquid 무기한 선물 상장 |
| Aster | Aster 거래소 상장 |

</details>

<details>
<summary><b>OnChain — 2개 소스</b> (engineType: "onchain") — Hyperliquid 고래 거래 및 대형 포지션 활동</summary>

| 소스 코드 | 설명 |
|----------|------|
| Hyperliquid Whale Trade | Hyperliquid 고래 거래 알림 |
| Hyperliquid Large Position | Hyperliquid 대형 포지션 변동 |

</details>

<details>
<summary><b>Meme — 1개 소스</b> (engineType: "meme") — 밈코인 소셜 센티먼트 추적</summary>

| 소스 코드 | 설명 |
|----------|------|
| Twitter | Twitter/X 밈코인 논의 및 바이럴 게시물 |

</details>

<details>
<summary><b>Market — 6개 소스</b> (engineType: "market") — 시장 이상 감지 및 퀀트 시그널</summary>

| 소스 코드 | 설명 |
|----------|------|
| Price Change | 대폭 가격 변동 (급등/급락) |
| Funding Rate | 펀딩비 이상 (무기한 선물) |
| Funding Rate Difference | 거래소 간 펀딩비 차이 |
| Large Liquidation | 대형 청산 이벤트 |
| Market Trends | 전체 시장 추세 변화 |
| OI Change | 미결제약정 대폭 변동 |

</details>

<details>
<summary><b>Prediction — 12개 소스</b> (engineType: "prediction") — AI 예측 및 상관관계 시그널</summary>

| 소스 코드 | 설명 |
|----------|------|
| CORRELATION_LOGICAL | 논리적 상관관계 분석 |
| SMART_MONEY_TRADE | 스마트 머니 거래 추적 |
| PRICE_SPIKE | 가격 급변 감지 |
| CLUSTER_ENTRY | 클러스터 진입 시그널 |
| WHALE_POSITION | 고래 포지션 모니터링 |
| NEW_WALLET_TRADE | 신규 지갑 거래 감지 |
| INSIDER_PATTERN | 내부자 패턴 인식 |
| CORRELATION_NARRATIVE | 내러티브 상관관계 분석 |
| CORRELATION_HEDGE | 헤지 상관관계 분석 |
| CORRELATION_ENTITY_GEO | 지정학적 엔티티 상관관계 |
| CORRELATION_CAUSAL | 인과 상관관계 분석 |
| SETTLEMENT_ARBITRAGE | 결제 차익거래 시그널 |

</details>

---

## 무엇을 할 수 있나요?

연결 후 AI 어시스턴트에게 말하기만 하면 됩니다:

| 당신이 말하면 | 실행되는 작업 |
|-------------|-------------|
| "최신 암호화폐 뉴스" | 최신 기사 조회 |
| "SEC 규제 뉴스 검색" | 전문 키워드 검색 |
| "BTC 관련 뉴스" | 코인으로 필터 |
| "Bloomberg 기사" | 소스로 필터 |
| "온체인 이벤트" | 엔진 유형으로 필터 (onchain) |
| "AI 점수 80 이상 중요 뉴스" | 고점수 필터 |
| "강세 시그널" | 트레이딩 시그널로 필터 (long) |
| "실시간 뉴스 구독" | WebSocket 실시간 업데이트 |

---

## 사용 가능한 도구

| 카테고리 | 도구 | 설명 |
|---------|------|------|
| 디스커버리 | `get_news_sources` | 완전한 엔진 트리 — 6개 카테고리 85+ 소스 및 메타데이터 |
| | `list_news_types` | 필터용 소스 코드 플랫 리스트 |
| 검색 | `get_latest_news` | 85+ 소스에서 최신 기사 조회 |
| | `search_news` | 전체 소스 대상 키워드 검색 |
| | `search_news_by_coin` | 코인별 (BTC, ETH, SOL...) 전체 소스 대상 |
| | `get_news_by_source` | 특정 소스 지정 (예: engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | 카테고리별: news, listing, onchain, meme, market, prediction |
| | `search_news_advanced` | 복합 필터: 코인 + 키워드 + 엔진 유형 조합 |
| AI | `get_high_score_news` | 높은 AI 영향도 점수 기사 (0-100 스케일) |
| | `get_news_by_signal` | AI 트레이딩 시그널별: long / short / neutral |
| 금융 강화 | `search_companies` | 후보를 찾거나 정확한 canonical issuer, ticker, CIK, KRX 코드, DART 코드, typed identifier로 식별 |
| | `get_company_info` | 정확히 하나의 issuer를 식별하고 SEC/DART filings, 리서치 보고서, transcript, 재무 항목을 나열 |
| | `get_company_report_text` | 안정적인 report ID/type으로 특정 issuer에 연결된 filing, 리서치 보고서, transcript를 조회 |
| | `get_key_market_events` | 주요 매크로 일정과 설정된 중점 기업의 실적 이벤트 조회 |
| | `get_politician_stock_activity` | 미국 하원 PTR 공식 주식 거래 공시 조회 |
| | `get_institution_stock_holdings` | 지연된 SEC Form 13F 기관 주식 보유 공시 조회 |
| | `get_crypto_holdings` | 기관 또는 주소의 지갑 기준 온체인 보유 증거 조회 |
| | `get_crypto_holding_changes` | 인접 스냅샷 사이의 온체인 보유 변화 조회 |
| 실시간 | `subscribe_latest_news` | WebSocket 라이브 피드, 코인 및 엔진 유형 필터 지원 |

여러 시장에 걸친 issuer나 동명이 회사의 경우 먼저 `ambiguity_candidates[]`를 확인한 뒤, 정확한 selector 하나만 지정해 다시 호출하세요. MCP 도구는 `canonical_issuer_id`, `ticker`, `cik`, `krx_stock_code`, `dart_corp_code` 또는 `identifier` + `identifier_type` + `market`을 받습니다. Raw HTTP 호출자는 범용 `identifier` 형식을 사용해야 합니다. 예: `SEC:0002120882`는 `identifier=0002120882, identifier_type=cik, market=US`, `DART:00164779`는 `identifier=00164779, identifier_type=dart_corp_code, market=KR`에 해당합니다.

> 자세한 사용 가이드와 예제는 [지식 가이드](../knowledge/guide.md)를 참조하세요.

---

## 설정

### API Token 받기

[https://6551.io/mcp](https://6551.io/mcp)에서 API Token을 받으세요.

환경 변수 설정:

```bash
# macOS / Linux
export OPENNEWS_TOKEN="<your-token>"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "<your-token>"
```

| 변수 | 필수 | 설명 |
|------|------|------|
| `OPENNEWS_TOKEN` | **예** | 6551 API Bearer 토큰 (https://6551.io/mcp에서 받기) |
| `OPENNEWS_API_BASE` | 아니오 | REST API URL 재정의 |
| `OPENNEWS_WSS_URL` | 아니오 | WebSocket URL 재정의 |
| `OPENNEWS_MAX_ROWS` | 아니오 | 요청당 최대 결과 수 (기본: 100) |

프로젝트 루트의 `config.json`도 지원 (환경 변수 우선):

```json
{
  "api_base_url": "https://ai.6551.io",
  "wss_url": "wss://ai.6551.io/open/news_wss",
  "api_token": "<your-token>",
  "max_rows": 100
}
```

---

## WebSocket 실시간 구독

**엔드포인트**: `wss://ai.6551.io/open/news_wss?token=YOUR_TOKEN`

실시간 암호화폐 뉴스 업데이트를 구독합니다.

### 하트비트

연결을 유지하기 위해 클라이언트는 `ping`을 보낼 수 있으며, 서버는 `pong`으로 응답합니다.

### 뉴스 구독

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "news.subscribe",
  "params": {
    "engineTypes": {
      "news": ["Bloomberg", "CoinDesk"],
      "onchain": []
    },
    "coins": ["BTC", "ETH"],
    "hasCoin": true
  }
}
```

**응답**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "filters": {
      "engineTypes": {...},
      "coins": [...],
      "hasCoin": true
    }
  }
}
```

**필터 매개변수** (모두 선택사항):
- `engineTypes`: 엔진 유형에서 뉴스 유형 코드로의 매핑 객체
  - 키: 엔진 유형 (예: `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`, `"prediction"`)
  - 값: 뉴스 유형 코드 배열 (예: `["Bloomberg", "CoinDesk"]`)
  - 빈 배열 `[]`은 해당 엔진의 모든 뉴스 유형을 의미
  - `list_news_types` 도구로 사용 가능한 코드 확인
- `coins`: 코인 심볼 배열 (예: `["BTC", "ETH"]`)
  - 지정한 코인으로 뉴스 필터
  - 빈 배열 `[]` 또는 생략 시 모든 코인 수신
- `hasCoin`: 불리언, true일 경우 코인 태그가 있는 뉴스만 수신

### 구독 취소

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "news.unsubscribe"
}
```

### 서버 푸시 - 뉴스 업데이트

필터와 일치하는 새 뉴스가 있으면 서버가 푸시:

```json
{
  "jsonrpc": "2.0",
  "method": "news.update",
  "params": {
    "id": "unique-article-id",
    "text": "기사 제목 또는 내용",
    "newsType": "Bloomberg",
    "engineType": "news",
    "link": "https://...",
    "coins": [
      {
        "symbol": "BTC",
        "market_type": "cex",
        "match": "title"
      }
    ],
    "ts": 1708473600000
  }
}
```

### 서버 푸시 - AI 뉴스 업데이트

AI 분석이 있는 뉴스 (구독한 경우):

```json
{
  "jsonrpc": "2.0",
  "method": "news.ai_update",
  "params": {
    "id": "unique-article-id",
    "text": "기사 제목",
    "newsType": "Bloomberg",
    "engineType": "news",
    "link": "https://...",
    "coins": [
      {
        "symbol": "BTC",
        "market_type": "cex",
        "score": 85,
        "signal": "long",
        "grade": "A"
      },
      {
        "symbol": "ETH",
        "market_type": "cex",
        "score": 45,
        "signal": "short",
        "grade": "B"
      }
    ],
    "aiRating": {
      "score": 85,
      "grade": "A",
      "signal": "long"
    },
    "ts": 1708473600000
  }
}
```

**참고**: `coins` 배열의 각 코인에는 개별 AI 평가가 포함됩니다:
- `score`: 해당 코인의 영향력 점수 (0-100)
- `signal`: 해당 코인의 시그널 방향 (long/short/neutral)
- `grade`: 해당 코인의 등급 (A+/A/B+/B/C)

최상위 `aiRating.score`는 모든 코인 중 최고 점수를 나타냅니다.

### 서버 푸시 - 전략 트리거

> **Max 구독이 필요합니다.** [https://www.newsliquid.com/strategy](https://www.newsliquid.com/strategy)에서 전략을 생성하고 관리하세요.

사용자 정의 전략이 트리거되면(예: 가격 알림, 키워드 매칭) 서버가 푸시합니다:

```json
{
  "jsonrpc": "2.0",
  "method": "strategy.triggered",
  "params": {
    "id": 1234567890,
    "newsType": "strategy",
    "engineType": "market",
    "text": "BTC 펀딩비율 0.15%",
    "link": "",
    "source": "binance",
    "description": "{...}",
    "coins": [
      {
        "symbol": "BTC",
        "market_type": "cex"
      }
    ],
    "ts": "2025-01-15T08:30:00Z",
    "strategy": {
      "id": 42,
      "name": "BTC 펀딩비율 알림",
      "sourceType": "market",
      "soundId": "alert-1",
      "bgColor": "#FF6B35",
      "metrics": {
        "funding_rate_high": {
          "value": 0.15,
          "unit": "%"
        }
      }
    },
    "aiRating": {
      "score": 85
    }
  }
}
```

**전략 푸시 필드 설명**:
- `id`: 뉴스/이벤트 ID
- `engineType`: 소스 엔진 유형 (`market`, `news`, `onchain`)
- `text`: 이벤트 설명
- `coins`: 관련 코인
- `ts`: 이벤트 타임스탬프
- `strategy.id`: 사용자 전략 ID
- `strategy.name`: 전략 이름
- `strategy.sourceType`: 전략 소스 유형
- `strategy.soundId`: 알림 사운드 ID
- `strategy.bgColor`: 알림 배경색
- `strategy.metrics`: 트리거된 지표 값 및 단위
- `aiRating` (선택): 뉴스에 AI 점수가 있을 때 존재:
  - `score`: 영향력 점수 (0-100)
- `relatedAddress` (선택): 관련 지갑 주소

**참고**: 전략 트리거 이벤트는 NATS를 통해 사용자별로 푸시됩니다. 별도의 구독이 필요 없으며, 연결 후 해당 사용자의 전략 이벤트를 자동으로 수신합니다.

---

## 데이터 구조

각 기사:

```json
{
  "id": "unique-article-id",
  "text": "제목 / 내용",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [
    {
      "symbol": "BTC",
      "market_type": "cex",
      "match": "title",
      "score": 85,
      "signal": "long",
      "grade": "A"
    }
  ],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long"
  },
  "ts": 1708473600000
}
```

| AI 필드 | 설명 |
|---------|------|
| `score` | 0-100 영향도 점수 (최상위 = 모든 코인 중 최고 점수) |
| `signal` | `long`(강세) / `short`(약세) / `neutral` |
| `coins[].score` | 개별 코인의 영향도 점수 (0-100) |
| `coins[].signal` | 개별 코인의 시그널 방향 (long/short/neutral) |
| `coins[].grade` | 개별 코인의 등급 (A+/A/B+/B/C) |

---

<details>
<summary><b>기타 클라이언트 — 수동 설치</b> (클릭하여 펼치기)</summary>

> 아래 모든 설정에서 `/path/to/opennews-mcp`를 로컬의 실제 프로젝트 경로로, `<your-token>`을 [https://6551.io/mcp](https://6551.io/mcp)에서 받은 Token으로 교체하세요.

### Claude Desktop

설정 파일 편집 (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` 또는 Settings > MCP Servers:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cline

VS Code 사이드바 > Cline > MCP Servers > Configure, `cline_mcp_settings.json` 편집:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Continue.dev

`~/.continue/config.yaml`:

```yaml
mcpServers:
  - name: opennews
    command: uv
    args:
      - --directory
      - /path/to/opennews-mcp
      - run
      - opennews-mcp
    env:
      OPENNEWS_TOKEN: <your-token>
```

### Cherry Studio

설정 > MCP 서버 > 추가 > 유형 stdio: Command `uv`, Args `--directory /path/to/opennews-mcp run opennews-mcp`, Env `OPENNEWS_TOKEN`.

### Zed Editor

`~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "opennews": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
        "env": {
          "OPENNEWS_TOKEN": "<your-token>"
        }
      }
    }
  }
}
```

### 기타 stdio MCP 클라이언트

```bash
OPENNEWS_TOKEN=<your-token> \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## 호환성

| 클라이언트 | 설치 방법 | 상태 |
|-----------|----------|------|
| **Claude Code** | `claude mcp add` | 원클릭 |
| **OpenClaw** | Skill 디렉토리 복사 | 원클릭 |
| Claude Desktop | JSON 설정 | 지원 |
| Cursor | JSON 설정 | 지원 |
| Windsurf | JSON 설정 | 지원 |
| Cline | JSON 설정 | 지원 |
| Continue.dev | YAML / JSON | 지원 |
| Cherry Studio | GUI | 지원 |
| Zed | JSON 설정 | 지원 |

---

## 관련 프로젝트

- [twitter-mcp](https://github.com/6551-io/twitter-mcp) - Twitter/X 데이터 MCP 서버

---

## 개발

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector 테스트
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### 프로젝트 구조

```
├── README.md
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # 내장 지식
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # 진입점
    ├── app.py                 # FastMCP 인스턴스
    ├── config.py              # 설정 로더
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # 도구
```

## 라이선스

MIT
