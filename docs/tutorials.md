---
layout: page
title: "Tutoriais"
description: "Guias passo a passo para criar dashboards profissionais"
permalink: /tutorials/
---

# 📚 Tutoriais Completos

Aprenda a criar dashboards profissionais com **Python**, **Plotly** e **Dash** através de nossos tutoriais detalhados e exemplos práticos.

---

## 🚀 Quick Start - Seu Primeiro Dashboard

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0;">
  <h3 style="margin-top: 0; color: white;">⚡ Começe em 5 Minutos</h3>
  <p style="font-size: 18px;">Tutorial rápido para criar seu primeiro dashboard interativo usando nosso template.</p>
</div>

### 📋 Pré-requisitos

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin: 20px 0;">
  <h4>🔧 Ambiente de Desenvolvimento</h4>
  <ul>
    <li><strong>Python 3.8+</strong> - Linguagem principal</li>
    <li><strong>pip</strong> - Gerenciador de pacotes Python</li>
    <li><strong>Git</strong> - Controle de versão</li>
    <li><strong>Editor de código</strong> - VS Code, PyCharm, ou similar</li>
  </ul>
</div>

### 🛠️ Instalação Passo a Passo

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```bash
# 1. Clone o repositório
git clone https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
cd Python-Data-Plotly-Predictive-Analytics-Dashboard

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Gere os dados sintéticos
python scripts/data_gen.py

# 5. Execute o dashboard
python scripts/viz.py

# 6. Acesse no navegador
# http://localhost:8050
```

</div>

### 🎯 Resultado Esperado

Após seguir os passos acima, você terá:

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">

<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
  <h4>📊 Dashboard Local</h4>
  <p>Dashboard rodando em localhost:8050 com todas as funcionalidades</p>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
  <h4>📁 Dados Gerados</h4>
  <p>6 datasets CSV com 2,508 registros sintéticos realísticos</p>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
  <h4>🎨 Visualizações</h4>
  <p>10+ tipos diferentes de gráficos interativos</p>
</div>

</div>

---

## 📖 Tutorial Detalhado: Anatomia do Dashboard

### 🧩 1. Estrutura do Projeto

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```
Python-Data-Plotly-Predictive-Analytics-Dashboard/
├── 📁 data/                    # Dados CSV gerados
│   ├── projects_master.csv     # Dados principais dos projetos
│   ├── budget_variance.csv     # Variações orçamentárias
│   ├── project_status.csv      # Status dos projetos
│   ├── project_stages.csv      # Cronogramas e marcos
│   ├── resources.csv          # Recursos e equipes
│   └── workload.csv           # Distribuição de trabalho
├── 📁 scripts/                # Scripts Python
│   ├── data_gen.py           # 🔄 Gerador de dados
│   └── viz.py                # 📊 Criador do dashboard
├── 📁 outputs/               # Dashboards HTML exportados
│   └── dashboard.html        # 🌐 Dashboard final
└── 📁 docs/                  # Site GitHub Pages
    └── ...                   # Documentação e tutoriais
```

</div>

### 🎲 2. Geração de Dados Sintéticos

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin: 20px 0;">
  <h4>📊 Como os Dados São Criados</h4>
  <p>O script <code>data_gen.py</code> cria dados realísticos seguindo padrões de negócio reais:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# Exemplo simplificado do data_gen.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Definir parâmetros do negócio
PROJECT_TYPES = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
PROJECT_STATUS = ['Planning', 'In Progress', 'On Hold', 'Completed']
MANAGERS = ['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson']

# 2. Gerar dados mestres dos projetos
def generate_projects_data(n_projects=25):
    projects = []
    for i in range(n_projects):
        project = {
            'project_id': f'PROJ_{i+1:03d}',
            'name': f'Construction Project {i+1}',
            'type': np.random.choice(PROJECT_TYPES),
            'manager': np.random.choice(MANAGERS),
            'status': np.random.choice(PROJECT_STATUS),
            'budget': np.random.uniform(50000, 5000000),
            'start_date': datetime.now() - timedelta(days=np.random.randint(0, 365)),
            'end_date': datetime.now() + timedelta(days=np.random.randint(30, 365))
        }
        projects.append(project)
    
    return pd.DataFrame(projects)

