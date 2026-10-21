from reviewkit import MARKER, load, next_step, parse_label, summarize


def test_parse_label():
    assert parse_label("nit: rename this") == "nit"
    assert parse_label("**Blocker:** hard-coded path") == "blocker"
    assert parse_label("looks fine to me") is None


def test_summary_on_examples():
    out = summarize(load("examples/comments.json"), load("examples/reviews.json"), 1)
    assert out.startswith(MARKER)
    assert "| `blocker:` | 1 |" in out
    assert "Blocked: 1 blocker" in out
    assert "@divyanshu" in out and "Unlabeled comments" in out
    assert "1 praise comment" in out


def test_next_step():
    none = dict.fromkeys(["blocker", "question", "nit", "praise"], 0)
    assert next_step(none, [{"state": "APPROVED"}]).startswith("Ready to merge")
    assert next_step(none, [{"state": "CHANGES_REQUESTED"}]).startswith("Changes requested")
    assert next_step(none, []).startswith("Awaiting approval")
