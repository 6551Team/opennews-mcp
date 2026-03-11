"""News content tools — search and retrieve news from 72+ sources via REST API.

Covers 5 engine categories: news (53 premium media & social sources), listing (9 exchanges),
onchain (whale & KOL trades), meme (social sentiment), market (6 anomaly signals).
Uses POST /open/news_search as the primary data source.
"""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import clamp_limit, make_serializable, MAX_ROWS


@mcp.tool()
async def get_latest_news(ctx: Context, limit: int = 10) -> dict:
    """Get the most recent crypto news articles, newest first.

    Returns news from 72+ sources across all 5 categories (news, listing, onchain,
    meme, market) with title text, source, link, related coins, AI rating, and tags.

    Args:
        limit: Maximum number of articles to return (default 10, max 100).
    """
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
    """Search crypto news by keyword in text content.

    Searches across all 72+ sources including Bloomberg, Reuters, CoinDesk,
    Twitter/X, on-chain alerts, exchange listings, and market signals.

    Args:
        keyword: Search term (e.g. "bitcoin", "SEC", "ETF").
        limit: Maximum results (default 10, max 100).
    """
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
    """Search news related to a specific cryptocurrency coin/token.

    Finds all mentions across 72+ sources: media coverage, exchange listings,
    whale trades, meme sentiment, and market anomalies for the given coin.

    Args:
        coin: Coin symbol or name (e.g. "BTC", "ETH", "SOL", "TRUMP").
        limit: Maximum results (default 10, max 100).
    """
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
    """Get news articles from a specific source.

    Use get_news_sources first to see available engine types and news type codes.

    Args:
        engine_type: The engine type (e.g. "news", "listing", "onchain", "meme", "market").
        news_type: The news source code (e.g. "Bloomberg", "Reuters", "Coindesk").
            For listing: "Binance", "Coinbase", "OKX", "Bybit", "Upbit", "Bithumb",
              "Robinhood", "Hyperliquid", "Aster".
            For onchain: "Hyperliquid Whale Trade", "Hyperliquid Large Position", "KOL Trade".
            For meme: "Twitter".
            For market: "Price Change", "Funding Rate", "Funding Rate Difference",
              "Large Liquidation", "Market Trends", "OI Change".
        limit: Maximum results (default 10, max 100).
    """
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
    """Get news articles filtered by engine type.

    Engine types: "news", "listing", "onchain", "meme", "market".
      - "news": 53 sources — Bloomberg, Reuters, FT, CNBC, CNN, BBC, CoinDesk, Twitter/X, etc.
      - "listing": 9 exchanges — Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, etc.
      - "onchain": Whale trades & KOL activity on Hyperliquid.
      - "meme": Meme coin social sentiment from Twitter.
      - "market": Price changes, funding rates, liquidations, OI changes, market trends.

    Args:
        engine_type: The engine type code.
        limit: Maximum results (default 10, max 100).
    """
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
    limit: int = 10,
) -> dict:
    """Advanced news search with multiple filters.

    Combines coin, keyword, engine type, and source filters for precise queries
    across the full 72+ source catalog.

    Args:
        coins: Comma-separated coin symbols (e.g. "BTC,ETH").
        keyword: Optional search keyword.
        engine_types: Engine type filter in format "type1:cat1,cat2;type2:cat3" (e.g. "news:Bloomberg,Reuters;listing:").
        has_coin: If true, only return news that have associated coins.
        limit: Maximum results (default 10, max 100).
    """
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
    """Get highly-rated news articles (by AI score), sorted by score descending.

    AI scores range 0-100 and reflect potential market impact.
    All articles from 72+ sources are AI-analyzed with score, grade, signal, and summary.

    Args:
        min_score: Minimum score threshold (default 70).
        limit: Maximum results to return (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        fetch_limit = min(limit * 3, MAX_ROWS)
        result = await api.search_news(limit=fetch_limit, page=1)
        raw = result.get("data", [])

        filtered = [it for it in raw
                     if (it.get("aiRating") or {}).get("score", 0) >= min_score]
        filtered.sort(
            key=lambda x: (x.get("aiRating") or {}).get("score", 0),
            reverse=True,
        )
        data = filtered[:limit]
        return make_serializable({
            "success": True, "min_score": min_score,
            "data": data, "count": len(data),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_signal(signal: str, ctx: Context, limit: int = 10) -> dict:
    """Get news filtered by trading signal type.

    Each article from 72+ sources is AI-analyzed for trading direction.

    Args:
        signal: The signal type: "long" (bullish), "short" (bearish), or "neutral".
        limit: Maximum results (default 10, max 100).
    """
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
