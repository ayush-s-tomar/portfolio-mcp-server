# Contributing

Thanks for taking a look. Bug reports, fixes, and ideas are welcome.

## Quick start

```bash
git clone https://github.com/ayush-s-tomar/portfolio-mcp-server.git
cd portfolio-mcp-server

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt -r requirements-dev.txt
```

Try the server interactively with the MCP Inspector:

```bash
mcp dev server.py
```

## Before you open a PR

Run the same checks CI runs. All three must pass:

```bash
ruff check .
mypy server.py
pytest
```

## Pull requests

1. Fork the repo and create a branch from `main`.
2. Keep the change focused: one fix or feature per PR.
3. Add or update a test if you change a tool's behavior.
4. Use a clear commit message, for example `fix: handle empty technology in search_projects_by_stack`.
5. Describe what changed and why in the PR description.

## Reporting bugs

Open an issue with:

- what you ran (client, install method, command)
- what you expected
- what happened instead, including any error output
- your Python version and OS

## Good first areas

These match the [roadmap](README.md#roadmap):

- multi-technology matching in `search_projects_by_stack`
- a `last_updated` field on every tool response
- link-checking demo URLs in CI

## Scope

This server exposes one person's portfolio, so the project data itself is not open to edits. Code, tests, docs, and tooling improvements are.