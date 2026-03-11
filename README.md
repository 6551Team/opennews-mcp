<p align="center">
  <b>OpenNews MCP Server</b><br>
  72+ Real-time Data Sources · 5 Engine Categories · AI Ratings · Trading Signals
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

## Data Sources — 72+ Sources Across 5 Categories

| Category | Count | Key Sources |
|----------|-------|-------------|
| **News** | 53 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, Coinbase, Phoenixnews, and more |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 3 | Hyperliquid Whale Trade, Hyperliquid Large Position, KOL Trade |
| **Meme** | 1 | Twitter meme coin social sentiment |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |

All articles are **AI-analyzed** with impact score (0-100), trading signal (long/short/neutral), and bilingual summaries (EN/ZH).

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
| Discovery | `get_news_sources` | Full engine tree — all 5 categories and 72+ sources with metadata |
| | `list_news_types` | Flat list of all source codes for filtering |
| Search | `get_latest_news` | Latest articles across all 72+ sources |
| | `search_news` | Full-text keyword search across all sources |
| | `search_news_by_coin` | By coin (BTC, ETH, SOL...) across all sources |
| | `get_news_by_source` | By specific source (e.g. engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | By category: news, listing, onchain, meme, market |
| | `search_news_advanced` | Multi-filter: coins + keywords + engine types combined |
| AI | `get_high_score_news` | High AI impact score articles (0-100 scale) |
| | `get_news_by_signal` | By AI trading signal: long / short / neutral |
| Real-time | `subscribe_latest_news` | WebSocket live feed with coin & engine type filters |

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
  - Key: Engine type (e.g., `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`)
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
        "market_type": "spot",
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
    "coins": [...],
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
}
```

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
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
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
| `score` | 0-100 impact score |
| `signal` | `long` (bullish) / `short` (bearish) / `neutral` |
| `status` | `done` = AI analysis completed |

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
