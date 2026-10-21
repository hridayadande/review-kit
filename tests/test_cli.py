from pathlib import Path

from reviewkit import pr_size
from reviewkit.cli import main
from reviewkit.pr_size import DiffStats

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
COMMENTS = str(EXAMPLES / "sample_comments.json")
REVIEWS = str(EXAMPLES / "sample_reviews.json")


def test_summary_prints_marker_and_next_step(capsys):
    rc = main(["summary", "--comments", COMMENTS, "--reviews", REVIEWS, "--pr", "1"])
    out = capsys.readouterr().out

    assert rc == 0
    assert out.startswith("<!-- reviewkit-summary -->\n")
    assert "## Review summary for PR #1" in out
    assert "Blocked: 1 blocker comment(s) must be addressed by the author before merge." in out
    assert "I am not sure this handles a tile with zero faces." in out


def test_lint_comments_strict_fails_on_unlabeled(capsys):
    assert main(["lint-comments", "--comments", COMMENTS]) == 0
    assert main(["lint-comments", "--comments", COMMENTS, "--strict"]) == 1
    assert "### Unlabeled comments (1)" in capsys.readouterr().out


def test_size_fail_over(monkeypatch, capsys):
    monkeypatch.setattr(pr_size, "diff_stats", lambda base, head: DiffStats(20, 400, 100))

    assert main(["size", "--base", "main"]) == 0
    assert main(["size", "--base", "main", "--fail-over", "Extra Large"]) == 0
    assert main(["size", "--base", "main", "--fail-over", "Large"]) == 1
    assert "### PR size: Large" in capsys.readouterr().out
