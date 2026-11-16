"""Tests for tool annotations, resources, and prompts."""

import asyncio
import json

from portfolio_mcp_server import server


def test_every_tool_is_marked_read_only():
    tools = asyncio.run(server.mcp.list_tools())
    assert len(tools) == 7
    for tool in tools:
        assert tool.annotations is not None, tool.name
        assert tool.annotations.readOnlyHint is True, tool.name


def test_resources_are_listed():
    uris = {str(r.uri) for r in asyncio.run(server.mcp.list_resources())}
    assert {"portfolio://projects", "portfolio://profile"} <= uris
    templates = {t.uriTemplate for t in asyncio.run(server.mcp.list_resource_templates())}
    assert "portfolio://projects/{name}" in templates


def test_resource_functions_return_json():
    assert len(json.loads(server.projects_resource())) == len(server.PROJECTS)
    assert json.loads(server.project_resource("sales"))["name"] == "SalesAgent"
    assert "error" in json.loads(server.project_resource("nonexistent-xyz"))
    assert "highlights" in json.loads(server.profile_resource())


def test_prompts_are_listed_and_point_at_tools():
    names = {p.name for p in asyncio.run(server.mcp.list_prompts())}
    assert {"evaluate_fit", "portfolio_tour"} <= names
    text = server.evaluate_fit("AI Engineer", "We use LangGraph and FastAPI.")
    assert "match_job_description" in text
    assert "LangGraph and FastAPI" in text
    assert "get_flagship_project" in server.portfolio_tour()