# 3. Salvar dados
projects_df = generate_projects_data()
projects_df.to_csv('data/projects_master.csv', index=False)
```

</div>

### 🎨 3. Criação das Visualizações

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">
  <h4>📈 Estrutura do Dashboard</h4>
  <p>O script <code>viz.py</code> usa programação orientada a objetos para organizar o código:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# Exemplo simplificado do viz.py
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

class ConstructionDashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.load_data()
        self.setup_layout()
        self.setup_callbacks()
    
    def load_data(self):
        """Carrega todos os dados CSV"""
        self.projects = pd.read_csv('data/projects_master.csv')
        self.budget = pd.read_csv('data/budget_variance.csv')
        # ... outros datasets
    
    def create_kpi_cards(self):
        """Cria cards com KPIs principais"""
        total_projects = len(self.projects)
        total_budget = self.projects['budget'].sum()
        
        return html.Div([
            html.Div([
                html.H3(f"{total_projects}", className="kpi-number"),
                html.P("Total Projects", className="kpi-label")
            ], className="kpi-card"),
            
            html.Div([
                html.H3(f"R$ {total_budget/1000000:.1f}M", className="kpi-number"),
                html.P("Total Budget", className="kpi-label")
            ], className="kpi-card")
        ], className="kpi-container")
    
    def create_status_distribution(self):
        """Cria gráfico de distribuição de status"""
        status_counts = self.projects['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Project Status Distribution"
        )
        return dcc.Graph(figure=fig)
    
    def setup_layout(self):
        """Define o layout principal"""
        self.app.layout = html.Div([
            html.H1("Construction Project Dashboard"),
            self.create_kpi_cards(),
            self.create_status_distribution(),
            # ... mais visualizações
        ])
    
    def run(self):
        """Executa o dashboard"""
        self.app.run_server(debug=True)

# Executar o dashboard
if __name__ == '__main__':
    dashboard = ConstructionDashboard()
    dashboard.run()
```

</div>

---

## 🎨 Tutorial: Customização e Temas

### 🌈 Sistema de Cores Corporativas

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #6c5ce7; margin: 20px 0;">
  <h4>🎯 Paleta de Cores Profissional</h4>
  <p>Aprenda a criar um sistema de cores consistente para seus dashboards:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# themes/corporate.py
class CorporateTheme:
    # Cores principais
    PRIMARY_COLORS = {
        'blue': '#2E86AB',      # Azul corporativo
        'pink': '#A23B72',      # Rosa de destaque  
        'orange': '#F18F01',    # Laranja sucesso
        'red': '#C73E1D',       # Vermelho alerta
    }
    
    # Cores de fundo
    BACKGROUND_COLORS = {
        'primary': '#F5F5F5',   # Cinza claro
        'surface': '#FFFFFF',   # Branco
        'card': '#FAFAFA',      # Cinza card
    }
    
    # Aplicar tema no Plotly
    def get_plotly_template(self):
        return {
            'layout': {
                'colorway': list(self.PRIMARY_COLORS.values()),
                'paper_bgcolor': self.BACKGROUND_COLORS['primary'],
                'plot_bgcolor': self.BACKGROUND_COLORS['surface'],
                'font': {'family': '"Segoe UI", sans-serif', 'size': 12}
            }
        }

# Usar o tema
theme = CorporateTheme()
fig.update_layout(template=theme.get_plotly_template())
```

</div>

### 🎛️ CSS Customizado

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```css
/* assets/style.css */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 5px solid #2E86AB;
}

.kpi-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2E86AB;
    margin: 0;
}

.kpi-label {
    color: #666;
    margin: 5px 0 0 0;
    font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
    .kpi-container {
        grid-template-columns: 1fr;
    }
}
```

</div>

---

## 🔄 Tutorial: Interatividade e Callbacks

### ⚡ Criando Filtros Dinâmicos

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #e74c3c; margin: 20px 0;">
  <h4>🎛️ Sistema de Filtros Avançados</h4>
  <p>Aprenda a criar filtros que atualizam múltiplos gráficos simultaneamente:</p>
</div>

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```python
# Exemplo de callbacks para filtros interativos
@app.callback(
    [Output('status-chart', 'figure'),
     Output('budget-chart', 'figure'),
     Output('timeline-chart', 'figure')],
    [Input('project-type-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date'),
     Input('manager-filter', 'value')]
)
def update_charts(selected_types, start_date, end_date, selected_managers):
    # Filtrar dados baseado nas seleções
    filtered_data = projects_df.copy()
    
    if selected_types:
        filtered_data = filtered_data[filtered_data['type'].isin(selected_types)]
    
    if selected_managers:
        filtered_data = filtered_data[filtered_data['manager'].isin(selected_managers)]
    
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['start_date'] >= start_date) &
            (filtered_data['end_date'] <= end_date)
        ]
    
    # Criar gráficos atualizados
    status_fig = create_status_chart(filtered_data)
    budget_fig = create_budget_chart(filtered_data)
    timeline_fig = create_timeline_chart(filtered_data)
    
    return status_fig, budget_fig, timeline_fig

# Componentes de filtro no layout
filters = html.Div([
    html.Div([
        html.Label("Project Type:"),
        dcc.Dropdown(
            id='project-type-filter',
            options=[{'label': t, 'value': t} for t in PROJECT_TYPES],
            multi=True,
            placeholder="Select project types..."
        )
    ], className="filter-item"),
    
    html.Div([
        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id='date-range-filter',
            start_date=projects_df['start_date'].min(),
            end_date=projects_df['end_date'].max()
        )
    ], className="filter-item"),
    
    html.Div([
        html.Label("Manager:"),
        dcc.Dropdown(
            id='manager-filter',
            options=[{'label': m, 'value': m} for m in MANAGERS],
            multi=True,
            placeholder="Select managers..."
        )
    ], className="filter-item")
], className="filters-container")
```

</div>

---

## 📤 Tutorial: Deploy no GitHub Pages

### 🚀 Configuração do GitHub Pages

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin: 20px 0;">
  <h4>🌐 Publicando Seu Dashboard</h4>
  <p>Passos para colocar seu dashboard online gratuitamente:</p>
</div>

#### 1️⃣ Preparação dos Arquivos

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```bash
# 1. Criar pasta docs (se não existir)
mkdir docs

