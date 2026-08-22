"""Entry point for the OpenNews MCP server."""

import sys

# MCP stdio on Windows requires SelectorEventLoop: ProactorEventLoop does not
# support add_reader(), which the stdio transport relies on.
if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from opennews_mcp.app import mcp

# Importing the tools package triggers registration of all @mcp.tool() decorators.
import opennews_mcp.tools  # noqa: F401


def main():
    """Run the MCP server (stdio transport by default)."""
    mcp.run()


if __name__ == "__main__":
    main()
