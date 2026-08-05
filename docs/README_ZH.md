<p align="center">
  <b>OpenNews MCP Server</b><br>
  85+ 实时数据源 · 6 大引擎类别 · AI 评分 · 交易信号
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

## 数据源 — 6 大类别 85+ 数据源

| 类别 | 数量 | 主要来源 |
|------|------|----------|
| **News** | 55 | Bloomberg、Reuters、Financial Times、CNBC、CNN、BBC、Fox Business、CoinDesk、Cointelegraph、The Block、Blockworks、Decrypt、DlNews、A16Z、TechCrunch、Wired、Politico、Business Insider、Twitter/X、Telegram、Weibo、Truth Social、U.S. Treasury、ECB、TASS、Handelsblatt、Welt、Ambrey、Morgan Stanley、PR Newswire、GlobeNewswire、Business Wire、Coinbase等 |
| **Listing** | 9 | Binance、Coinbase、OKX、Bybit、Upbit、Bithumb、Robinhood、Hyperliquid、Aster |
| **OnChain** | 2 | Hyperliquid Whale Trade、Hyperliquid Large Position |
| **Meme** | 1 | Twitter meme 币社交情绪 |
| **Market** | 6 | Price Change、Funding Rate、Funding Rate Difference、Large Liquidation、Market Trends、OI Change |
| **Prediction** | 12 | CORRELATION_LOGICAL（相关性-逻辑）、SMART_MONEY_TRADE（聪明钱交易）、PRICE_SPIKE（价格异动）、CLUSTER_ENTRY（集群进场）、WHALE_POSITION（鲸鱼持仓）、NEW_WALLET_TRADE（新钱包交易）、INSIDER_PATTERN（内幕模式）、CORRELATION_NARRATIVE（相关性-叙述）、CORRELATION_HEDGE（相关性-对冲）、CORRELATION_ENTITY_GEO（相关性-地缘）、CORRELATION_CAUSAL（相关性-因果）、SETTLEMENT_ARBITRAGE（套利） |

所有文章均经 **AI 分析**，包含影响力评分（0-100）、交易信号（long/short/neutral）及中英双语摘要。

<details>
<summary><b>News — 55 个来源</b>（engineType: "news"）— 顶级财经与加密媒体、政府机构、社交平台</summary>

| 来源代码 | 描述 |
|----------|------|
| Bloomberg | 彭博社 — 顶级财经新闻 |
| Reuters | 路透社 — 全球通讯社 |
| Financial Times | 金融时报 — 高端商业新闻 |
| CNBC | CNBC — 财经电视 |
| CNN | CNN — 美国新闻网 |
| BBC | BBC — 英国广播公司 |
| Fox Business | Fox Business — 美国财经新闻 |
| CoinDesk | CoinDesk — 头部加密媒体 |
| Cointelegraph | Cointelegraph — 加密媒体 |
| The Block | The Block — 加密数据与新闻 |
| Blockworks | Blockworks — 加密原生媒体 |
| Decrypt | Decrypt — 加密与 web3 媒体 |
| DlNews | DL News — 加密调查新闻 |
| A16Z | a16z（Andreessen Horowitz）— 头部加密 VC |
| TechCrunch | TechCrunch — 科技与创业新闻 |
| Wired | Wired — 科技杂志 |
| Politico | Politico — 美欧政治新闻 |
| Business Insider | Business Insider |
| Twitter/X | Twitter/X 加密 KOL 动态 |
| X / Twitter Profile | Twitter/X 个人资料变更（用户名、简介更新） |
| Telegram | Telegram 频道 |
| Weibo | 微博 — 中国社交媒体 |
| Truth Social | Truth Social — 特朗普社交平台 |
| U.S. Treasury | 美国财政部 — 官方声明 |
| U.S. Trade Representative | 美国贸易代表办公室 — 贸易政策公告 |
| ECB | 欧洲央行 — 官方通讯 |
| TASS | 塔斯社 — 俄罗斯国家通讯社 |
| Interfax | 国际文传电讯社 — 俄罗斯通讯社 |
| Handelsblatt | 德国商报 |
| Hadelsblatt | Hadelsblatt — 德国商业 |
| Welt | 世界报 — 德国报纸 |
| Telegraph | 每日电讯报 — 英国新闻 |
| MS NOW | 摩根士丹利 NOW — 机构研究 |
| Ambrey | Ambrey — 海事与地缘政治情报 |
| PR Newswire | 美通社 — 新闻稿发布 |
| GlobeNewswire | GlobeNewswire — 新闻稿发布 |
| Business Wire | Business Wire — 新闻稿发布 |
| Coinbase | Coinbase 公告与博客 |
| Binance | Binance 公告与博客 |
| jin10 | 金十数据 — 财经快讯 |
| The Big Whale | The Big Whale — 欧洲加密媒体 |
| The Verge | The Verge — 科技媒体 |
| Techinasia | Tech in Asia — 亚洲科技新闻 |
| Medium | Medium 博客 |
| Chainwire | Chainwire — 加密新闻稿 |
| Token Relations | 代币合作与关系 |
| Crypto Narratives | 加密叙事追踪 |
| Crypto in America | 美国加密行业报道 |
| 6551News | 6551 平台原创分析 |
| BWEnews | BWE 新闻线 |
| AGGRNEWS | 聚合新闻源 |
| Velo | Velo 数据情报 |

