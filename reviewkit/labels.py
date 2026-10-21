from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    name: str
    description: str
    blocks: bool


BLOCKER = Label("blocker", "Must change before merge.", blocks=True)
QUESTION = Label(
    "question",
    "Reviewer needs to understand something; needs a reply, not necessarily a change.",
    blocks=False,
)
SUGGESTION = Label("suggestion", "Non-blocking improvement.", blocks=False)
NIT = Label("nit", "Style or personal preference; take it or leave it.", blocks=False)
PRAISE = Label("praise", "Something done well. Say so; it reinforces good habits.", blocks=False)

LABELS: tuple[Label, ...] = (BLOCKER, QUESTION, SUGGESTION, NIT, PRAISE)
LABEL_NAMES: tuple[str, ...] = tuple(label.name for label in LABELS)

# allows a leading emoji or "- " and markdown bold around the label
_LABEL_RE = re.compile(
    r"^\s*(?:[^\w\s*_]+\s*)?[*_]{0,2}(" + "|".join(LABEL_NAMES) + r")[*_]{0,2}:",
    re.IGNORECASE,
)


def parse_label(body: str) -> str | None:
    match = _LABEL_RE.match(body)
    return match.group(1).lower() if match else None
