"""Configuration and shared utilities for the OpenNews MCP server.

Reads settings from config.json at project root. Environment variables
can still override any value.
"""

import json
import os
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path

# ---------- Load config.json ----------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config.json"

_cfg: dict = {}
if _CONFIG_PATH.exists():
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        _cfg = json.load(f)

# ---------- API (env vars take precedence) ----------
API_BASE_URL = os.environ.get("OPENNEWS_API_BASE") or _cfg.get("api_base_url", "")
WSS_URL      = os.environ.get("OPENNEWS_WSS_URL")  or _cfg.get("wss_url", "")
API_TOKEN    = os.environ.get("OPENNEWS_TOKEN")    or _cfg.get("api_token", "")

# Token 状态检查（可选）
HAS_TOKEN = bool(API_TOKEN)

TOKEN_REQUIRED_MSG = (
    "此工具需要 API Token 才能使用。\n"
    "请前往 https://6551.io/mcp 免费申请 Token，\n"
    "然后设置环境变量 OPENNEWS_TOKEN 或在 config.json 中填写 api_token。\n\n"
    "This tool requires an API token. "
    "Get your free token at https://6551.io/mcp, "
    "then set OPENNEWS_TOKEN env var or add api_token to config.json."
)


def require_token() -> dict | None:
    """检查是否配置了 token，未配置时返回错误信息。"""
    if not HAS_TOKEN:
        return {"success": False, "error": TOKEN_REQUIRED_MSG}
    return None

# ---------- Safety ----------
MAX_ROWS = int(os.environ.get("OPENNEWS_MAX_ROWS", 0) or _cfg.get("max_rows", 100))


def clamp_limit(limit: int) -> int:
    """Clamp user-supplied limit to [1, MAX_ROWS]."""
    return min(max(1, limit), MAX_ROWS)


def make_serializable(obj):
    """Recursively convert non-JSON-serializable types."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    return obj
