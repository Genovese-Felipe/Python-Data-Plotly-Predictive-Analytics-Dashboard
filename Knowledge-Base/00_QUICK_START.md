# 🎯 QUICK START GUIDE - Guia de Início Rápido

Este guia vai te levar do **zero ao dashboard funcional** em 1-2 horas seguindo o caminho mais direto e testado.

---

## ⚡ **SETUP RÁPIDO (15 minutos)**

### **1. Dependências Essenciais**
```bash
pip install dash plotly pandas numpy
```

### **2. Estrutura de Projeto**
```
meu_dashboard/
├── data/               # Seus dados CSV
├── scripts/
│   ├── data_gen.py    # Gerar dados sintéticos
│   └── app.py         # Dashboard principal
└── outputs/
    └── dashboard.html # Resultado final
```

### **3. Template Mínimo Funcional**
Copie este código para `scripts/app.py`:

```python
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Dados de exemplo
df = pd.DataFrame({
    'mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'vendas': [1000, 1200, 800, 1500, 1300],
    'categoria': ['A', 'B', 'A', 'C', 'B']
})

# Criar app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Meu Dashboard", style={'textAlign': 'center'}),
    
    dcc.Graph(
        figure=px.line(df, x='mes', y='vendas', title='Vendas Mensais')
    ),
    
    dcc.Graph(
        figure=px.bar(df, x='categoria', y='vendas', title='Vendas por Categoria')
    )
])

# Executar
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
```

---

## 🚀 **PRIMEIROS PASSOS (30 minutos)**

### **Passo 1: Execute o Template**
```bash
cd meu_dashboard/scripts
python app.py
# Abra: http://localhost:8050
```

### **Passo 2: Adapte os Dados**
Substitua o DataFrame de exemplo pelos seus dados:

```python
# Ao invés de dados fake, carregue seus dados reais
df = pd.read_csv('../data/meus_dados.csv')

# Ou gere dados sintéticos mais realistas
import numpy as np
from datetime import datetime, timedelta

dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
df = pd.DataFrame({
    'data': dates,
    'vendas': np.random.normal(1000, 200, len(dates)),
    'regiao': np.random.choice(['Norte', 'Sul', 'Centro'], len(dates))
})
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
