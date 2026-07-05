"""Discovery tools — list available financial market news sources and categories."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import require_token


@mcp.tool()
async def get_news_sources(ctx: Context) -> dict:
    """Get all available market news source categories and their metadata.

    This platform aggregates 85+ real-time data sources across 6 engine categories:

    NEWS (55 sources): Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business,
      CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch,
      Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social,
      U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley (MS NOW),
      PR Newswire, GlobeNewswire, Business Wire, Coinbase, and more. Useful for crypto, U.S. equities, macro,
      semiconductors, AI infrastructure, supply chains, commodities, rates, policy,
      and market-moving social/news signals.

    LISTING (9 sources): Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood,
      Hyperliquid, Aster — new token listing announcements from major exchanges.

    ONCHAIN (2 sources): Hyperliquid Whale Trade, Hyperliquid Large Position —
      Hyperliquid whale trades and large position activity.

    MEME (1 source): Twitter — meme coin social sentiment tracking.

    MARKET (6 sources): Price Change, Funding Rate, Funding Rate Difference,
      Large Liquidation, Market Trends, OI Change — quantitative market anomaly signals.

    PREDICTION (12 sources): CORRELATION_LOGICAL, SMART_MONEY_TRADE, PRICE_SPIKE,
      CLUSTER_ENTRY, WHALE_POSITION, NEW_WALLET_TRADE, INSIDER_PATTERN,
      CORRELATION_NARRATIVE, CORRELATION_HEDGE, CORRELATION_ENTITY_GEO,
      CORRELATION_CAUSAL, SETTLEMENT_ARBITRAGE — AI-powered prediction signals.

    Returns a tree structure with all engine types and their sub-categories.
    Use this first to discover what sources are available before searching.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api

    try:
        result = await api.get_engine_tree()
        data = result.get("data", [])

        # Build a simplified summary
        sources = []
        for engine in data:
            categories = []
            for cat in engine.get("categories", []):
                categories.append({
                    "code": cat.get("code"),
                    "name": cat.get("name"),
                    "enName": cat.get("enName"),
                    "aiEnabled": cat.get("aiEnabled", False),
                })
            sources.append({
                "code": engine.get("code"),
                "name": engine.get("name"),
                "enName": engine.get("enName"),
                "category_count": len(categories),
                "categories": categories,
            })

        return {
            "success": True,
            "data": sources,
            "engine_count": len(sources),
        }
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def list_news_types(ctx: Context) -> dict:
    """List all available market news type codes for filtering.

    Returns a flat list of news source codes that can be used with
    the newsType parameter in search_news.
    """
    if (err := require_token()):
        return err
    # See get_news_sources for the full 85+ source catalog.
    api = ctx.request_context.lifespan_context.api

    try:
        result = await api.get_engine_tree()
        data = result.get("data", [])

        types = []
        for engine in data:
            for cat in engine.get("categories", []):
                types.append({
                    "code": cat.get("code"),
                    "engineType": engine.get("code"),
                    "name": cat.get("enName") or cat.get("name"),
                })

        return {
            "success": True,
            "data": types,
            "count": len(types),
        }
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
