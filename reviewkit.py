import argparse
import json
import re
import sys

# label -> blocks merge
LABELS = {"blocker": True, "question": False, "nit": False, "praise": False}
MARKER = "<!-- reviewkit-summary -->"
LABEL_RE = re.compile(r"^\W*(blocker|question|nit|praise)\W*:", re.IGNORECASE)


def parse_label(body):
    match = LABEL_RE.match(body or "")
    return match.group(1).lower() if match else None


def load(path):
    with open(path) as f:
        return json.load(f)


def next_step(counts, reviews):
    states = {r.get("state") for r in reviews}
    if counts["blocker"]:
        return f"Blocked: {counts['blocker']} blocker comment(s) must be addressed before merge."
    if "CHANGES_REQUESTED" in states:
        return "Changes requested without a blocker: add a blocker: comment or approve."
    if "APPROVED" in states:
        return "Ready to merge: approved with no blockers."
    return "Awaiting approval: no blockers found."


def summarize(comments, reviews, pr):
    counts = dict.fromkeys(LABELS, 0)
    unlabeled = []
    for c in comments:
        label = parse_label(c.get("body"))
        if label:
            counts[label] += 1
        else:
            line = c.get("line") or c.get("original_line") or "?"
            text = " ".join(c.get("body", "").split())[:80]
            unlabeled.append(f"- @{c['user']['login']} `{c.get('path')}:{line}` — {text}")

    out = [MARKER, f"## Review summary for PR #{pr}", "", "| Label | Count |", "|---|---:|"]
    out += [f"| `{label}:` | {n} |" for label, n in counts.items()]
    out += ["", f"**Next step:** {next_step(counts, reviews)}"]
    if unlabeled:
        out += ["", "### Unlabeled comments"]
        out += unlabeled
        out.append("Start each comment with `blocker:`, `question:`, `nit:` or `praise:`.")
    if counts["praise"]:
        out += ["", f"Nice: {counts['praise']} praise comment(s). Positive feedback matters."]
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize PR review comments by label.")
    parser.add_argument("comments")
    parser.add_argument("reviews")
    parser.add_argument("--pr", type=int, default=0)
    args = parser.parse_args(argv)
    print(summarize(load(args.comments), load(args.reviews), args.pr), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
