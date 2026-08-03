<p align="center">
  <b>OpenNews MCP Server</b><br>
  85+ Real-time Data Sources · 6 Engine Categories · AI Ratings · Trading Signals
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./docs/README_ZH.md">中文</a> | <a href="./docs/README_JA.md">日本語</a> | <a href="./docs/README_KO.md">한국어</a>
</p>

---

## Quick Install

> **First, get your API Token at [https://6551.io/mcp](https://6551.io/mcp).**

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=<your-token> \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> Replace `/path/to/opennews-mcp` with your local project path, and `<your-token>` with your API token.

### OpenClaw

```bash
export OPENNEWS_TOKEN="<your-token>"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

---

## Let AI Review and Install

Not sure if this MCP is safe? Send the following prompt to your AI assistant to review the source code before installing:

> **Copy the prompt below and paste it to your AI assistant (replace `<project-path>` and `<your-token>` with actual values):**

```text
Please help me review and install the opennews-mcp MCP server. The project is at <project-path>.

Steps:
1. Review the security of the following files:
   - src/opennews_mcp/api_client.py — Confirm it only connects to ai.6551.io, no data sent elsewhere
   - src/opennews_mcp/config.py — Confirm token is only read from local config.json or env vars, not hardcoded or leaked
   - src/opennews_mcp/tools/*.py — Confirm all tools only do API queries, no file writes, command execution, or dangerous operations
   - pyproject.toml — Confirm dependencies are only mcp, httpx, websockets, no suspicious packages
2. Tell me your conclusion: Safe / Risky / Problematic, and the specific reasons
3. If safe, help me install (Token from https://6551.io/mcp):
   claude mcp add opennews -e OPENNEWS_TOKEN=<your-token> -- uv --directory <project-path> run opennews-mcp
```

---

## Data Sources — 85+ Sources Across 6 Categories

| Category | Count | Key Sources |
|----------|-------|-------------|
| **News** | 55 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, GlobeNewswire, Business Wire, Coinbase, and more |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 2 | Hyperliquid Whale Trade, Hyperliquid Large Position |
| **Meme** | 1 | Twitter meme coin social sentiment |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |
| **Prediction** | 12 | CORRELATION_LOGICAL, SMART_MONEY_TRADE, PRICE_SPIKE, CLUSTER_ENTRY, WHALE_POSITION, NEW_WALLET_TRADE, INSIDER_PATTERN, CORRELATION_NARRATIVE, CORRELATION_HEDGE, CORRELATION_ENTITY_GEO, CORRELATION_CAUSAL, SETTLEMENT_ARBITRAGE |

All articles are **AI-analyzed** with impact score (0-100), trading signal (long/short/neutral), and bilingual summaries (EN/ZH).

<details>
<summary><b>News — 55 sources</b> (engineType: "news") — Premium financial & crypto media, government agencies, social platforms</summary>

| Source Code | Description |
|-------------|-------------|
| Bloomberg | Bloomberg — top-tier financial news |
| Reuters | Reuters — global wire service |
| Financial Times | Financial Times — premium business news |
| CNBC | CNBC — financial television |
| CNN | CNN — US news network |
| BBC | BBC — British Broadcasting Corporation |
| Fox Business | Fox Business — US financial news |
| CoinDesk | CoinDesk — leading crypto media |
| Cointelegraph | Cointelegraph — crypto media |
| The Block | The Block — crypto data & journalism |
| Blockworks | Blockworks — crypto-native media |
| Decrypt | Decrypt — crypto & web3 media |
| DlNews | DL News — crypto investigative journalism |
| A16Z | a16z (Andreessen Horowitz) — leading crypto VC |
| TechCrunch | TechCrunch — tech & startup news |
| Wired | Wired magazine — tech journalism |
| Politico | Politico — US & EU political news |
| Business Insider | Business Insider |
| Twitter/X | Twitter/X posts from crypto influencers |
| X / Twitter Profile | Twitter/X profile changes (name, bio updates) |
| Telegram | Telegram channels |
| Weibo | Weibo — Chinese social media |
| Truth Social | Truth Social — Trump's social platform |
| U.S. Treasury | U.S. Treasury Department — official statements |
| U.S. Trade Representative | USTR — trade policy announcements |
| ECB | European Central Bank — official communications |
| TASS | TASS — Russian state news agency |
| Interfax | Interfax — Russian news agency |
| Handelsblatt | Handelsblatt — German business newspaper |
| Hadelsblatt | Hadelsblatt — German business |
| Welt | Welt — German newspaper |
| Telegraph | The Telegraph — UK news |
| MS NOW | Morgan Stanley NOW — institutional research |
| Ambrey | Ambrey — maritime & geopolitical intelligence |
| PR Newswire | PR Newswire — press releases |
| GlobeNewswire | GlobeNewswire — press releases |
| Business Wire | Business Wire — press releases |
| Coinbase | Coinbase announcements & blog |
| Binance | Binance announcements & blog |
| jin10 | Jin10 — Chinese financial data flash news |
| The Big Whale | The Big Whale — European crypto media |
| The Verge | The Verge — tech media |
| Techinasia | Tech in Asia — Asian tech news |
| Medium | Medium blog posts |
| Chainwire | Chainwire — crypto press releases |
| Token Relations | Token relations & partnerships |
| Crypto Narratives | Crypto narrative tracking |
| Crypto in America | Crypto in America coverage |
| 6551News | 6551 platform original analysis |
| BWEnews | BWE news wire |
| AGGRNEWS | Aggregated news feed |
| Velo | Velo data intelligence |

</details>

<details>
<summary><b>Listing — 9 sources</b> (engineType: "listing") — Token listing announcements from major exchanges</summary>

| Source Code | Description |
|-------------|-------------|
| Binance | Binance new token listings |
| Coinbase | Coinbase new token listings |
| OKX | OKX new token listings |
| Bybit | Bybit new token listings |
| Upbit | Upbit (Korean exchange) listings |
| Bithumb | Bithumb (Korean exchange) listings |
| Robinhood | Robinhood crypto listings |
| Hyperliquid | Hyperliquid perp listings |
| Aster | Aster exchange listings |

</details>

<details>
<summary><b>OnChain — 2 sources</b> (engineType: "onchain") — Hyperliquid whale trades and large position activity</summary>

| Source Code | Description |
|-------------|-------------|
| Hyperliquid Whale Trade | Hyperliquid whale trade alerts |
| Hyperliquid Large Position | Hyperliquid large position changes |

</details>

<details>
<summary><b>Meme — 1 source</b> (engineType: "meme") — Meme coin social sentiment tracking</summary>

| Source Code | Description |
|-------------|-------------|
| Twitter | Twitter/X meme coin discussions & viral posts |

</details>

<details>
<summary><b>Market — 6 sources</b> (engineType: "market") — Market anomaly detection and quantitative signals</summary>

| Source Code | Description |
|-------------|-------------|
| Price Change | Significant price movements (pumps/dumps) |
| Funding Rate | Funding rate anomalies (perp futures) |
| Funding Rate Difference | Cross-exchange funding rate divergences |
| Large Liquidation | Large liquidation events |
| Market Trends | Overall market trend shifts |
| OI Change | Open interest significant changes |

</details>

<details>
<summary><b>Prediction — 12 sources</b> (engineType: "prediction") — AI-powered prediction and correlation signals</summary>

| Source Code | Description |
|-------------|-------------|
| CORRELATION_LOGICAL | Logical correlation analysis |
| SMART_MONEY_TRADE | Smart money trade tracking |
| PRICE_SPIKE | Price spike detection |
| CLUSTER_ENTRY | Cluster entry signals |
| WHALE_POSITION | Whale position monitoring |
| NEW_WALLET_TRADE | New wallet trade detection |
| INSIDER_PATTERN | Insider pattern recognition |
| CORRELATION_NARRATIVE | Narrative correlation analysis |
| CORRELATION_HEDGE | Hedge correlation analysis |
| CORRELATION_ENTITY_GEO | Geopolitical entity correlation |
| CORRELATION_CAUSAL | Causal correlation analysis |
| SETTLEMENT_ARBITRAGE | Settlement arbitrage signals |

</details>

---

## What Can It Do?

After connecting, just tell your AI assistant:

| You Say | It Does |
|---------|---------|
| "Latest crypto news" | Get latest articles |
| "Search SEC regulation news" | Full-text keyword search |
| "BTC related news" | Filter by coin |
| "Bloomberg articles" | Filter by source |
| "On-chain events" | Filter by engine type (onchain) |
| "Important news with AI score above 80" | High score filtering |
| "Bullish signals" | Filter by trading signal (long) |
| "Subscribe to real-time news" | WebSocket live updates |

---

## Available Tools

| Category | Tool | Description |
|----------|------|-------------|
| Discovery | `get_news_sources` | Full engine tree — all 6 categories and 85+ sources with metadata |
| | `list_news_types` | Flat list of all source codes for filtering |
| Search | `get_latest_news` | Latest articles across all 85+ sources |
| | `search_news` | Full-text keyword search across all sources |
| | `search_news_by_coin` | By coin (BTC, ETH, SOL...) across all sources |
| | `get_news_by_source` | By specific source (e.g. engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | By category: news, listing, onchain, meme, market, prediction |
| | `search_news_advanced` | Multi-filter: coins + keywords + engine types combined |
| AI | `get_high_score_news` | High AI impact score articles (0-100 scale) |
| | `get_news_by_signal` | By AI trading signal: long / short / neutral |
| Finance | `search_companies` | Discover candidates or resolve an exact canonical issuer, ticker, CIK, KRX code, DART code, or typed identifier |
| | `get_company_info` | Resolve exactly one issuer and list its SEC/DART filings, research reports, transcripts, and financial fields |
| | `get_company_report_text` | Fetch one issuer-bound filing, research report, or transcript by stable report ID/type |
| | `get_key_market_events` | Query key macro dates and configured focus-company earnings events |
| | `get_crypto_holdings` | Query wallet-visible on-chain holdings evidence for an institution or address |
| | `get_crypto_holding_changes` | Query adjacent-snapshot on-chain holdings changes |
| Real-time | `subscribe_latest_news` | WebSocket live feed with coin & engine type filters |

> For a comprehensive usage guide with detailed examples, see [Knowledge Guide](./knowledge/guide.md).

---

## Configuration

### Get API Token

Get your API Token at [https://6551.io/mcp](https://6551.io/mcp).

Set environment variable:

```bash
# macOS / Linux
export OPENNEWS_TOKEN="<your-token>"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "<your-token>"
```

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENNEWS_TOKEN` | **Yes** | 6551 API Bearer Token (from https://6551.io/mcp) |
| `OPENNEWS_API_BASE` | No | Override REST API URL |
| `OPENNEWS_WSS_URL` | No | Override WebSocket URL |
| `OPENNEWS_MAX_ROWS` | No | Max results per request (default 100) |

Also supports `config.json` in project root (env vars take precedence):

```json
{
  "api_base_url": "https://ai.6551.io",
  "wss_url": "wss://ai.6551.io/open/news_wss",
  "api_token": "<your-token>",
  "max_rows": 100
}
```

---

## WebSocket Real-time Subscriptions

**Endpoint**: `wss://ai.6551.io/open/news_wss?token=YOUR_TOKEN`

Subscribe to real-time crypto news updates.

### Heartbeat

To keep the connection alive, the client can send `ping`, and the server responds with `pong`.

### Subscribe to News

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

**Response**:
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

**Filter Parameters** (all optional):
- `engineTypes`: Object mapping engine type to news type codes
  - Key: Engine type (e.g., `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`, `"prediction"`)
  - Value: Array of news type codes (e.g., `["Bloomberg", "CoinDesk"]`)
  - Empty array `[]` means all news types under that engine
  - Use `list_news_types` tool to get available codes
- `coins`: Array of coin symbols (e.g., `["BTC", "ETH"]`)
  - Filter news by specific coins
  - Empty array `[]` or omit to receive all coins
- `hasCoin`: Boolean, if true only receive news with coin tags

### Unsubscribe

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "news.unsubscribe"
}
```

### Server Push - News Update

When new news matches your filters, the server pushes:

```json
{
  "jsonrpc": "2.0",
  "method": "news.update",
  "params": {
    "id": "unique-article-id",
    "text": "Article title or content",
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

### Server Push - AI News Update

For news with AI analysis (if subscribed):

```json
{
  "jsonrpc": "2.0",
  "method": "news.ai_update",
  "params": {
    "id": "unique-article-id",
    "text": "Article title",
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

### Server Push - Strategy Triggered

> **Requires Max subscription.** Create and manage your strategies at [https://www.newsliquid.com/strategy](https://www.newsliquid.com/strategy).

When a user-defined strategy is triggered (e.g., price alert, keyword match), the server pushes:

```json
{
  "jsonrpc": "2.0",
  "method": "strategy.triggered",
  "params": {
    "id": 1234567890,
    "newsType": "strategy",
    "engineType": "market",
    "text": "BTC funding rate 0.15%",
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
      "name": "BTC Funding Rate Alert",
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

**Strategy Params Fields**:
- `id`: News/event ID
- `engineType`: Source engine type (`market`, `news`, `onchain`)
- `text`: Human-readable event description
- `coins`: Related coins
- `ts`: Event timestamp
- `strategy.id`: User strategy ID
- `strategy.name`: Strategy name
- `strategy.sourceType`: Strategy source type
- `strategy.soundId`: Notification sound ID
- `strategy.bgColor`: Notification background color
- `strategy.metrics`: Triggered metric values with units
- `aiRating` (optional): Present when the news has an AI score. Contains:
  - `score`: 0-100 impact score
- `relatedAddress` (optional): Related wallet address if applicable

**Note**: Strategy triggered events are pushed per-user via NATS. No explicit subscription is required — events are automatically delivered to the connected user who owns the strategy.

**Note**: Each coin in the `coins` array now includes individual AI ratings:
- `score`: 0-100 impact score for this specific coin
- `signal`: `long` / `short` / `neutral` for this coin
- `grade`: `A+` / `A` / `B+` / `B` / `C` for this coin

The top-level `aiRating.score` represents the highest score among all coins.

---

## Data Structure

Each article returns:

```json
{
  "id": "unique-article-id",
  "text": "Title / Content",
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
    "signal": "long",
    "status": "done",
    "summary": "Chinese summary",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI Field | Description |
|----------|-------------|
| `score` | 0-100 impact score (top-level = highest among all coins) |
| `signal` | `long` (bullish) / `short` (bearish) / `neutral` |
| `coins[].score` | Individual coin impact score (0-100) |
| `coins[].signal` | Individual coin signal (long/short/neutral) |
| `coins[].grade` | Individual coin grade (A+/A/B+/B/C) |

---

<details>
<summary><b>Manual Installation for Other Clients</b> (click to expand)</summary>

> In all configurations below, replace `/path/to/opennews-mcp` with your actual local project path, and `<your-token>` with your token from [https://6551.io/mcp](https://6551.io/mcp).

### Claude Desktop

Edit config file (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

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

`~/.cursor/mcp.json` or Settings > MCP Servers:

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

VS Code sidebar > Cline > MCP Servers > Configure, edit `cline_mcp_settings.json`:

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

Settings > MCP Servers > Add > Type stdio: Command `uv`, Args `--directory /path/to/opennews-mcp run opennews-mcp`, Env `OPENNEWS_TOKEN`.

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

### Any stdio MCP Client

```bash
OPENNEWS_TOKEN=<your-token> \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## Compatibility

| Client | Installation | Status |
|--------|--------------|--------|
| **Claude Code** | `claude mcp add` | One-click |
| **OpenClaw** | Copy Skill directory | One-click |
| Claude Desktop | JSON config | Supported |
| Cursor | JSON config | Supported |
| Windsurf | JSON config | Supported |
| Cline | JSON config | Supported |
| Continue.dev | YAML / JSON | Supported |
| Cherry Studio | GUI | Supported |
| Zed | JSON config | Supported |

---

## Related Projects

- [twitter-mcp](https://github.com/6551-io/twitter-mcp) - Twitter/X data MCP server

---

## Development

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector test
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### Project Structure

```
├── README.md
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # Embedded knowledge
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # Entry point
    ├── app.py                 # FastMCP instance
    ├── config.py              # Config loading
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # Tools
```

## License

MIT
