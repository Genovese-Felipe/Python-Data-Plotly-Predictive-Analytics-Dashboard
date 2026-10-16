"""Static HTML export used by CI and GitHub Pages."""

from __future__ import annotations

from html import escape
from pathlib import Path

from plotly.io import to_html

from .data import load_dataset
from .figures import build_figures
from .paths import resolve_output_path
from .predictive import train_delay_model


def export_dashboard(output: str | Path = "outputs/dashboard.html", csv_path=None) -> Path:
    """Export a standalone, non-callback snapshot of the canonical dashboard."""
    dataset = load_dataset(csv_path)
    result = train_delay_model(dataset.projects)
    figures = build_figures(result.projects)
    chart_html = []
    for index, figure in enumerate(figures.values()):
        chart_html.append(
            to_html(
                figure,
                full_html=False,
                include_plotlyjs="cdn" if index == 0 else False,
                config={"responsive": True, "displaylogo": False},
            )
        )

    path = resolve_output_path(output)
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Construction Analytics Dashboard</title>
  <style>
    body {{ margin: 0; padding: 28px; background: #f4f7fb; color: #172033; font-family: Inter, system-ui, sans-serif; }}
    header {{ display: flex; justify-content: space-between; align-items: start; gap: 20px; }}
    .badge {{ padding: 8px 12px; border-radius: 999px; background: #dbeafe; color: #1d4ed8; font-weight: 700; }}
    .metrics, .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 20px; }}
    .metric, .chart {{ background: white; border: 1px solid #e5eaf2; border-radius: 14px; padding: 16px; box-shadow: 0 8px 24px rgba(35,55,80,.08); }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 1.5rem; }}
    footer {{ margin-top: 20px; color: #64748b; font-size: .85rem; }}
  </style>
</head>
<body>
  <header><div><h1>Construction Analytics</h1><p>Portfolio monitoring with a reproducible schedule-delay model.</p></div><span class="badge">{escape(dataset.source_label)}</span></header>
  <section class="metrics">
    <div class="metric">Projects<strong>{len(result.projects)}</strong></div>
    <div class="metric">Portfolio budget<strong>${result.projects["budget"].sum() / 1_000_000:.1f}M</strong></div>
    <div class="metric">Holdout MAE<strong>{result.mae_days:.1f} days</strong></div>
    <div class="metric">Holdout R²<strong>{result.r2:.2f}</strong></div>
  </section>
  <main class="grid">{"".join(f'<section class="chart">{item}</section>' for item in chart_html)}</main>
  <footer>Educational predictive demonstration trained on synthetic data; not a production forecast.</footer>
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")
    return path
