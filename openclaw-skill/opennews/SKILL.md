---
name: opennews
description: "Real-time crypto, equities, macro, and financial market news aggregator — 85+ data sources across 6 categories covering digital assets, U.S. stocks, semiconductors, AI infrastructure, supply chains, commodities, rates, policy, and market-moving social/news signals. Sources include Bloomberg, Reuters, FT, CNBC, CoinDesk, Twitter/X, Binance, Coinbase, OKX, Hyperliquid whale trades, price/funding/liquidation alerts, and 12 AI prediction signals. AI-analyzed with impact score, trading signals, and bilingual summaries. **Free tools available without token**."

user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - curl
    optionalEnv:
      - OPENNEWS_TOKEN
    primaryEnv: OPENNEWS_TOKEN
    emoji: "\U0001F4F0"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
  version: 1.0.7
---

# OpenNews Financial Market News Skill

Real-time crypto, equities, macro, and financial market news aggregator powered by 6551.io — **85+ data sources** across 6 engine categories, all AI-analyzed with impact scores, trading signals, and bilingual summaries.

Use OpenNews for time-sensitive, market-moving news and signals across digital assets, U.S. stocks, semiconductors, AI infrastructure, supply chains, commodities, rates, policy, and social/news channels that can affect prices or investor positioning.

**Get your token**: https://6551.io/mcp

**Base URL**: `https://ai.6551.io`

## Data Sources — 85+ Sources Across 6 Categories

| Category | Count | Key Sources |
|----------|-------|-------------|
| **News** | 55 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, GlobeNewswire, Business Wire, Coinbase, and more; useful for crypto, U.S. equities, semiconductors, AI infrastructure, supply chains, commodities, rates, policy, and market-moving social/news signals |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 2 | Hyperliquid Whale Trade, Hyperliquid Large Position |
| **Meme** | 1 | Twitter meme coin social sentiment |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |
| **Prediction** | 12 | CORRELATION_LOGICAL, SMART_MONEY_TRADE, PRICE_SPIKE, CLUSTER_ENTRY, WHALE_POSITION, NEW_WALLET_TRADE, INSIDER_PATTERN, CORRELATION_NARRATIVE, CORRELATION_HEDGE, CORRELATION_ENTITY_GEO, CORRELATION_CAUSAL, SETTLEMENT_ARBITRAGE |

## Authentication

All requests require the header:
```
Authorization: Bearer $OPENNEWS_TOKEN
```

---

## News Operations

### 1. Get News Sources

Fetch the full engine tree with all 6 categories and 85+ sources.

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/news_type"
```

Returns a tree with engine types (`news` — 55 sources, `listing` — 9 exchanges, `onchain` — 2 Hyperliquid trackers, `meme` — 1 sentiment source, `market` — 6 anomaly signals, `prediction` — 12 AI prediction signals) and their sub-categories.

### 2. Search News

`POST /open/news_search` is the primary search endpoint.

**Get latest news:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'
```

**Search by keyword:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q": "bitcoin OR ETF", "limit": 10, "page": 1}'
```

**Search by coin symbol:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 10, "page": 1}'
```

**Filter by engine type and news type:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"engineTypes": {"news": ["Bloomberg", "Reuters"]}, "limit": 10, "page": 1}'
```

**Only news with coins:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hasCoin": true, "limit": 10, "page": 1}'
```

### News Search Parameters

| Parameter     | Type                      | Required | Description                                   |
|--------------|---------------------------|----------|-----------------------------------------------|
| `limit`      | integer                   | yes      | Max results per page (1-100)                  |
| `page`       | integer                   | yes      | Page number (1-based)                         |
| `q`          | string                    | no       | Full-text keyword search                      |
| `coins`      | string[]                  | no       | Filter by coin symbols (e.g. `["BTC","ETH"]`) |
| `engineTypes`| map[string][]string       | no       | Filter by engine and news types               |
| `hasCoin`    | boolean                   | no       | Only return news with associated coins        |
| `score`      | integer                   | no       | Filter by minimum AI score (0-100)            |

Important: You need to understand the user's query intent and perform word segmentation, then combine them using OR/AND to form search keywords, supporting both Chinese and English.

---

## Strategy History Operations

These authenticated endpoints query the current user's strategy configuration and historical strategy-triggered events. Each call consumes 1 quota. Create and manage strategies at https://www.newsliquid.com/strategy.

### 1. Get Strategy List

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/strategy_list?page=1&limit=20"
```

Returns only `id`, `name`, `description`, `enabled`, and `createdAt` for each strategy.

### 2. Get Strategy Hits

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/strategy_hits?strategyId=42&page=1&limit=20"
```

Returns historical triggered events for the given strategy ID. Each hit uses the same news-like payload shape as the WebSocket `strategy.triggered` event, including nested `strategy`, `coins`, optional `aiRating`, `source`, `description`, `relatedAddress`, and triggered metric fields when available.

---

## WebSocket news_wss Protocol

Connect with the token in the query string:

