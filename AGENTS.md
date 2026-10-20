# AGENTS.md — contrato de execução para IA externa

Este arquivo define como agentes de IA (ou humanos automatizados) devem operar neste repo sem quebrar a main ou publicar dados errados.

## Caminho canônico

- Código vivo: dashboard_app/ (data.py, predictive.py, figures.py, app.py, exporter.py, __main__.py).
- Legado: generate_static_dashboard.py, scripts/, notebooks/, docs/remixes/. Não rodar o gerador v1: grava index.html na raiz com números desatualizados.

## Comandos seguros

- Rodar app: python -m dashboard_app
- Export HTML: python -m dashboard_app --export docs/assets/dashboards/construction.html
- Testes: pytest -q
- Lint: ruff check .

## Regras de dados

- O dataset do app é sintético (240 projetos, seed 42) e rotulado como tal na UI.
- data/projects_master.csv é legado v1 (30 projetos); nunca citá-lo como números atuais.
- load_dataset aceita um CSV validado; fallback sintético rotulado.

## Regras de modificação

- main é protegida: todo trabalho em branch audit/* ou review/* com PR draft.
- Consulte docs/audit/AUDIT_2026-10-20.md (matriz P01–P12) antes de "corrigir" algo que já está catalogado.
- Callback P01 corrigido em audit/pages-readme-html-2026-10: Output("project-table", "children").

## GitHub Pages

- Receita: docs/GITHUB_PAGES.md.
- Nunca usar generate_static_dashboard.py para o site; export via CLI canônica.
