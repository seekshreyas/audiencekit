# Ferrari Luce Example

This example is the public case-study shape for AudienceKit.

It tests a fictional Ferrari Luce electric GT concept with:

- a fixed product stimulus,
- alternate treatment descriptions,
- a weighted synthetic audience frame,
- structured Likert, choice, and verbatim questions,
- report generation through `audiencekit.report`.

Run a small live smoke test:

```bash
uv run python scripts/run_survey.py \
  --spec examples/ferrari_luce/study.json \
  --n 25 \
  --segment broad \
  --treatment neutral \
  --out examples/ferrari_luce/results
```

Generated CSVs, charts, and reports should stay under
`examples/ferrari_luce/results/` and are ignored by git.

Add the production narrative case-study URL here once the post is live.