</details>

<details>
<summary><b>Listing — 9 个来源</b>（engineType: "listing"）— 主要交易所代币上新公告</summary>

| 来源代码 | 描述 |
|----------|------|
| Binance | 币安新币上线 |
| Coinbase | Coinbase 新币上线 |
| OKX | OKX 新币上线 |
| Bybit | Bybit 新币上线 |
| Upbit | Upbit（韩国交易所）上新 |
| Bithumb | Bithumb（韩国交易所）上新 |
| Robinhood | Robinhood 加密货币上线 |
| Hyperliquid | Hyperliquid 永续合约上线 |
| Aster | Aster 交易所上新 |

</details>

<details>
<summary><b>OnChain — 2 个来源</b>（engineType: "onchain"）— Hyperliquid 巨鲸交易与大额持仓活动</summary>

| 来源代码 | 描述 |
|----------|------|
| Hyperliquid Whale Trade | Hyperliquid 巨鲸交易预警 |
| Hyperliquid Large Position | Hyperliquid 大额持仓变动 |

</details>

<details>
<summary><b>Meme — 1 个来源</b>（engineType: "meme"）— Meme 币社交情绪追踪</summary>

| 来源代码 | 描述 |
|----------|------|
| Twitter | Twitter/X meme 币讨论与病毒式传播 |

</details>

<details>
<summary><b>Market — 6 个来源</b>（engineType: "market"）— 市场异动检测与量化信号</summary>

| 来源代码 | 描述 |
|----------|------|
| Price Change | 价格剧烈波动（暴涨/暴跌） |
| Funding Rate | 资金费率异常（永续合约） |
| Funding Rate Difference | 跨交易所资金费率差异 |
| Large Liquidation | 大额清算事件 |
| Market Trends | 整体市场趋势变化 |
| OI Change | 未平仓合约量显著变化 |

</details>

<details>
<summary><b>Prediction — 12 个来源</b>（engineType: "prediction"）— AI 预测与相关性信号</summary>

| 来源代码 | 描述 |
|----------|------|
| CORRELATION_LOGICAL | 相关性（逻辑） |
| SMART_MONEY_TRADE | 聪明钱交易 |
| PRICE_SPIKE | 价格异动 |
| CLUSTER_ENTRY | 集群进场 |
| WHALE_POSITION | 鲸鱼持仓 |
| NEW_WALLET_TRADE | 新钱包交易 |
| INSIDER_PATTERN | 内幕模式 |
| CORRELATION_NARRATIVE | 相关性（叙述） |
| CORRELATION_HEDGE | 相关性（对冲） |
| CORRELATION_ENTITY_GEO | 相关性（地缘） |
| CORRELATION_CAUSAL | 相关性（因果） |
| SETTLEMENT_ARBITRAGE | 套利 |

