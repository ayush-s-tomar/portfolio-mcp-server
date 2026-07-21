"""
Portfolio MCP Server -- root-level entry point.

The actual implementation lives in portfolio_mcp_server/server.py so the
project can be packaged and published to PyPI / the MCP Registry. This file
is kept so existing instructions keep working unchanged:

    mcp dev server.py
    python server.py

and so the Claude Desktop config snippet (which points at this file's
absolute path) continues to work without edits.
"""

from portfolio_mcp_server.server import main, mcp  # noqa: F401

if __name__ == "__main__":
    main()
