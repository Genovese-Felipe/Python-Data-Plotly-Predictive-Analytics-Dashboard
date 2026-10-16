---
layout: home
title: "Construction Analytics Dashboard"
description: "Python, Plotly, Dash e uma demonstração preditiva reproduzível"
---

# Construction Analytics Dashboard

Uma referência educacional para acompanhar portfólios de projetos e demonstrar um pipeline de previsão de atraso com avaliação treino/teste.

> O site usa dados sintéticos. As previsões não representam projetos reais nem substituem análise profissional.

## Dashboard

<iframe src="assets/dashboards/construction.html" width="100%" height="760" frameborder="0" title="Construction Analytics Dashboard"></iframe>

[Abrir o dashboard em página inteira](assets/dashboards/construction.html)

## Execução local

```bash
python -m venv .venv
python -m pip install -r requirements-dashboard.txt
python -m dashboard_app
```

O servidor usa `http://127.0.0.1:8050`. Veja o [guia completo](../SETUP_GUIDE.md), a [arquitetura](ARCHITECTURE.md) e o [roadmap](ROADMAP.md).

## Escopo

O caminho oficial está em `dashboard_app/`. Sistemas Monica AI, base de conhecimento, notebooks e versões históricas permanecem no repositório como módulos opcionais ou referências.

