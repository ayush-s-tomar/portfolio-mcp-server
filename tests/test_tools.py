"""
Smoke/unit tests for the portfolio MCP server's tools.

These call the underlying tool functions directly (FastMCP's @mcp.tool()
decorator doesn't wrap them, so they're plain callables) rather than going
through the MCP protocol layer -- fast, no transport needed.
"""

from portfolio_mcp_server.server import (
    PROJECTS,
    get_flagship_project,
    get_project_details,
    get_resume_summary,
    list_projects,
    search_projects_by_stack,
)


def test_list_projects_returns_all_projects():
    result = list_projects()
    assert isinstance(result, list)
    assert len(result) == len(PROJECTS)


def test_list_projects_has_expected_keys():
    result = list_projects()
    for item in result:
        assert "name" in item
        assert "description" in item
        assert "stack" in item


def test_get_project_details_found():
    result = get_project_details("SalesAgent")
    assert result["name"] == "SalesAgent"
    assert "stack" in result


def test_get_project_details_case_insensitive_partial_match():
    result = get_project_details("sales")
    assert result["name"] == "SalesAgent"


def test_get_project_details_not_found():
    result = get_project_details("NonexistentProjectXYZ")
    assert "error" in result
    assert "available_projects" in result


def test_search_projects_by_stack_found():
    result = search_projects_by_stack("Groq")
    assert isinstance(result, list)
    assert len(result) > 0
    assert all("stack" in item for item in result)


def test_search_projects_by_stack_not_found():
    result = search_projects_by_stack("NonexistentTechXYZ")
    assert isinstance(result, list)
    assert "message" in result[0]


def test_get_flagship_project_returns_a_project():
    result = get_flagship_project()
    assert "name" in result
    assert result in PROJECTS


def test_get_resume_summary_has_expected_keys():
    result = get_resume_summary()
    assert isinstance(result, dict)
    assert "github" in result
    assert "highlights" in result
