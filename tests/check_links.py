"""Check every URL in the bundled data.

Run from the repo root:  python -m tests.check_links
Exits 1 if any link fails. Used by the weekly GitHub Actions link check.
"""

import sys
import time
import urllib.error
import urllib.request

from portfolio_mcp_server.server import PROJECTS


def check(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "portfolio-mcp-server-link-check"}
    )
    last = "error"
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return "ok" if resp.status == 200 else f"HTTP {resp.status}"
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code in (404, 410):
                break
        except Exception as exc:
            last = type(exc).__name__
        time.sleep(5)
    return last


def main() -> int:
    urls = []
    for p in PROJECTS:
        for key in ("github", "demo", "writeup"):
            if p[key]:
                urls.append((p["name"], key, p[key]))
    failures = 0
    for name, key, url in urls:
        status = check(url)
        print(f"{status:10} {name} [{key}] {url}")
        if status != "ok":
            failures += 1
    print(f"{len(urls) - failures}/{len(urls)} links ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())