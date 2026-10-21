from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from reviewkit.labels import BLOCKER, LABEL_NAMES, LABELS, PRAISE, parse_label

# the workflow greps for this to find and edit its own comment
SUMMARY_MARKER = "<!-- reviewkit-summary -->"
SNIPPET_LENGTH = 80


@dataclass
class ReviewComment:
    author: str
    body: str
    path: str | None
    line: int | None
    label: str | None


class Review(NamedTuple):
    author: str
    state: str
    body: str


class UnlabeledComment(NamedTuple):
    author: str
    path: str | None
    line: int | None
    snippet: str


@dataclass
class LintReport:
    counts: dict[str, int]
    unlabeled: list[UnlabeledComment]
    blockers_open: int


def _author(item: dict) -> str:
    return (item.get("user") or {}).get("login", "unknown")


def load_comments(path: str | Path) -> list[ReviewComment]:
    comments = []
    for item in json.loads(Path(path).read_text()):
        body = item.get("body") or ""
        comments.append(
            ReviewComment(
                author=_author(item),
                body=body,
                path=item.get("path"),
                # line is null for outdated comments, original_line still has it
                line=item.get("line") or item.get("original_line"),
                label=parse_label(body),
            )
        )
    return comments


def load_reviews(path: str | Path) -> list[Review]:
    return [
        Review(_author(item), item.get("state", ""), item.get("body") or "")
        for item in json.loads(Path(path).read_text())
    ]


def lint(comments: list[ReviewComment]) -> LintReport:
    counts = dict.fromkeys(LABEL_NAMES, 0)
    unlabeled = []
    for comment in comments:
        if comment.label is None:
            flat = " ".join(comment.body.split())
            snippet = flat if len(flat) <= SNIPPET_LENGTH else flat[: SNIPPET_LENGTH - 1] + "…"
            unlabeled.append(UnlabeledComment(comment.author, comment.path, comment.line, snippet))
        else:
            counts[comment.label] += 1
    # REST API has no thread resolution, so every blocker counts as open
    return LintReport(counts=counts, unlabeled=unlabeled, blockers_open=counts[BLOCKER.name])


def next_step(report: LintReport, reviews: list[Review]) -> str:
    states = {review.state.upper() for review in reviews}
    if report.blockers_open:
        return (
            f"Blocked: {report.blockers_open} blocker comment(s) must be addressed "
            "by the author before merge."
        )
    if "CHANGES_REQUESTED" in states:
        return (
            "Request changes without any blocker: reviewer should add a `blocker:` comment "
            "or switch to Approve."
        )
    if "APPROVED" in states:
        return "Ready to merge: approved with no open blockers."
    return "Awaiting approval: no blockers found, but no approval yet."


def _label_table(report: LintReport) -> list[str]:
    rows = ["| Label | Count | Blocks merge? |", "|---|---:|:---:|"]
    for label in LABELS:
        blocks = "yes" if label.blocks else "no"
        rows.append(f"| `{label.name}:` | {report.counts[label.name]} | {blocks} |")
    return rows


def _unlabeled_section(report: LintReport) -> list[str]:
    if not report.unlabeled:
        return ["All comments carry a label. Thank you!"]
    options = ", ".join(f"`{name}:`" for name in LABEL_NAMES)
    lines = [
        f"### Unlabeled comments ({len(report.unlabeled)})",
        "",
        f"Friendly reminder: start each comment with one of {options} so the author "
        "knows what must change and what is optional.",
        "",
    ]
    for item in report.unlabeled:
        where = item.path or "(general)"
        if item.line is not None:
            where += f":{item.line}"
        lines.append(f"- @{item.author} `{where}` — {item.snippet}")
    return lines


def render_report(report: LintReport) -> str:
    return "\n".join([*_label_table(report), "", *_unlabeled_section(report)]) + "\n"


def render_markdown(report: LintReport, reviews: list[Review], pr_number: int) -> str:
    submitted = ", ".join(f"{r.state} by @{r.author}" for r in reviews) or "none yet"
    praise = report.counts[PRAISE.name]
    if praise:
        praise_line = (
            f"Nice: {praise} praise comment(s) left. Positive feedback reinforces good habits."
        )
    else:
        praise_line = (
            "No praise comments yet. If something was done well, say so; "
            "positive feedback reinforces good habits."
        )
    lines = [
        SUMMARY_MARKER,
        f"## Review summary for PR #{pr_number}",
        "",
        *_label_table(report),
        "",
        f"Reviews submitted: {submitted}",
        "",
        f"**Next step:** {next_step(report, reviews)}",
        "",
        *_unlabeled_section(report),
        "",
        praise_line,
    ]
    return "\n".join(lines) + "\n"
