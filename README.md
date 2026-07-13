# Python Data Plotly Predictive Analytics Dashboard

Dashboard de portfólio de projetos com Python, Plotly e Dash. A versão 2 define um caminho de execução único, dados reproduzíveis, uma demonstração preditiva avaliada em holdout, testes automatizados e exportação para GitHub Pages.

> **Transparência:** o dataset padrão é sintético. O modelo estima dias de atraso para fins educacionais; não é uma previsão operacional nem recebe dados em tempo real sem que uma fonte CSV seja fornecida.

## Comece em três comandos

```bash
python -m venv .venv
python -m pip install -r requirements-dashboard.txt
python -m dashboard_app
```

Abra [http://localhost:8050](http://localhost:8050).

Para exportar uma versão HTML estática:

```bash
python -m dashboard_app --export outputs/dashboard.html
```

Para usar um CSV próprio:

```bash
python -m dashboard_app --data data/projects.csv
```

Consulte [SETUP_GUIDE.md](SETUP_GUIDE.md) para Windows, Linux/macOS, validação e solução de problemas.

## O que está implementado

- Filtros por tipo de projeto e risco previsto.
- KPIs de portfólio e métricas do modelo.
- Status, orçamento, complexidade, progresso e atraso previsto.
- Random Forest com divisão treino/teste reproduzível.
- MAE e R² calculados apenas no conjunto de teste.
- Entrada por CSV com validação de esquema.
- Exportação HTML usada pelo GitHub Pages.
- Testes de dados, caminhos, modelo, app e exportação.
- CI para Python 3.10 e 3.12.

### Contrato mínimo do CSV

| Coluna | Significado |
| --- | --- |
| `project_id`, `project_name` | Identidade do projeto |
| `project_type`, `status` | Categoria e situação |
| `planned_duration_days` | Duração planejada |
| `budget`, `team_size` | Recursos do projeto |
| `complexity_score` | Escala de 1 a 10 |
| `completion_pct` | Progresso de 0 a 100 |
| `delay_days` | Alvo histórico usado no treinamento |

Um exemplo pode ser criado com:

```bash
python scripts/data_gen.py
python -m dashboard_app --data data/projects.csv
```

## Arquitetura canônica

```text
dashboard_app/
├── __main__.py      # CLI: servidor e exportação
├── app.py           # layout e callbacks Dash
├── data.py          # geração, carga e validação
├── predictive.py    # treino, holdout e métricas
├── figures.py       # gráficos compartilhados
├── exporter.py      # snapshot HTML
└── paths.py         # caminhos baseados no arquivo

tests/               # testes automatizados
docs/                # site, arquitetura e roadmap
```

Detalhes: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Sistemas secundários e legado

O repositório cresceu como laboratório e preserva implementações anteriores:

- `AI_Dashboard_Implementation/`: versão detalhada do dashboard original.
- `AI_Knowledge_Extraction_System/` e `Monica_AI_System/`: pesquisa e processamento de conhecimento.
- `Knowledge-Base/`: referências, tutoriais e experimentos.
- demais scripts e notebooks: versões históricas e estudos.

Esses diretórios permanecem disponíveis, mas `dashboard_app` é o caminho oficial. Para instalar as dependências da Monica AI:

```bash
python -m pip install -r requirements-monica.txt
cd AI_Knowledge_Extraction_System
python run_monica_ai.py --test
```

As integrações listadas pela Monica AI são uma estrutura de demonstração; cada serviço externo exige credenciais, permissões e validação próprias.

## Qualidade e contribuição

```bash
python -m pip install -r requirements-dev.txt
ruff check .
pytest
python -m dashboard_app --export outputs/dashboard.html
```

O plano de evolução e os limites atuais estão em [docs/ROADMAP.md](docs/ROADMAP.md).

