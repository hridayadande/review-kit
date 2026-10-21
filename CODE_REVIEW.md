# Code Review Process: Qualcomm Digital Twin Capstone

How our five-person team reviews code for the "Improved 3D Modeling in Digital Twin" pipeline
(textured 3D city meshes: segmentation, mesh refinement, evaluation). It follows the six questions
from Trisha Gee's _Better Code Reviews in 6 Simple Steps_ in order: **Why, When, Who, Where,
What, How**. Each section ends in a decision.

**Team.** Amr: segmentation and ML. Ayush: pipeline infrastructure and evaluation. Divyanshu: 3D
geometry and mesh processing. Himanshu: research infrastructure and ML. Hridaya: architecture and
integration (integration lead). Everyone works on a personal branch and merges into `main` through
a pull request. Sprints are two weeks.

## 1. Why we review

1. **Catch hard-coded dataset assumptions.** The sponsor wants a method that works across 3D model
   sources. Reviewers look for paths, tile ids, class lists, resolutions, coordinate conventions
   and texture layouts tied to one dataset.
2. **Keep five people's code consistent.** Naming, module boundaries and the data formats passed
   between stages should read like one codebase.
3. **Share knowledge across specialties.** ML people read geometry code and vice versa so no stage
   depends on one person.
4. **Not for style or running tests by eye.** Formatting, lint and tests run in CI. If a human is
   commenting on whitespace, the automation is missing a rule. Fix the rule, not the PR.

## 2. When

- Changes to a **stage interface** (inputs/outputs between segmentation, geometry, refinement,
  evaluation) get a short design conversation _before_ implementation: a Teams call or an issue
  comment with a sketch of the data format.
- Every change into `main` gets a **gateway review** on its PR before merge.
- **Research spikes** (experiments, notebooks, evaluation scripts) can be reviewed _after_ merge
  for knowledge sharing. Prefix the PR title with `[spike]`.

A review is complete when every `blocker:` is resolved and one code owner of the touched area has
approved. `nit:` and `question:` never block; a `question:` needs a reply, not necessarily a change.

**Turnaround.** First reviewer response within 24 hours on weekdays. The author replies to
comments within 24 hours. If you cannot review in time, say so in the PR so the author can ask
someone else.

## 3. Who

- **One required approval** from a code owner of the touched area (`.github/CODEOWNERS`):
  segmentation: Amr or Himanshu; geometry: Divyanshu; evaluation: Ayush; core, `.github/`,
  `reviewkit/` and anything unmatched: Hridaya.
- **Anyone may comment** on any PR with non-blocking comments.
- **Authors never approve their own PR.**
- **Deadlock rule.** If author and reviewer still disagree after one round, the integration lead
  (Hridaya) decides and writes the reasoning in the PR. If Hridaya is the author, the sprint's
  Scrum Master decides.

## 4. Where

- **Asynchronously on GitHub PRs.** The PR is the record; anything decided elsewhere gets
  summarised back into it.
- **Three-reply rule.** If a thread goes past 3 replies, move to a 10-minute call and post the
  outcome in the thread.
- **Pairing** counts as the review for stage-interface changes if the pair is named in the PR
  description. The partner still clicks Approve.

## 5. What reviewers look for

CI already checked format, lint and tests. Reviewers check:

1. Does the change do what the issue says, and do the **tests check that requirement**?
2. Does it **respect the stage interfaces**? If one changed, did the design conversation happen?
3. Is anything **dataset-specific hard-coded**?
4. Can a **teammate outside the specialty follow it**?
5. Are **performance-sensitive paths** (city-scale meshes, millions of faces) handled sensibly?
   No quadratic loops over faces, no loading a whole tile when one window will do.
6. Does the **PR description explain the trade-offs** so the reviewer evaluates the choice instead
   of reconstructing it?

## 6. How

**PR size.** `python -m reviewkit size --base origin/main` classifies a branch:

| Size        | Changed lines | Files |
| ----------- | ------------- | ----- |
| Small       | <= 100        | <= 5  |
| Medium      | <= 300        | <= 15 |
| Large       | <= 600        | any   |
| Extra Large | > 600         | any   |

Aim for Small or Medium. Large and Extra Large need a sentence in the description on why they
could not be split. CI reports the size but never blocks on it.

**Comment labels.** Every review comment starts with one of:

| Label         | Meaning                                                | Blocks merge? |
| ------------- | ------------------------------------------------------ | ------------- |
| `blocker:`    | Must change before merge.                              | Yes           |
| `question:`   | Reviewer needs to understand something. Needs a reply. | No            |
| `suggestion:` | Non-blocking improvement.                              | No            |
| `nit:`        | Style or personal preference.                          | No            |
| `praise:`     | Something done well.                                   | No            |

Leave at least one `praise:` when something is genuinely good. Comments are about the code, not
the author, and specific: "this loop re-reads the tile for every window", not "this is slow". The
review-summary workflow tallies labels and lists comments without one.

**Verdicts.** Submit **Approve** when there are no blockers, or **Approve with concerns** (a
Comment-type review listing the blockers) when the fix is clear and small. Use GitHub's "Request
changes" only when a `blocker:` needs a second look after the fix, and never without at least one
`blocker:` comment. A rejection that does not say what must change is not a review.

**Closing the loop.** The author resolves the threads they addressed and replies to every
`question:`. The approver squash-merges once the last blocker is resolved. After every review the
next step is one of: merge, change, or someone else decides (deadlock rule). The summary comment
on the PR says which.

## Author checklist

- [ ] `ruff format --check .`, `ruff check .` and `pytest -q` pass locally.
- [ ] `reviewkit size` says Small or Medium, or the description says why not.
- [ ] Description covers what and why, how to verify, and trade-offs.
- [ ] Anything unusual in the diff has a self-comment.
- [ ] Tests check the requirement from the issue.
- [ ] Nothing dataset-specific is hard-coded.
- [ ] Stage-interface changes had their design conversation first (linked).
- [ ] After review: every `question:` answered, every `blocker:` fixed, threads resolved.

## Reviewer checklist

- [ ] Responded within 24 hours (or said I could not).
- [ ] Did not comment on anything CI already checks.
- [ ] Every comment starts with `blocker:`, `question:`, `suggestion:`, `nit:` or `praise:`.
- [ ] Every comment is about the code and says what and why.
- [ ] Left a `praise:` where something was good.
- [ ] Verdict is Approve or Approve with concerns; if I requested changes, there is a `blocker:`.
- [ ] The next step is obvious to the author from my review alone.
