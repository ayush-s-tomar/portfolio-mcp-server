"""
Portfolio MCP Server
---------------------
Exposes Ayush Singh Tomar's project portfolio as MCP tools so any
MCP-compatible client (Claude Desktop, Claude Code, Cursor, etc.) can query it.

Run locally with the inspector (from the repo root):
    mcp dev server.py

Run standalone (stdio transport, used by MCP clients):
    portfolio-mcp-server
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("portfolio-server")

# ---------------------------------------------------------------------------
# Data: edit this to keep it current, then bump the version and republish.
# ---------------------------------------------------------------------------

PROJECTS: list[dict] = [
    {
        "name": "AskMyDocs",
        "description": (
            "RAG chatbot that answers questions over uploaded PDFs with "
            "source citations and similarity scores. Hybrid search (RRF), "
            "section-aware chunking, and conversation memory. Eval "
            "benchmark: 80% pass rate, average score 6.2/10."
        ),
        "stack": ["Next.js", "Supabase", "pgvector", "Cohere"],
        "github": "https://github.com/ayush-s-tomar/intellect-docs-ai",
        "demo": "https://intellect-docs-ai.vercel.app/",
        "writeup": None,
        "flagship": True,
    },
    {
        "name": "SalesAgent",
        "description": (
            "Autonomous B2B sales agent. Paste a LinkedIn URL and it "
            "researches the lead, scores them with a Random Forest model "
            "(trained on synthetic data), and drafts a personalized cold "
            "email referencing real company events. Saves leads to a CRM "
            "pipeline with SQLite memory."
        ),
        "stack": [
            "LangGraph", "FastAPI", "React", "scikit-learn", "Groq",
            "Tavily", "SQLite",
        ],
        "github": "https://github.com/ayush-s-tomar/salesagent",
        "demo": "https://salesagent-theta.vercel.app/",
        "writeup": "https://dev.to/ayushsinghtomar/i-got-tired-of-writing-cold-emails-so-i-built-an-ai-agent-to-do-it-for-me-2m4h",
        "flagship": False,
    },
    {
        "name": "AgentLoop",
        "description": (
            "Multi-step research agent built as a LangGraph pipeline "
            "(Recall, Plan, Research, Reflect, Synthesize, Persist). Breaks "
            "a question into sub-questions, searches the live web, reflects "
            "on gaps, loops back, and delivers a cited report. SQLite "
            "long-term memory and rate limiting."
        ),
        "stack": ["LangGraph", "Groq", "Tavily", "SQLite"],
        "github": "https://github.com/ayush-s-tomar/agentloop",
        "demo": "https://agentloop.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "LoRA Resume Screener",
        "description": (
            "LoRA fine-tune of Qwen2.5-0.5B-Instruct that returns "
            "structured JSON resume verdicts. On 96 held-out examples, "
            "verdict accuracy rose from 17.7% (zero-shot) to 88.5%, and "
            "mean score error fell from 32.03 to 5.39. Adapter is on "
            "Hugging Face. The hosted demo uses a Groq-backed model because "
            "Render's free tier cannot run the adapter; local inference "
            "runs the trained adapter."
        ),
        "stack": [
            "LoRA", "Qwen2.5", "Hugging Face", "Transformers", "Groq",
        ],
        "github": "https://github.com/ayush-s-tomar/resume-screener-lora",
        "demo": "https://resume-screener-finetune.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "Portfolio MCP Server",
        "description": (
            "This server. A FastMCP server that exposes the portfolio as 5 "
            "MCP tools. Published on PyPI and the official MCP registry, "
            "with CI (ruff, mypy, pytest, and a stdio smoke test)."
        ),
        "stack": ["Python", "FastMCP", "MCP"],
        "github": "https://github.com/ayush-s-tomar/portfolio-mcp-server",
        "demo": "https://pypi.org/project/portfolio-mcp-server/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "StartupScope",
        "description": (
            "Multi-agent CrewAI crew (Researcher, Analyst, Writer) that "
            "searches the web and generates structured company intelligence "
            "reports, with PDF export and a parallel compare mode."
        ),
        "stack": ["CrewAI", "Groq", "Serper", "Streamlit"],
        "github": "https://github.com/ayush-s-tomar/startupscope",
        "demo": "https://startupscope-ai.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "Agentic RAG Research Assistant",
        "description": (
            "LangGraph ReAct agent with Qdrant retrieval and cost-aware "
            "routing between a fast model and a stronger model on Groq. It "
            "refuses to answer when retrieved chunks do not cover the "
            "question. RAGAS eval harness included (eval set is still "
            "placeholder data)."
        ),
        "stack": ["LangGraph", "Qdrant", "Groq", "Streamlit", "FastAPI"],
        "github": "https://github.com/ayush-s-tomar/agentic-rag-research-assistant",
        "demo": "https://agentic-rag-groq.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "Self-Healing RAG",
        "description": (
            "RAG pipeline with a LangGraph critique-and-reformulate loop: "
            "when retrieved context is weak, the graph critiques it, "
            "rewrites the query, and retries."
        ),
        "stack": ["LangGraph", "Groq", "Chroma", "FastAPI", "Streamlit"],
        "github": "https://github.com/ayush-s-tomar/self-healing-rag",
        "demo": None,
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "LLM Cost Router",
        "description": (
            "Streamlit app that routes each query to a cheap or expensive "
            "Groq model using a keyword and length heuristic (no extra LLM "
            "call), with a live dashboard comparing spend against an "
            "always-expensive baseline."
        ),
        "stack": ["Streamlit", "Groq", "Python"],
        "github": "https://github.com/ayush-s-tomar/llm-cost-router",
        "demo": "https://llm-cost-router.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "AgentOps",
        "description": (
            "LLM observability and eval dashboard. Traces latency, tokens, "
            "and cost per step with a @traced decorator, stores run history "
            "in Supabase Postgres, and flags eval regressions. Currently "
            "instruments AgentLoop; the cost formula is approximate."
        ),
        "stack": ["Streamlit", "Supabase", "PostgreSQL", "Python"],
        "github": "https://github.com/ayush-s-tomar/agentops",
        "demo": "https://agentops-dashboard.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "AI Interview Coach",
        "description": (
            "Voice-based mock interview simulator. Transcribes spoken "
            "answers, scores them on relevance, clarity, technical "
            "accuracy, and confidence for SDE, AI Engineer, and Data "
            "Analyst roles, and exports a PDF report. No audio is stored."
        ),
        "stack": [
            "Streamlit", "Faster-Whisper", "Groq", "gTTS", "ReportLab",
        ],
        "github": "https://github.com/ayush-s-tomar/ai-interview-coach",
        "demo": "https://mockinterview-ai.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "ARIA - Voice AI Assistant",
        "description": (
            "Speech-to-speech assistant (v3.0.0) with Groq Whisper "
            "large-v3 speech-to-text, a Groq-hosted LLM, gTTS or ElevenLabs "
            "voice, Redis memory, WebSocket streaming, tool use with web "
            "search, and GitHub OAuth."
        ),
        "stack": [
            "FastAPI", "Groq", "Whisper", "gTTS", "ElevenLabs", "Redis",
            "WebSocket",
        ],
        "github": "https://github.com/ayush-s-tomar/aria-voice-assistant",
        "demo": "https://ayush-s-tomar.github.io/aria-voice-assistant/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "JobHunt",
        "description": (
            "Telegram job aggregator. AI scores every post and can "
            "auto-apply via email or form-fill, with Telegram "
            "notifications and a daily digest. The live demo is a "
            "single-user Streamlit rebuild."
        ),
        "stack": [
            "FastAPI", "PostgreSQL", "Supabase", "Groq", "Playwright",
            "Telegram",
        ],
        "github": "https://github.com/ayush-s-tomar/jobhunt",
        "demo": "https://jobhunt-ai.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "AI Data Analyst Agent",
        "description": (
            "Upload a CSV, Excel, JSON, Parquet, or other tabular file, ask "
            "questions in plain English, and get analysis plus generated "
            "pandas and matplotlib charts. Session memory keeps follow-up "
            "questions in context."
        ),
        "stack": ["Streamlit", "Groq", "pandas", "matplotlib"],
        "github": "https://github.com/ayush-s-tomar/ai-data-analyst",
        "demo": "https://askthedata-ai.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "Email Agent",
        "description": (
            "AI email agent that reads Gmail, classifies messages, drafts "
            "context-aware replies, and lets you approve or edit before "
            "sending. Multi-account Gmail, Slack alerts, and FTS5 "
            "full-text search."
        ),
        "stack": ["FastAPI", "React", "SQLite", "Groq"],
        "github": "https://github.com/ayush-s-tomar/Email-agent",
        "demo": "https://ai-inbox-agent.streamlit.app/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "North Star",
        "description": (
            "Customer support chatbot for outdoor gear shoppers (persona: "
            "Stella) with 5 intent-routed flows: order tracking, returns, "
            "product recommendations, human handoff, and fallback. Runs "
            "locally; order data is mocked."
        ),
        "stack": ["FastAPI", "React", "Groq"],
        "github": "https://github.com/ayush-s-tomar/northstar-chatbot",
        "demo": None,
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "ResumeIQ",
        "description": (
            "AI resume screener that scores ATS compatibility, identifies "
            "gaps, and exports detailed PDF reports."
        ),
        "stack": ["Python", "Flask", "Groq", "pdfplumber", "Docker"],
        "github": "https://github.com/ayush-s-tomar/ResumeIQ",
        "demo": "https://resumeiq-55h8.onrender.com/",
        "writeup": None,
        "flagship": False,
    },
    {
        "name": "n8n Email to Slack",
        "description": (
            "No-code AI automation: fetches unread Gmail, filters noise "
            "(OTPs, spam, resets), summarizes with Groq, detects priority, "
            "and posts a digest to Slack."
        ),
        "stack": ["n8n", "Groq", "Gmail", "Slack"],
        "github": "https://github.com/ayush-s-tomar/n8n-email-slack",
        "demo": None,
        "writeup": None,
        "flagship": False,
    },
]

PROFILE = {
    "name": "Ayush Singh Tomar",
    "role_target": "AI Engineer / GenAI Developer (full-time and freelance)",
    "education": "B.Tech IT, MITS Gwalior (2023-2027, final year)",
    "core_stack": [
        "Python", "FastAPI", "LangGraph", "CrewAI", "LangChain", "Groq",
        "Qdrant", "Supabase pgvector", "Tavily", "React", "Next.js",
        "Streamlit", "Render", "Vercel",
    ],
    "github": "https://github.com/ayush-s-tomar",
    "highlights": [
        "9+ AI projects built and deployed solo: agents, RAG, voice, fine-tuning",
        "LoRA fine-tune of Qwen2.5-0.5B: resume verdict accuracy 17.7% to 88.5% on 96 held-out examples",
        "Published this MCP server on PyPI and the official MCP registry to expose the portfolio itself",
        "Freelance AI developer: multi-agent systems, RAG pipelines, LangGraph, FastAPI backends",
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


def main() -> None:
    """Entry point used by the `portfolio-mcp-server` console script."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
