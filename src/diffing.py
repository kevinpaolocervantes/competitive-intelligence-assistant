from __future__ import annotations

import difflib
from typing import Any


def compare_runs(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, str]]:
    if not previous:
        return [
            {
                "url": page["url"],
                "status": "baseline",
                "summary": "Initial snapshot captured; future scans will compare against this version.",
                "diff": "",
            }
            for page in current["pages"]
        ]

    old_by_url = {page["url"]: page for page in previous["pages"]}
    changes: list[dict[str, str]] = []

    for page in current["pages"]:
        old = old_by_url.get(page["url"])
        if old is None:
            changes.append({
                "url": page["url"],
                "status": "new_page",
                "summary": "New monitored page detected.",
                "diff": page["text"][:2500],
            })
            continue
        if old.get("content_hash") == page.get("content_hash"):
            continue

        diff_lines = list(
            difflib.unified_diff(
                old.get("text", "").splitlines(),
                page.get("text", "").splitlines(),
                fromfile="previous",
                tofile="current",
                lineterm="",
                n=2,
            )
        )
        meaningful = [line for line in diff_lines if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
        changes.append({
            "url": page["url"],
            "status": "changed",
            "summary": f"{len(meaningful)} changed text lines detected.",
            "diff": "\n".join(diff_lines[:180]),
        })

    removed = set(old_by_url) - {page["url"] for page in current["pages"]}
    for url in removed:
        changes.append({
            "url": url,
            "status": "removed",
            "summary": "Previously monitored page is no longer in this scan.",
            "diff": "",
        })
    return changes
