<p align="center">
  <b>OpenNews MCP Server</b><br>
  72+ 实时数据源 · 5 大引擎类别 · AI 评分 · 交易信号
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_ZH.md">中文</a> | <a href="./README_JA.md">日本語</a> | <a href="./README_KO.md">한국어</a>
</p>

---

## 快速安装

> **首先，在 [https://6551.io/mcp](https://6551.io/mcp) 获取你的 API Token。**

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=<your-token> \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> 将 `/path/to/opennews-mcp` 替换为你的本地项目路径，`<your-token>` 替换为你的 API Token。

### OpenClaw

```bash
export OPENNEWS_TOKEN="<your-token>"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

---

## 让 AI 审查并安装

不确定这个 MCP 是否安全？发送以下提示词给你的 AI 助手，让它在安装前审查源代码：

> **复制下面的提示词并发送给你的 AI 助手（将 `<project-path>` 和 `<your-token>` 替换为实际值）：**

```text
请帮我审查并安装 opennews-mcp MCP 服务器。项目位于 <project-path>。

步骤：
1. 审查以下文件的安全性：
   - src/opennews_mcp/api_client.py — 确认只连接 ai.6551.io，没有向其他地方发送数据
   - src/opennews_mcp/config.py — 确认 token 只从本地 config.json 或环境变量读取，没有硬编码或泄露
   - src/opennews_mcp/tools/*.py — 确认所有工具只做 API 查询，没有文件写入、命令执行或危险操作
   - pyproject.toml — 确认依赖只有 mcp、httpx、websockets，没有可疑包
2. 告诉我你的结论：安全 / 有风险 / 有问题，以及具体原因
3. 如果安全，帮我安装（Token 从 https://6551.io/mcp 获取）：
   claude mcp add opennews -e OPENNEWS_TOKEN=<your-token> -- uv --directory <project-path> run opennews-mcp
```

---

## 数据源 — 5 大类别 72+ 数据源

| 类别 | 数量 | 主要来源 |
|------|------|----------|
| **News** | 53 | Bloomberg、Reuters、Financial Times、CNBC、CNN、BBC、Fox Business、CoinDesk、Cointelegraph、The Block、Blockworks、Decrypt、DlNews、A16Z、TechCrunch、Wired、Politico、Business Insider、Twitter/X、Telegram、Weibo、Truth Social、U.S. Treasury、ECB、TASS、Handelsblatt、Welt、Ambrey、Morgan Stanley、PR Newswire、Coinbase、凤凰新闻等 |
| **Listing** | 9 | Binance、Coinbase、OKX、Bybit、Upbit、Bithumb、Robinhood、Hyperliquid、Aster |
| **OnChain** | 3 | Hyperliquid Whale Trade、Hyperliquid Large Position、KOL Trade |
| **Meme** | 1 | Twitter meme 币社交情绪 |
| **Market** | 6 | Price Change、Funding Rate、Funding Rate Difference、Large Liquidation、Market Trends、OI Change |

所有文章均经 **AI 分析**，包含影响力评分（0-100）、交易信号（long/short/neutral）及中英双语摘要。

---

## 功能介绍

连接后，直接告诉你的 AI 助手：

| 你说 | 它做 |
|------|------|
| "最新加密货币新闻" | 获取最新文章 |
| "搜索 SEC 监管新闻" | 全文关键词搜索 |
| "BTC 相关新闻" | 按币种筛选 |
| "Bloomberg 的文章" | 按来源筛选 |
| "链上事件" | 按引擎类型筛选 (onchain) |
| "AI 评分 80 以上的重要新闻" | 高分筛选 |
| "看涨信号" | 按交易信号筛选 (long) |
| "订阅实时新闻" | WebSocket 实时更新 |

---

## 可用工具

| 分类 | 工具 | 描述 |
|------|------|------|
| 发现 | `get_news_sources` | 完整引擎树 — 5 大类别 72+ 数据源及元数据 |
| | `list_news_types` | 所有来源代码的扁平列表，用于过滤 |
| 搜索 | `get_latest_news` | 跨 72+ 数据源获取最新文章 |
| | `search_news` | 跨所有数据源全文关键词搜索 |
| | `search_news_by_coin` | 按币种搜索 (BTC, ETH, SOL...) 跨所有数据源 |
| | `get_news_by_source` | 按特定来源搜索 (如 engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | 按类别搜索: news, listing, onchain, meme, market |
| | `search_news_advanced` | 多条件组合: 币种 + 关键词 + 引擎类型 |
| AI | `get_high_score_news` | 高 AI 影响力评分文章 (0-100 分制) |
| | `get_news_by_signal` | 按 AI 交易信号: long / short / neutral |
| 实时 | `subscribe_latest_news` | WebSocket 实时推送，支持币种和引擎类型过滤 |

---

## 配置

### 获取 API Token

在 [https://6551.io/mcp](https://6551.io/mcp) 获取你的 API Token。

设置环境变量：

```bash
# macOS / Linux
export OPENNEWS_TOKEN="<your-token>"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "<your-token>"
```

| 变量 | 必需 | 描述 |
|------|------|------|
| `OPENNEWS_TOKEN` | **是** | 6551 API Bearer Token（从 https://6551.io/mcp 获取） |
| `OPENNEWS_API_BASE` | 否 | 覆盖 REST API URL |
| `OPENNEWS_WSS_URL` | 否 | 覆盖 WebSocket URL |
| `OPENNEWS_MAX_ROWS` | 否 | 每次请求最大结果数（默认 100） |

也支持项目根目录的 `config.json`（环境变量优先）：

```json
{
  "api_base_url": "https://ai.6551.io",
  "wss_url": "wss://ai.6551.io/open/news_wss",
  "api_token": "<your-token>",
  "max_rows": 100
}
```

---

## WebSocket 实时订阅

**端点**: `wss://ai.6551.io/open/news_wss?token=YOUR_TOKEN`

订阅实时加密货币新闻更新。

### 订阅新闻

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

**响应**:
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

**过滤参数**（全部可选）：
- `engineTypes`: 引擎类型到新闻类型代码的映射对象
  - 键：引擎类型（如 `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`）
  - 值：新闻类型代码数组（如 `["Bloomberg", "CoinDesk"]`）
  - 空数组 `[]` 表示该引擎下的所有新闻类型
  - 使用 `list_news_types` 工具获取可用代码
- `coins`: 币种符号数组（如 `["BTC", "ETH"]`）
  - 按指定币种过滤新闻
  - 空数组 `[]` 或不传表示接收所有币种
- `hasCoin`: 布尔值，为 true 时只接收带币种标签的新闻

### 取消订阅

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "news.unsubscribe"
}
```

### 服务器推送 - 新闻更新

当有新闻匹配你的过滤条件时，服务器推送：

```json
{
  "jsonrpc": "2.0",
  "method": "news.update",
  "params": {
    "id": "unique-article-id",
    "text": "文章标题或内容",
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

### 服务器推送 - AI 新闻更新

对于有 AI 分析的新闻（如果订阅）：

```json
{
  "jsonrpc": "2.0",
  "method": "news.ai_update",
  "params": {
    "id": "unique-article-id",
    "text": "文章标题",
    "newsType": "Bloomberg",
    "engineType": "news",
    "link": "https://...",
    "coins": [...],
    "aiRating": {
      "score": 85,
      "grade": "A",
      "signal": "long",
      "status": "done",
      "summary": "中文摘要",
      "enSummary": "English summary"
    },
    "ts": 1708473600000
  }
}
```

---

## 数据结构

每篇文章返回：

```json
{
  "id": "unique-article-id",
  "text": "标题 / 内容",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "中文摘要",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI 字段 | 描述 |
|---------|------|
| `score` | 0-100 影响力评分 |
| `signal` | `long`（看涨）/ `short`（看跌）/ `neutral`（中性） |
| `status` | `done` = AI 分析完成 |

---

<details>
<summary><b>其他客户端手动安装</b>（点击展开）</summary>

> 在以下所有配置中，将 `/path/to/opennews-mcp` 替换为你的实际本地项目路径，`<your-token>` 替换为从 [https://6551.io/mcp](https://6551.io/mcp) 获取的 Token。

### Claude Desktop

编辑配置文件（macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`，Windows: `%APPDATA%\Claude\claude_desktop_config.json`）：

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

`~/.cursor/mcp.json` 或 Settings > MCP Servers：

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

`~/.codeium/windsurf/mcp_config.json`：

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

VS Code 侧边栏 > Cline > MCP Servers > Configure，编辑 `cline_mcp_settings.json`：

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

`~/.continue/config.yaml`：

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

Settings > MCP Servers > Add > Type stdio：Command `uv`，Args `--directory /path/to/opennews-mcp run opennews-mcp`，Env `OPENNEWS_TOKEN`。

### Zed Editor

`~/.config/zed/settings.json`：

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

### 任意 stdio MCP 客户端

```bash
OPENNEWS_TOKEN=<your-token> \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## 兼容性

| 客户端 | 安装方式 | 状态 |
|--------|----------|------|
| **Claude Code** | `claude mcp add` | 一键安装 |
| **OpenClaw** | 复制 Skill 目录 | 一键安装 |
| Claude Desktop | JSON 配置 | 支持 |
| Cursor | JSON 配置 | 支持 |
| Windsurf | JSON 配置 | 支持 |
| Cline | JSON 配置 | 支持 |
| Continue.ML / JSON | 支持 |
| Cherry Studio | GUI | 支持 |
| Zed | JSON 配置 | 支持 |

---

## 相关项目

- [twitter-mcp](https://github.com/6551-io/twitter-mcp) - Twitter/X 数据 MCP 服务器

---

## 开发

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector 测试
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### 项目结构

```
├── README.md
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # 内嵌知识
├── pyproject.toml
├── config.json
└── src/opennews_mcp/  ├── server.py              # 入口
    ├── app.py                 # FastMCP 实例
    ├── config.py              # 配置加载
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # 工具
```

## 许可证

MIT
