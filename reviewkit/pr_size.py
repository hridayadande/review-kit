from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

SMALL = "Small"
MEDIUM = "Medium"
LARGE = "Large"
EXTRA_LARGE = "Extra Large"
SIZES: tuple[str, ...] = (SMALL, MEDIUM, LARGE, EXTRA_LARGE)

# lines = insertions + deletions
SMALL_MAX_LINES = 100
SMALL_MAX_FILES = 5
MEDIUM_MAX_LINES = 300
MEDIUM_MAX_FILES = 15
LARGE_MAX_LINES = 600

RECOMMENDATIONS = {
    SMALL: "Good size: a reviewer can read this in one sitting.",
    MEDIUM: "Reasonable size. Use the PR description to point reviewers at the important parts.",
    LARGE: "Consider splitting this PR; reviewers do their best work under ~300 changed lines.",
    EXTRA_LARGE: (
        "Please split this PR; reviewers do their best work under ~300 changed lines. "
        "If it truly cannot be split, say why in the description and walk a reviewer through it."
    ),
}


@dataclass
class DiffStats:
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0

    @property
    def total(self) -> int:
        return self.insertions + self.deletions


def parse_numstat(output: str) -> DiffStats:
    stats = DiffStats()
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added, deleted = parts[0], parts[1]
        stats.files_changed += 1
        # binary files show "-" instead of numbers
        if added.isdigit():
            stats.insertions += int(added)
        if deleted.isdigit():
            stats.deletions += int(deleted)
    return stats


def diff_stats(base: str, head: str = "HEAD", cwd: str | Path | None = None) -> DiffStats:
    result = subprocess.run(
        ["git", "diff", "--numstat", f"{base}...{head}"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    return parse_numstat(result.stdout)


def classify(stats: DiffStats) -> str:
    if stats.total <= SMALL_MAX_LINES and stats.files_changed <= SMALL_MAX_FILES:
        return SMALL
    if stats.total <= MEDIUM_MAX_LINES and stats.files_changed <= MEDIUM_MAX_FILES:
        return MEDIUM
    if stats.total <= LARGE_MAX_LINES:
        return LARGE
    return EXTRA_LARGE


def render_markdown(stats: DiffStats, size: str) -> str:
    lines = [
        f"### PR size: {size}",
        "",
        "| Files changed | Insertions | Deletions | Changed lines |",
        "|---:|---:|---:|---:|",
        f"| {stats.files_changed} | {stats.insertions} | {stats.deletions} | {stats.total} |",
        "",
        RECOMMENDATIONS[size],
    ]
    return "\n".join(lines) + "\n"
