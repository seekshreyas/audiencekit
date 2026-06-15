from __future__ import annotations

import pandas as pd

from audiencekit import AudienceFrame, PersonaTemplate


def test_audience_frame_samples_any_weighted_dataset() -> None:
    data = pd.DataFrame(
        {
            "person_id": ["a", "b", "c"],
            "survey_weight": [0, 0, 5],
            "age": [25, 35, 45],
            "cohort": ["student", "parent", "parent"],
        }
    )

    frame = AudienceFrame(data, id_column="person_id", weight_column="survey_weight")
    sampled = frame.sample(n=2, segment=lambda row: row["cohort"] == "parent", segment_name="parents", seed=3)

    assert sampled["person_id"].tolist() == ["c", "c"]
    assert sampled["segment"].tolist() == ["parents", "parents"]


def test_persona_template_renders_missing_fields_as_unknown() -> None:
    template = PersonaTemplate("You are {age}, live in {region}, and buy {category}.")

    assert template.render({"age": 35, "category": "coffee"}) == (
        "You are 35, live in Unknown, and buy coffee."
    )
