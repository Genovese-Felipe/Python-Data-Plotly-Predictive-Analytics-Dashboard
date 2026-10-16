"""Shared Plotly figure builders for the live and static dashboards."""

from __future__ import annotations

import pandas as pd
import plotly.express as px

COLORS = {
    "Low": "#16a34a",
    "Medium": "#f59e0b",
    "High": "#dc2626",
}


def build_figures(frame: pd.DataFrame) -> dict[str, object]:
    """Build a consistent set of analytics figures."""
    status = px.pie(
        frame,
        names="status",
        hole=0.48,
        title="Project status",
    )
    status.update_traces(textposition="inside", textinfo="percent+label")

    delay_by_type = (
        frame.groupby("project_type", as_index=False)["predicted_delay_days"]
        .mean()
        .sort_values("predicted_delay_days")
    )
    delay = px.bar(
        delay_by_type,
        x="predicted_delay_days",
        y="project_type",
        orientation="h",
        title="Average predicted delay by project type",
        labels={"predicted_delay_days": "Predicted delay (days)", "project_type": "Type"},
    )
    delay.update_traces(marker_color="#2563eb")

    budget = px.scatter(
        frame,
        x="budget",
        y="predicted_delay_days",
        color="predicted_risk",
        size="complexity_score",
        hover_name="project_name",
        color_discrete_map=COLORS,
        title="Budget, complexity and schedule risk",
        labels={
            "budget": "Budget",
            "predicted_delay_days": "Predicted delay (days)",
            "predicted_risk": "Risk",
        },
    )

    progress = px.histogram(
        frame,
        x="completion_pct",
        color="predicted_risk",
        nbins=12,
        barmode="overlay",
        color_discrete_map=COLORS,
        title="Completion distribution by predicted risk",
        labels={"completion_pct": "Completion (%)", "predicted_risk": "Risk"},
    )

    for figure in (status, delay, budget, progress):
        figure.update_layout(
            template="plotly_white",
            margin=dict(l=28, r=28, t=64, b=32),
            legend_title_text="",
        )
    return {"status": status, "delay": delay, "budget": budget, "progress": progress}
