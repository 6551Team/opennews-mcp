# OpenNews MCP Server — Usage Guide

## Overview

This MCP server provides real-time access to a **massive, multi-source crypto & financial news aggregation platform** powered by 6551.io. It aggregates **72+ data sources** across 5 engine categories, covering everything from Bloomberg and Reuters breaking news to on-chain whale trades, meme coin signals, and market anomaly alerts — all with AI-powered ratings and trading signal analysis.

## Data Source Coverage (5 Categories, 72+ Sources)

### 1. News — 53 sources (engineType: "news")
Premium financial & crypto media, government agencies, social platforms:

| Source Code | Description |
|-------------|-------------|
| 6551News | 6551 platform original analysis |
| BWEnews | BWE news wire |
| Bloomberg | Bloomberg — top-tier financial news |
| Reuters | Reuters — global wire service |
| A16Z | a16z (Andreessen Horowitz) — leading crypto VC |
| AGGRNEWS | Aggregated news feed |
| dbnews | DB news |
| Tree | Tree news |
| Velo | Velo data intelligence |
| Phoenixnews | Phoenix news (凤凰新闻) |
| BBC | BBC — British Broadcasting Corporation |
| Binance | Binance announcements & blog |
| Blockworks | Blockworks — crypto-native media |
| Business Insider | Business Insider |
| Chainwire | Chainwire — crypto press releases |
| CNBC | CNBC — financial television |
| CNN | CNN — US news network |
| CoinDesk | CoinDesk — leading crypto media |
| Cointelegraph | Cointelegraph — crypto media |
| Crypto Narratives | Crypto narrative tracking |
| Decrypt | Decrypt — crypto & web3 media |
| DlNews | DL News — crypto investigative journalism |
| Financial Times | Financial Times — premium business news |
| Interfax | Interfax — Russian news agency |
| Medium | Medium blog posts |
| MS NOW | Morgan Stanley NOW — institutional research |
| Politico | Politico — US & EU political news |
| PR Newswire | PR Newswire — press releases |
| TechCrunch | TechCrunch — tech & startup news |
| Techinasia | Tech in Asia — Asian tech news |
| Telegram | Telegram channels |
| Telegraph | The Telegraph — UK news |
| The Big Whale | The Big Whale — European crypto media |
| The Block | The Block — crypto data & journalism |
| The Verge | The Verge — tech media |
| Token Relations | Token relations & partnerships |
| U.S. Treasury | U.S. Treasury Department — official statements |
| Truth Social | Truth Social — Trump's social platform |
| Twitter/X | Twitter/X posts from crypto influencers |
| X / Twitter Profile | Twitter/X profile changes (name, bio updates) |
| U.S. Trade Representative | USTR — trade policy announcements |
| Weibo | Weibo (微博) — Chinese social media |
| Wired | Wired magazine — tech journalism |
| Coinbase | Coinbase announcements & blog |
| Crypto in America | Crypto in America coverage |
| AI_Helper | AI-generated analysis & helper |
| Fox Business | Fox Business — US financial news |
| TASS | TASS — Russian state news agency |
| Hadelsblatt | Hadelsblatt — German business |
| Welt | Welt — German newspaper |
| Handelsblatt | Handelsblatt — German business newspaper |
| Ambrey | Ambrey — maritime & geopolitical intelligence |
| ECB | European Central Bank — official communications |

### 2. Listing — 9 sources (engineType: "listing")
Token listing announcements from major exchanges:

| Source Code | Description |
|-------------|-------------|
| Binance | Binance new token listings |
| Aster | Aster exchange listings |
| Hyperliquid | Hyperliquid perp listings |
| Bithumb | Bithumb (Korean exchange) listings |
| Upbit | Upbit (Korean exchange) listings |
| Robinhood | Robinhood crypto listings |
| Bybit | Bybit new token listings |
| OKX | OKX new token listings |
| Coinbase | Coinbase new token listings |

### 3. OnChain — 3 sources (engineType: "onchain")
On-chain activity from whales and key opinion leaders:

