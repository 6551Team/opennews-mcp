"""Free news tools — no token required, access via /open/free_* endpoints.

These tools provide basic news access without authentication.
For full features (84+ sources, AI analysis, real-time WebSocket), get a free token at https://6551.io/mcp.
"""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp


@mcp.tool()
async def get_news_categories(ctx: Context) -> dict:
    """Get all available news categories and subcategories.

    Returns a list of categories, each containing subcategories,
    for use with the get_hot_news tool.

    This is a free tool that does not require an API token.
    """
    free_api = ctx.request_context.lifespan_context.free_api
    try:
        result = await free_api.get_free_categories()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_hot_news(
    category: str,
    ctx: Context,
    subcategory: str = "",
) -> dict:
    """Get hot news and tweets by category.

    Args:
        category: Category key (required). Use get_news_categories to list available keys.
        subcategory: Subcategory key (optional).

    Returns:
        Combined news articles and tweets for the given category.

    This is a free tool that does not require an API token.
    """
    free_api = ctx.request_context.lifespan_context.free_api
    try:
        result = await free_api.get_free_hot(
            category=category,
            subcategory=subcategory,
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
