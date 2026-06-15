---
name: persona-browse
description: Have one synthetic audience member browse a website and narrate a first-person stream of consciousness. Use for synthetic UX walkthroughs, landing-page reactions, checkout friction, product discovery, and qualitative website testing.
---

# Persona Browse

Run a short qualitative website walkthrough from one sampled persona's point of view.

## Inputs

- URL to browse.
- Audience frame or persona constraints.
- Optional task, e.g. "find pricing", "evaluate the product", or "decide whether to sign up".

If no persona is specified, sample one respondent from the available frame with a fresh seed.

## Cast The Persona

Use AudienceKit to sample and render the persona:

```python
import audiencekit as ak

pool = ak.load_panel()
row = ak.sample_panel(pool, n=1, seed=13).iloc[0].to_dict()
print(ak.build_persona(row))
```

For non-GSS data, use `ak.AudienceFrame` plus `ak.PersonaTemplate`.

Show the persona card before browsing. Keep the attributes in working memory and let them shape attention, skepticism, budget sensitivity, and vocabulary.

## Browse

Use the configured browser automation tool for navigation. Make 4-6 moves maximum:

- On each page, inspect the visible content before acting.
- Narrate what the persona notices first.
- Choose one plausible next action.
- Let the persona leave if the page would lose them.

When using `agent-browser`, start headed mode explicitly on the first call:

```bash
agent-browser --headed open <url>
```

Put `--headed` before the subcommand. Do not rely on a local `agent-browser.json` file being read from the current directory.

## Narration Format

After every page interaction, print:

```text
Page/action: <where the persona is>
Inner voice: "<2-4 first-person sentences, grounded in the persona and concrete page details>"
Next action: <one action or leave>
```

Voice rules:

- First person, direct, and colloquial.
- Match reading level and category familiarity to the persona.
- React to concrete page elements, not generic UX theory.
- Preserve boredom, confusion, sticker shock, and distrust when they appear.

## Debrief

End with:

- Overall impression in the persona's voice.
- One thing that helped.
- One thing that lost them.
- Whether they would return or convert.
- One researcher sentence with the most actionable UX insight.
