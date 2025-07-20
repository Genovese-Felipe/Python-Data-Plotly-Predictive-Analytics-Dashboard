# 📊 Specialized Charts - Gráficos Avançados e Especializados

Esta pasta contém **recursos específicos** para implementar visualizações complexas e especializadas que vão além dos gráficos básicos.

## 🌞 **Sunburst Charts - Gráficos Hierárquicos**

### **Recursos Disponíveis:**
- `How to Wrap Text in Plotly's Sunburst Diagram.pdf`
- `Multi-Level Sunburst Charts using Plotly and Pytho.pdf`
- `Multiple leaves on Sunburst Chart - 📊 Plotly Python.pdf`
- `multi-level sunburst chart using plotly and python 2.pdf`
- `python - How to wrap text in plotly.py's sunburst diagram_.pdf`

### **Casos de Uso Ideais:**
```python
# Sunburst é perfeito para:
- Estruturas organizacionais (Empresa → Departamento → Equipe → Pessoa)
- Categorização de produtos (Categoria → Subcategoria → Produto → Variação)
- Análise de orçamento (Área → Projeto → Item → Subitem)
- Navegação de websites (Seção → Página → Subpágina → Ação)
```

### **Implementação Base:**
```python
import plotly.graph_objects as go

# Estrutura de dados hierárquica
fig = go.Figure(go.Sunburst(
    labels=["Total", "Vendas", "Marketing", "Produto A", "Produto B"],
    parents=["", "Total", "Total", "Vendas", "Vendas"],
    values=[100, 60, 40, 35, 25],
    branchvalues="total"  # ou "remainder"
))

# Customizações avançadas
fig.update_layout(
    title="Distribuição Hierárquica",
    font_size=12
)
```

---

## 🗺️ **Mapas Interativos**

### **Recursos Disponíveis:**
- `Mapas em Dashboards Web com Plotly em Python.pdf`
- `__Mapas em Dashboards para Web Apps HTML com Pytho.pdf`
- `Plotly-Dash Interactive Mapping. Following on from an article written by….pdf`

### **Tipos de Mapas Suportados:**

#### **1. Mapas Choropleth (Regiões Coloridas)**
```python
import plotly.express as px

# Mapa do Brasil por estados
fig = px.choropleth(
    df, 
    locations='estado_sigla',
    color='valor_metrica',
    locationmode='geojson-id',
    scope='south america'
)
```

#### **2. Scatter Maps (Pontos Geográficos)**
```python
# Pontos em coordenadas específicas
fig = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    size='tamanho_bolha',
    color='categoria',
    hover_name='cidade'
)
```

#### **3. Density Maps (Mapas de Densidade)**
```python
# Densidade de eventos por região
fig = px.density_mapbox(
    df, 
    lat='lat', 
    lon='lon',
    radius=10,
    mapbox_style='open-street-map'
)
```

### **Integração com Dashboards:**
```python
# Callbacks para interatividade
@app.callback(
    Output('mapa', 'figure'),
    Input('filtro-regiao', 'value')
)
def atualizar_mapa(regiao_selecionada):
    df_filtrado = df[df['regiao'] == regiao_selecionada]
    return criar_mapa_choropleth(df_filtrado)
```

---

## 📈 **Padrões de Implementação Avançada**

### **Sunburst com Drill-Down:**
```python
# Multi-nível interativo
def criar_sunburst_dinamico(dados_hierarquicos):
    fig = go.Figure(go.Sunburst(
        labels=dados_hierarquicos['labels'],
        parents=dados_hierarquicos['parents'],
        values=dados_hierarquicos['values'],
        
        # Configurações avançadas
        maxdepth=3,  # Profundidade máxima
        insidetextorientation='radial',
        
        # Hover personalizado
        hovertemplate='<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percentParent}'
    ))
    
    return fig
```

### **Mapas com Múltiplas Camadas:**
```python
# Combinação de scatter + choropleth
def criar_mapa_multicamada(df_regioes, df_pontos):
    fig = go.Figure()
    
    # Camada 1: Regiões (choropleth)
    fig.add_trace(go.Choropleth(...))
    
    # Camada 2: Pontos específicos
    fig.add_trace(go.Scattergeo(...))
    
    return fig
```

---

## 🎯 **Casos de Uso Empresariais**

### **Dashboard Executivo com Sunburst:**
```
Cenário: Análise de receita por divisão
├── Total Empresa ($10M)
    ├── Divisão América ($6M)
    │   ├── Brasil ($2.5M)
    │   └── EUA ($3.5M)
    └── Divisão Europa ($4M)
        ├── Alemanha ($2.2M)
        └── França ($1.8M)
```

### **Dashboard Logístico com Mapas:**
```
Cenário: Rastreamento de entregas
- Mapa choropleth: Volume por estado
- Scatter points: Centros de distribuição
- Density map: Concentração de pedidos
- Filtros: Por período, transportadora
```

---

## 🛠️ **Ferramentas e Configurações**

### **Performance para Gráficos Complexos:**
```python
# Otimizações recomendadas
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    # Reduzir rerenders
    uirevision='constant',
    
    # Otimizar hover
    hovermode='closest',
    
    # Controlar zoom
    dragmode='pan'
)

# Para datasets grandes
fig.update_traces(
    # Simplificar geometrias
    simplify=True,
    
    # Limitar pontos visíveis
    visible='legendonly'  # Mostrar apenas quando selecionado
)
```

### **Responsividade:**
```python
# Adaptação automática para mobile
fig.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=50, b=0),
    
    # Para mapas
    geo=dict(
        projection_scale=1,
        center_lat=-15,  # Centro do Brasil
        center_lon=-55
    )
)
```

---

## ⚡ **Quick Start - Exemplos Prontos**

### **Sunburst Básico Funcional:**
```python
# Copie e execute este código
import plotly.graph_objects as go

labels = ["Empresa", "TI", "Vendas", "Python", "JavaScript", "B2B", "B2C"]
parents = ["", "Empresa", "Empresa", "TI", "TI", "Vendas", "Vendas"]
values = [100, 40, 60, 25, 15, 35, 25]

fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values
))

fig.show()
```

### **Mapa Brasil Funcional:**
```python
# Mapa choropleth simples
import plotly.express as px

# Dados de exemplo
df = pd.DataFrame({
    'estado': ['SP', 'RJ', 'MG', 'RS'],
    'valor': [1000, 800, 600, 400]
})

fig = px.choropleth(
    df,
    locations='estado',
    color='valor',
    locationmode='geojson-id',
    scope='south america'
)

fig.show()
```

---

**🎯 Dica:** Use os PDFs desta pasta como **referência técnica detalhada** quando precisar implementar funcionalidades específicas como wrapping de texto ou múltiplas camadas em mapas.
