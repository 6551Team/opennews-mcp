"""Strategy tools — list user strategies and query triggered event history."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import clamp_limit, make_serializable, require_token


@mcp.tool()
async def get_strategy_list(ctx: Context, limit: int = 20, page: int = 1) -> dict:
    """Get the authenticated user's strategy list.

    Requires an OpenNews API token. Each call consumes 1 quota.
    Returned strategy items include only id, name, description, enabled, and createdAt.

    Args:
        limit: Maximum number of strategies to return (default 20, max OPENNEWS_MAX_ROWS).
        page: Page number, 1-based.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    page = max(1, page)
    try:
        result = await api.get_strategy_list(limit=limit, page=page)
        if result.get("success") is False:
            return make_serializable(result)
        data = (result.get("data") or [])[:limit]
        return make_serializable({
            "success": True,
            "data": data,
            "count": len(data),
            "total": result.get("total", 0),
            "page": result.get("page", page),
            "limit": result.get("limit", limit),
            "usage": result.get("usage"),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_strategy_hits(strategy_id: int, ctx: Context, limit: int = 20, page: int = 1) -> dict:
    """Get triggered event history for a strategy ID.

    Requires an OpenNews API token. Each call consumes 1 quota.
    Returned hit items use the same news-like payload shape as WebSocket
    strategy.triggered events, including nested strategy fields and optional
    aiRating, coins, relatedAddress, source, description, and metrics.

    Args:
        strategy_id: User strategy ID from get_strategy_list.
        limit: Maximum number of triggered events to return (default 20, max OPENNEWS_MAX_ROWS).
        page: Page number, 1-based.
    """
    if (err := require_token()):
        return err
    if strategy_id <= 0:
        return {"success": False, "error": "strategy_id must be a positive integer"}
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    page = max(1, page)
    try:
        result = await api.get_strategy_hits(strategy_id=strategy_id, limit=limit, page=page)
        if result.get("success") is False:
            return make_serializable(result)
        data = (result.get("data") or [])[:limit]
        return make_serializable({
            "success": True,
            "strategy_id": strategy_id,
            "data": data,
            "count": len(data),
            "total": result.get("total", 0),
            "page": result.get("page", page),
            "limit": result.get("limit", limit),
            "usage": result.get("usage"),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
