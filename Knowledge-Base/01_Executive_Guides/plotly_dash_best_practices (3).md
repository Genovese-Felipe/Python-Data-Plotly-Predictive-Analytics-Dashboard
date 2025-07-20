# 🤖 **Guia de Instruções para Modelos de IA - Desenvolvimento Plotly/Dash**

> **Manual completo para evitar erros comuns no desenvolvimento de dashboards Plotly/Dash**

---

## 🎯 **OBJETIVO DESTE DOCUMENTO**

Este guia foi criado após uma sessão intensiva de debugging onde múltiplos problemas foram identificados e resolvidos. Use estas instruções para evitar os mesmos erros e acelerar o desenvolvimento de dashboards funcionais.

---

## 📋 **PROTOCOLO DE DESENVOLVIMENTO RECOMENDADO**

### **1. SEMPRE COMECE COM ANÁLISE** 🔍

#### **Antes de Escrever Código:**
```python
# ✅ FAÇA SEMPRE:
1. Analise arquivos existentes que funcionam
2. Extraia dados reais de referências funcionais  
3. Identifique padrões de código que funcionam
4. Entenda completamente a estrutura de dados

# ❌ NUNCA FAÇA:
1. Tente "consertar" código complexo quebrado
2. Use dados fictícios quando dados reais estão disponíveis
3. Comece com funcionalidades complexas
4. Assuma que código anterior está correto
```

#### **Quando Encontrar HTML Funcional:**
```python
# ✅ PROCESSO CORRETO:
1. Extraia dados usando grep_search/read_file
2. Identifique padrões: labels, parents, values
3. Copie estruturas que funcionam
4. Recrie com dados reais extraídos

# Exemplo de extração bem-sucedida:
labels = ["Item1", "Item2", ...]  # Do HTML
parents = ["Parent1", "Parent2", ...]  # Do HTML  
values = [1000, 2000, ...]  # Do HTML
```

### **2. DESENVOLVIMENTO INCREMENTAL** 📈

#### **Sequência Obrigatória:**
```python
# ✅ ORDEM CORRETA:
V1: Dashboard SIMPLES e FUNCIONAL
├── 1 gráfico básico
├── Dados reais
├── Layout mínimo
└── 100% funcional

V2: Adicionar INTERATIVIDADE
├── V1 + Filtros
├── Callbacks simples  
├── UI melhorada
└── 100% funcional

V3: Adicionar COMPLEXIDADE
├── V2 + ML/Mapas
├── Múltiplas visualizações
├── Design avançado
└── 100% funcional
```

#### **❌ ANTI-PADRÕES A EVITAR:**
```python
# NUNCA faça tudo de uma vez:
❌ V1: Dashboard completo com ML + Mapas + Filtros + UI complexa
❌ Múltiplos callbacks complexos no primeiro código
❌ Dados simulados quando dados reais existem
❌ Over-engineering antes da funcionalidade básica
```

---

## 🔧 **REGRAS DE CÓDIGO ESPECÍFICAS**

### **3. IMPORTS E DEPENDÊNCIAS** 📦

#### **✅ Imports Corretos:**
```python
# SEMPRE use estes imports para Dash:
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Para ML (apenas quando necessário):
from sklearn.linear_model import LinearRegression
```

#### **❌ Imports a Evitar:**
```python
# NUNCA misture imports antigos e novos:
❌ from dash.dependencies import Input, Output  # Obsoleto
❌ from dash import callback  # Desnecessário
❌ import dash_table  # Apenas se usar DataTable

# NUNCA use display() fora do Jupyter:
❌ display(df)  # Use print(df)
```

### **4. EXECUÇÃO DE APPS** 🚀

