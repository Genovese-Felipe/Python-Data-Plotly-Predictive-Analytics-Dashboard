# Guia de instalação e uso

Este é o procedimento canônico da versão 2. Os antigos `final_dashboard.py`, `run_construction_dashboard.py` e `scripts/viz.py` continuam funcionando como wrappers de compatibilidade, mas novos usos devem preferir `python -m dashboard_app`.

## 1. Instalação

Requisitos: Git e Python 3.10 ou superior.

```bash
git clone https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
cd Python-Data-Plotly-Predictive-Analytics-Dashboard
python -m venv .venv
```

Ative o ambiente:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instale apenas o dashboard:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dashboard.txt
```

Para desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Para os sistemas Monica AI e extração de conhecimento:

```bash
python -m pip install -r requirements-monica.txt
```

## 2. Uso

### Dashboard interativo

```bash
python -m dashboard_app
```

URL padrão: `http://127.0.0.1:8050`.

Opções úteis:

```bash
python -m dashboard_app --host 0.0.0.0 --port 8060
python -m dashboard_app --debug
python -m dashboard_app --data data/projects.csv
python -m dashboard_app --export outputs/dashboard.html
```

O modo padrão usa 240 projetos sintéticos reproduzíveis. Ao informar `--data`, o CSV é validado antes do treinamento.

### Gerar um CSV de exemplo

```bash
python scripts/data_gen.py
```

Saída: `data/projects.csv`, independentemente da pasta em que o comando for executado.

### Monica AI

```bash
cd AI_Knowledge_Extraction_System
python run_monica_ai.py --test
python run_monica_ai.py --queries "AI visualization" "ML dashboards"
```

A busca web é opcional e depende do serviço externo. Resultados externos devem ser tratados como fontes não verificadas até validação.

## 3. Validação e problemas comuns

Execute a mesma sequência usada pela CI:

```bash
ruff check .
pytest
python -m dashboard_app --export outputs/dashboard.html
```

| Problema | Correção |
| --- | --- |
| Pacote não encontrado | Ative `.venv` e reinstale o arquivo de requisitos correto. |
| CSV rejeitado | Compare as colunas com o contrato descrito no README. |
| Porta ocupada | Use `--port 8060` ou outra porta livre. |
| App acessível localmente, mas não em outro dispositivo | Use `--host 0.0.0.0` somente em uma rede confiável. |
| Exportação não aparece | O caminho relativo é criado a partir da raiz do projeto. |
| Métrica preditiva muda | Verifique se o CSV mudou; o dataset padrão e a semente são fixos. |
| GitHub Pages falha | Execute exportação e testes localmente e examine o workflow `pages.yml`. |

### Limites da demonstração

- O modelo aprende relações de dados sintéticos e não deve orientar decisões reais.
- Não há ingestão externa em tempo real por padrão.
- O CSV precisa incluir o alvo histórico `delay_days` para treinamento.
- Uma implantação real deve versionar dados/modelos, monitorar drift e proteger dados sensíveis.

