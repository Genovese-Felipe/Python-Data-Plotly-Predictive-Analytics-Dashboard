"""Canonical interactive Dash application."""

from __future__ import annotations

from pathlib import Path

from dash import Dash, Input, Output, dcc, html

from .data import load_dataset
from .figures import build_figures
from .predictive import train_delay_model

PAGE_STYLE = {
    "fontFamily": "Inter, system-ui, sans-serif",
    "background": "#f4f7fb",
    "color": "#172033",
    "minHeight": "100vh",
    "padding": "24px",
}
CARD_STYLE = {
    "background": "white",
    "border": "1px solid #e5eaf2",
    "borderRadius": "14px",
    "boxShadow": "0 8px 24px rgba(35, 55, 80, 0.08)",
    "padding": "18px",
}


def _metric_card(label: str, value: str, note: str = "") -> html.Div:
    return html.Div(
        [
            html.P(label, style={"margin": 0, "color": "#607089", "fontSize": "0.82rem"}),
            html.H3(value, style={"margin": "6px 0 3px"}),
            html.Small(note, style={"color": "#7b8798"}),
        ],
        style=CARD_STYLE,
    )


def _project_table(frame):
    columns = [
        ("Project", "project_name"),
        ("Type", "project_type"),
        ("Status", "status"),
        ("Completion %", "completion_pct"),
        ("Predicted delay", "predicted_delay_days"),
        ("Risk", "predicted_risk"),
    ]
    header = html.Tr([html.Th(label) for label, _ in columns])
    rows = [
        html.Tr([html.Td(row[key]) for _, key in columns]) for _, row in frame.head(20).iterrows()
    ]
    return html.Table(
        [html.Thead(header), html.Tbody(rows)],
        style={"width": "100%", "borderCollapse": "collapse"},
    )


def create_app(csv_path: str | Path | None = None) -> Dash:
    """Create an application using a validated CSV or synthetic fallback data."""
    dataset = load_dataset(csv_path)
    prediction = train_delay_model(dataset.projects)
    projects = prediction.projects

    app = Dash(__name__)
    app.title = "Construction Analytics Dashboard"
    source_badge = "Synthetic demo" if dataset.is_synthetic else dataset.source_label
    app.layout = html.Div(
        [
            html.Header(
                [
                    html.Div(
                        [
                            html.H1("Construction Analytics", style={"margin": 0}),
                            html.P(
                                "Portfolio monitoring with a reproducible schedule-delay model.",
                                style={"margin": "8px 0 0", "color": "#64748b"},
                            ),
                        ]
                    ),
                    html.Span(
                        source_badge,
                        style={
                            "background": "#dbeafe",
                            "color": "#1d4ed8",
                            "borderRadius": "999px",
                            "padding": "8px 12px",
                            "fontWeight": 700,
                        },
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-between", "gap": "20px"},
            ),
            html.Div(
                [
                    _metric_card("Projects", f"{len(projects):,}", dataset.source_label),
                    _metric_card(
                        "Portfolio budget", f"${projects['budget'].sum() / 1_000_000:.1f}M"
                    ),
                    _metric_card("Model MAE", f"{prediction.mae_days:.1f} days", "Holdout set"),
                    _metric_card(
                        "Model R²", f"{prediction.r2:.2f}", f"{prediction.test_rows} test rows"
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                    "gap": "14px",
                    "margin": "24px 0",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Project type"),
                            dcc.Dropdown(
                                id="type-filter",
                                options=sorted(projects["project_type"].unique()),
                                value=sorted(projects["project_type"].unique()),
                                multi=True,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Predicted risk"),
                            dcc.Dropdown(
                                id="risk-filter",
                                options=["Low", "Medium", "High"],
                                value=["Low", "Medium", "High"],
                                multi=True,
                            ),
                        ]
                    ),
                ],
                style={
                    **CARD_STYLE,
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "18px",
                },
            ),
            html.Div(
                [
                    dcc.Graph(id="status-chart"),
                    dcc.Graph(id="delay-chart"),
                    dcc.Graph(id="budget-chart"),
                    dcc.Graph(id="progress-chart"),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                    "gap": "16px",
                    "marginTop": "18px",
                },
            ),
            html.Div(
                [
                    html.H3("Projects requiring attention"),
                    html.Div(id="project-table", style={"overflowX": "auto"}),
                ],
                style={**CARD_STYLE, "marginTop": "18px"},
            ),
            html.P(
                (
                    "Prediction is an educational demonstration trained on synthetic data; "
                    "it is not a production forecast."
                ),
                style={"color": "#64748b", "marginTop": "18px", "fontSize": "0.82rem"},
            ),
        ],
        style=PAGE_STYLE,
    )

    @app.callback(
        Output("status-chart", "figure"),
        Output("delay-chart", "figure"),
        Output("budget-chart", "figure"),
        Output("progress-chart", "figure"),
        Output("project-table", "data"),
        Input("type-filter", "value"),
        Input("risk-filter", "value"),
    )
    def update_dashboard(project_types, risks):
        selected_types = project_types or projects["project_type"].unique().tolist()
        selected_risks = risks or projects["predicted_risk"].unique().tolist()
        filtered = projects[
            projects["project_type"].isin(selected_types)
            & projects["predicted_risk"].isin(selected_risks)
        ]
        if filtered.empty:
            filtered = projects
        figures = build_figures(filtered)
        attention = filtered.sort_values("predicted_delay_days", ascending=False).head(40)
        return (
            figures["status"],
            figures["delay"],
            figures["budget"],
            figures["progress"],
            _project_table(attention),
        )

    return app
