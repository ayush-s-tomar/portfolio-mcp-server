"""Stdio smoke test: start the server the way an MCP client does and call every tool.

Run from the repo root:  python -m tests.smoke_test
"""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CALLS = {
    "list_projects": {},
    "get_project_details": {"project_name": "SalesAgent"},
    "search_projects_by_stack": {"technology": "LangGraph and FastAPI"},
    "match_job_description": {"job_description": "LangGraph, FastAPI, RAG, agents"},
    "get_flagship_project": {},
    "get_resume_summary": {},
    "get_data_info": {},
}


async def main() -> int:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "portfolio_mcp_server.server"],
        env={"PORTFOLIO_MCP_OFFLINE": "1"},
    )
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        names = {tool.name for tool in (await session.list_tools()).tools}
        if names != set(CALLS):
            print(f"Tool mismatch. Missing: {sorted(set(CALLS) - names)} Extra: {sorted(names - set(CALLS))}")
            return 1
        print(f"Discovered all {len(names)} expected tools")
        for name, arguments in CALLS.items():
            result = await session.call_tool(name, arguments)
            if result.isError or not result.content:
                print(f"{name} FAILED")
                return 1
            print(f"{name} returned content")
    print("All tools responded correctly over stdio. Smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))