# 2. Exportar dashboard como HTML estático
python scripts/viz.py --export-html --output docs/index.html

# 3. Copiar assets necessários
cp -r assets/ docs/
cp outputs/*.html docs/

# 4. Criar estrutura do site
docs/
├── index.html          # Dashboard principal
├── dashboards.html     # Página de dashboards  
├── tutorials.html      # Esta página de tutoriais
├── assets/             # CSS, JS, imagens
└── _config.yml         # Configuração Jekyll
```

</div>

#### 2️⃣ Configuração do Repositório

<div style="background: #2d3748; color: #e2e8f0; padding: 25px; border-radius: 10px; margin: 30px 0;">

```yaml
# docs/_config.yml
title: "Meu Dashboard Plotly"
description: "Dashboard profissional com Python e Plotly"
baseurl: "/nome-do-seu-repositorio"
url: "https://seu-usuario.github.io"

# Configurações do GitHub Pages
plugins:
  - jekyll-feed
  - jekyll-sitemap

# Tema (opcional)
theme: minima
```

</div>

#### 3️⃣ Ativação do GitHub Pages

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
  <ol>
    <li>Vá para <strong>Settings</strong> do seu repositório</li>
    <li>Role até a seção <strong>Pages</strong></li>
    <li>Em <strong>Source</strong>, selecione <strong>"Deploy from a branch"</strong></li>
    <li>Escolha <strong>Branch: main</strong> e <strong>Folder: /docs</strong></li>
    <li>Clique <strong>Save</strong></li>
    <li>Aguarde alguns minutos e acesse: <code>https://seu-usuario.github.io/nome-repositorio</code></li>
  </ol>
</div>

#### 4️⃣ Automação com GitHub Actions

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
    
    - name: Generate data and build dashboard
      run: |
        python scripts/data_gen.py
        python scripts/viz.py --export-html --output docs/index.html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

</div>

---

## 🎯 Projetos Práticos

### 🏗️ Projeto 1: Dashboard de Vendas

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 15px; color: white; margin: 30px 0;">
  <h4 style="margin-top: 0; color: white;">🎯 Desafio Prático</h4>
  <p>Crie um dashboard de vendas usando os conceitos aprendidos. Dados de exemplo fornecidos.</p>
</div>

**Funcionalidades a implementar:**
- KPIs de vendas (receita, volume, crescimento)
- Gráfico de vendas por período
- Top produtos/vendedores
- Análise geográfica
- Filtros por região, período, produto

### 🏗️ Projeto 2: Dashboard de RH

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; margin: 30px 0;">
  <h4 style="margin-top: 0; color: white;">👥 Recursos Humanos</h4>
  <p>Dashboard para análise de métricas de RH com visualizações especializadas.</p>
</div>

**Funcionalidades a implementar:**
- Headcount por departamento
- Turnover analysis
- Performance ratings
- Salary analysis
- Diversity metrics

---

## 🤝 Comunidade e Suporte

<div style="text-align: center; background: #f8f9fa; padding: 40px; border-radius: 15px; margin: 40px 0;">
  <h3>💬 Precisa de Ajuda?</h3>
  <p>Nossa comunidade está aqui para ajudar você a criar dashboards incríveis!</p>
  
  <div style="margin: 25px 0;">
    <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/discussions" style="background: #28a745; color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; margin: 0 10px;">💬 Discussões</a>
    <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard/issues" style="background: #dc3545; color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; margin: 0 10px;">🐛 Report Bug</a>
    <a href="../examples.html" style="background: #007bff; color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; margin: 0 10px;">💡 Ver Exemplos</a>
  </div>
</div>

---

## 📚 Próximos Passos

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 40px 0;">

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>📊 Dashboards</h4>
  <p>Explore os dashboards prontos e veja o resultado final</p>
  <a href="../dashboards.html" style="color: #007bff; text-decoration: none; font-weight: bold;">Ver Dashboards →</a>
</div>

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>💡 Exemplos</h4>
  <p>Código fonte completo e casos de uso práticos</p>
  <a href="../examples.html" style="color: #28a745; text-decoration: none; font-weight: bold;">Ver Código →</a>
</div>

<div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;">
  <h4>🧠 Knowledge Base</h4>
  <p>60+ recursos organizados para aprendizado avançado</p>
  <a href="../knowledge-base.html" style="color: #ffc107; text-decoration: none; font-weight: bold;">Explorar →</a>
</div>

</div>

---

<div style="text-align: center; padding: 20px; color: #666; border-top: 1px solid #eee; margin-top: 50px;">
  <p><strong>🎓 Continue Aprendendo:</strong> Este é apenas o começo! Explore nossa base de conhecimento para técnicas avançadas.</p>
</div>