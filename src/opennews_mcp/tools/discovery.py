"""Discovery tools — list available news sources and categories."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp


@mcp.tool()
async def get_news_sources(ctx: Context) -> dict:
    """Get all available news source categories and their metadata.

    This platform aggregates 72+ real-time data sources across 5 engine categories:

    NEWS (53 sources): Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business,
      CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch,
      Wired, Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social,
      U.S. Treasury, ECB, TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley (MS NOW),
      PR Newswire, Coinbase, Phoenixnews, and more.

    LISTING (9 sources): Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood,
      Hyperliquid, Aster — new token listing announcements from major exchanges.

    ONCHAIN (3 sources): Hyperliquid Whale Trade, Hyperliquid Large Position,
      KOL Trade — on-chain whale & KOL activity alerts.

    MEME (1 source): Twitter — meme coin social sentiment tracking.

    MARKET (6 sources): Price Change, Funding Rate, Funding Rate Difference,
      Large Liquidation, Market Trends, OI Change — quantitative market anomaly signals.

    Returns a tree structure with all engine types and their sub-categories.
    Use this first to discover what sources are available before searching.
    """
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
    """List all available news type codes for filtering.

    Returns a flat list of news source codes that can be used with
    the newsType parameter in search_news.
    """
    # See get_news_sources for the full 72+ source catalog.
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
