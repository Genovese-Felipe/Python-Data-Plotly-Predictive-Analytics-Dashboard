---
layout: page
title: "Exemplos Práticos"
description: "Código fonte e casos de uso reais"
permalink: /examples/
---

# 💡 Exemplos Práticos e Código Fonte

Explore exemplos completos, código fonte documentado e casos de uso reais para criar seus próprios dashboards profissionais.

---

## 🎯 Exemplo Principal: Construction Dashboard

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0;">
  <h3 style="margin-top: 0; color: white;">🏗️ Dashboard de Gestão de Projetos de Construção</h3>
  <p style="font-size: 18px;">Implementação completa com 800+ linhas de código Python, 6 datasets e 10+ visualizações interativas.</p>
</div>

### 📁 Estrutura do Código

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# scripts/viz.py - Dashboard Principal (800+ linhas)
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

class ConstructionDashboard:
    """
    Dashboard profissional para gestão de projetos de construção
    
    Features:
    - 8 KPIs executivos
    - 10+ tipos de visualizações
    - Filtros interativos
    - Export HTML otimizado
    - Tema corporativo
    """
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.data = {}
        self.load_all_data()
        self.setup_layout()
    
    def load_all_data(self):
        """Carrega todos os datasets CSV"""
        self.data['projects'] = pd.read_csv('data/projects_master.csv')
        self.data['budget'] = pd.read_csv('data/budget_variance.csv')
        # ... outros datasets
    
    def create_kpi_section(self):
        """Cria seção de KPIs executivos"""
        projects_df = self.data['projects']
        total_projects = len(projects_df)
        total_budget = projects_df['budget'].sum()
        
        return html.Div([
            self.create_kpi_card("Total Projects", total_projects, "number"),
            self.create_kpi_card("Total Budget", total_budget/1000000, "currency"),
        ])
    
    def create_status_distribution_chart(self):
        """Gráfico de distribuição de status"""
        status_counts = self.data['projects']['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index)
        return dcc.Graph(figure=fig)
```

</div>

### 🔥 Link para Código Completo

<div style="text-align: center; margin: 30px 0;">
  <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/blob/main/scripts/viz.py" 
     target="_blank"
     style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); display: inline-block;">
    📄 Ver Código Completo no GitHub
  </a>
</div>

---

## 🎲 Exemplo: Geração de Dados Sintéticos

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin: 20px 0;">
  <h4>📊 Como Criar Dados Realísticos</h4>
  <p>Script que gera 2,508 registros com lógica de negócio realística:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# scripts/data_gen.py - Exemplo Simplificado
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_construction_projects(n_projects=25):
    """Gera dados sintéticos de projetos de construção"""
    
    projects = []
    project_types = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
    managers = ['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson']
    
    for i in range(n_projects):
        project_type = np.random.choice(project_types)
        
        # Budget realístico baseado no tipo
        budget_ranges = {
            'Infrastructure': (1000000, 5000000),
            'Commercial': (500000, 2000000),
            'Industrial': (800000, 3000000),
            'Residential': (100000, 800000)
        }
        
        budget = np.random.uniform(*budget_ranges[project_type])
        
        # Datas e progresso realísticos
        start_date = datetime.now() - timedelta(days=np.random.randint(0, 365))
        duration = np.random.randint(30, 730)
        end_date = start_date + timedelta(days=duration)
        
        project = {
            'project_id': f'PROJ_{i+1:03d}',
            'name': f'Construction Project {i+1}',
            'type': project_type,
            'manager': np.random.choice(managers),
            'budget': round(budget, 2),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'completion_rate': np.random.uniform(10, 95)
        }
        
        projects.append(project)
    
    return pd.DataFrame(projects)

# Gerar e salvar dados
projects_df = generate_construction_projects()
projects_df.to_csv('data/projects_master.csv', index=False)
print(f"✅ Generated {len(projects_df)} projects")
```

</div>

---

## 🎨 Exemplo: Sistema de Temas

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #6c5ce7; margin: 20px 0;">
  <h4>🌈 Tema Corporativo Reutilizável</h4>
  <p>Sistema de cores e estilos consistentes:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# themes/corporate.py
class CorporateTheme:
    COLORS = {
        'primary_blue': '#2E86AB',
        'primary_pink': '#A23B72', 
        'primary_orange': '#F18F01',
        'primary_red': '#C73E1D',
        'background': '#F5F5F5',
        'surface': '#FFFFFF'
    }
    
    @classmethod
    def get_plotly_template(cls):
        return {
            'layout': {
                'colorway': list(cls.COLORS.values())[:4],
                'paper_bgcolor': cls.COLORS['background'],
                'plot_bgcolor': cls.COLORS['surface'],
                'font': {'family': '"Segoe UI", sans-serif'}
            }
        }
    
    @classmethod
    def apply_to_figure(cls, fig):
        template = cls.get_plotly_template()
        fig.update_layout(template['layout'])
        return fig

# Uso do tema
fig = px.bar(data, x='category', y='values')
fig = CorporateTheme.apply_to_figure(fig)
```

</div>

---

## 🔄 Exemplo: Callbacks Interativos

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #e74c3c; margin: 20px 0;">
  <h4>⚡ Filtros Dinâmicos</h4>
  <p>Callbacks que atualizam múltiplos gráficos simultaneamente:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# Exemplo de callback avançado
@app.callback(
    [Output('status-chart', 'figure'),
     Output('budget-chart', 'figure'),
     Output('kpi-section', 'children')],
    [Input('project-type-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_dashboard(selected_types, start_date, end_date):
    # Filtrar dados
    filtered_data = projects_df.copy()
    
    if selected_types:
        filtered_data = filtered_data[filtered_data['type'].isin(selected_types)]
    
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['start_date'] >= start_date) &
            (filtered_data['end_date'] <= end_date)
        ]
    
    # Criar gráficos atualizados
    status_fig = create_status_chart(filtered_data)
    budget_fig = create_budget_chart(filtered_data)
    kpis = create_kpi_cards(filtered_data)
    
    return status_fig, budget_fig, kpis

# Layout com filtros
app.layout = html.Div([
    # Filtros
    html.Div([
        dcc.Dropdown(
            id='project-type-filter',
            options=[{'label': t, 'value': t} for t in project_types],
            multi=True,
            placeholder="Select project types..."
        ),
        dcc.DatePickerRange(id='date-range-filter')
    ]),
    
    # KPIs e Gráficos
    html.Div(id='kpi-section'),
    dcc.Graph(id='status-chart'),
    dcc.Graph(id='budget-chart')
])
```

</div>

---

## 📊 Exemplo: Componentes Reutilizáveis

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #00b894; margin: 20px 0;">
  <h4>🧩 Sistema de Componentes</h4>
  <p>Componentes modulares para reutilização:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# components/kpi_card.py
def create_kpi_card(title, value, format_type="number", color="#2E86AB"):
    """Cria um card de KPI reutilizável"""
    
    # Formatação baseada no tipo
    if format_type == "currency":
        formatted_value = f"R$ {value/1000000:.1f}M"
    elif format_type == "percentage":
        formatted_value = f"{value:.1f}%"
    else:
        formatted_value = f"{value:,.0f}"
    
    return html.Div([
        html.H3(formatted_value, style={
            'fontSize': '2.5rem',
            'fontWeight': 'bold',
            'color': color,
            'margin': '0'
        }),
        html.P(title, style={
            'color': '#666',
            'margin': '5px 0 0 0'
        })
    ], style={
        'background': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
        'textAlign': 'center',
        'borderLeft': f'5px solid {color}'
    })

# Uso do componente
kpi_section = html.Div([
    create_kpi_card("Total Projects", 25, "number", "#2E86AB"),
    create_kpi_card("Total Budget", 15200000, "currency", "#A23B72"),
    create_kpi_card("Completion", 76.2, "percentage", "#F18F01")
], style={
    'display': 'grid',
    'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
    'gap': '20px'
})
```

</div>

---

## 🚀 Exemplo: Deploy Automático

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #fd79a8; margin: 20px 0;">
  <h4>⚙️ GitHub Actions para Deploy</h4>
  <p>Automação completa de build e deploy:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy Dashboard

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate data
      run: |
        python scripts/data_gen.py
    
    - name: Build dashboard
      run: |
        python scripts/viz.py --export-html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

</div>

---

## 📁 Repositório Completo

<div style="text-align: center; background: #f8f9fa; padding: 40px; border-radius: 15px; margin: 40px 0;">
  <h3>🔗 Código Fonte Completo</h3>
  <p>Explore o repositório completo com todos os exemplos, documentação e implementações:</p>
  
  <div style="margin: 25px 0;">
    <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard" 
       target="_blank"
       style="background: #28a745; color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 0 10px; display: inline-block;">
      📂 Ver Repositório Completo
    </a>
    
    <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/fork" 
       target="_blank"
       style="background: #007bff; color: white; padding: 15px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 0 10px; display: inline-block;">
      🔄 Fork do Projeto
    </a>
  </div>
  
  <div style="margin: 20px 0;">
    <p style="color: #666;">
      <strong>Estatísticas:</strong> 800+ linhas de código Python | 6 datasets | 10+ visualizações | 40K+ palavras de documentação
    </p>
  </div>
</div>

---

## 📚 Próximos Passos

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 40px 0;">

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>📊 Dashboards Live</h4>
  <p>Veja os dashboards funcionando em tempo real</p>
  <a href="../dashboards.html" style="color: #007bff; text-decoration: none; font-weight: bold;">Explorar Dashboards →</a>
</div>

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>📚 Tutoriais</h4>
  <p>Aprenda a criar seus próprios dashboards</p>
  <a href="../tutorials.html" style="color: #28a745; text-decoration: none; font-weight: bold;">Começar Tutorial →</a>
</div>

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>🧠 Knowledge Base</h4>
  <p>60+ recursos para aprendizado avançado</p>
  <a href="../knowledge-base.html" style="color: #ffc107; text-decoration: none; font-weight: bold;">Explorar Conhecimento →</a>
</div>

</div>

---

<div style="text-align: center; padding: 20px; color: #666; border-top: 1px solid #eee; margin-top: 50px;">
  <p><strong>💡 Dica:</strong> Use estes exemplos como base para seus próprios projetos. Todo código está comentado e documentado!</p>
</div>