"""
Portfolio MCP Server
---------------------
Exposes Ayush Tomar's project portfolio as MCP tools so any MCP-compatible
client (Claude Desktop, etc.) can query it interactively.

Run locally with the inspector:
    mcp dev server.py

Run standalone (stdio transport, used by Claude Desktop):
    python server.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("portfolio-server")

# ---------------------------------------------------------------------------
# Data — edit this to keep it current. Later you can swap this for a JSON
# file or a small DB without changing any tool signatures below.
# ---------------------------------------------------------------------------

PROJECTS = [
    {
        "name": "SalesAgent",
        "description": (
            "Autonomous B2B sales agent. Paste a LinkedIn URL, it researches "
            "the lead, scores them with ML (84/100), and drafts a hyper-"
            "personalized cold email referencing real company events, in "
            "under 45 seconds."
        ),
        "stack": ["LangGraph", "FastAPI", "React", "scikit-learn", "Groq", "Tavily"],
        "github": "https://github.com/ayush-s-tomar/salesagent",
        "demo": "https://salesagent-theta.vercel.app/",
        "writeup": "https://dev.to/ayushsinghtomar/i-got-tired-of-writing-cold-emails-so-i-built-an-ai-agent-to-do-it-for-me-2m4h",
        "flagship": True,
    },
    {
        "name": "AgentLoop",
        "description": (
            "A multi-step research agent that breaks a question into "
            "sub-questions, searches the live web, reflects on gaps, loops "
            "back, and delivers a fully cited report."
        ),
        "stack": ["FastAPI", "LangGraph", "Groq", "Tavily"],
        "github": "https://github.com/ayush-s-tomar/agentloop",
        "demo": "https://agentloop.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "AskMyDocs",
        "description": (
            "RAG pipeline that answers questions over 50-page PDFs in under "
            "3 seconds, with source citations and cosine similarity scores. "
            "No SQL, no code."
        ),
        "stack": ["Next.js", "Supabase", "pgvector", "Cohere"],
        "github": "https://github.com/ayush-s-tomar/intellect-docs-ai",
        "demo": "https://intellect-docs-ai.vercel.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "AI Data Analyst Agent",
        "description": (
            "Upload any CSV, ask questions in plain English, get instant "
            "charts and insights. No SQL. No code."
        ),
        "stack": ["FastAPI", "React", "Groq", "pandas", "matplotlib"],
        "github": "https://github.com/ayush-s-tomar/ai-data-analyst",
        "demo": "https://ai-data-analyst-six-sooty.vercel.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "JobHunt",
        "description": (
            "Multi-user Telegram job aggregator. AI scores every post and "
            "auto-applies via email or form-fill. Watches job channels 24/7."
        ),
        "stack": ["FastAPI", "PostgreSQL", "Groq", "Playwright"],
        "github": "https://github.com/ayush-s-tomar/jobhunt",
        "demo": "https://jobhunt-demo.vercel.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "Email Agent",
        "description": (
            "AI agent that reads Gmail, classifies emails, drafts context-"
            "aware replies, and lets you approve or edit before sending."
        ),
        "stack": ["FastAPI", "React", "LLaMA 3.3"],
        "github": "https://github.com/ayush-s-tomar/Email-agent",
        "demo": "https://email-agent-xi-drab.vercel.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "ARIA - Voice AI Assistant",
        "description": (
            "Speech-to-speech AI assistant with 99-language support and "
            "conversation memory. Speak in any language, ARIA transcribes, "
            "thinks, and talks back."
        ),
        "stack": ["FastAPI", "Faster-Whisper", "Groq", "LLaMA", "gTTS"],
        "github": "https://github.com/ayush-s-tomar/aria-voice-assistant",
        "demo": "https://ayush-s-tomar.github.io/aria-voice-assistant",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "StartupScope",
        "description": (
            "Multi-agent CrewAI crew: Researcher, Analyst, and Writer agents "
            "collaborate to search the web and generate structured startup "
            "intelligence reports."
        ),
        "stack": ["CrewAI", "Groq", "SerperDev"],
        "github": "https://github.com/ayush-s-tomar/startupscope",
        "demo": "https://startupscope-ephq.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "n8n Email to Slack",
        "description": (
            "No-code AI automation pipeline: fetches unread Gmail, "
            "summarizes with Groq LLaMA, detects priority, pushes digest to "
            "Slack."
        ),
        "stack": ["n8n", "Groq", "Gmail", "Slack"],
        "github": "https://github.com/ayush-s-tomar/n8n-email-slack",
        "demo": "https://ayush22.app.n8n.cloud/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "ResumeIQ",
        "description": (
            "AI resume screener that scores ATS compatibility, identifies "
            "gaps, and exports detailed PDF reports."
        ),
        "stack": ["Python", "Flask", "Groq"],
        "github": "https://github.com/ayush-s-tomar/ResumeIQ",
        "demo": "https://resumeiq-55h8.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
]

PROFILE = {
    "name": "Ayush Tomar",
    "role_target": "AI Developer (early-stage startups)",
    "education": "B.Tech IT, MITS Gwalior (2023-2027, final year)",
    "core_stack": [
        "Python", "LangChain", "LangGraph", "CrewAI", "FastAPI", "Groq",
        "Supabase pgvector", "Tavily", "React", "Render", "Vercel",
    ],
    "github": "https://github.com/ayush-s-tomar",
    "highlights": [
        "9 independently built and deployed AI projects, no prior internship",
        "Built and shipped an MCP server (this one) to expose the portfolio itself",
        "Active LinkedIn cold-outreach campaign targeting Indian AI startups",
    ],
}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_projects() -> list[dict]:
    """List all projects in Ayush's portfolio with a short summary of each.

    Returns a compact list (name, one-line description, stack) — use
    get_project_details for the full description, GitHub link, and demo URL.
    """
    return [
        {
            "name": p["name"],
            "description": p["description"][:120] + "...",
            "stack": p["stack"],
        }
        for p in PROJECTS
    ]


@mcp.tool()
def get_project_details(project_name: str) -> dict:
    """Get full details for a single project by name (case-insensitive,
    partial match allowed, e.g. 'sales' matches 'SalesAgent').

    Returns description, full stack, GitHub repo, live demo link, and
    writeup link if one exists.
    """
    query = project_name.lower().strip()
    for p in PROJECTS:
        if query in p["name"].lower():
            return p
    return {
        "error": f"No project found matching '{project_name}'",
        "available_projects": [p["name"] for p in PROJECTS],
    }


@mcp.tool()
def search_projects_by_stack(technology: str) -> list[dict]:
    """Find all projects that use a given technology or tool, e.g.
    'LangGraph', 'Groq', 'FastAPI', 'React'. Case-insensitive, partial match.

    Useful for answering "does Ayush have experience with X?"
    """
    query = technology.lower().strip()
    matches = [
        {"name": p["name"], "stack": p["stack"], "github": p["github"]}
        for p in PROJECTS
        if any(query in tech.lower() for tech in p["stack"])
    ]
    if not matches:
        return [{"message": f"No projects found using '{technology}'"}]
    return matches


@mcp.tool()
def get_flagship_project() -> dict:
    """Get Ayush's flagship/best project — the one to look at first for a
    quick sense of his skill level."""
    for p in PROJECTS:
        if p.get("flagship"):
            return p
    return PROJECTS[0]


@mcp.tool()
def get_resume_summary() -> dict:
    """Get a summary of Ayush's background: education, target role, core
    tech stack, and career highlights."""
    return PROFILE


if __name__ == "__main__":
    mcp.run(transport="stdio")
