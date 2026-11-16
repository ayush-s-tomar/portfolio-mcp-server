# Changelog

## 1.1.0 - 2026-11-16

### Added
- `match_job_description` tool: ranks the portfolio against a pasted job description (keyword overlap, no LLM)
- `get_data_info` tool: data date, source (live or bundled), project count, package version
- Multi-technology search ("LangGraph and FastAPI") and topic words (RAG, agents, voice, fine-tuning)
- Live data refresh: the first tool call fetches `portfolio_mcp_server/data/projects.json` from this repository (3 second timeout, validated, falls back to the bundled copy). Set `PORTFOLIO_MCP_OFFLINE=1` to disable the network call
- MCP resources: `portfolio://projects`, `portfolio://projects/{name}`, `portfolio://profile`
- MCP prompts: `evaluate_fit` and `portfolio_tour`
- All tools are marked read-only (`readOnlyHint`), so clients can run them without asking each time

### Changed
- Project data moved from Python code to `portfolio_mcp_server/data/projects.json` (one source of truth, also bundled in the package)
- `get_project_details` prefers exact and prefix matches, understands descriptions ("RAG chatbot"), and lists other matches
- Minimum `mcp` version is now 1.10.0 (needed for tool annotations)
- Tool descriptions no longer contain corrupted characters

### Tests
- Added tests for data refresh, validation, search, matching, annotations, resources, and prompts; the stdio smoke test now covers all 7 tools
## 1.0.4 - 2026-10-27

### Changed
- PyPI page: collapsed README sections now render as normal headings (applied at build time)
- README: project structure lists the new tests, workflows, and policy files
## 1.0.3 - 2026-10-25

### Changed
- Added the AI Data Analyst demo link
- Shortened the MCP registry description
- README: clearer quickstart, and commands use double quotes so they work in PowerShell, cmd, and bash

## 1.0.2 - 2026-10-24

### Changed
- Refreshed the bundled project data: 18 projects (was 10), AskMyDocs is now the flagship
- Updated demo links; descriptions now state eval numbers and known limitations
- Updated the profile: role target, core stack, highlights

### Fixed
- Corrupted characters in the module header
- README: project structure matches the repo layout, added Claude Code and uvx install options, links work on PyPI

### Packaging
- `mcp` dependency pinned to `>=1.0.0,<2.0.0`

## 1.0.1 - 2026-07-21

- First PyPI and MCP registry release