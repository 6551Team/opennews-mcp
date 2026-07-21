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
  version: 1.0.5
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

## Finance Enhancement Endpoints

These authenticated endpoints provide company report discovery, company report text, and wallet-visible on-chain holdings evidence. Responses are wrapped as `{"success": true, "data": ...}` and may include usage quota metadata.

### Company Search

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "IBM", "limit": 20, "auto_collect": true}'
```

### Company Info

Returns company identity, available SEC filings, third-party research reports, earnings-call transcripts, report forms, and financial item names.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-info" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"company": "IBM", "auto_collect": true, "filing_limit": 300, "fact_limit": 5000}'
```

### Company Report Text

Fetches SEC filing, third-party research report, or earnings-call transcript text by report name, form, accession, source key, quarter hint, section, or text search.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/company-report-text" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"company": "IBM", "report_name": "10-K", "form_type": "10-K", "auto_collect": true}'
```

### Key Market Events

Returns important macro events and configured focus-company earnings dates. Rows marked `estimated_schedule` should be confirmed against official calendars before alerting or trading.

```bash
curl -s -X POST "https://ai.6551.io/open/finance-enhance/key-market-events" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-07-21", "end_date": "2026-08-31", "importance": "high", "limit": 10}'
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