</details>

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
| 发现 | `get_news_sources` | 完整引擎树 — 6 大类别 85+ 数据源及元数据 |
| | `list_news_types` | 所有来源代码的扁平列表，用于过滤 |
| 搜索 | `get_latest_news` | 跨 85+ 数据源获取最新文章 |
| | `search_news` | 跨所有数据源全文关键词搜索 |
| | `search_news_by_coin` | 按币种搜索 (BTC, ETH, SOL...) 跨所有数据源 |
| | `get_news_by_source` | 按特定来源搜索 (如 engine_type="news", news_type="Bloomberg") |
| | `get_news_by_engine` | 按类别搜索: news, listing, onchain, meme, market, prediction |
| | `search_news_advanced` | 多条件组合: 币种 + 关键词 + 引擎类型 |
| AI | `get_high_score_news` | 高 AI 影响力评分文章 (0-100 分制) |
| | `get_news_by_signal` | 按 AI 交易信号: long / short / neutral |
| 金融增强 | `search_companies` | 发现候选项，或按精确 canonical issuer、ticker、CIK、KRX 代码、DART 代码、typed identifier 解析 |
| | `get_company_info` | 精确解析一个 issuer，并列出 SEC/DART filings、研报、transcript 和财务字段 |
| | `get_company_report_text` | 按稳定 report ID/type 获取某个 issuer 绑定的 filing、研报或 transcript |
| | `get_key_market_events` | 查询关键宏观日期和重点公司财报事件 |
| | `get_politician_stock_activity` | 查询官方美国众议院 PTR 股票交易披露 |
| | `get_institution_stock_holdings` | 查询延迟的 SEC Form 13F 机构股票持仓披露 |
| | `get_crypto_holdings` | 查询机构或地址的钱包可见链上持仓证据 |
| | `get_crypto_holding_changes` | 查询相邻快照之间的链上持仓变化 |
| 实时 | `subscribe_latest_news` | WebSocket 实时推送，支持币种和引擎类型过滤 |

对于跨市场或同名公司，请先查看 `ambiguity_candidates[]`，再用且只用一个精确 selector 重试。MCP 工具支持 `canonical_issuer_id`、`ticker`、`cik`、`krx_stock_code`、`dart_corp_code`，或 `identifier` + `identifier_type` + `market`；原始 HTTP 调用方应使用通用 `identifier` 形式。例如，`SEC:0002120882` 对应 `identifier=0002120882, identifier_type=cik, market=US`，`DART:00164779` 对应 `identifier=00164779, identifier_type=dart_corp_code, market=KR`。

> 完整使用指南和详细示例，请查看 [知识指南](../knowledge/guide.md)。

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

### 心跳

为了保持连接活跃，客户端可以发送 `ping`，服务端会响应 `pong`。

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
  - 键：引擎类型（如 `"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`, `"prediction"`）
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
        "market_type": "cex",
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

**注意**：`coins` 数组中的每个币种现在包含独立的 AI 评分：
- `score`：该币种的影响力评分（0-100）
- `signal`：该币种的信号方向（long/short/neutral）
- `grade`：该币种的评级（A+/A/B+/B/C）

顶层 `aiRating.score` 代表所有币种中的最高分。

### 服务器推送 - 策略命中

> **需要 Max 订阅套餐。** 在 [https://www.newsliquid.com/strategy](https://www.newsliquid.com/strategy) 创建和管理您的策略。

当用户自定义策略被触发时（如价格预警、关键词匹配），服务器推送：

```json
{
  "jsonrpc": "2.0",
  "method": "strategy.triggered",
  "params": {
    "id": 1234567890,
    "newsType": "strategy",
    "engineType": "market",
    "text": "BTC 资金费率 0.15%",
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
      "name": "BTC 资金费率预警",
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

**策略推送字段说明**：
- `id`：新闻/事件 ID
- `engineType`：来源引擎类型（`market`、`news`、`onchain`）
- `text`：可读的事件描述
- `coins`：相关币种
- `ts`：事件时间戳
- `strategy.id`：用户策略 ID
- `strategy.name`：策略名称
- `strategy.sourceType`：策略来源类型
- `strategy.soundId`：通知音效 ID
- `strategy.bgColor`：通知背景色
- `strategy.metrics`：触发的指标值及单位
- `aiRating`（可选）：当新闻有 AI 评分时存在，包含：
  - `score`：影响力评分（0-100）
- `relatedAddress`（可选）：相关钱包地址

**注意**：策略命中事件通过 NATS 按用户推送，无需额外订阅，连接后自动接收属于该用户的策略事件。

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

| AI 字段 | 描述 |
|---------|------|
| `score` | 0-100 影响力评分（顶层 = 所有币种中的最高分） |
| `signal` | `long`（看涨）/ `short`（看跌）/ `neutral`（中性） |
| `coins[].score` | 单个币种的影响力评分（0-100） |
| `coins[].signal` | 单个币种的信号方向（long/short/neutral） |
| `coins[].grade` | 单个币种的评级（A+/A/B+/B/C） |

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
