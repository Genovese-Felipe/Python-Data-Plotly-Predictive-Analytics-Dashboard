# Python-Data-Plotly-Predictive-Analytics-Dashboard

[![CI](https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/actions/workflows/ci.yml)

Visualização de dados, data storytelling e engenharia reversa visual com Python e Plotly, incluindo módulos de extração de conhecimento assistida por IA.

> Aviso de dados: o dataset do app canônico é sintético (240 projetos, seed 42), gerado para demonstração educacional. Não é um portfólio real.

## Início rápido

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements-dashboard.txt
    python -m dashboard_app

Export do dashboard HTML self-contained:

    python -m dashboard_app --export docs/assets/dashboards/construction.html

## O que é verdade hoje vs o que não é

| É verdade | Não é (mais) |
|-----------|--------------|
| App Dash em dashboard_app/ com 240 projetos sintéticos | "Real-time" — nada é streaming |
| Modelo Random Forest com holdout e MAE/R² reportados no app | 25 projetos, R$ 15,2M como números atuais (legado v1) |
| Export HTML self-contained reprodutível | Dashboard "WCAG AA certificado" |
| CI ruff+pytest 3.10/3.12 | Cobertura de callback (sendo adicionada — P01) |

## Arquitetura (5 linhas)

- dashboard_app/data.py: geração/carregamento (CSV validado ou sintético rotulado, seed 42)
- dashboard_app/predictive.py: Random Forest de atraso com split holdout
- dashboard_app/figures.py: figuras Plotly
- dashboard_app/app.py: Dash app com filtros por tipo e risco
- dashboard_app/exporter.py: export HTML self-contido compartilhado entre CLI e CI

## GitHub Pages

Ver docs/GITHUB_PAGES.md. URL: https://genovese-felipe.github.io/Python-Data-Plotly-Predictive-Analytics-Dashboard/

## Dados

- data/projects_master.csv: dataset legado v1 (30 projetos, USD 15,3M) — mantido como referência histórica.
- scripts/data_gen.py: gerador do dataset sintético.

## Legado nomeado

- generate_static_dashboard.py, scripts/, notebooks/, docs/remixes/: v1 legada, não deletada, não canônica. Ver docs/audit/AUDIT_2026-10-20.md para a matriz P01–P12.
