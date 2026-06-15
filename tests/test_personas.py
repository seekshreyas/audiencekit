from __future__ import annotations

import pandas as pd
import pytest

from audiencekit import build_persona, load_panel, sample_panel
from audiencekit.gss import prepare_gss_persona_frame


def test_sample_panel_accepts_callable_segment_and_uses_weights() -> None:
    df = pd.DataFrame(
        {
            "id": ["a", "b", "c"],
            "weight": [0.0, 0.0, 10.0],
            "income16": ["Under $1,000", "$170,000 or over", "$170,000 or over"],
            "class": ["Working Class", "Middle Class", "Upper Class"],
            "degree": ["High school", "Bachelor's", "Graduate"],
            "prestg10": ["Low", "High", "High"],
            "finrela": ["Average", "Above average", "Far above average"],
        }
    )

    sampled = sample_panel(
        df,
        n=3,
        segment=lambda row: row["income16"] == "$170,000 or over",
        seed=7,
        weighted=True,
        segment_name="affluent",
    )

    assert sampled["id"].tolist() == ["c", "c", "c"]
    assert sampled["segment"].tolist() == ["affluent", "affluent", "affluent"]


def test_load_panel_defaults_to_packaged_sample_panel() -> None:
    panel = load_panel()

    assert {"id", "weight", "age", "sex"}.issubset(panel.columns)
    assert len(panel) > 1000


def test_weighted_sampling_requires_positive_weight_column() -> None:
    df = pd.DataFrame({"id": ["a"], "weight": [0]})

    with pytest.raises(ValueError, match="positive"):
        sample_panel(df, n=1, weighted=True)


def test_prepare_gss_persona_frame_filters_years_and_maps_values() -> None:
    raw = pd.DataFrame(
        {
            "id": [101, 102],
            "year": [2022, 2024],
            "wtssnrps": [1.2, 2.3],
            "age": [35, 44],
            "sex": [1, 2],
            "race": [1, 2],
            "region": [1, 9],
            "res16": [3, 5],
            "marital": [1, 5],
            "educ": [16, 14],
            "degree": [3, 1],
            "income16": [26, -99],
            "class": [3, 2],
            "occ10": [10, 4700],
            "prestg10": [70, 40],
            "finrela": [4, 3],
            "satfin": [1, 2],
            "partyid": [3, 0],
            "polviews": [4, 2],
            "relig": [4, 1],
            "attend": [0, 8],
            "childs": [0, 2],
            "happy": [2, 1],
            "health": [2, 1],
            "tvhours": [1, 3],
            "usewww": [1, 2],
            "getahead": [1, 2],
        }
    )

    panel = prepare_gss_persona_frame(raw, years=[2024])

    assert panel["id"].tolist() == ["2024-102"]
    assert panel["weight"].tolist() == [2.3]
    assert panel.loc[0, "sex"] == "Female"
    assert panel.loc[0, "race"] == "Black"
    assert panel.loc[0, "income16"] is None


def test_build_persona_renders_unknown_for_missing_values() -> None:
    persona = build_persona({"age": 44, "sex": "Female", "race": None})

    assert "44 year old Female Unknown adult" in persona
    assert "household income is Unknown" in persona
