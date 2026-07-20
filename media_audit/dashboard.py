from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "media_audit" / "data" / "github_audit.json").read_text(encoding="utf-8"))
PERIODS = pd.DataFrame(DATA["periods"])
COMMITS = pd.DataFrame(DATA["commits"])
COMMITS["created_at"] = pd.to_datetime(COMMITS["created_at"], utc=True)

app = Dash(__name__)
app.title = "Evidence-backed Media Audit"
app.layout = html.Div(
    [
        html.H1("Evidence-backed multimedia audit"),
        html.P(
            "Filtros alteram KPIs, cobertura e narrativa; ausência de evidência "
            "não é zero produtividade."
        ),
        dcc.Dropdown(
            id="period-filter",
            options=[{"label": p, "value": p} for p in PERIODS["period"]],
            value=list(PERIODS["period"]),
            multi=True,
        ),
        html.Div(id="kpis", style={"display": "flex", "gap": "28px", "margin": "20px 0"}),
        dcc.Graph(id="coverage-chart"),
        dcc.Graph(id="monthly-chart"),
        html.Div(id="evidence-table"),
        html.Hr(),
        html.P(
            "Fonte: GitHub commit metadata; consulta limitada aos 100 commits "
            "mais recentes; corte 2026-07-20."
        ),
    ],
    style={"maxWidth": "1200px", "margin": "0 auto", "fontFamily": "Arial", "padding": "24px"},
)


@app.callback(
    Output("kpis", "children"),
    Output("coverage-chart", "figure"),
    Output("monthly-chart", "figure"),
    Output("evidence-table", "children"),
    Input("period-filter", "value"),
)
def update(selected):
    selected = selected or []
    rows = PERIODS[PERIODS["period"].isin(selected)].copy()
    observed = int((rows["coverage_status"] == "observed").sum())
    total = int(rows["commit_count"].sum())
    kpis = [
        html.Div([html.H3("Janelas selecionadas"), html.P(str(len(rows)))]),
        html.Div([html.H3("Janelas com evidência"), html.P(f"{observed}/{len(rows)}")]),
        html.Div([html.H3("Commits observados"), html.P(str(total))]),
        html.Div([html.H3("Confiança"), html.P("média, limitada")]),
    ]
    fig_cov = px.bar(
        rows,
        x="period",
        y="commit_count",
        color="coverage_status",
        title="Commits observados por janela",
    )
    fig_cov.update_layout(template="plotly_white", legend_title="Status de evidência")
    monthly = (
        COMMITS.assign(month=COMMITS["created_at"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .size()
    )
    monthly = monthly.rename(columns={"size": "commits"})
    fig_month = px.line(
        monthly, x="month", y="commits", markers=True, title="Concentração mensal da atividade"
    )
    fig_month.update_layout(template="plotly_white")
    table = html.Table(
        [
            html.Tr([html.Th(c) for c in ["Período", "Commits", "Status", "Limite"]]),
            *[
                html.Tr(
                    [
                        html.Td(r["period"]),
                        html.Td(str(r["commit_count"])),
                        html.Td(r["coverage_status"]),
                        html.Td(
                            "Sem evidência no resultado consultado"
                            if r["commit_count"] == 0
                            else "100 registros consultados"
                        ),
                    ]
                )
                for _, r in rows.iterrows()
            ],
        ],
        style={"width": "100%", "borderSpacing": "10px"},
    )
    return kpis, fig_cov, fig_month, table


if __name__ == "__main__":
    app.run(debug=False)
