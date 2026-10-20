# GitHub Pages — receita de publicação

Repo: Python-Data-Plotly-Predictive-Analytics-Dashboard. URL final:
https://genovese-felipe.github.io/Python-Data-Plotly-Predictive-Analytics-Dashboard/

## Decisão de arquitetura

- Source: GitHub Actions (Settings → Pages → Build and deployment → Source: GitHub Actions). Não usar "Deploy from branch" — o repo precisa do passo de export Python antes do build Jekyll.
- Manter a ideia do pages.yml existente: export via CLI canônica + build Jekyll em docs/ + deploy-pages@v4.
- O dashboard público é um HTML self-contained exportado por python -m dashboard_app — sem servidor Python, Plotly embutido no arquivo.

## Passo a passo

1. Settings → Pages → Source: GitHub Actions.
2. Garantir no pages.yml (ou nova versão) a sequência: checkout → setup-python → pip install -r requirements-dashboard.txt → python -m dashboard_app --export docs/assets/dashboards/construction.html → actions/configure-pages → actions/jekyll-build → actions/deploy-pages@v4.
3. Arquivar o HTML legado (P02), localmente com token de escrita:
   git mv docs/index.html docs/archive/index-legacy.html
   git commit -m "docs(P02): archive legacy v1 index; Jekyll home is index.md"
4. docs/_config.yml: baseurl: "" (o workflow injeta --baseurl; duplicar quebra links). Layouts permitidos: page, home, default (tema minima). exclude: [remixes/, archive/].
5. Incluir a página do dashboard com um iframe ou link direto para /assets/dashboards/construction.html a partir do index.md.
6. Gate: o job de Pages só roda depois do CI verde (needs na matriz ruff+pytest).
7. Não rodar generate_static_dashboard.py — grava index.html na raiz com dados da v1 (25 projetos, "real-time" falso).

## Checklist de verificação pós-deploy

- Home mostra index.md da v2, não o HTML legado.
- Link do dashboard abre construction.html com Plotly funcionando.
- Links internos sem //Python-Data-Plotly-Predictive-Analytics-Dashboard duplo (baseurl aplicado uma vez).
- docs/remixes/ não aparece no sitemap/pesquisa do site.
