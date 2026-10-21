import subprocess

import pytest

from reviewkit.pr_size import (
    EXTRA_LARGE,
    LARGE,
    MEDIUM,
    SMALL,
    DiffStats,
    classify,
    diff_stats,
    parse_numstat,
    render_markdown,
)

# diagram.png is binary so git prints "-"
NUMSTAT = "10\t2\tpipeline/core/stage.py\n-\t-\tdocs/diagram.png\n0\t5\tREADME.md\n"


def test_diff_stats_runs_git_and_parses_numstat(monkeypatch):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout=NUMSTAT, stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    stats = diff_stats("origin/main", "feature")

    assert calls == [["git", "diff", "--numstat", "origin/main...feature"]]
    assert stats == DiffStats(files_changed=3, insertions=10, deletions=7)
    assert stats.total == 17


def test_parse_numstat_ignores_blank_and_malformed_lines():
    assert parse_numstat("\nnot a numstat line\n3\t1\tx.py\n") == DiffStats(1, 3, 1)


@pytest.mark.parametrize(
    ("lines", "files", "expected"),
    [
        (100, 5, SMALL),
        (101, 5, MEDIUM),
        (100, 6, MEDIUM),
        (300, 15, MEDIUM),
        (301, 15, LARGE),
        (300, 16, LARGE),
        (600, 40, LARGE),
        (601, 1, EXTRA_LARGE),
    ],
)
def test_classify_boundaries(lines, files, expected):
    assert classify(DiffStats(files_changed=files, insertions=lines, deletions=0)) == expected


def test_render_markdown_recommends_splitting_large_prs():
    stats = DiffStats(files_changed=20, insertions=400, deletions=100)
    markdown = render_markdown(stats, classify(stats))
    assert "### PR size: Large" in markdown
    assert "| 20 | 400 | 100 | 500 |" in markdown
    assert "Consider splitting this PR" in markdown
