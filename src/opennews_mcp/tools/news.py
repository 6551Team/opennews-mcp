"""News content tools — search and retrieve real-time financial market news via REST API.

Covers crypto, U.S. equities, macro, semiconductors, AI infrastructure, supply chains,
commodities, rates, policy, and market-moving social/news signals across 6 engine categories:
news (55 premium media & social sources), listing (9 exchanges), onchain (Hyperliquid whale trades and large positions),
meme (social sentiment), market (6 anomaly signals), and prediction (12 AI prediction signals).
Uses POST /open/news_search as the primary data source.
"""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import clamp_limit, make_serializable, MAX_ROWS, require_token


@mcp.tool()
async def get_latest_news(ctx: Context, limit: int = 10) -> dict:
    """Get the most recent market-moving news and signals, newest first.

    Returns news from 85+ sources across all 6 categories (news, listing, onchain,
    meme, market, prediction) with title text, source, link, related assets, AI rating, and tags.
    Coverage includes crypto, U.S. equities, macro, semiconductors, AI infrastructure,
    supply chains, commodities, rates, policy, and social/news signals.

    Args:
        limit: Maximum number of articles to return (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news(keyword: str, ctx: Context, limit: int = 10) -> dict:
    """Search real-time financial market news by keyword in text content.

    Searches across all 85+ sources for crypto, U.S. equities, macro, semiconductors,
    AI infrastructure, supply chains, commodities, rates, policy, and market-moving
    social/news signals. Sources include Bloomberg, Reuters, FT, CNBC, CoinDesk,
    Twitter/X, on-chain alerts, exchange listings, market signals, and AI predictions.

    Args:
        keyword: Search term (e.g. "bitcoin", "NVDA", "FOMC", "tariffs", "oil", "AI chips").
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(query=keyword, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "keyword": keyword, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news_by_coin(coin: str, ctx: Context, limit: int = 10) -> dict:
    """Search news and market signals related to a specific digital asset coin/token.

    Finds all mentions across 85+ sources: media coverage, exchange listings,
    whale trades, meme sentiment, market anomalies, and AI predictions for the given coin.

    Args:
        coin: Coin symbol or name (e.g. "BTC", "ETH", "SOL", "TRUMP").
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(coins=[coin], limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "coin": coin, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_source(engine_type: str, news_type: str, ctx: Context, limit: int = 10) -> dict:
    """Get market news or signal items from a specific source/category.

    Use get_news_sources first to see available engine types and news type codes.

    Args:
        engine_type: The engine type (e.g. "news", "listing", "onchain", "meme", "market", "prediction").
        news_type: The news source code (e.g. "Bloomberg", "Reuters", "Coindesk").
            For listing: "Binance", "Coinbase", "OKX", "Bybit", "Upbit", "Bithumb",
              "Robinhood", "Hyperliquid", "Aster".
            For onchain: "Hyperliquid Whale Trade", "Hyperliquid Large Position".
            For meme: "Twitter".
            For market: "Price Change", "Funding Rate", "Funding Rate Difference",
              "Large Liquidation", "Market Trends", "OI Change".
            For prediction: "CORRELATION_LOGICAL", "SMART_MONEY_TRADE", "PRICE_SPIKE",
              "CLUSTER_ENTRY", "WHALE_POSITION", "NEW_WALLET_TRADE", "INSIDER_PATTERN",
              "CORRELATION_NARRATIVE", "CORRELATION_HEDGE", "CORRELATION_ENTITY_GEO",
              "CORRELATION_CAUSAL", "SETTLEMENT_ARBITRAGE".
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(engine_types={engine_type: [news_type]}, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "engine_type": engine_type, "news_type": news_type, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_engine(engine_type: str, ctx: Context, limit: int = 10) -> dict:
    """Get market news or signal items filtered by engine type.

    Engine types: "news", "listing", "onchain", "meme", "market", "prediction".
      - "news": 55 sources — Bloomberg, Reuters, FT, CNBC, CNN, BBC, CoinDesk, Twitter/X, etc.,
        covering crypto, U.S. equities, macro, semiconductors, AI infrastructure,
        supply chains, commodities, rates, policy, and social/news signals.
      - "listing": 9 exchanges — Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, etc.
      - "onchain": Hyperliquid whale trades and large position activity.
      - "meme": Meme coin social sentiment from Twitter.
      - "market": Price changes, funding rates, liquidations, OI changes, market trends.
      - "prediction": 12 AI prediction signals — smart money, whale positions, correlations, etc.

    Args:
        engine_type: The engine type code.
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(engine_types={engine_type: []}, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "engine_type": engine_type, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news_advanced(
    ctx: Context,
    coins: str = "",
    keyword: str = "",
    engine_types: str = "",
    has_coin: bool = False,
    min_score: int = 0,
    limit: int = 10,
) -> dict:
    """Advanced financial market news search with multiple filters.

    Combines keyword, digital asset coin, engine type, source, and score filters for precise
    queries across the full 85+ source catalog. Use it for crypto, U.S. equities, macro,
    semiconductors, AI infrastructure, supply chains, commodities, rates, policy, and
    market-moving social/news signals.

    Args:
        coins: Comma-separated coin symbols (e.g. "BTC,ETH").
        keyword: Optional search keyword (e.g. "NVDA", "FOMC", "tariffs", "oil", "AI chips").
        engine_types: Engine type filter in format "type1:cat1,cat2;type2:cat3" (e.g. "news:Bloomberg,Reuters;listing:;prediction:").
        has_coin: If true, only return items that have associated digital asset coins.
        min_score: Minimum AI score threshold (default 0, range 0-100).
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)

    coin_list = [c.strip() for c in coins.split(",") if c.strip()] if coins else None

    # 解析 engine_types 字符串为 dict
    engine_types_dict = None
    if engine_types:
        engine_types_dict = {}
        for part in engine_types.split(";"):
            if ":" in part:
                engine, cats = part.split(":", 1)
                engine = engine.strip()
                cat_list = [c.strip() for c in cats.split(",") if c.strip()]
                engine_types_dict[engine] = cat_list

    try:
        result = await api.search_news(
            coins=coin_list, query=keyword or None,
            engine_types=engine_types_dict, has_coin=has_coin,
            score=min_score if min_score > 0 else None,
            limit=limit, page=1,
        )
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_high_score_news(ctx: Context, min_score: int = 70, limit: int = 10) -> dict:
    """Get highly-rated market news and signals by AI score, sorted by score descending.

    AI scores range 0-100 and reflect potential market impact across crypto,
    U.S. equities, macro, semiconductors, AI infrastructure, supply chains,
    commodities, rates, policy, and social/news signals. All items from 85+
    sources are AI-analyzed with score, grade, signal, and summary.

    Args:
        min_score: Minimum score threshold (default 70).
        limit: Maximum results to return (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(score=min_score, limit=limit, page=1)
        data = result.get("data", [])
        data.sort(key=lambda x: x.get("score", 0), reverse=True)
        return make_serializable({
            "success": True, "min_score": min_score,
            "data": data[:limit], "count": len(data[:limit]), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_signal(signal: str, ctx: Context, limit: int = 10) -> dict:
    """Get market news filtered by AI trading signal type.

    Each item from 85+ sources is AI-analyzed for directional market impact.

    Args:
        signal: The signal type: "long" (bullish), "short" (bearish), or "neutral".
        limit: Maximum results (default 10, max 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        fetch_limit = min(limit * 3, MAX_ROWS)
        result = await api.search_news(limit=fetch_limit, page=1)
        raw = result.get("data", [])

        filtered = [it for it in raw
                     if (it.get("aiRating") or {}).get("signal") == signal
                     and (it.get("aiRating") or {}).get("status") == "done"]
        data = filtered[:limit]
        return make_serializable({
            "success": True, "signal": signal,
            "data": data, "count": len(data),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
