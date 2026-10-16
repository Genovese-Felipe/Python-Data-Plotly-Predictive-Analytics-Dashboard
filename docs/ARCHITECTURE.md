# Arquitetura da versão 2

## Fluxo principal

```text
CSV opcional ─┐
              ├─> validação ─> treino/teste ─> previsões ─> Dash
Sintético ────┘                                  └───────> HTML estático
```

`dashboard_app.data` é a fronteira de entrada. Ele gera dados reproduzíveis ou valida um CSV. `dashboard_app.predictive` separa treino e teste, ajusta o pipeline e adiciona previsões sem substituir o alvo histórico. `dashboard_app.figures` alimenta tanto o app interativo quanto o exportador, evitando gráficos divergentes.

## Decisões

- **Pacote na raiz:** permite `python -m dashboard_app` sem depender do diretório atual.
- **Caminhos com `pathlib`:** elimina o problema dos antigos `../data`.
- **Importação tardia do Dash:** testes de dados e modelo não dependem da interface.
- **Modelo em pipeline:** o `OneHotEncoder` e o regressor são treinados juntos, reduzindo inconsistências entre treino e inferência.
- **Holdout explícito:** MAE e R² são calculados em dados não usados no ajuste.
- **Fonte rotulada:** a interface diferencia dataset sintético de CSV fornecido.
- **Exportação compartilhada:** o GitHub Pages usa as mesmas funções de figuras e predição.

## Fronteiras do repositório

| Área | Estado |
| --- | --- |
| `dashboard_app/` | Produto canônico e mantido |
| `tests/` | Contrato mínimo de qualidade |
| `docs/` | Site e documentação atual |
| `AI_Knowledge_Extraction_System/`, `Monica_AI_System/` | Subsistemas opcionais |
| `AI_Dashboard_Implementation/`, notebooks e scripts antigos | Legado preservado para referência |

## Evolução para produção

Uma versão operacional deve separar treinamento e inferência, registrar versão do dataset e do modelo, armazenar artefatos fora do Git, autenticar a fonte de dados e implementar observabilidade, monitoramento de drift e controle de acesso.

