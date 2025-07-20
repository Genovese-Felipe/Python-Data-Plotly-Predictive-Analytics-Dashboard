# Dashboard de Análise Preditiva com Python, Plotly e Dash

## Visão Geral

Este projeto implementa um sistema completo de análise preditiva utilizando Python, Plotly e Dash. O sistema inclui preparação de dados, modelagem de machine learning e um dashboard interativo para visualização e predições em tempo real.

## Estrutura do Projeto

```
predictive_analytics_dash/
├── app.py                      # Aplicação principal Dash
├── requirements.txt            # Dependências do projeto
├── data/
│   ├── load_data.py           # Script para carregar dados
│   └── iris.csv               # Dataset Iris
├── models/
│   ├── train_model.py         # Script de treinamento
│   ├── logistic_regression_model.pkl  # Modelo treinado
│   └── scaler.pkl             # Scaler para normalização
├── components/
│   └── dashboard_layout.py    # Layout do dashboard
├── utils/
│   ├── data_exploration.py    # Análise exploratória
│   └── data_preprocessing.py  # Pré-processamento
└── assets/
    ├── sepal_scatter.html     # Gráfico scatter
    └── petal_hist.html        # Histograma
```

## Funcionalidades

### 1. Análise Exploratória de Dados
- Visualização de scatter plot das características das flores
- Histograma da distribuição das pétalas
- Estatísticas descritivas do dataset

### 2. Modelagem Preditiva
- Implementação de Regressão Logística
- Pré-processamento com StandardScaler
- Avaliação de performance com 100% de acurácia

### 3. Dashboard Interativo
- Sliders para ajuste de parâmetros em tempo real
- Predições instantâneas com probabilidades
- Visualizações dinâmicas e responsivas

## Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
python app.py
```

3. Acesse o dashboard em: http://localhost:8050

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal
- **Dash**: Framework para dashboards interativos
- **Plotly**: Biblioteca de visualização
- **Scikit-learn**: Machine learning
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica

## Resultados

O modelo de Regressão Logística alcançou 100% de acurácia no conjunto de teste, demonstrando excelente performance na classificação das espécies de íris.

## Autor

**Manus AI** - Sistema de Inteligência Artificial para Análise Preditiva

