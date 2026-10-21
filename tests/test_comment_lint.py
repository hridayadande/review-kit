from pathlib import Path

from reviewkit.comment_lint import (
    SUMMARY_MARKER,
    LintReport,
    Review,
    lint,
    load_comments,
    load_reviews,
    next_step,
    render_markdown,
)
from reviewkit.labels import LABEL_NAMES

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _report(blockers: int) -> LintReport:
    counts = dict.fromkeys(LABEL_NAMES, 0)
    counts["blocker"] = blockers
    return LintReport(counts=counts, unlabeled=[], blockers_open=blockers)


def test_load_and_lint_fixture():
    comments = load_comments(EXAMPLES / "sample_comments.json")
    assert len(comments) == 7

    report = lint(comments)
    assert report.counts == {"blocker": 1, "question": 2, "suggestion": 1, "nit": 1, "praise": 1}
    assert report.blockers_open == 1

    assert len(report.unlabeled) == 1
    author, path, line, snippet = report.unlabeled[0]
    assert author == "divyanshu"
    assert path == "pipeline/geometry/window_split.py"
    assert line == 72  # from original_line, line is null in the fixture
    assert snippet.startswith("I am not sure this handles a tile with zero faces.")
    assert len(snippet) <= 80


def test_load_reviews_fixture():
    reviews = load_reviews(EXAMPLES / "sample_reviews.json")
    assert [(r.author, r.state) for r in reviews] == [
        ("divyanshu", "COMMENTED"),
        ("hridayadande", "CHANGES_REQUESTED"),
    ]


def test_next_step_blocked_wins_over_approval():
    reviews = [Review("ayush", "APPROVED", "")]
    assert next_step(_report(2), reviews) == (
        "Blocked: 2 blocker comment(s) must be addressed by the author before merge."
    )


def test_next_step_changes_requested_without_blocker():
    reviews = [Review("amr", "CHANGES_REQUESTED", "please fix")]
    assert next_step(_report(0), reviews).startswith("Request changes without any blocker:")


def test_next_step_ready_to_merge():
    reviews = [Review("amr", "COMMENTED", ""), Review("himanshu", "approved", "")]
    assert next_step(_report(0), reviews) == "Ready to merge: approved with no open blockers."


def test_next_step_awaiting_approval():
    assert next_step(_report(0), []).startswith("Awaiting approval:")
    assert next_step(_report(0), [Review("amr", "COMMENTED", "")]).startswith("Awaiting approval:")


def test_render_markdown_sections():
    report = lint(load_comments(EXAMPLES / "sample_comments.json"))
    reviews = load_reviews(EXAMPLES / "sample_reviews.json")
    markdown = render_markdown(report, reviews, 7)

    assert markdown.startswith(SUMMARY_MARKER + "\n")
    assert "## Review summary for PR #7" in markdown
    assert "| `blocker:` | 1 | yes |" in markdown
    assert "| `question:` | 2 | no |" in markdown
    assert "**Next step:** Blocked: 1 blocker comment(s)" in markdown
    assert "### Unlabeled comments (1)" in markdown
    assert "- @divyanshu `pipeline/geometry/window_split.py:72`" in markdown
    assert "Nice: 1 praise comment(s) left." in markdown
