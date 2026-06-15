"""Analyze a Ferrari Luce example study run.

Produces:
    examples/ferrari_luce/results/report.html        self-contained study report
    examples/ferrari_luce/results/summary.txt        headline numbers
    examples/ferrari_luce/results/luce_scores.png    mean scores by segment & framing
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audiencekit.report import ACCENT, CLAY, plot_likert, write_html_report

EXAMPLE = Path("examples/ferrari_luce")
RESULTS = EXAMPLE / "results"
LIKERT = ["brand_fit", "emotional_pull", "ritual_loss", "status_signal"]
CELLS = [("broad", "neutral"), ("broad", "heritage"), ("luxury", "neutral"), ("luxury", "heritage")]


def main() -> None:
    survey = json.loads((EXAMPLE / "study.json").read_text())
    cells = {
        (seg, treat): pd.read_csv(RESULTS / f"{seg}_{treat}_responses.csv")
        for seg, treat in CELLS
    }
    df = pd.concat(cells.values())

    lines = [f"Total responses: {len(df)} ({int(df['valid'].sum())} valid, "
             f"{100 * df['valid'].mean():.1f}%)", ""]
    means = df.groupby(["segment", "treatment"])[LIKERT].mean().round(2)
    lines += ["Mean scores by cell:", means.to_string(), ""]

    for seg in ["broad", "luxury"]:
        verdict = (
            df[df.segment == seg]["ferrari_feel_verdict"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
        )
        lines.append(f"{seg} verdict shares (%): {verdict.to_dict()}")
    lines.append("")

    # Luce identity index = mean of the three "is this a Ferrari" dimensions
    # (ritual_loss excluded: it scores the *pain*, not the fit).
    index_cols = ["brand_fit", "emotional_pull", "status_signal"]
    for seg in ["broad", "luxury"]:
        neutral = cells[(seg, "neutral")][index_cols].mean().mean()
        heritage = cells[(seg, "heritage")][index_cols].mean().mean()
        lines.append(
            f"{seg} Luce index — neutral {neutral:.2f}, heritage {heritage:.2f}, "
            f"framing effect {heritage - neutral:+.2f}"
        )
    summary = "\n".join(lines)
    (RESULTS / "summary.txt").write_text(summary)
    print(summary)

    # chart: grouped bars, one group per likert question
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    width = 0.2
    x = range(len(LIKERT))
    styles = [
        (("broad", "neutral"), CLAY, 0.45, "Broad · neutral"),
        (("broad", "heritage"), CLAY, 0.9, "Broad · heritage"),
        (("luxury", "neutral"), ACCENT, 0.45, "Affluent · neutral"),
        (("luxury", "heritage"), ACCENT, 0.9, "Affluent · heritage"),
    ]
    for k, (cell, color, alpha, label) in enumerate(styles):
        vals = [cells[cell][q].mean() for q in LIKERT]
        ax.bar([xi + (k - 1.5) * width for xi in x], vals, width=width * 0.92,
               color=color, alpha=alpha, label=label)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["Brand fit", "Emotional pull", "Ritual loss\n(pain score)", "Status signal"])
    ax.set_ylim(1, 5)
    ax.set_ylabel("Mean score (1–5)")
    ax.set_title("Ferrari Luce — 600 AudienceKit respondents, by segment and framing")
    ax.legend(fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(RESULTS / "luce_scores.png", dpi=160)

    quotes = (
        pd.concat([c["best_argument_against"] for c in cells.values()])
        .dropna()
        .sample(6, random_state=3)
        .tolist()
    )
    write_html_report(RESULTS / "report.html", survey, df,
                      [plot_likert(df, survey, "All cells pooled")], quotes)
    print(f"\nWrote {RESULTS}/report.html, luce_scores.png, summary.txt")


if __name__ == "__main__":
    main()
