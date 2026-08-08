# OpenNews MCP Server — Usage Guide

## Overview

This MCP server provides real-time access to a **massive, multi-source crypto & financial news aggregation platform** powered by 6551.io. It aggregates **85+ data sources** across 6 engine categories, covering everything from Bloomberg and Reuters breaking news to on-chain whale trades, meme coin signals, market anomaly alerts, and AI prediction signals — all with AI-powered ratings and trading signal analysis.

## Data Source Coverage (6 Categories, 85+ Sources)

### 1. News — 55 sources (engineType: "news")
Premium financial & crypto media, government agencies, social platforms:

| Source Code | Description |
|-------------|-------------|
| 6551News | 6551 platform original analysis |
| BWEnews | BWE news wire |
| Bloomberg | Bloomberg — top-tier financial news |
| Reuters | Reuters — global wire service |
| A16Z | a16z (Andreessen Horowitz) — leading crypto VC |
| AGGRNEWS | Aggregated news feed |
| Velo | Velo data intelligence |
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
| GlobeNewswire | GlobeNewswire — press releases |
| Business Wire | Business Wire — press releases |
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
| jin10 | 金十数据快讯 |

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

### 3. OnChain — 2 sources (engineType: "onchain")
Hyperliquid whale trades and large position activity:

| Source Code | Description |
|-------------|-------------|
| Hyperliquid Whale Trade | Hyperliquid whale trade alerts |
| Hyperliquid Large Position | Hyperliquid large position changes |

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

### 6. Prediction — 12 sources (engineType: "prediction")
AI-powered prediction and correlation signals:

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

## Available Tools

### Discovery
- **get_news_sources**: Get the full engine tree with all 6 categories and 85+ sources, including metadata (names, icons, AI-enabled status)
- **list_news_types**: Flat list of all source codes for use in filters

### News Search
- **get_latest_news**: Most recent articles across all sources
- **search_news**: Full-text keyword search across all sources
- **search_news_by_coin**: Filter by coin symbol (BTC, ETH, SOL, etc.)
- **get_news_by_source**: Filter by specific source within a category (e.g. engine_type="news", news_type="Bloomberg")
- **get_news_by_engine**: Filter by entire engine category (e.g. "listing" for all exchange listing alerts, "prediction" for AI prediction signals)
- **search_news_advanced**: Combined multi-filter search (coins + keywords + engine types + has_coin)
- **get_india_news**: India-focused keyword search (India, Sensex, Nifty, RBI, rupee, etc.) across all sources. Coverage is limited to India mentions from global media; there are no dedicated Indian news sources in the backend catalog yet.

### AI Ratings & Signals
- **get_high_score_news**: Articles with high AI impact scores (0-100 scale)
- **get_news_by_signal**: Filter by AI trading signal — "long" (bullish), "short" (bearish), or "neutral"

### Finance Enhancement
- **search_companies**: Discover company candidates or resolve one exact ticker, CIK, KRX code, DART code, generic typed identifier, or canonical issuer ID
- **get_company_info**: Resolve exactly one issuer and list its SEC/DART filings, research reports, earnings-call transcripts, report forms, and financial item names
- **get_company_report_text**: Fetch one issuer-bound SEC, DART, research, or transcript report by stable `report_id` and `report_type`
- **get_key_market_events**: Query important macro events and configured focus-company earnings dates; estimated schedule rows should be confirmed before alerting or trading
- **get_politician_stock_activity**: Query official U.S. House PTR stock transaction disclosures by ticker, filer, district, date, transaction code, owner code, or disclosed amount bucket; these are disclosure rows, not current holdings
- **get_institution_stock_holdings**: Query latest-per-manager SEC Form 13F stock holdings by ticker, issuer name, CUSIP, manager name, or manager CIK; these are delayed quarter-end filings from the staged manager universe
- **get_crypto_holdings**: Query wallet-visible on-chain holdings evidence for an institution or address; results are Blockscout address-balance evidence, not proof of beneficial ownership or a trading signal
- **get_crypto_holding_changes**: Query on-chain holdings changes between adjacent snapshots, with optional token, date, and change-type filters