#### **✅ Método Atual Correto:**
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8052)
```

#### **❌ Métodos Incorretos:**
```python
❌ app.run_server(debug=True)  # Obsoleto desde Dash 2.x
❌ app.run(jupyter_mode='inline')  # Apenas para Jupyter
❌ app.run_server(mode='inline')  # Obsoleto
```

### **5. ESTRUTURA DE CALLBACKS** 🔄

#### **✅ Callbacks Simples e Funcionais:**
```python
# MÁXIMO 1-2 Inputs, 1-4 Outputs relacionados
@app.callback(
    Output('chart-id', 'figure'),
    Input('dropdown-id', 'value')
)
def update_chart(selected_value):
    # Lógica simples
    fig = px.sunburst(data, ...)
    return fig
```

#### **❌ Callbacks Problemáticos:**
```python
❌ # Muitos inputs/outputs não relacionados
@app.callback(
    Output('chart1', 'figure'),
    Output('chart2', 'figure'), 
    Output('table', 'data'),
    Output('metric', 'children'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('slider', 'value'),
    Input('tabs', 'value'),
    State('store', 'data')
)

❌ # Dependências circulares
@app.callback(Output('A', 'value'), Input('B', 'value'))
@app.callback(Output('B', 'value'), Input('A', 'value'))
```

---

## 📊 **REGRAS ESPECÍFICAS PARA VISUALIZAÇÕES**

### **6. GRÁFICOS SUNBURST** 🌅

#### **✅ Estrutura Correta:**
```python
# SEMPRE garanta hierarquia consistente:
fig = go.Figure(go.Sunburst(
    labels=labels,           # Lista de strings únicas
    parents=parents,         # Hierarchy paths
    values=values,           # Números positivos
    branchvalues="total",    # Importante para hierarquia
    maxdepth=4,              # Limite de níveis
    insidetextorientation='radial'
))
```

#### **❌ Erros Comuns em Sunburst:**
```python
❌ values=[0, 0, 0, ...]  # Valores zerados quebram o gráfico
❌ parents=['', '', '', ...] # Muitos roots causam problemas
❌ labels=['A', 'A', 'B'] # Labels duplicados em mesmo nível
❌ Falta de branchvalues="total"  # Hierarquia incorreta
```

### **7. MAPAS GEOGRÁFICOS** 🗺️

#### **✅ Configuração Correta:**
```python
fig = px.scatter_geo(
    df,
    lat='Latitude',
    lon='Longitude', 
    size='value_column',
    color='category_column',
    projection="albers usa",  # Para dados dos EUA
    hover_name='name_column'
)
fig.update_layout(geo=dict(scope='usa'))  # Importante para EUA
```

### **8. MACHINE LEARNING INTEGRATION** 🧠

#### **✅ ML Simples e Efetivo:**
```python
# Para pequenos datasets, use modelos simples:
from sklearn.linear_model import LinearRegression

X = df[['feature1', 'feature2', 'feature3']]  # Numérico
y = df['target']
model = LinearRegression()
model.fit(X, y)

# Visualização da importância:
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': np.abs(model.coef_)
})
```

#### **❌ ML Over-Engineering:**
```python
❌ # Complexidade desnecessária para dados pequenos
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
model = GridSearchCV(RandomForestRegressor(), param_grid)

