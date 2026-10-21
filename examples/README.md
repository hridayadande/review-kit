# Example fixtures

`sample_comments.json` and `sample_reviews.json` look like the GitHub REST API output the
review-summary workflow feeds into `reviewkit summary`. Seven comments (one has no label),
one COMMENTED review and one CHANGES_REQUESTED review.

```bash
python -m reviewkit lint-comments --comments examples/sample_comments.json
python -m reviewkit summary --comments examples/sample_comments.json \
    --reviews examples/sample_reviews.json --pr 1
```

To pull fresh ones from a real PR (needs `gh auth login`):

```bash
gh api --paginate "repos/OWNER/REPO/pulls/42/comments" --jq '.[]' | jq -s '.' \
    > examples/sample_comments.json
gh api --paginate "repos/OWNER/REPO/pulls/42/reviews" --jq '.[]' | jq -s '.' \
    > examples/sample_reviews.json
```

Only `user.login`, `body`, `path`, `line` / `original_line` and `state` are read, the rest can
be trimmed by hand.
