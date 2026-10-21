# Code Review Process

For the Qualcomm Digital Twin capstone team: five people, personal branches, everything merges
into `main` through a pull request. Decided by answering six questions in order.

## 1. Why do we review?

- To catch anything hard-coded to one dataset. The sponsor needs the method to work across 3D
  sources, so a path, class list or resolution tied to one tile is a blocker.
- To keep five people's code consistent where pipeline stages meet (names, data formats).
- To share knowledge: ML people read geometry code and vice versa.
- Not for style or test results. CI does that; fix the rule, not the PR.

## 2. When?

- Design chat (Teams call or issue comment) before touching a stage interface.
- Gateway review on the PR before every merge to `main`.
- Research spikes marked `[spike]` can be reviewed after merge.
- A review is done when every `blocker:` is resolved and one code owner has approved.
- First response within 24 hours on weekdays, both directions.

## 3. Who?

- One approval from a CODEOWNER of the touched area. Anyone may comment.
- Nobody approves their own PR.
- Deadlock after one round: the integration lead (Hridaya) decides and writes the reasoning in the
  PR. If Hridaya is the author, the sprint's Scrum Master decides.

## 4. Where?

- The GitHub PR is the record.
- A thread longer than three replies moves to a 10-minute call; the outcome goes back in the PR.
- Pairing counts as a review when the pair is named in the PR description.

## 5. What do reviewers look for?

- Does it do what the issue says, and do the tests check that requirement?
- Are stage interfaces and data formats respected?
- Is anything dataset-specific hard-coded?
- Could a teammate outside the specialty read it?
- Does the PR description explain the trade-offs?

## 6. How?

- Keep PRs under about 300 changed lines, or explain why not.
- Start every comment with a label:

| Label       | Meaning                               | Blocks merge |
| ----------- | ------------------------------------- | ------------ |
| `blocker:`  | Must change before merge              | yes          |
| `question:` | Reviewer needs an answer              | no           |
| `nit:`      | Preference, optional                  | no           |
| `praise:`   | Something done well, say what and why | no           |

- Verdict is Approve, or Approve with concerns listing the blockers. Never Request changes without
  at least one `blocker:` comment.
- The author resolves the threads they addressed and answers every `question:`.
- The approver squash-merges as soon as the last blocker is resolved.
- The review-summary workflow posts the label counts and the next step on every review.

## Author checklist

- [ ] Format, lint and tests pass locally
- [ ] Under ~300 lines, or explained
- [ ] Description says what, why and the trade-offs
- [ ] Nothing dataset-specific is hard-coded

## Reviewer checklist

- [ ] Every comment has a label and is about the code, not the author
- [ ] At least one `praise:` if something was done well
- [ ] Every `blocker:` says what must change
- [ ] Responded within 24 hours
