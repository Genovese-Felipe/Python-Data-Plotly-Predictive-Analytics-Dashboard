# 🤖 Machine Learning - Análise Preditiva Integrada

Esta pasta contém **recursos especializados** para integrar machine learning e análise preditiva em dashboards Plotly/Dash.

## 🧠 **Recursos Disponíveis**

### **📚 Guias Fundamentais**
- `Predictive Analytics with Python Plotly Dash_ A Co.pdf`
- `Predictive Analytics with Python, Plotly, and Dash.pdf`
- **Integração completa** ML + Dashboard
- **Workflows testados** de ponta a ponta

### **📊 Análise de Séries Temporais**
- `gabri-al_sarima_dashboard_ Introducing a Dash web app that guides the analysis of time series datasets, using sARIMA models.pdf`
- **Modelos sARIMA** para previsão temporal
- **Interface interativa** para análise exploratória
- **Visualizações especializadas** para séries temporais

### **🔬 Implementações Práticas**
- `predictive analytics on Python-197945815.pdf`
- `predictive analytics on Python-197945851.pdf`
- **Casos de uso reais** documentados
- **Performance e validação** de modelos

---

## 🎯 **Padrões de Integração ML + Dashboard**

### **1. Pipeline Completo de ML**
```python
# Estrutura padrão para ML em Dash
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# 1. Preparação dos dados
def preparar_dados(df):
    # Feature engineering
    # Limpeza e transformação
    # Encoding de variáveis categóricas
    return X, y

# 2. Treinamento do modelo
def treinar_modelo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    modelo = RandomForestRegressor(n_estimators=100)
    modelo.fit(X_train, y_train)
    
    return modelo, X_test, y_test

# 3. Integração com Dashboard
@app.callback(
    Output('predicao-grafico', 'figure'),
    Input('input-features', 'value')
)
def atualizar_predicao(features_input):
    predicao = modelo.predict([features_input])
    return criar_grafico_predicao(predicao)
```

### **2. Modelos de Séries Temporais**
```python
# sARIMA integrado com Dash
from statsmodels.tsa.statespace.sarimax import SARIMAX

def criar_dashboard_sarima():
    app = Dash(__name__)
    
    app.layout = html.Div([
        # Controles de parâmetros SARIMA
        html.Div([
            dcc.Slider(id='p-param', min=0, max=5, value=1),
            dcc.Slider(id='d-param', min=0, max=2, value=1),
            dcc.Slider(id='q-param', min=0, max=5, value=1),
        ]),
        
        # Gráficos de resultados
        dcc.Graph(id='serie-original'),
        dcc.Graph(id='predicao-sarima'),
        dcc.Graph(id='residuos')
    ])
    
    @app.callback(
        [Output('serie-original', 'figure'),
         Output('predicao-sarima', 'figure'),
         Output('residuos', 'figure')],
        [Input('p-param', 'value'),
         Input('d-param', 'value'),
         Input('q-param', 'value')]
    )
    def atualizar_sarima(p, d, q):
        # Treinar modelo sARIMA
        modelo = SARIMAX(dados_serie, order=(p,d,q))
        resultado = modelo.fit()
        
        # Gerar previsões
        previsao = resultado.forecast(steps=30)
        
        # Criar gráficos
        return (
            plotar_serie_original(dados_serie),
            plotar_predicao(previsao),
            plotar_residuos(resultado.resid)
        )
    
    return app
```

---

## 📊 **Visualizações ML Especializadas**

### **1. Matriz de Confusão Interativa**
```python
def criar_matriz_confusao(y_true, y_pred, classes):
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(y_true, y_pred)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=classes,
        y=classes,
        colorscale='Blues',
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 20},
    ))
    
    fig.update_layout(
        title="Matriz de Confusão",
        xaxis_title="Predito",
        yaxis_title="Real"
    )
    
    return fig
```

### **2. Feature Importance Dashboard**
```python
def criar_dashboard_importancia():
    # Extrair importância das features
    importances = modelo.feature_importances_
    features = X.columns
    
    # Criar gráfico de barras
    fig = go.Figure(go.Bar(
        x=importances,
        y=features,
        orientation='h',
        marker_color='steelblue'
    ))
    
    fig.update_layout(
        title="Importância das Features",
        xaxis_title="Importância",
        yaxis_title="Features"
    )
    
    return fig
```