❌ # One-hot encoding em dados já numéricos
X = pd.get_dummies(X, columns=['numeric_column'])
```

---

## 🎨 **DESIGN E LAYOUT**

### **9. LAYOUT RESPONSIVO** 📱

#### **✅ Design Moderno:**
```python
# Use CSS Grid/Flexbox patterns:
html.Div([
    html.Div([...], style={
        'width': '48%', 
        'display': 'inline-block',
        'marginRight': '4%',
        'backgroundColor': 'white',
        'padding': '15px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
])
```

#### **❌ Layout Problemático:**
```python
❌ style={'width': '500px'}  # Pixels fixos
❌ style={'float': 'left'}   # Float antiquado
❌ Sem padding/margin adequados
❌ Cores hard-coded sem consistência
```

### **10. CORES E TEMAS** 🎨

#### **✅ Sistema de Cores Consistente:**
```python
# Defina color maps explícitos:
color_map = {
    'Category1': '#1f77b4',
    'Category2': '#ff7f0e', 
    'Category3': '#2ca02c',
    'Category4': '#d62728'
}

fig = px.sunburst(df, color='category', 
                 color_discrete_map=color_map)
```

---

## 🚨 **DEBUGGING E TROUBLESHOOTING**

### **11. PROCESSO DE DEBUG** 🔍

#### **✅ Metodologia Sistemática:**
```python
# 1. ISOLE o problema:
print("Data shape:", df.shape)
print("Unique values:", df['column'].unique())
print("Null values:", df.isnull().sum())

# 2. TESTE incrementalmente:
fig = go.Figure()  # Figura vazia primeiro
fig.add_trace(...)  # Adicione um elemento
fig.show()         # Teste se renderiza

# 3. VALIDE dados:
assert len(labels) == len(parents) == len(values)
assert all(v >= 0 for v in values)  # Valores não-negativos
```

#### **❌ Debug Ineficiente:**
```python
❌ Tentar corrigir múltiplos problemas simultaneamente
❌ Não isolar o problema específico  
❌ Assumir que dados estão corretos sem validar
❌ Não testar cada mudança incrementalmente
```

### **12. SINAIS DE ALERTA** 🚨

#### **🔴 Pare e Reconsidere Se:**
```python
- O app não carrega após 10+ tentativas de correção
- Callbacks retornam erros de ID não encontrado
- Gráficos aparecem em branco/vazios
- Dados simulados não fazem sentido visualmente
- Código tem mais de 500 linhas e não funciona
- Imports têm warnings de deprecation
```

#### **✅ Quando Isso Acontecer:**
```python
1. PARE de tentar corrigir
2. ANALISE código que funciona (como HTML)
3. EXTRAIA dados reais funcionais  
4. REESCREVA com abordagem incremental (V1→V2→V3)
5. TESTE cada passo individualmente
```

---

## 📚 **RECURSOS E REFERÊNCIAS**

### **13. DOCUMENTAÇÃO OFICIAL** 📖
```python
# SEMPRE consulte documentação atual:
- Dash: https://dash.plotly.com/
- Plotly: https://plotly.com/python/
- Sklearn: https://scikit-learn.org/

# ❌ Evite tutoriais antigos (< 2023)
# ❌ Evite Stack Overflow sem verificar data
```

### **14. VALIDAÇÃO DE CÓDIGO** ✅
```python
# Antes de considerar "terminado":
✅ App carrega sem erros
✅ Todos os filtros funcionam
✅ Gráficos são interativos
✅ Tooltips mostram dados corretos
✅ Design é responsivo
✅ Não há warnings no console
✅ Código está comentado
✅ README está atualizado
```

---

## 🎓 **RESUMO PARA MODELOS DE IA**

### **PRIORIDADES (em ordem):**
1. **FUNCIONALIDADE** > Complexidade
2. **DADOS REAIS** > Dados simulados  
3. **CÓDIGO SIMPLES** > Código "elegante"
4. **TESTES CONSTANTES** > Desenvolvimento extenso
5. **DOCUMENTAÇÃO** > Código sem explicação

### **PROCESSO OBRIGATÓRIO:**
```
1. Analise → 2. Extraia → 3. Simplifique → 4. Teste → 5. Itere
     ↓           ↓           ↓            ↓         ↓
  HTML real   Dados reais   V1 básico    Valida   V2,V3
```

### **SINAIS DE SUCESSO:**
- ✅ Dashboard carrega em < 5s
- ✅ Interações funcionam perfeitamente
- ✅ Código tem < 200 linhas para funcionalidade básica
- ✅ Zero warnings/errors no console
- ✅ Visualmente atraente e informativo

---

**🤖 Para Modelos de IA: Este documento foi criado com base em experiência real de debugging. Siga estas diretrizes religiosamente para evitar horas de problemas desnecessários.**
