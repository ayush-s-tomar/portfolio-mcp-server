"""Test setup: never touch the network unless a test opts in."""

import os

os.environ.setdefault("PORTFOLIO_MCP_OFFLINE", "1")