| Source Code | Description |
|-------------|-------------|
| Hyperliquid Whale Trade | Hyperliquid whale trade alerts |
| Hyperliquid Large Position | Hyperliquid large position changes |
| KOL Trade | KOL (Key Opinion Leader) on-chain trades |

### 4. Meme — 1 source (engineType: "meme")
Meme coin social sentiment tracking:

| Source Code | Description |
|-------------|-------------|
| Twitter | Twitter/X meme coin discussions & viral posts |

### 5. Market — 6 sources (engineType: "market")
Market anomaly detection and quantitative signals:

| Source Code | Description |
|-------------|-------------|
| Price Change | Significant price movements (pumps/dumps) |
| Funding Rate | Funding rate anomalies (perp futures) |
| Funding Rate Difference | Cross-exchange funding rate divergences |
| Large Liquidation | Large liquidation events |
| Market Trends | Overall market trend shifts |
| OI Change | Open interest significant changes |

## Available Tools

### Discovery
- **get_news_sources**: Get the full engine tree with all 5 categories and 72+ sources, including metadata (names, icons, AI-enabled status)
- **list_news_types**: Flat list of all source codes for use in filters

### News Search
- **get_latest_news**: Most recent articles across all sources
- **search_news**: Full-text keyword search across all sources
- **search_news_by_coin**: Filter by coin symbol (BTC, ETH, SOL, etc.)
- **get_news_by_source**: Filter by specific source within a category (e.g. engine_type="news", news_type="Bloomberg")
- **get_news_by_engine**: Filter by entire engine category (e.g. "listing" for all exchange listing alerts)
- **search_news_advanced**: Combined multi-filter search (coins + keywords + engine types + has_coin)

### AI Ratings & Signals
- **get_high_score_news**: Articles with high AI impact scores (0-100 scale)
- **get_news_by_signal**: Filter by AI trading signal — "long" (bullish), "short" (bearish), or "neutral"

### Real-time
- **subscribe_latest_news**: WebSocket live feed with optional filters by coins, engine types

## Workflow Examples

1. **Breaking news scan**: `get_latest_news(limit=20)` — see what's happening right now across all 72+ sources
2. **Institutional media only**: `get_news_by_source(engine_type="news", news_type="Bloomberg")` — Bloomberg-only feed
3. **Exchange listing alpha**: `get_news_by_engine(engine_type="listing")` — catch new token listings on Binance, Coinbase, Upbit, etc.
4. **Whale watching**: `get_news_by_engine(engine_type="onchain")` — Hyperliquid whale trades & KOL activity
5. **Market anomalies**: `get_news_by_engine(engine_type="market")` — price spikes, liquidations, OI changes, funding rate divergences
6. **Coin deep-dive**: `search_news_by_coin(coin="ETH", limit=30)` — all ETH-related news across every source
7. **Bullish signals**: `get_news_by_signal(signal="long")` — AI-detected bullish catalysts
8. **Multi-filter power search**: `search_news_advanced(coins="BTC,ETH", engine_types="news:Bloomberg,Reuters;market:", keyword="ETF")` — Bloomberg & Reuters ETF news for BTC/ETH plus all market signals
9. **Live monitoring**: `subscribe_latest_news(wait_seconds=15, coins="BTC", engine_types="news:;market:")` — real-time BTC news + market anomalies

## Data Structure

Each news article contains:
- `id`: Unique article ID
- `text`: Article headline/content
- `newsType`: Source code (e.g. "Bloomberg", "Binance", "price_change")
- `engineType`: Engine category ("news", "listing", "onchain", "meme", "market")
- `link`: URL to original article
- `coins`: Array of related coins `[{symbol, market_type, match}]`
- `aiRating`: AI analysis object:
  - `score`: Impact score 0-100
  - `grade`: Letter grade (A/B/C/D)
  - `signal`: Trading signal ("long" / "short" / "neutral")
  - `status`: Analysis status ("done" = completed)
  - `summary`: Chinese summary
  - `enSummary`: English summary
- `ts`: ISO timestamp
