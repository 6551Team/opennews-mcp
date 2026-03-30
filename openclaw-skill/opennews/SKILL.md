---
name: opennews
description: "Real-time crypto & financial news aggregator — 72+ data sources across 5 categories (News: Bloomberg, Reuters, FT, CNBC, CoinDesk, Twitter/X + 47 more; Listing: Binance, Coinbase, OKX + 6 more; OnChain: whale & KOL trades; Meme: social sentiment; Market: price/funding/liquidation alerts). AI-analyzed with impact score, trading signals, and bilingual summaries. **Free tools available without token**."

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
  version: 1.0.2
---

# OpenNews Crypto News Skill

Real-time crypto & financial news aggregator powered by 6551.io — **72+ data sources** across 5 engine categories, all AI-analyzed with impact scores, trading signals, and bilingual summaries.

**Get your token**: https://6551.io/mcp

**Base URL**: `https://ai.6551.io`

## Data Sources — 72+ Sources Across 5 Categories

| Category | Count | Key Sources |
|----------|-------|-------------|
| **News** | 53 | Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, Coinbase, Phoenixnews, and more |
| **Listing** | 9 | Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, Hyperliquid, Aster |
| **OnChain** | 3 | Hyperliquid Whale Trade, Hyperliquid Large Position, KOL Trade |
| **Meme** | 1 | Twitter meme coin social sentiment |
| **Market** | 6 | Price Change, Funding Rate, Funding Rate Difference, Large Liquidation, Market Trends, OI Change |

## Free Tools (No Token Required)

Two tools are available **without** an API token:

### 1. Get News Categories

Get all available news categories and subcategories.

```bash
curl -s "https://ai.6551.io/open/free_categories"
```

### 2. Get Hot News

Get hot news articles and trending tweets by category.

```bash
curl -s "https://ai.6551.io/open/free_hot?category=macro"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | Yes | Category key from free_categories (e.g., `macro`, `crypto`, `defi`) |
| subcategory | string | No | Subcategory key for filtered results |

**Example categories:**
- `macro` - Macro economics and policy
- `crypto` - Cryptocurrency news
- `blockchain` - Blockchain technology
- `defi` - DeFi updates
- `nft` - NFT news
- `market` - Market analysis

**Response structure:**
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
        "title": "DeFi Protocol Reaches $1B TVL",
        "source": "CoinDesk",
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

### Get API Token for Full Access

To access all 72+ sources with AI analysis, trading signals, and real-time WebSocket updates, get your API token at https://6551.io/mcp

## Authentication

All requests require the header:
```
Authorization: Bearer $OPENNEWS_TOKEN
```

---

## News Operations

### 1. Get News Sources

Fetch the full engine tree with all 5 categories and 72+ sources.

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/news_type"
```

Returns a tree with engine types (`news` — 53 sources, `listing` — 9 exchanges, `onchain` — 3 whale/KOL trackers, `meme` — 1 sentiment source, `market` — 6 anomaly signals) and their sub-categories.

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

Important: You need to understand the user's query intent and perform word segmentation, then combine them using OR/AND to form search keywords, supporting both Chinese and English.

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
  "coins": [{"symbol": "BTC", "market_type": "spot", "match": "title"}],
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

### Free Tools (No Token Required)

**Get all categories:**
```bash
curl -s "https://ai.6551.io/open/free_categories"
```

**Get hot crypto news:**
```bash
curl -s "https://ai.6551.io/open/free_hot?category=macro"
```

**Get DeFi subcategory news:**
```bash
curl -s "https://ai.6551.io/open/free_hot?category=macro&subcategory=defi"
```

### Premium Tools (Requires API Token)

**Quick Market Overview:**
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
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.score >= 80)]'
```

## Notes

### Free vs. Premium Features

**Free (no token required):**
- `get_news_categories` - Browse available news categories
- `get_hot_news` - Get hot news by category

**Premium (requires API token from https://6551.io/mcp):**
- Full access to 72+ data sources
- AI analysis with impact scores (0-100), grades (A-F), and trading signals (long/short/neutral)
- Advanced search by keyword, coin, source, or engine type
- Real-time WebSocket news streaming
- Bilingual summaries (English & Chinese)
- Market anomaly signals (liquidations, funding rates, OI changes)

### API Limits

- Rate limits apply; max 100 results per request
- AI ratings may not be available on all articles (check `status == "done"`)
- **Free API data is cached and updated periodically** - not real-time
- If data is still being generated, a 503 response may be returned
- Get your API token at https://6551.io/mcp for full access
