"""
Portfolio MCP Server
---------------------
Exposes Ayush Singh Tomar's project portfolio as MCP tools so any
MCP-compatible client (Claude Desktop, Claude Code, Cursor, etc.) can query it.

All data lives in one file, portfolio_mcp_server/data/projects.json. The server
starts with the copy bundled in the installed package and, unless offline mode
is set, refreshes it from the repository the first time a tool is used.

Environment variables:
    PORTFOLIO_MCP_OFFLINE=1      never use the network, only the bundled data
    PORTFOLIO_MCP_DATA_URL=...   https URL of an alternative projects.json

Run locally with the inspector (from the repo root):
    mcp dev server.py

Run standalone (stdio transport, used by MCP clients):
    portfolio-mcp-server
"""

import http.client
import json
import os
import re
import time
import urllib.request
from datetime import date
from importlib import resources
from importlib.metadata import PackageNotFoundError, version
from typing import Any, NamedTuple

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("portfolio-server")

# Every tool only reads the portfolio data.
_READ_ONLY = ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False)

# ---------------------------------------------------------------------------
# Data: one JSON file, bundled in the package and refreshed from the repo
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
DEFAULT_DATA_URL = (
    "https://raw.githubusercontent.com/ayush-s-tomar/portfolio-mcp-server/"
    "main/portfolio_mcp_server/data/projects.json"
)
FETCH_TIMEOUT = 3.0
MAX_BYTES = 262144
CACHE_SECONDS = 6 * 60 * 60
RETRY_SECONDS = 10 * 60


class Dataset(NamedTuple):
    projects: list[dict[str, Any]]
    profile: dict[str, Any]
    updated: str
    source: str


def _clean_text(value: object, limit: int) -> str | None:
    if isinstance(value, str) and 0 < len(value) <= limit:
        return value
    return None


def _clean_list(value: object, max_items: int, max_len: int) -> list[str]:
    if not isinstance(value, list) or not 0 < len(value) <= max_items:
        return []
    items = [_clean_text(item, max_len) for item in value]
    if any(item is None for item in items):
        return []
    return [item for item in items if item is not None]


def _clean_project(raw: object) -> dict[str, Any] | None:
    """Keep only known keys with the expected types and sizes."""
    if not isinstance(raw, dict):
        return None
    name = _clean_text(raw.get("name"), 100)
    description = _clean_text(raw.get("description"), 1500)
    stack = _clean_list(raw.get("stack"), 30, 60)
    github = raw.get("github")
    if name is None or description is None or not stack:
        return None
    if not (isinstance(github, str) and github.startswith("https://")):
        return None
    project: dict[str, Any] = {
        "name": name,
        "description": description,
        "stack": stack,
        "github": github,
    }
    for key in ("demo", "writeup"):
        value = raw.get(key)
        if value is None:
            project[key] = None
        elif isinstance(value, str) and value.startswith("https://") and len(value) <= 300:
            project[key] = value
        else:
            return None
    project["flagship"] = raw.get("flagship") is True
    return project


def _clean_profile(raw: object) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    profile: dict[str, Any] = {}
    for key in ("name", "role_target", "education", "github"):
        text = _clean_text(raw.get(key), 300)
        if text is None:
            return None
        profile[key] = text
    core_stack = _clean_list(raw.get("core_stack"), 40, 60)
    highlights = _clean_list(raw.get("highlights"), 12, 300)
    if not core_stack or not highlights:
        return None
    profile["core_stack"] = core_stack
    profile["highlights"] = highlights
    return profile


def _parse(raw: object, source: str) -> Dataset | None:
    """Validate a projects.json document. Returns None if anything is off."""
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA_VERSION:
        return None
    updated = raw.get("updated")
    if not isinstance(updated, str):
        return None
    try:
        date.fromisoformat(updated)
    except ValueError:
        return None
    items = raw.get("projects")
    if not isinstance(items, list) or not 0 < len(items) <= 60:
        return None
    projects = [_clean_project(item) for item in items]
    cleaned = [p for p in projects if p is not None]
    if len(cleaned) != len(items):
        return None
    names = [p["name"].lower() for p in cleaned]
    if len(set(names)) != len(names):
        return None
    profile = _clean_profile(raw.get("profile"))
    if profile is None:
        return None
    return Dataset(cleaned, profile, updated, source)


