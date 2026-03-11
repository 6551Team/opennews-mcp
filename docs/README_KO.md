<p align="center">
  <b>OpenNews MCP Server</b><br>
  72+ 실시간 데이터 소스 · 5개 엔진 카테고리 · AI 평가 · 트레이딩 시그널
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

## 데이터 소스 — 5개 카테고리 72+ 소스

| 카테고리 | 수량 | 주요 소스 |
|---------|------|----------|
| **News** | 53 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, Coinbase, Phoenixnews 등 |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 3 | Hyperliquid Whale Trade, Hyperliquid Large Position, KOL Trade |
| **Meme** | 1 | Twitter 밈코인 소셜 센티먼트 |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |

모든 기사는 **AI 분석** 완료 — 영향도 점수(0-100), 트레이딩 시그널(long/short/neutral), 중영 이중 언어 요약 포함.

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
| 디스커버리 | `get_news_sources` | 완전한 엔진 트리 — 5개 카테고리 72+ 소스 및 메타데이터 |
| | `list_news_types` | 필터용 소스 코드 플랫 리스트 |
| 검색 | `get_latest_news` | 72+ 소스에서 최신 기사 조회 |
| | `search_news` | 전체 소스 대상 키워드 검색 |
| | `search_news_by_coin` | 코인별 (BTC, ETH, SOL...) 전체 소스 대상 |
| | `get_news_by_source` | 특정 소스 지정 (예: engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | 카테고리별: news, listing, onchain, meme, market |
| | `search_news_advanced` | 복합 필터: 코인 + 키워드 + 엔진 유형 조합 |
| AI | `get_high_score_news` | 높은 AI 영향도 점수 기사 (0-100 스케일) |
| | `get_news_by_signal` | AI 트레이딩 시그널별: long / short / neutral |
| 실시간 | `subscribe_latest_news` | WebSocket 라이브 피드, 코인 및 엔진 유형 필터 지원 |

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
  - 키: 엔진 유형 (예: `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`)
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
        "market_type": "spot",
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
    "coins": [...],
    "aiRating": {
      "score": 85,
      "grade": "A",
      "signal": "long",
      "status": "done",
      "summary": "중국어 요약",
      "enSummary": "English summary"
    },
    "ts": 1708473600000
  }
}
```

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
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "중국어 요약",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI 필드 | 설명 |
|---------|------|
| `score` | 0-100 영향도 점수 |
| `signal` | `long`(강세) / `short`(약세) / `neutral` |
| `status` | `done` = AI 분석 완료 |

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
