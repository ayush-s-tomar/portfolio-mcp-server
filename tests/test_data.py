"""Data integrity checks for the bundled portfolio data."""

from portfolio_mcp_server.server import (
    PROFILE,
    PROJECTS,
    get_project_details,
    search_projects_by_stack,
)

REQUIRED_KEYS = {
    "name",
    "description",
    "stack",
    "github",
    "demo",
    "writeup",
    "flagship",
}


def test_every_project_has_required_keys() -> None:
    for p in PROJECTS:
        assert REQUIRED_KEYS <= set(p), f"{p.get('name')} is missing keys"


def test_project_names_are_unique() -> None:
    names = [p["name"].lower() for p in PROJECTS]
    assert len(names) == len(set(names))


def test_exactly_one_flagship() -> None:
    flagships = [p["name"] for p in PROJECTS if p["flagship"]]
    assert len(flagships) == 1, flagships


def test_stack_is_a_nonempty_list_of_strings() -> None:
    for p in PROJECTS:
        assert p["stack"], p["name"]
        assert all(isinstance(s, str) and s for s in p["stack"]), p["name"]


def test_urls_are_https_or_none() -> None:
    for p in PROJECTS:
        for key in ("github", "demo", "writeup"):
            url = p[key]
            assert url is None or url.startswith("https://"), (p["name"], key)


def test_github_links_point_to_owner() -> None:
    prefix = "https://github.com/ayush-s-tomar/"
    for p in PROJECTS:
        assert p["github"].startswith(prefix), p["name"]


def test_every_project_is_found_by_its_name() -> None:
    for p in PROJECTS:
        assert get_project_details(p["name"])["name"] == p["name"]


def test_every_project_is_found_by_each_stack_item() -> None:
    for p in PROJECTS:
        for tech in p["stack"]:
            found = [r.get("name") for r in search_projects_by_stack(tech)]
            assert p["name"] in found, (p["name"], tech)


def test_profile_has_expected_keys() -> None:
    expected = {
        "name",
        "role_target",
        "education",
        "core_stack",
        "github",
        "highlights",
    }
    assert expected <= set(PROFILE)