def _load_bundled() -> Dataset:
    text = (
        resources.files("portfolio_mcp_server")
        .joinpath("data")
        .joinpath("projects.json")
        .read_text(encoding="utf-8")
    )
    dataset = _parse(json.loads(text), "bundled")
    if dataset is None:
        raise RuntimeError("bundled projects.json is invalid")
    return dataset


def _fetch_json(url: str) -> object | None:
    """Download and parse a small JSON document. Returns None on any failure."""
    if not url.startswith("https://"):
        return None
    request = urllib.request.Request(url, headers={"User-Agent": "portfolio-mcp-server"})
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            body = response.read(MAX_BYTES + 1)
    except (OSError, http.client.HTTPException):
        return None
    if len(body) > MAX_BYTES:
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


BUNDLED = _load_bundled()
PROJECTS: list[dict[str, Any]] = BUNDLED.projects
PROFILE: dict[str, Any] = BUNDLED.profile

_state: dict[str, Any] = {"live": None, "fetched_at": 0.0, "retry_at": 0.0}


def _offline() -> bool:
    flag = os.environ.get("PORTFOLIO_MCP_OFFLINE", "").strip().lower()
    return flag in {"1", "true", "yes", "on"}


def _data_url() -> str:
    url = os.environ.get("PORTFOLIO_MCP_DATA_URL", "").strip()
    return url if url.startswith("https://") else DEFAULT_DATA_URL


def _reset_cache() -> None:
    _state.update(live=None, fetched_at=0.0, retry_at=0.0)


def _data() -> Dataset:
    """Current dataset: live copy if fresh and valid, else the bundled one."""
    if _offline():
        return BUNDLED
    now = time.monotonic()
    live = _state["live"]
    if live is not None and now - _state["fetched_at"] < CACHE_SECONDS:
        return live  # type: ignore[no-any-return]
    if now < _state["retry_at"]:
        return live if live is not None else BUNDLED  # type: ignore[no-any-return]
    fetched = _parse(_fetch_json(_data_url()), "live")
    if fetched is not None and fetched.updated >= BUNDLED.updated:
        _state.update(live=fetched, fetched_at=now, retry_at=0.0)
        return fetched
    _state["retry_at"] = now + RETRY_SECONDS
    return live if live is not None else BUNDLED  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------

# Topic words people use in questions, mapped to the tools and terms that
# show up in project stacks and descriptions.
SYNONYMS: dict[str, tuple[str, ...]] = {
    "rag": ("rag", "retrieval", "pgvector", "qdrant", "chroma"),
    "retrieval": ("retrieval", "rag", "pgvector", "qdrant", "chroma"),
    "vector db": ("pgvector", "qdrant", "chroma"),
    "vector database": ("pgvector", "qdrant", "chroma"),
    "agent": ("agent", "agents", "langgraph", "crewai"),
    "agents": ("agent", "agents", "langgraph", "crewai"),
    "multi-agent": ("multi-agent", "crewai", "langgraph"),
    "llm": ("llm", "groq", "llama"),
    "fine-tuning": ("fine-tune", "fine-tuning", "finetune", "lora"),
    "fine-tune": ("fine-tune", "fine-tuning", "finetune", "lora"),
    "voice": ("voice", "speech", "whisper", "gtts", "elevenlabs"),
    "speech": ("speech", "voice", "whisper", "gtts", "elevenlabs"),
    "frontend": ("react", "next.js", "streamlit"),
    "backend": ("fastapi", "flask"),
    "observability": ("observability", "tracing", "traced"),
    "evals": ("eval", "evals", "ragas"),
    "automation": ("automation", "n8n"),
}

_SPLIT = re.compile(r"\s*(?:,|;|\+|&|\band\b)\s*", re.IGNORECASE)


def _split_terms(query: str) -> list[str]:
    terms = [part.strip().lower() for part in _SPLIT.split(query)]
    return [term for term in terms if term][:8]


def _in_text(term: str, text: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text) is not None


def _tokens(text: str) -> set[str]:
    return {t.rstrip(".-") for t in re.findall(r"[a-z0-9][a-z0-9.+#-]*", text.lower())}