```text
wss://ai.6551.io/open/news_wss?token=$OPENNEWS_TOKEN
```

Supported client messages:

| Client sends | Server returns |
|---|---|
| text frame `ping` | text frame `pong` |
| JSON-RPC `news.subscribe` with optional `engineTypes`, `coins`, `hasCoin` | JSON-RPC response with matching `id` and `result.success=true` |
| JSON-RPC `news.unsubscribe` | JSON-RPC response with matching `id` and `result.success=true` |

Server-pushed events:

| Server method | Meaning |
|---|---|
| `news.update` | New matched news item |
| `news.ai_update` | New matched news item with AI rating fields |
| `strategy.triggered` | Strategy hit for the authenticated user who owns the strategy |

`news.subscribe` controls `news.update` and `news.ai_update`. `strategy.triggered` is automatically delivered to the authenticated strategy owner and does not need a separate subscribe method.

Subscribe example:

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

Unsubscribe example:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "news.unsubscribe"
}
```

---

## Finance Enhancement Entity Protocol

These authenticated endpoints provide company discovery, report catalogs, report text, key market events, public stock-disclosure evidence, and wallet-visible on-chain evidence. Responses are wrapped as `{"success": true, "data": ...}` and may include usage quota metadata. Treat `data.status` as the business result; HTTP success alone does not mean the company, report, or disclosure query was resolved.

### Resolve the Company Before Reading Reports

Company names can legitimately map to more than one issuer or listed security. Use this sequence:

```text
user company expression
→ broad company-search
→ inspect ambiguity_candidates[]
→ choose the intended market/issuer
→ retry with one exact identifier namespace
→ read company-info
→ choose report_id + report_type
→ read company-report-text
```

Never send a fuzzy company name together with an exact identifier. Exactly one company selector must be authoritative.

The OpenNews MCP tools accept any one of these selectors directly:

| MCP selector | Example | Meaning |
|---|---|---|
| `canonical_issuer_id` | `SEC:0002120882` | Stable issuer ID returned by company search |
| `ticker` | `SKHY` | Exact listed ticker |
| `cik` | `0002120882` | SEC CIK |
| `krx_stock_code` | `000660` | Six-digit KRX security code |
| `dart_corp_code` | `00164779` | Eight-digit DART issuer code |
| `identifier` + `identifier_type` + `market` | `00164779` + `dart_corp_code` + `KR` | Generic typed selector |
| `company` / search `keyword` | `SK hynix Inc.` / `Hynix` | Fuzzy discovery only |

The raw HTTP endpoints use the generic form `identifier` + `identifier_type` + `market`. Do not send `cik`, `ticker`, `dart_corp_code`, `krx_stock_code`, or `canonical_issuer_id` as standalone HTTP JSON fields: those are MCP conveniences. Convert stable IDs as follows:

| Search result | Exact raw HTTP selector |
|---|---|
| `SEC:0002120882` | `{"identifier":"0002120882","identifier_type":"cik","market":"US"}` |
| `DART:00164779` | `{"identifier":"00164779","identifier_type":"dart_corp_code","market":"KR"}` |
| `KRX:000660` security | `{"identifier":"000660","identifier_type":"krx_stock_code","market":"KR"}` |

### Company Search

Use a name only for discovery. An `ambiguous_entity` response is expected when multiple markets or issuers match.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"Hynix","identifier_type":"company_name","market":"GLOBAL","result_scope":"issuer","limit":20,"auto_collect":false}'
```

For SK hynix this can return both the U.S. SEC issuer (`SEC:0002120882`, including ticker `SKHY`) and the Korean DART issuer (`DART:00164779`, security `KRX:000660`). Choose from the user's requested market; do not silently take the first candidate.

### Company Info

Returns the resolved identity and available SEC/DART filings, third-party research reports, earnings-call transcripts, report forms, and financial item names.

U.S. SEC issuer:

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-info" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"0002120882","identifier_type":"cik","market":"US","auto_collect":false,"filing_limit":50,"fact_limit":1000}'
```

Korean DART issuer:

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-info" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"00164779","identifier_type":"dart_corp_code","market":"KR","auto_collect":false,"filing_limit":50,"fact_limit":1000}'
```

Verify the returned `canonical_issuer_id`, `market`, `matched_by`, and `match_confidence` before using any report catalog entry.

### Company Report Text

Prefer the stable `report_id` and `report_type` returned by company-info. Report types are `SEC`, `DART`, `RESEARCH`, and `TRANSCRIPT`.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-report-text" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"0002120882","identifier_type":"cik","market":"US","report_id":"<catalog report_id>","report_type":"RESEARCH","max_section_chars":50000,"auto_collect":false}'
```

Before treating text as evidence, verify that the response company, selected report `canonical_issuer_id`, `report_id`, and `report_type` all match the chosen catalog entry.

Business statuses include `ok`, `invalid_input`, `selector_conflict`, `ambiguous_entity`, `entity_not_found`, `report_not_found`, `text_not_cached`, `section_not_found`, `unsupported`, `partial_result`, and `upstream_error`. For `ambiguous_entity`, use `ambiguity_candidates[]` and the returned resolution hint to retry with one exact selector.

### Key Market Events

Returns important macro events and configured focus-company earnings dates. Rows marked `estimated_schedule` should be confirmed against official calendars before alerting or trading.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/key-market-events" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-07-21", "end_date": "2026-08-31", "importance": "high", "limit": 10}'
```

