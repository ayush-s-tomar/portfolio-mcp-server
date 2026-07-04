# Portfolio MCP Server

An MCP (Model Context Protocol) server that exposes my AI project portfolio
as queryable tools. Point any MCP client (Claude Desktop, etc.) at it and
ask things like "What has Ayush built with LangGraph?" or "What's his
flagship project?" — it answers from live structured data, not a static PDF.

## Why this exists

Most AI-developer portfolios are a list of links. This is a working MCP
server — the same protocol agentic products use to connect to tools — built
around my own portfolio. It's both a real implementation of the spec and a
answer to "show me you've actually built with MCP."

## Tools exposed

- `list_projects` — short summary of all 9 projects
- `get_project_details(project_name)` — full details for one project
- `search_projects_by_stack(technology)` — find projects using a given tech
- `get_flagship_project` — the single best project to look at first
- `get_resume_summary` — background, target role, core stack

## Run it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Test it interactively with the MCP Inspector:

```bash
mcp dev server.py
```

This opens a browser UI to call each tool manually.

## Connect to Claude Desktop

Open your Claude Desktop config file:

- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

If the file already has an `mcpServers` key with other servers in it, just
add the `"portfolio"` entry inside the existing object rather than
overwriting the file. Use the absolute path to `server.py` on your machine:

```json
{
  "mcpServers": {
    "portfolio": {
      "command": "python",
      "args": ["/absolute/path/to/portfolio-mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop. Then ask it something like:

> "What projects has Ayush built with FastAPI?"

Claude will call `search_projects_by_stack` and answer from the live data.

## Stack

- Python
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`FastMCP`)
- stdio transport

## Author

Ayush Tomar — [GitHub](https://github.com/ayush-s-tomar)
