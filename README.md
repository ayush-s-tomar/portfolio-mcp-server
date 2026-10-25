<div align="center">

# 🗂️ Portfolio MCP Server

### Ask an AI about my work. It answers from real data, not a PDF.

An MCP server that makes my AI project portfolio **queryable**.<br/>
Connect it to Claude, Cursor, or any MCP client and just ask.

<br/>

[![PyPI](https://img.shields.io/pypi/v/portfolio-mcp-server?color=blue)](https://pypi.org/project/portfolio-mcp-server/)
[![CI](https://github.com/ayush-s-tomar/portfolio-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/ayush-s-tomar/portfolio-mcp-server/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/protocol-MCP-5A67D8.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ayush-s-tomar/portfolio-mcp-server/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ayush-s-tomar/portfolio-mcp-server/blob/main/CONTRIBUTING.md)

**[Quickstart](#-quickstart)** ·
**[Tools](#-tools)** ·
**[Demo](#-demo)** ·
**[Connect a client](#-connect-a-client)** ·
**[Limitations](#known-limitations)** ·
**[Roadmap](#roadmap)**

<br/>

<img src="https://raw.githubusercontent.com/ayush-s-tomar/portfolio-mcp-server/main/assets/MCP.gif" alt="Portfolio MCP Server demo" width="720">

</div>

<br/>

## ⚡ Quickstart

The server command (clients launch it for you; run by hand, it just waits silently for a client):

```bash
uvx --with "mcp<2" portfolio-mcp-server
```

Add it to Claude Code with one line:

```bash
claude mcp add --scope user portfolio -- uvx --with "mcp<2" portfolio-mcp-server
```

Then ask:

> *"What has Ayush built with LangGraph?"*

Prefer pip? `pip install portfolio-mcp-server`

## 💡 Why this exists

Most AI-developer portfolios are a list of links. This is a working MCP server built around my own portfolio, using the same protocol agentic products use to connect to tools. It is a real implementation of the spec and a direct answer to *"show me you've actually built with MCP."*

| | |
|---|---|
| 📦 **Published** | Live on PyPI and the official MCP registry |
| 🔧 **5 tools** | List, detail lookup, stack search, flagship pick, resume summary |
| ✅ **Tested** | Lint, type-check, and a stdio smoke test on every push |

## 🧰 Tools

| Tool | What it does | Try asking |
|---|---|---|
| `list_projects` | Summary of every project in the dataset | *"List everything Ayush has built."* |
| `get_project_details(project_name)` | Full details for one project | *"Tell me about his RAG chatbot."* |
| `search_projects_by_stack(technology)` | Projects using a given technology | *"Which projects use FastAPI?"* |
| `get_flagship_project` | The best project to look at first | *"What should I look at first?"* |
| `get_resume_summary` | Background, target role, core stack | *"Summarize his background."* |

## 🧠 How it works

```text
MCP client (Claude, Cursor, agents)  <--stdio-->  portfolio-mcp-server (FastMCP)  -->  bundled project data
```

The client launches the server as a local process and talks to it over stdio. The server answers each tool call from its bundled project data. Nothing is hosted, and no API keys are needed.

## 🎬 Demo

| MCP Inspector: tool discovery | Live chat demo |
|---|---|
| ![MCP Inspector Demo](https://raw.githubusercontent.com/ayush-s-tomar/portfolio-mcp-server/main/assets/MCP_Inspector_Demo.png) | ![MCP Chat Demo](https://raw.githubusercontent.com/ayush-s-tomar/portfolio-mcp-server/main/assets/MCP_Chat_Demo.png) |

<details>
<summary><b>🎥 Full video walkthrough</b></summary>
<br/>

https://github.com/user-attachments/assets/4c1b844a-087f-48a6-b156-bdef27282acc

*Setup → tool calls → live answers, end to end.*

</details>

## 🔌 Connect a client

<details open>
<summary><b>Claude Code</b></summary>
<br/>

```bash
claude mcp add --scope user portfolio -- uvx --with "mcp<2" portfolio-mcp-server
```

</details>

<details>
<summary><b>Claude Desktop</b></summary>
<br/>

Open your config file:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

If the file already has an `mcpServers` key, add `"portfolio"` inside it instead of overwriting the file.

**Installed with pip:**

```json
{
  "mcpServers": {
    "portfolio": {
      "command": "portfolio-mcp-server"
    }
  }
}
```

**Running from a cloned checkout** (use the absolute path to `server.py`):

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

Restart Claude Desktop and ask: *"What projects has Ayush built with FastAPI?"*

</details>

<details>
<summary><b>Cursor and other clients</b></summary>
<br/>

Any MCP client that can launch a stdio server works. Use `portfolio-mcp-server` (after `pip install`) or the `uvx` command above as the server command.

</details>

## 🛠️ Development

<details>
<summary><b>Run from source</b></summary>
<br/>

```bash
git clone https://github.com/ayush-s-tomar/portfolio-mcp-server.git
cd portfolio-mcp-server

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Test it interactively with the MCP Inspector:

```bash
mcp dev server.py
```

This opens a browser UI where you can call each tool and inspect raw request and response payloads.

</details>

<details>
<summary><b>Testing & CI</b></summary>
<br/>

Every push and pull request runs through GitHub Actions:

| Check | Command |
|---|---|
| Lint | `ruff check .` |
| Type check | `mypy server.py` |
| Smoke test | Starts the server and calls all 5 tools over stdio, confirming each returns valid, schema-matching JSON |

Run the same checks locally before opening a PR:

```bash
pip install -r requirements-dev.txt
ruff check .
mypy server.py
pytest
```

See [`.github/workflows/ci.yml`](https://github.com/ayush-s-tomar/portfolio-mcp-server/blob/main/.github/workflows/ci.yml).

</details>

<details>
<summary><b>Project structure</b></summary>
<br/>

```text
portfolio-mcp-server/
|-- portfolio_mcp_server/
|   |-- __init__.py
|   `-- server.py          # packaged module (what PyPI ships)
|-- server.py              # top-level entry point (dev / MCP Inspector / CI)
|-- tests/
|   |-- smoke_test.py      # stdio smoke test: calls all 5 tools, validates JSON schema
|   `-- test_tools.py      # per-tool tests
|-- assets/                # demo GIF and screenshots
|-- .github/workflows/ci.yml
|-- pyproject.toml         # PyPI packaging config
|-- server.json            # MCP registry manifest
|-- requirements.txt
|-- requirements-dev.txt
|-- claude_desktop_config_snippet.json
|-- CONTRIBUTING.md
`-- LICENSE
```

</details>

**Built with:** Python 3.10+ · [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`FastMCP`) · stdio transport · registered on the [MCP registry](https://modelcontextprotocol.io) as `io.github.ayush-s-tomar/portfolio-mcp-server`

<a id="known-limitations"></a>

## ⚠️ Known limitations

> **Warning:** **The installed package is a snapshot.** `pip install` gets the portfolio as it was at that release (v1.0.3, published 2026-10-25, at the time of writing). Projects added and demo links changed since then won't appear until a new version is published, and tool responses can't yet say how current they are.

- **Static project data.** Tools read from bundled data, so updating a project means editing it and republishing. There is no live sync with the GitHub repos or portfolio site yet.
- **stdio only.** It works for local clients that can spawn the process, such as Claude Desktop, but there is no HTTP/SSE option yet for remote clients.
- **One technology per search.** `search_projects_by_stack` filters on a single technology per call, so "LangGraph *and* FastAPI together" isn't supported yet.

<a id="roadmap"></a>

## 🗺️ Roadmap

**Done**

- [x] Publish to PyPI as an installable package
- [x] Publish to the official MCP server registry
- [x] Refresh the bundled project data (v1.0.2)

**Next**

- [ ] Fetch project data from the portfolio site at startup, with the bundled snapshot as an offline fallback (one source of truth instead of two copies that drift apart)
- [ ] Return a `last_updated` date from every tool so an answer can say how current it is
- [ ] Link-check every demo URL in the dataset in CI
- [ ] Support matching multiple technologies at once in `search_projects_by_stack`
- [ ] Add an HTTP/SSE transport option alongside stdio for remote clients

## 🌐 Also listed on

<a href="https://mcprush.com/to/ayush-s-tomar-portfolio-mcp?ref=badge">
  <img src="https://mcprush.com/badge/ayush-s-tomar-portfolio-mcp/card.svg" alt="Portfolio MCP server on mcprush" width="320">
</a>

## 📄 License

Released under the [MIT License](https://github.com/ayush-s-tomar/portfolio-mcp-server/blob/main/LICENSE).

---

<div align="center">

**Built by Ayush Singh Tomar**

[GitHub](https://github.com/ayush-s-tomar) · [LinkedIn](https://www.linkedin.com/in/ayushsinghtomar) · [Portfolio](https://ayush-s-tomar.vercel.app)

If this helped you build your own MCP server, a ⭐ on the repo is appreciated.

</div>


mcp-name: io.github.ayush-s-tomar/portfolio-mcp-server
