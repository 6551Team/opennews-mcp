---
name: opennews
description: Crypto news search, AI ratings, trading signals, and real-time updates via the OpenNews 6551 API. Supports keyword search, coin filtering, source filtering, AI score ranking, and WebSocket live feeds.

user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - OPENNEWS_TOKEN
      bins:
        - curl
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
  version: 1.0.0
---

# OpenNews Crypto News Skill

Query crypto news from the 6551 platform REST API. All endpoints require a Bearer token via `$OPENNEWS_TOKEN`.

**Get your token**: https://6551.io/mcp

**Base URL**: `https://ai.6551.io`

## Authentication

All requests require the header:
```
Authorization: Bearer $OPENNEWS_TOKEN
```

---

## News Operations

### 1. Get News Sources

Fetch all available news source categories organized by engine type.

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/news_type"
```

Returns a tree with engine types (`news`, `listing`, `onchain`, `meme`, `market`) and their sub-categories.

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
  -d '{"q": "bitcoin ETF", "limit": 10, "page": 1}'
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
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.score >= 80)]'
```

## Notes

- Get your API token at https://6551.io/mcp
- Rate limits apply; max 100 results per request
- AI ratings may not be available on all articles (check `status == "done"`)