def _match_kind(project: dict[str, Any], term: str) -> int:
    """0 = no match, 1 = mentioned in name or description, 2 = in the stack."""
    text = f"{project['name']} {project['description']}".lower()
    stack = [item.lower() for item in project["stack"]]
    best = 0
    for variant in SYNONYMS.get(term, (term,)):
        in_stack = variant in stack if len(variant) < 3 else any(variant in s for s in stack)
        if in_stack:
            return 2
        if _in_text(variant, text):
            best = 1
    return best


def _find_projects(query: str, projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return []
    tiers = (
        lambda p: p["name"].lower() == q,
        lambda p: p["name"].lower().startswith(q),
        lambda p: q in p["name"].lower(),
    )
    for tier in tiers:
        found = [p for p in projects if tier(p)]
        if found:
            return found
    words = _tokens(q)
    if not words:
        return []
    return [p for p in projects if words <= _tokens(f"{p['name']} {p['description']}")]


def _vocabulary(projects: list[dict[str, Any]]) -> set[str]:
    vocab = set(SYNONYMS)
    for project in projects:
        vocab.update(item.lower() for item in project["stack"] if len(item) >= 2)
    return vocab


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def list_projects() -> list[dict[str, Any]]:
    """List all projects in Ayush's portfolio with a short summary of each.

    Returns a compact list (name, short description, stack). Use
    get_project_details for the full description, GitHub link, and demo URL.
    """
    result = []
    for p in _data().projects:
        text = p["description"]
        short = text if len(text) <= 120 else text[:117].rstrip() + "..."
        result.append({"name": p["name"], "description": short, "stack": p["stack"]})
    return result


@mcp.tool(annotations=_READ_ONLY)
def get_project_details(project_name: str) -> dict[str, Any]:
    """Get full details for one project by name.

    Matching is case-insensitive: an exact name wins, then a name prefix, then
    any part of a name ('sales' finds SalesAgent), then the words in a
    description ('RAG chatbot' finds AskMyDocs). If several projects match,
    the best one is returned and the others are listed under 'also_matches'.

    Returns description, full stack, GitHub repo, live demo link, and writeup
    link if one exists.
    """
    projects = _data().projects
    matches = _find_projects(project_name, projects)
    if not matches:
        return {
            "error": f"No project found matching '{project_name}'",
            "available_projects": [p["name"] for p in projects],
        }
    result = dict(matches[0])
    if len(matches) > 1:
        result["also_matches"] = [p["name"] for p in matches[1:]]
    return result


@mcp.tool(annotations=_READ_ONLY)
def search_projects_by_stack(technology: str) -> list[dict[str, Any]]:
    """Find projects that use one or more technologies or topics.

    Case-insensitive, partial names match ('lang' finds LangGraph). Separate
    several with commas, '+', '&' or 'and' to require all of them, e.g.
    'LangGraph and FastAPI'. Common topics are understood too: 'RAG',
    'agents', 'voice', 'fine-tuning', 'frontend', 'backend'.

    Useful for answering "does Ayush have experience with X?"
    """
    terms = _split_terms(technology)
    if not terms:
        return [{"message": "Give at least one technology, for example 'LangGraph' or 'RAG'."}]
    matches = [
        {"name": p["name"], "stack": p["stack"], "github": p["github"]}
        for p in _data().projects
        if all(_match_kind(p, term) for term in terms)
    ]
    if not matches:
        return [{"message": f"No projects found using '{technology}'"}]
    return matches


@mcp.tool(annotations=_READ_ONLY)
def match_job_description(job_description: str, top_n: int = 5) -> dict[str, Any]:
    """Rank Ayush's projects against a pasted job description.

    Finds the technologies and topics in the text (LangGraph, FastAPI, RAG,
    agents, ...) and scores each project by how many it covers. This is a
    keyword overlap, a quick way to see which projects to open first. It is
    not an assessment of fit.
    """
    data = _data()
    text = job_description.lower()[:20000]
    if not text.strip():
        return {"error": "Paste the job description text."}
    terms = sorted(term for term in _vocabulary(data.projects) if _in_text(term, text))
    base: dict[str, Any] = {
        "requirements_detected": terms,
        "note": "Keyword overlap with the portfolio data, not an evaluation of fit.",
        "data_updated": data.updated,
        "data_source": data.source,
    }
    if not terms:
        base["matches"] = []
        base["message"] = "No technologies from the portfolio were found in that text."
        return base
    scored = []
    for project in data.projects:
        kinds = [(term, _match_kind(project, term)) for term in terms]
        score = sum(kind for _, kind in kinds)
        if score:
            scored.append((score, project, [term for term, kind in kinds if kind]))
    scored.sort(key=lambda item: (-item[0], not item[1]["flagship"], item[1]["name"]))
    limit = max(1, min(top_n, 10))
    base["matches"] = [
        {
            "name": project["name"],
            "score": score,
            "matched": matched,
            "github": project["github"],
            "demo": project["demo"],
        }
        for score, project, matched in scored[:limit]
    ]
    return base


@mcp.tool(annotations=_READ_ONLY)
def get_flagship_project() -> dict[str, Any]:
    """Get Ayush's flagship project, the one to look at first for a quick
    sense of his skill level."""
    projects = _data().projects
    for p in projects:
        if p["flagship"]:
            return p
    return projects[0]


@mcp.tool(annotations=_READ_ONLY)
def get_resume_summary() -> dict[str, Any]:
    """Get a summary of Ayush's background: education, target role, core
    tech stack, and career highlights."""
    data = _data()
    return {**data.profile, "data_updated": data.updated, "data_source": data.source}


@mcp.tool(annotations=_READ_ONLY)
def get_data_info() -> dict[str, Any]:
    """Say how current the portfolio data is: its date, whether it came from
    the live repository or the copy bundled with the installed package, how
    many projects it holds, and the package version."""
    data = _data()
    try:
        package_version = version("portfolio-mcp-server")
    except PackageNotFoundError:
        package_version = "unknown"
    return {
        "data_updated": data.updated,
        "data_source": data.source,
        "project_count": len(data.projects),
        "package_version": package_version,
        "offline_mode": _offline(),
        "data_url": _data_url(),
    }


# ---------------------------------------------------------------------------
# Resources and prompts
# ---------------------------------------------------------------------------


@mcp.resource("portfolio://projects", mime_type="application/json")
def projects_resource() -> str:
    """All projects as JSON."""
    return json.dumps(_data().projects, indent=2)


@mcp.resource("portfolio://projects/{name}", mime_type="application/json")
def project_resource(name: str) -> str:
    """One project as JSON, looked up by name (same matching as get_project_details)."""
    matches = _find_projects(name, _data().projects)
    if not matches:
        return json.dumps({"error": f"No project found matching '{name}'"})
    return json.dumps(matches[0], indent=2)


@mcp.resource("portfolio://profile", mime_type="application/json")
def profile_resource() -> str:
    """Background, target role, and core stack as JSON."""
    return json.dumps(_data().profile, indent=2)


@mcp.prompt()
def evaluate_fit(role: str, job_description: str = "") -> str:
    """Assess how well Ayush's portfolio fits a role."""
    lines = [
        f"Assess how well Ayush Singh Tomar's portfolio fits this role: {role}.",
        "",
        "Use the portfolio tools instead of guessing:",
        "1. get_resume_summary for his background and target role.",
        "2. match_job_description with the job description below, or one you write from the role, to find the most relevant projects.",
        "3. get_project_details for the top 2 or 3 projects.",
        "",
        "Answer with strengths, gaps, and which projects to open first, with their links.",
        "Base every claim on the tool results, say plainly where the portfolio does not cover something, and do not invent experience.",
    ]
    if job_description.strip():
        lines += ["", "Job description:", job_description.strip()]
    return "\n".join(lines)


@mcp.prompt()
def portfolio_tour() -> str:
    """A short guided tour of the portfolio."""
    lines = [
        "Give me a five-minute tour of Ayush Singh Tomar's portfolio.",
        "Start with get_flagship_project, then use list_projects and pick three more that show different skills (agents, RAG, fine-tuning, voice, tooling).",
        "For each, say what it does, the stack, one concrete result if the data has one, and the links.",
        "Use only what the tools return.",
    ]
    return "\n".join(lines)


def main() -> None:
    """Entry point used by the `portfolio-mcp-server` console script."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()