# review-kit

A code review process for my capstone team, plus a small script that summarizes a pull
request's review comments by label and tells the author what happens next.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install pytest "ruff==0.17.1"
.venv/bin/pytest -q
.venv/bin/python reviewkit.py examples/comments.json examples/reviews.json --pr 1
```

## Files

- `CODE_REVIEW.md` - the team process: why, when, who, where, what, how
- `reviewkit.py` - counts `blocker:` / `question:` / `nit:` / `praise:` comments, lists unlabeled ones, prints the next step
- `test_reviewkit.py` - tests
- `examples/` - review comments and reviews in the GitHub API shape
- `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS` - author checklist and who approves what
- `.github/workflows/ci.yml` - format, lint, tests
- `.github/workflows/review-summary.yml` - runs `reviewkit.py` when a review is submitted and posts the summary on the PR

## Notes

The REST API does not say whether a thread is resolved, so a fixed blocker still counts until a
human approves. To get real data for a PR:
`gh api repos/OWNER/REPO/pulls/N/comments > comments.json` and `.../pulls/N/reviews > reviews.json`.
