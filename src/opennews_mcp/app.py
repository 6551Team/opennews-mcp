"""FastMCP application instance, lifespan, and knowledge resources."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from opennews_mcp.api_client import FreeNewsAPIClient, NewsAPIClient, NewsWSClient
from opennews_mcp.config import HAS_TOKEN

# Knowledge directory (project root / knowledge)
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "knowledge"


@dataclass
class AppContext:
    """Shared application state available to all tools via ctx."""
    free_api: FreeNewsAPIClient
    api: NewsAPIClient | None = None
    ws: NewsWSClient | None = None


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage the API client lifecycle."""
    free_api = FreeNewsAPIClient()
    api = NewsAPIClient() if HAS_TOKEN else None
    ws = NewsWSClient() if HAS_TOKEN else None
    try:
        yield AppContext(free_api=free_api, api=api, ws=ws)
    finally:
        await free_api.close()
        if api:
            await api.close()
        if ws:
            await ws.close()


# ---------- FastMCP instance ----------
_INSTRUCTIONS = """\
OpenNews MCP — Real-time crypto & financial news aggregator powered by 6551.io.

Aggregates 85+ data sources across 6 engine categories:
- NEWS (55 sources): Bloomberg, Reuters, Financial Times, CNBC, CNN, BBC, Fox Business, \
CoinDesk, Cointelegraph, The Block, Blockworks, Decrypt, DlNews, A16Z, TechCrunch, Wired, \
Politico, Business Insider, Twitter/X, Telegram, Weibo, Truth Social, U.S. Treasury, ECB, \
TASS, Handelsblatt, Welt, Ambrey, Morgan Stanley, PR Newswire, GlobeNewswire, Business Wire, \
Coinbase, and more.
- LISTING (9 sources): Binance, Coinbase, OKX, Bybit, Upbit, Bithumb, Robinhood, \
Hyperliquid, Aster — new token listing announcements.
- ONCHAIN (2 sources): Hyperliquid Whale Trade, Hyperliquid Large Position — \
Hyperliquid whale trades and large position activity.
- MEME (1 source): Twitter meme coin social sentiment.
- MARKET (6 sources): Price Change, Funding Rate, Funding Rate Difference, \
Large Liquidation, Market Trends, OI Change — quantitative market signals.
- PREDICTION (12 sources): CORRELATION_LOGICAL, SMART_MONEY_TRADE, PRICE_SPIKE, \
CLUSTER_ENTRY, WHALE_POSITION, NEW_WALLET_TRADE, INSIDER_PATTERN, \
CORRELATION_NARRATIVE, CORRELATION_HEDGE, CORRELATION_ENTITY_GEO, \
CORRELATION_CAUSAL, SETTLEMENT_ARBITRAGE — AI-powered prediction signals.

All articles are AI-analyzed with impact score (0-100), trading signal (long/short/neutral), \
and bilingual summaries (EN/ZH).
"""

mcp = FastMCP(
    "opennews-6551",
    instructions=_INSTRUCTIONS,
    lifespan=app_lifespan,
    json_response=True,
)


# ---------- Knowledge resources ----------
def _read_knowledge(name: str) -> str:
    path = KNOWLEDGE_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Knowledge file '{name}' not found."


@mcp.resource("knowledge://guide")
async def knowledge_guide() -> str:
    """Usage guide — tool workflows, search strategies, best practices."""
    return _read_knowledge("guide.md")
