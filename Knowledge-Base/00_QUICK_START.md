# 🎯 QUICK START GUIDE - IA & Python Coding

Este guia vai te levar do **zero ao dashboard com IA funcional** em 1-2 horas seguindo o caminho mais direto e testado para **desenvolvimento de IA com Python**.

---

## ⚡ **SETUP RÁPIDO IA & PYTHON (15 minutos)**

### **1. Dependências Essenciais para IA**
```bash
# Bibliotecas básicas
pip install dash plotly pandas numpy

# IA e Machine Learning
pip install scikit-learn transformers sentence-transformers

# Processamento de dados avançado
pip install chromadb faiss-cpu

# Opcional: GPU acceleration
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### **2. Estrutura de Projeto IA**
```
meu_dashboard_ia/
├── data/               # Seus dados CSV + embeddings
├── models/             # Modelos ML treinados (.pkl, .pt)
├── scripts/
│   ├── ai_utils.py     # Utilitários de IA
│   ├── data_gen.py     # Gerar dados sintéticos
│   └── app.py          # Dashboard principal com IA
├── knowledge_base/     # Base de conhecimento para RAG
└── outputs/
    └── dashboard.html  # Resultado final
```

### **3. Template Mínimo com IA Funcional**
Copie este código para `scripts/app.py`:

```python
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Dados de exemplo com features para IA
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
df = pd.DataFrame({
    'data': dates,
    'vendas': np.random.normal(1000, 200, 100) + np.sin(np.arange(100) * 0.1) * 100,
    'marketing': np.random.normal(500, 100, 100),
    'temperatura': np.random.normal(25, 5, 100),
    'categoria': np.random.choice(['A', 'B', 'C'], 100)
})

# Adicionar tendência para tornar predição interessante
df['vendas'] = df['vendas'] + np.arange(100) * 2

class SimpleAIPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, data):
        """Prepara features para o modelo"""
        features = data[['marketing', 'temperatura']].values
        if self.is_trained:
            return self.scaler.transform(features)
        else:
            return self.scaler.fit_transform(features)
    
    def train(self, data):
        """Treina modelo simples de predição"""
        X = self.prepare_features(data)
        y = data['vendas'].values
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Salvar modelo
        os.makedirs('models', exist_ok=True)
        with open('models/predictor.pkl', 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def predict(self, marketing, temperatura):
        """Faz predição"""
        if not self.is_trained:
            return None
        
        X = self.scaler.transform([[marketing, temperatura]])
        prediction = self.model.predict(X)[0]
        return round(prediction, 2)

# Inicializar IA
ai_predictor = SimpleAIPredictor()
ai_predictor.train(df)

# Criar app
app = dash.Dash(__name__)

# Layout com IA
app.layout = html.Div([
    html.H1("🤖 Dashboard com IA - Python Coding", style={'textAlign': 'center'}),
    
    # Seção de predição IA
    html.Div([
        html.H3("🎯 Predição de Vendas com IA"),
        html.Div([
            html.Label("Investimento em Marketing:"),
            dcc.Slider(id='marketing-slider', min=300, max=700, value=500, step=10,
                      marks={300: '300', 500: '500', 700: '700'}),
            
            html.Label("Temperatura:"),
            dcc.Slider(id='temp-slider', min=15, max=35, value=25, step=1,
                      marks={15: '15°C', 25: '25°C', 35: '35°C'}),
            
            html.Div(id='prediction-output', style={
                'fontSize': '24px', 'fontWeight': 'bold', 
                'textAlign': 'center', 'margin': '20px',
                'padding': '20px', 'border': '2px solid #1f77b4',
                'borderRadius': '10px', 'backgroundColor': '#f0f8ff'
            })
        ], style={'margin': '20px'}),
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'margin': '10px'}),
    
    # Gráficos com insights de IA
    dcc.Graph(
        figure=px.line(df, x='data', y='vendas', title='📈 Vendas Históricas (Dados para IA)')
    ),
    
    dcc.Graph(
        figure=px.scatter(df, x='marketing', y='vendas', color='categoria', 
                         title='🎯 Correlação Marketing vs Vendas (IA Training Data)',
                         trendline="ols")
    ),
    
    # Métricas de IA
    html.Div([
        html.H3("📊 Métricas do Modelo IA"),
        html.P(f"Accuracy Score: {ai_predictor.model.score(ai_predictor.prepare_features(df), df['vendas']):.3f}"),
        html.P(f"Features: Marketing, Temperatura"),
        html.P(f"Algoritmo: Linear Regression (scikit-learn)"),
    ], style={'backgroundColor': '#e8f5e8', 'padding': '15px', 'margin': '10px'})
])

# Callback para predição em tempo real
@app.callback(
    Output('prediction-output', 'children'),
    [Input('marketing-slider', 'value'),
     Input('temp-slider', 'value')]
)
def update_prediction(marketing, temperatura):
    prediction = ai_predictor.predict(marketing, temperatura)
    return [
        html.Div("🤖 Predição IA:", style={'fontSize': '16px'}),
        html.Div(f"R$ {prediction:,.2f}", style={'fontSize': '32px', 'color': '#1f77b4'}),
        html.Div(f"Marketing: R${marketing} | Temp: {temperatura}°C", 
                style={'fontSize': '14px', 'color': '#666'})
    ]

# Executar
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
```

---

## 🚀 **PRIMEIROS PASSOS COM IA (30 minutos)**

### **Passo 1: Execute o Template com IA**
```bash
cd meu_dashboard_ia/scripts
python app.py
# Abra: http://localhost:8050
# Teste os sliders de predição IA!
```

### **Passo 2: Entenda o Código Python IA**
O template inclui:
- **Classe AI Predictor**: Demonstra estrutura OOP para IA
- **Treino automático**: Modelo treinado nos dados históricos
- **Predição em tempo real**: Callback Dash conectado à IA
- **Persistência**: Modelo salvo em pickle para reutilização

### **Passo 3: Adapte com Seus Dados e IA**
```python
# Ao invés de dados fake, carregue seus dados reais
df = pd.read_csv('../data/meus_dados.csv')

# Ou gere dados sintéticos mais complexos para IA
import numpy as np
from datetime import datetime, timedelta

dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
df = pd.DataFrame({
    'data': dates,
    'vendas': np.random.normal(1000, 200, len(dates)),
    'marketing': np.random.normal(500, 100, len(dates)),
    'sazonalidade': np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
    'regiao': np.random.choice(['Norte', 'Sul', 'Centro'], len(dates))
})

# Adicionar complexidade para tornar IA mais interessante
df['vendas'] = df['vendas'] + df['marketing'] * 0.8 + df['sazonalidade'] * 100
```

---

## 📊 **EXPANDIR FUNCIONALIDADE IA (45 minutos)**

### **Adicionar Modelos ML Mais Avançados**
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

class AdvancedAIPredictor:
    def __init__(self):
        self.models = {
            'linear': LinearRegression(),
            'forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        self.best_model = None
        self.metrics = {}
    
    def train_multiple_models(self, X, y):
        """Treina múltiplos modelos e escolhe o melhor"""
        X_train, X_test = X[:80], X[80:]
        y_train, y_test = y[:80], y[80:]
        
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            self.metrics[name] = {
                'mse': mean_squared_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred)
            }
        
        # Escolher melhor modelo baseado em R²
        best_name = max(self.metrics.keys(), key=lambda k: self.metrics[k]['r2'])
        self.best_model = self.models[best_name]
        
        return best_name, self.metrics
```

### **Adicionar Sistema de Embeddings**
```python
from sentence_transformers import SentenceTransformer

class KnowledgeAI:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = []
        self.embeddings = []
    
    def add_knowledge(self, texts):
        """Adiciona conhecimento à base"""
        self.knowledge_base.extend(texts)
        new_embeddings = self.model.encode(texts)
        self.embeddings.extend(new_embeddings)
    
    def search_knowledge(self, query, top_k=3):
        """Busca semântica na base de conhecimento"""
        if not self.embeddings:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [self.knowledge_base[i] for i in top_indices]
        
        return results

# No layout, adicione busca inteligente:
html.Div([
    html.H3("🔍 Busca Inteligente com IA"),
    dcc.Input(id='search-input', placeholder='Pergunte algo sobre os dados...',
              style={'width': '70%', 'margin': '10px'}),
    html.Button('Buscar', id='search-button'),
    html.Div(id='search-results')
])
```

### **Passo 3: Melhore o Visual**
Adicione cores e estilo profissional:

```python
# Adicione no topo do arquivo
import dash_bootstrap_components as dbc

# Mude a criação do app para:
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Update o layout com cards:
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard Profissional", className="text-center mb-4"),
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig1)
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig2)
                ])
            ])
        ], width=6)
    ])
])
```

---

## 📊 **EXPANDIR FUNCIONALIDADE (45 minutos)**

### **Adicionar Interatividade**
```python
from dash import Input, Output

@app.callback(
    Output('grafico-vendas', 'figure'),
    Input('filtro-regiao', 'value')
)
def atualizar_grafico(regiao_selecionada):
    df_filtrado = df[df['regiao'] == regiao_selecionada]
    return px.line(df_filtrado, x='data', y='vendas')

# No layout, adicione:
dcc.Dropdown(
    id='filtro-regiao',
    options=[{'label': r, 'value': r} for r in df['regiao'].unique()],
    value=df['regiao'].unique()[0]
),
dcc.Graph(id='grafico-vendas')
```

### **Adicionar KPIs**
```python
# Calcular métricas
total_vendas = df['vendas'].sum()
media_vendas = df['vendas'].mean()
crescimento = ((df['vendas'].iloc[-1] / df['vendas'].iloc[0]) - 1) * 100

# No layout, adicione cards de KPI:
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H2(f"R$ {total_vendas:,.0f}", className="text-primary"),
                html.P("Total de Vendas")
            ])
        ])
    ], width=4),
    
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H2(f"R$ {media_vendas:,.0f}", className="text-success"),
                html.P("Média Mensal")
            ])
        ])
    ], width=4),
    
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H2(f"{crescimento:+.1f}%", className="text-info"),
                html.P("Crescimento")
            ])
        ])
    ], width=4)
], className="mb-4")
```

---

## 🎨 **FINALIZAR E EXPORTAR (30 minutos)**

### **Aplicar Paleta Profissional**
```python
# Paleta corporativa
cores = {
    'primaria': '#1f77b4',
    'secundaria': '#ff7f0e', 
    'sucesso': '#2ca02c',
    'info': '#17becf',
    'fundo': '#f8f9fa'
}

# Aplicar em todos os gráficos
fig.update_layout(
    plot_bgcolor=cores['fundo'],
    paper_bgcolor='white',
    colorway=[cores['primaria'], cores['secundaria'], cores['sucesso']]
)
```

### **Exportar para HTML**
```python
# Adicione no final do arquivo
if __name__ == '__main__':
    # Para desenvolvimento
    if False:  # Mude para True para exportar
        fig_final = criar_dashboard_completo()
        fig_final.write_html('../outputs/dashboard.html', 
                            include_plotlyjs='cdn')
        print("Dashboard exportado para outputs/dashboard.html")
    else:
        app.run_server(debug=True, port=8050)
```

---

## ✅ **CHECKLIST FINAL**

### **Funcionalidade:**
- [ ] Dashboard carrega sem erros
- [ ] Todos os gráficos aparecem
- [ ] Filtros funcionam (se tiver)
- [ ] Dados fazem sentido

### **Visual:**
- [ ] Cores profissionais aplicadas
- [ ] Layout organizado e limpo
- [ ] Títulos claros e informativos
- [ ] Responsivo em diferentes telas

### **Performance:**
- [ ] Carregamento < 3 segundos
- [ ] Interações fluidas
- [ ] Não há warnings no console

---

## 🔗 **PRÓXIMOS PASSOS**

Se seu dashboard básico está funcionando:

1. **📈 Gráficos Avançados:** Explore `06_Specialized_Charts/` para Sunburst, mapas
2. **🤖 Machine Learning:** Veja `07_Machine_Learning/` para análise preditiva  
3. **🎨 Design Profissional:** Use `05_Design_and_UX/` para melhorar visual
4. **🏗️ Arquitetura:** Para projetos maiores, consulte `01_Executive_Guides/advanced_dashboard_guide.md`

---

## 🆘 **SE ALGO DEU ERRADO**

### **Dashboard não carrega:**
1. Verifique se instalou todas as dependências
2. Consulte `01_Executive_Guides/plotly_dash_best_practices (3).md`
3. Compare com exemplo funcionando em `02_Practical_Examples/`

### **Gráfico não aparece:**
1. Verifique se dados têm as colunas corretas
2. Print do DataFrame para debug: `print(df.head())`
3. Teste gráfico isoladamente: `fig.show()` antes do layout

### **Erro de callback:**
1. Verifique IDs dos componentes (Input/Output)
2. Teste função de callback isoladamente
3. Use `print()` para debug dentro do callback

---

**🎯 Em 1-2 horas você terá um dashboard funcional e profissional pronto!**