For multi-market issuers, first inspect `ambiguity_candidates[]`, then retry with exactly one exact selector. The MCP tools accept `canonical_issuer_id`, `ticker`, `cik`, `krx_stock_code`, `dart_corp_code`, or `identifier` plus `identifier_type` and `market`. Raw HTTP callers must use the generic `identifier` form. For example, `SEC:0002120882` maps to `identifier=0002120882, identifier_type=cik, market=US`, while `DART:00164779` maps to `identifier=00164779, identifier_type=dart_corp_code, market=KR`.

For stock-disclosure tools, preserve evidence boundaries in answers. House PTR amounts are disclosure buckets and Senate is not supported. Form 13F holdings are delayed reporting-period evidence and only cover managers staged in Finance Enhance.

For the MCP tool, pass `change_types` as a comma-separated string such as `"increase,decrease"`. `get_crypto_holding_changes` defaults `auto_collect` to false; call `get_crypto_holdings` first with `auto_collect=true` or `force_collect=true` when you need to populate a fresh wallet snapshot.

### Real-time
- **subscribe_latest_news**: WebSocket live feed with optional filters by coins, engine types

## Workflow Examples

1. **Breaking news scan**: `get_latest_news(limit=20)` — see what's happening right now across all 85+ sources
2. **Institutional media only**: `get_news_by_source(engine_type="news", news_type="Bloomberg")` — Bloomberg-only feed
3. **Exchange listing alpha**: `get_news_by_engine(engine_type="listing")` — catch new token listings on Binance, Coinbase, Upbit, etc.
4. **Whale watching**: `get_news_by_engine(engine_type="onchain")` — Hyperliquid whale trades and large position activity
5. **Market anomalies**: `get_news_by_engine(engine_type="market")` — price spikes, liquidations, OI changes, funding rate divergences
6. **AI predictions**: `get_news_by_engine(engine_type="prediction")` — smart money trades, whale positions, correlations, insider patterns
7. **Coin deep-dive**: `search_news_by_coin(coin="ETH", limit=30)` — all ETH-related news across every source
8. **Bullish signals**: `get_news_by_signal(signal="long")` — AI-detected bullish catalysts
9. **Multi-filter power search**: `search_news_advanced(coins="BTC,ETH", engine_types="news:Bloomberg,Reuters;market:", keyword="ETF")` — Bloomberg & Reuters ETF news for BTC/ETH plus all market signals
10. **Live monitoring**: `subscribe_latest_news(wait_seconds=15, coins="BTC", engine_types="news:;market:")` — real-time BTC news + market anomalies
11. **Company filings workflow**: `search_companies(keyword="Hynix")`, choose one candidate, call `get_company_info(canonical_issuer_id="SEC:0002120882")`, then call `get_company_report_text(canonical_issuer_id="SEC:0002120882", report_id="<catalog id>", report_type="SEC")`
12. **Market event calendar**: `get_key_market_events(start_date="2026-07-21", end_date="2026-08-31", importance="high", limit=10)` — inspect macro and focus-company earnings dates
13. **House PTR activity**: `get_politician_stock_activity(source_year=2026, ticker="AAPL", transaction_codes="P,S", limit=25)` — inspect official House transaction disclosures
14. **13F holdings evidence**: `get_institution_stock_holdings(stock="AAPL", institution="0001067983", limit=25)` — inspect delayed SEC manager filing evidence
15. **On-chain holdings evidence**: `get_crypto_holdings(address="0x...", chain="ethereum", token_symbol="ETH")` — inspect visible wallet-balance evidence
16. **India market scan**: `get_india_news(limit=20)` — India-related mentions (Sensex, Nifty, RBI, rupee, etc.) from the global source catalog

## Data Structure

Each news article contains:
- `id`: Unique article ID
- `text`: Article headline/content
- `newsType`: Source code (e.g. "Bloomberg", "Binance", "price_change")
- `engineType`: Engine category ("news", "listing", "onchain", "meme", "market", "prediction")
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
