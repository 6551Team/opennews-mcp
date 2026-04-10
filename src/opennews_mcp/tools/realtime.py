"""Real-time news tools — WebSocket subscription for live updates from 84+ sources."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import make_serializable, require_token


@mcp.tool()
async def subscribe_latest_news(
    ctx: Context,
    wait_seconds: int = 10,
    max_items: int = 5,
    coins: str = "",
    engine_types: str = "",
    has_coin: bool = False,
) -> dict:
    """Subscribe to real-time news updates via WebSocket.

    Connects to the WebSocket feed, subscribes to news with optional filters,
    and collects incoming messages for the specified duration.

    Streams live data from 84+ sources across 6 categories:
    news (Bloomberg, Reuters, etc.), listing (Binance, Coinbase, etc.),
    onchain (whale trades), meme (Twitter sentiment), market (price/funding/liquidation alerts),
    prediction (AI prediction signals — smart money, correlations, whale positions, etc.).

    Args:
        wait_seconds: How long to listen for news (default 10, max 30 seconds).
        max_items: Maximum news items to collect (default 5, max 20).
        coins: Comma-separated coin symbols to filter (e.g. "BTC,ETH").
        engine_types: Engine type filter in format "type1:cat1,cat2;type2:cat3".
        has_coin: If true, only receive news that have associated coins.
    """
    if (err := require_token()):
        return err
    ws = ctx.request_context.lifespan_context.ws
    wait_seconds = min(max(1, wait_seconds), 30)
    max_items = min(max(1, max_items), 20)

    # 解析过滤器参数
    coin_list = [c.strip() for c in coins.split(",") if c.strip()] if coins else None
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
        await ws.subscribe_latest(
            engine_types=engine_types_dict,
            coins=coin_list,
            has_coin=has_coin,
        )

        items = []
        for _ in range(max_items):
            msg = await ws.receive_news(timeout=float(wait_seconds))
            if msg is None:
                break
            items.append(msg)

        return make_serializable({
            "success": True,
            "data": items,
            "count": len(items),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
    finally:
        await ws.close()
