# review-kit

Code review process for the Qualcomm "Improved 3D Modeling in Digital Twin" capstone team at
ASU. It takes the six questions from Trisha Gee's _Better Code Reviews in 6 Simple Steps_ (Why,
When, Who, Where, What, How) and turns them into a written process ([CODE_REVIEW.md](CODE_REVIEW.md)),
GitHub templates and workflows, and a small standard-library CLI, `reviewkit`, that measures PR
size and tallies review comments by label.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest -q
ruff check . && ruff format --check .

reviewkit size --base main
reviewkit size --base main --fail-over Large
reviewkit lint-comments --comments examples/sample_comments.json --strict
reviewkit summary --comments examples/sample_comments.json \
    --reviews examples/sample_reviews.json --pr 1
```

## What is where

- `CODE_REVIEW.md`: the team process and the author / reviewer checklists.
- `.github/PULL_REQUEST_TEMPLATE.md`: what, why, how to verify, trade-offs, self-review.
- `.github/CODEOWNERS`: who approves each pipeline area.
- `.github/workflows/ci.yml`: format, lint, tests, PR size in the job summary.
- `.github/workflows/review-summary.yml`: one comment per PR with label counts and the next step.
- `reviewkit/`: the CLI (`size`, `lint-comments`, `summary`).
- `examples/`: fixtures shaped like the GitHub API output.
- `tests/`: pytest suite.

## Principle to implementation

| Principle from the video                                                            | Where it lives                                                                                                                  |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Decide Why first, then When, Who, Where, What, How                                  | `CODE_REVIEW.md` is in that order, each section ends in a decision                                                              |
| Humans should not do what can be automated                                          | `ci.yml` runs ruff and pytest; `CODE_REVIEW.md` sections 1 and 5 limit humans to what CI cannot check                           |
| Keep reviews small                                                                  | `reviewkit size`, thresholds in `reviewkit/pr_size.py`, reported by `ci.yml`, limits in `CODE_REVIEW.md` section 6              |
| Authors annotate, describe trade-offs, self-check                                   | PR template; author checklist in `CODE_REVIEW.md`                                                                               |
| Respond in a timely fashion                                                         | 24-hour turnaround in `CODE_REVIEW.md` section 2                                                                                |
| Constructive, specific, prioritised comments; leave praise                          | labels in `reviewkit/labels.py`; `lint-comments` finds unlabeled ones; the summary counts praise                                |
| Prefer accept or accept with concerns; never reject without saying what must change | `next_step()` in `reviewkit/comment_lint.py` flags Request changes with no blocker; verdict rules in `CODE_REVIEW.md` section 6 |

## Known limitation

The GitHub REST API does not say whether a review thread is resolved, so `reviewkit summary`
counts every `blocker:` as open. Use it as a checklist; the code owner approval is the merge gate.

## Using it in another repo

1. Copy `.github/` and `reviewkit/`. Copy the `[tool.ruff]` and `[tool.pytest.ini_options]`
   sections of `pyproject.toml` if you want the same CI rules.
2. Replace the `@<name>` placeholders in `.github/CODEOWNERS` with real usernames and your paths.
3. Change the thresholds at the top of `reviewkit/pr_size.py` if your norm differs.
4. Keep `CODE_REVIEW.md` as is or change the decisions. The order (Why first, How last) is the
   part worth keeping.
