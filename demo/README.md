# Demo: practise reviewing

`mesh_stats.py` counts vertices and faces in an OBJ string and returns the bounding box. It passes
`ruff` and `pytest`, so CI is green, but it still deserves review comments. That is the exercise.

This folder lives on the `demo/mesh-stats` branch only, which also adds `"demo"` to `testpaths`
in `pyproject.toml`.

```bash
git push -u origin main
git push -u origin demo/mesh-stats
gh pr create --base main --head demo/mesh-stats
```

Reviewers leave inline comments starting with `blocker:`, `question:`, `suggestion:`, `nit:` or
`praise:`. The review-summary workflow posts the tally and the next step. There are at least four
things worth a comment and at least one worth a `praise:`. Do your own pass before comparing notes.
