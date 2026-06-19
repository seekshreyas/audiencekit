from __future__ import annotations

import pandas as pd

from audiencekit import Study
from audiencekit.report import likert_summary, write_html_report


def test_likert_summary_handles_missing_question_columns() -> None:
    study = Study.from_dict(
        {
            "title": "Concept test",
            "questions": [{"id": "fit", "type": "likert", "text": "Fit?"}],
        }
    )
    df = pd.DataFrame({"valid": [False]})

    summary = likert_summary(df, study)

    assert summary.loc[0, "n"] == 0
    assert pd.isna(summary.loc[0, "mean"])


def test_likert_summary_counts_valid_scores() -> None:
    study = Study.from_dict(
        {
            "title": "Concept test",
            "questions": [{"id": "fit", "type": "likert", "text": "Fit?"}],
        }
    )
    df = pd.DataFrame({"fit": [1, 3, 5, None], "valid": [True, True, True, False]})

    summary = likert_summary(df, study)

    assert summary.loc[0, "n"] == 3
    assert summary.loc[0, "mean"] == 3
    assert summary.loc[0, "pct_1"] == 1 / 3


def test_write_html_report_escapes_model_text(tmp_path) -> None:
    study = Study.from_dict(
        {
            "title": "Unsafe <study>",
            "questions": [{"id": "fit", "type": "likert", "text": "Fit?"}],
        }
    )
    df = pd.DataFrame({"fit": [4], "valid": [True]})

    out = write_html_report(tmp_path / "report.html", study, df, figures=[], quotes=["<script>alert(1)</script>"])

    html = out.read_text()
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<title>Unsafe &lt;study&gt;</title>" in html
