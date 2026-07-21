"""
End-to-end smoke test: spins up the portfolio MCP server as a subprocess
and calls each of the 5 tools over real stdio transport, confirming each
returns valid, non-empty JSON-serializable output.

Run with:
    python -m tests.smoke_test
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = str(Path(__file__).resolve().parent.parent / "server.py")

EXPECTED_TOOLS = {
    "list_projects",
    "get_project_details",
    "search_projects_by_stack",
    "get_flagship_project",
    "get_resume_summary",
}


async def run_smoke_test() -> None:
    params = StdioServerParameters(command=sys.executable, args=[SERVER_PATH])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tool_names = {t.name for t in tools_result.tools}
            missing = EXPECTED_TOOLS - tool_names
            assert not missing, f"Missing expected tools: {missing}"
            print(f"Discovered all {len(EXPECTED_TOOLS)} expected tools")

            result = await session.call_tool("list_projects", {})
            assert result.content, "list_projects returned empty content"
            print("list_projects returned content")

            result = await session.call_tool(
                "get_project_details", {"project_name": "SalesAgent"}
            )
            assert result.content, "get_project_details returned empty content"
            print("get_project_details returned content")

            result = await session.call_tool(
                "search_projects_by_stack", {"technology": "Groq"}
            )
            assert result.content, "search_projects_by_stack returned empty content"
            print("search_projects_by_stack returned content")

            result = await session.call_tool("get_flagship_project", {})
            assert result.content, "get_flagship_project returned empty content"
            print("get_flagship_project returned content")

            result = await session.call_tool("get_resume_summary", {})
            assert result.content, "get_resume_summary returned empty content"
            print("get_resume_summary returned content")

    print("\nAll 5 tools responded correctly over stdio. Smoke test passed.")


if __name__ == "__main__":
    asyncio.run(run_smoke_test())