### **3. Curva ROC Interativa**
```python
def criar_curva_roc(y_true, y_prob):
    from sklearn.metrics import roc_curve, auc
    
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {roc_auc:.2f})',
        line=dict(color='darkorange', width=2)
    ))
    
    # Linha diagonal (classificador aleatório)
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='navy', dash='dash')
    ))
    
    return fig
```

---

## 🎯 **Casos de Uso por Setor**

### **📈 Dashboards Financeiros com ML**
```python
# Previsão de receitas
- Modelo: ARIMA/Prophet para séries temporais
- Features: Sazonalidade, tendências históricas
- Visualizações: Linha temporal + intervalo confiança
- Interatividade: Ajuste de parâmetros do modelo
```

### **🛒 Dashboards de E-commerce**
```python
# Sistema de recomendação
- Modelo: Collaborative Filtering
- Features: Histórico de compras, perfil usuário
- Visualizações: Network graph, heatmaps
- Interatividade: Filtros por usuário/produto
```

### **🏭 Dashboards Industriais**
```python
# Manutenção preditiva
- Modelo: Random Forest para classificação
- Features: Sensores IoT, histórico manutenções
- Visualizações: Gauges, alertas visuais
- Interatividade: Simulação de cenários
```

---

## 🛠️ **Ferramentas e Bibliotecas**

### **Stack Recomendado:**
```python
# Machine Learning
import sklearn
import statsmodels
import xgboost
import lightgbm

# Séries Temporais
import prophet
from statsmodels.tsa.arima.model import ARIMA

# Visualização ML
import plotly.graph_objects as go
import plotly.express as px

# Dashboard
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
```

### **Performance e Otimização:**
```python
# Cache de modelos treinados
from flask_caching import Cache

cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple'
})

@cache.memoize(timeout=3600)  # Cache por 1 hora
def treinar_modelo_cache(dados_hash):
    # Treinar modelo apenas se dados mudaram
    return modelo_treinado

# Previsões em batch
def gerar_predicoes_batch(modelo, dados_novos):
    # Processar múltiplas previsões de uma vez
    return modelo.predict(dados_novos)
```

---

## ⚡ **Quick Start - Template ML**

### **Dashboard ML Mínimo Funcional:**
```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Carregar dados (substitua pelo seu dataset)
df = pd.read_csv('dados.csv')
X = df.drop('target', axis=1)
y = df['target']

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
modelo = RandomForestRegressor().fit(X_train, y_train)

# Dashboard
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard ML Básico"),
    
    # Controles de entrada
    html.Div([
        html.Label("Feature 1:"),
        dcc.Slider(id='feature1', min=X.min().iloc[0], max=X.max().iloc[0], value=X.mean().iloc[0]),
        # Adicionar mais controles conforme necessário
    ]),
    
    # Gráficos
    dcc.Graph(id='predicao-resultado'),
    dcc.Graph(id='feature-importance')
])

@app.callback(
    [Output('predicao-resultado', 'figure'),
     Output('feature-importance', 'figure')],
    Input('feature1', 'value')
)
def atualizar_dashboard(feature1_val):
    # Fazer previsão
    entrada = [[feature1_val]]  # Adapte conforme suas features
    predicao = modelo.predict(entrada)[0]
    
    # Gráfico de predição
    fig_pred = px.bar(x=['Previsão'], y=[predicao], title=f"Previsão: {predicao:.2f}")
    
    # Gráfico de importância
    importances = modelo.feature_importances_
    fig_imp = px.bar(x=X.columns, y=importances, title="Importância das Features")
    
    return fig_pred, fig_imp

if __name__ == '__main__':
    app.run_server(debug=True)
```

---

**🎯 Lembre-se:** A integração ML + Dashboard deve ser **incremental** - comece com modelos simples e visualizações básicas, depois evolua para análises mais sofisticadas conforme necessário.
