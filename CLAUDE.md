# AudienceKit

AudienceKit is a Python library for synthetic audience research grounded in
real respondent rows. GSS is the first supported adapter, but core behavior
must stay dataset-agnostic:

- `AudienceFrame` handles weighted respondent sampling for any DataFrame.
- `PersonaTemplate` renders row attributes into persona prompts.
- `Study` defines structured survey instruments.
- `SyntheticPanel` runs studies against an injectable model backend.
- `audiencekit.gss` prepares full GSS files into an AudienceKit frame.

Run commands through `uv run`. Use `uv run --extra dev python -m pytest tests`
for the test suite.

Open-source hygiene:

- Keep generated outputs under `results/` or `examples/*/results/`; do not
  commit fresh run artifacts.
- Keep top-level `skills/` as the canonical agent skill source.
- Frame synthetic audience findings as directional pressure tests, not
  substitutes for fieldwork.
- Do not hard-code GSS assumptions into generic primitives; add new datasets
  as adapters beside `audiencekit.gss`.
