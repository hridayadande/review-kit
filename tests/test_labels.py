import pytest

from reviewkit.labels import LABELS, parse_label


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("nit: prefer a comprehension here", "nit"),
        ("**blocker:** this path is hard-coded", "blocker"),
        ("**nit**: trailing whitespace", "nit"),
        ("Question: why is this cached?", "question"),
        ("  suggestion: extract a helper", "suggestion"),
        ("🔴 blocker: tests do not cover the requirement", "blocker"),
        ("👏 praise: nice clear naming", "praise"),
        ("- nit: list marker in front", "nit"),
        ("Looks good to me", None),
        ("This is a nit: but not at the start", None),
        ("blocker without a colon", None),
        ("", None),
    ],
)
def test_parse_label(body, expected):
    assert parse_label(body) == expected


def test_only_blocker_blocks_merge():
    assert [label.name for label in LABELS if label.blocks] == ["blocker"]
