"""Import all tool modules to register their @mcp.tool() decorators.

Each module is self-contained and atomic — no inter-tool dependencies.
"""

from opennews_mcp.tools import discovery  # noqa: F401
from opennews_mcp.tools import finance    # noqa: F401
from opennews_mcp.tools import free       # noqa: F401
from opennews_mcp.tools import news       # noqa: F401
from opennews_mcp.tools import realtime   # noqa: F401
from opennews_mcp.tools import strategy   # noqa: F401
