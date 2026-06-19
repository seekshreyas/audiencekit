"""Lightweight summaries and charts for survey results."""

from __future__ import annotations

import base64
import html
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .survey import Study

ACCENT = "#0e7c86"   # teal, matches the deck palette
CLAY = "#b3592e"


def _as_study_dict(study: Study | dict) -> dict:
    return study.to_dict() if isinstance(study, Study) else study


def likert_ids(survey: Study | dict) -> list[str]:
    survey_dict = _as_study_dict(survey)
    return [q["id"] for q in survey_dict["questions"] if q["type"] == "likert"]


def text_ids(survey: Study | dict) -> list[str]:
    survey_dict = _as_study_dict(survey)
    return [q["id"] for q in survey_dict["questions"] if q["type"] == "text"]


def likert_summary(df: pd.DataFrame, survey: Study | dict) -> pd.DataFrame:
    """Mean and response distribution per likert question."""
    rows = []
    for qid in likert_ids(survey):
        if qid not in df.columns:
            rows.append({"question": qid, "n": 0, "mean": float("nan"),
                         **{f"pct_{k}": 0.0 for k in range(1, 6)}})
            continue
        valid = df[qid].dropna()
        counts = valid.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
        rows.append({"question": qid, "n": len(valid), "mean": valid.mean(),
                     **{f"pct_{k}": v / max(len(valid), 1) for k, v in counts.items()}})
    return pd.DataFrame(rows)


def plot_likert(df: pd.DataFrame, survey: Study | dict, title: str = "") -> plt.Figure:
    """One horizontal mean-score bar per likert question."""
    survey_dict = _as_study_dict(survey)
    summary = likert_summary(df, survey).sort_values("mean")
    fig, ax = plt.subplots(figsize=(8, 0.6 * len(summary) + 1.5))
    ax.barh(summary["question"], summary["mean"], color=ACCENT, alpha=0.85)
    ax.set_xlim(1, 5)
    ax.set_xlabel("Mean score (1-5)")
    ax.set_title(title or survey_dict.get("title", "Survey results"))
    for y, (_, row) in enumerate(summary.iterrows()):
        ax.text(row["mean"] + 0.05, y, f"{row['mean']:.2f}", va="center", fontsize=9)
    fig.tight_layout()
    return fig


def plot_treatment_comparison(
    results: dict[str, pd.DataFrame], survey: Study | dict, question: str, title: str = ""
) -> plt.Figure:
    """Mean score for one question across treatment arms."""
    names = list(results)
    means = [results[name][question].dropna().mean() for name in names]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(names, means, color=[CLAY, ACCENT][: len(names)] + [ACCENT] * 8, alpha=0.85)
    ax.set_ylim(1, 5)
    ax.set_ylabel(f"Mean {question} (1-5)")
    ax.set_title(title or f"{question} by framing")
    ax.bar_label(bars, fmt="%.2f")
    fig.tight_layout()
    return fig


def _fig_to_base64(fig: plt.Figure) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=140)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def write_html_report(
    path: str | Path,
    survey: Study | dict,
    df: pd.DataFrame,
    figures: list[plt.Figure],
    quotes: list[str] | None = None,
) -> Path:
    """Self-contained HTML report: summary table, charts, sample verbatims."""
    survey_dict = _as_study_dict(survey)
    title = html.escape(survey_dict.get("title", "Survey report"))
    summary = likert_summary(df, survey)
    imgs = "\n".join(
        f'<img src="data:image/png;base64,{_fig_to_base64(fig)}" style="max-width:100%;margin:16px 0;">'
        for fig in figures
    )
    quote_block = ""
    if quotes:
        items = "\n".join(f"<blockquote>{html.escape(q)}</blockquote>" for q in quotes)
        quote_block = f"<h2>In their own words</h2>{items}"
    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
 body {{ font-family: -apple-system, 'Helvetica Neue', sans-serif; max-width: 880px; margin: 40px auto; color: #1a1a1a; padding: 0 20px; }}
 h1 {{ border-bottom: 3px solid {ACCENT}; padding-bottom: 8px; }}
 table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
 th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: right; }}
 th:first-child, td:first-child {{ text-align: left; }}
 blockquote {{ border-left: 4px solid {CLAY}; margin: 12px 0; padding: 6px 14px; color: #444; font-style: italic; }}
 .meta {{ color: #666; font-size: 14px; }}
</style></head><body>
<h1>{title}</h1>
<p class="meta">Synthetic panel of {len(df)} GSS-grounded respondents · {int(df['valid'].sum())} valid responses</p>
<h2>Scores</h2>
{summary.round(2).to_html(index=False)}
{imgs}
{quote_block}
</body></html>"""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc)
    return out