### Politician Stock Activity

Returns official U.S. House PTR transaction disclosure evidence by ticker, filer, district, date, transaction code, owner code, or disclosed amount bucket. It is not current holdings, exact trade value, cost basis, profit, or investment advice. Senate eFD is deliberately unsupported until consent/terms review is complete.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/politician-stock-activity" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chamber":"house","source_year":2026,"ticker":"AAPL","transaction_codes":["P","S"],"limit":25}'
```

The MCP tool accepts `transaction_codes` and `owner_codes` as comma-separated strings, for example `P,S` and `SP,JT`.

### Institution Managers

Returns staged SEC Form 13F manager identity and filing coverage metadata only. Use this before holdings when the user gives a fuzzy institution name; pass a returned `manager_cik` or exact staged manager name to the holdings endpoint.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/institution-managers" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"search":"Berkshire","limit":5}'
```

### Institution Stock Holdings

Returns one manager's latest SEC Form 13F stock holding disclosure evidence from the staged manager universe. `institution` is required and accepts a staged manager name or exact SEC manager CIK. Results are delayed quarter-end filings, not real-time holdings or complete economic exposure.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/institution-stock-holdings" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"institution":"0001067983","sort_by":"value","limit":25}'
```

### Crypto Holdings Evidence

Returns Blockscout address-balance evidence for an institution or wallet address. It is not proof of economic ownership, beneficial ownership, investment advice, or a trading signal.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/crypto-holdings" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "chain": "ethereum", "token_symbol": "ETH", "limit": 100}'
```

### Crypto Holding Changes

Returns changes between adjacent wallet snapshots. At least two snapshots are needed to produce changed records.
The raw HTTP API accepts `change_types` as a JSON array. The MCP tool `get_crypto_holding_changes` accepts a comma-separated string such as `increase,decrease` and defaults `auto_collect` to `false`; collect holdings first when a fresh wallet snapshot is needed.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/crypto-holding-changes" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "chain": "ethereum", "change_types": ["increase", "decrease"], "auto_collect": false, "limit": 100}'
```

---

## Data Structures

### News Article

```json
{
  "id": "unique-article-id",
  "text": "Article headline / content",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{"symbol": "BTC", "market_type": "cex", "match": "title"}],
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

---

## Common Workflows

### Quick Market Overview
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}' | jq '.data[] | {text, newsType, signal: .aiRating.signal}'
```

### High-Impact News (score >= 80)
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"score": 80, "limit": 50, "page": 1}'
```

---

## Free API Endpoints (No Token Required)

If you don't have an `OPENNEWS_TOKEN`, you can use these free endpoints as a fallback. These provide curated hot news and trending tweets by category, but with limited search capabilities compared to the authenticated API.

### 1. Get Free News Categories

Get all available news categories and subcategories for the free tier.

```bash
curl -s -X GET "https://ai.6551.io/open/free_categories"
```

### 2. Get Hot News by Category

Get hot news articles and trending tweets by category. No authentication required.

```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro"
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | yes | Category key from free_categories |
| `subcategory` | string | no | Subcategory key for more specific filtering |

**Response Structure:**
```json
{
  "success": true,
  "category": "crypto",
  "subcategory": "defi",
  "news": {
    "success": true,
    "count": 10,
    "items": [
      {
        "id": 123,
        "title": "...",
        "source": "...",
        "link": "https://...",
        "score": 85,
        "grade": "A",
        "signal": "bullish",
        "summary_zh": "...",
        "summary_en": "...",
        "coins": ["BTC", "ETH"],
        "published_at": "2026-03-17T10:00:00Z"
      }
    ]
  },
  "tweets": {
    "success": true,
    "count": 5,
    "items": [
      {
        "author": "Vitalik Buterin",
        "handle": "VitalikButerin",
        "content": "...",
        "url": "https://...",
        "metrics": { "likes": 1000, "retweets": 200, "replies": 50 },
        "posted_at": "2026-03-17T09:00:00Z",
        "relevance": "high"
      }
    ]
  }
}
```

**Example - Get Hot Macro News:**
```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro"
```

**Example - Get DeFi Subcategory News:**
```bash
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro&subcategory=defi"
```

---

## Notes

- **Primary API**: Get your token at https://6551.io/mcp for full access to 85+ sources with advanced search
- **Free API**: Use free endpoints as fallback when token is unavailable (limited to curated hot news)
- Rate limits apply; max 100 results per request for authenticated API
- AI ratings may not be available on all articles (check `status == "done"`)
- Free API data is cached and updated periodically; if data is still being generated, a 503 response will be returned
