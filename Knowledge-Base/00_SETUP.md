# ⚙️ SETUP & CONFIGURATION - Configuração de Ambiente

Este guia garante que você tenha **tudo configurado corretamente** antes de começar o desenvolvimento. Evite 90% dos problemas seguindo este setup.

---

## 🐍 **PYTHON ENVIRONMENT SETUP**

### **Versão Recomendada**
```bash
# Python 3.8+ (testado até 3.11)
python --version
# Deve mostrar: Python 3.8.x ou superior
```

### **Virtual Environment (Recomendado)**
```bash
# Criar ambiente virtual
python -m venv venv_dash

# Ativar (Linux/Mac)
source venv_dash/bin/activate

# Ativar (Windows)
venv_dash\Scripts\activate

# Verificar ativação
which python  # Deve mostrar path do venv
```

---

## 📦 **DEPENDÊNCIAS ESSENCIAIS**

### **Core Requirements**
```bash
# Instalação básica (sempre necessária)
pip install dash plotly pandas numpy

# Verificar instalação
python -c "import dash, plotly, pandas, numpy; print('✅ Core libs OK')"
```

### **Requirements Expandidos**
```bash
# Para projetos avançados
pip install dash-bootstrap-components
pip install scikit-learn  # Para ML
pip install gunicorn      # Para deploy
pip install redis         # Para cache
pip install sqlalchemy    # Para databases

# Salvar requirements
pip freeze > requirements.txt
```

### **Requirements.txt Template**
```text
# Core dashboard
dash==2.14.1
plotly==5.17.0
pandas==2.0.3
numpy==1.24.3

# UI/UX
dash-bootstrap-components==1.5.0

# Data science (opcional)
scikit-learn==1.3.0
scipy==1.11.1

# Production (opcional)
gunicorn==21.2.0
redis==4.6.0
```

---

## 🗂️ **ESTRUTURA DE PROJETO RECOMENDADA**

### **Template de Pastas**
```
meu_dashboard_projeto/
├── .env                    # Variáveis ambiente
├── .gitignore             # Git ignore
├── requirements.txt       # Dependências
├── README.md             # Documentação projeto
├── 
├── data/                 # Dados (não versionar se grandes)
│   ├── raw/             # Dados brutos originais
│   ├── processed/       # Dados processados
│   └── synthetic/       # Dados gerados
├── 
├── src/                  # Código fonte
│   ├── __init__.py
│   ├── app.py           # Aplicação principal
│   ├── config.py        # Configurações
│   ├── 
│   ├── components/      # Componentes reutilizáveis
│   │   ├── __init__.py
│   │   ├── charts.py    # Funções de gráficos
│   │   └── layouts.py   # Layouts de UI
│   ├── 
│   ├── callbacks/       # Lógica de interatividade
│   │   ├── __init__.py
│   │   └── main_callbacks.py
│   ├── 
│   └── utils/           # Utilitários
│       ├── __init__.py
│       ├── data_loader.py
│       └── helpers.py
├── 
├── assets/              # CSS, JS, imagens
│   ├── style.css
│   └── images/
├── 
├── tests/               # Testes (opcional)
│   └── test_app.py
├── 
└── outputs/             # Resultados finais
    ├── dashboard.html   # Dashboard exportado
    └── screenshots/     # Capturas de tela
```

### **Comando para Criar Estrutura**
```bash
# Execute este script para criar todas as pastas
mkdir -p meu_dashboard_projeto/{data/{raw,processed,synthetic},src/{components,callbacks,utils},assets/images,tests,outputs/screenshots}

# Criar arquivos vazios essenciais
touch meu_dashboard_projeto/src/__init__.py
touch meu_dashboard_projeto/src/components/__init__.py
touch meu_dashboard_projeto/src/callbacks/__init__.py
touch meu_dashboard_projeto/src/utils/__init__.py
touch meu_dashboard_projeto/requirements.txt
touch meu_dashboard_projeto/.gitignore
```

---

## 🔧 **CONFIGURAÇÃO DE DESENVOLVIMENTO**

### **VS Code Setup (Recomendado)**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv_dash/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### **Git Configuration**
```bash
# .gitignore template
echo "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv*/
.venv/

# Data files (adjust as needed)
data/raw/
*.csv
*.xlsx
*.db

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Dash
assets/plotly.min.js

# Environment
.env
*.log" > .gitignore
```

### **Environment Variables**
```bash
# .env template
# Database
DATABASE_URL=sqlite:///database.db

# Dashboard
DASH_DEBUG=True
DASH_HOST=0.0.0.0
DASH_PORT=8050

# Cache
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300

# API Keys (se necessário)
# OPENAI_API_KEY=your_key_here
# GOOGLE_MAPS_API_KEY=your_key_here
```

---

## 🔍 **VALIDAÇÃO DO SETUP**

### **Script de Teste Completo**
```python
# test_setup.py - Execute para validar seu ambiente

def test_imports():
    """Testa se todas as bibliotecas essenciais foram instaladas"""
    try:
        import dash
        import plotly
        import pandas as pd
        import numpy as np
        print("✅ Core libraries: OK")
        
        # Teste versões mínimas
        assert dash.__version__ >= '2.0.0', f"Dash muito antigo: {dash.__version__}"
        assert plotly.__version__ >= '5.0.0', f"Plotly muito antigo: {plotly.__version__}"
        print("✅ Versions: OK")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except AssertionError as e:
        print(f"⚠️ Version warning: {e}")
    
    return True

def test_basic_dashboard():
    """Cria dashboard mínimo para testar funcionalidade"""
    try:
        from dash import Dash, dcc, html
        import plotly.express as px
        
        # Dados teste
        df = pd.DataFrame({'x': [1,2,3], 'y': [1,4,2]})
        
        # App mínimo
        app = Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(figure=px.line(df, x='x', y='y'))
        ])
        
        print("✅ Dashboard creation: OK")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        return False

def test_data_generation():
    """Testa geração de dados sintéticos"""
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Gerar dados teste
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'value': np.random.normal(100, 15, len(dates))
        })
        
        assert len(df) > 0, "DataFrame vazio"
        assert 'date' in df.columns, "Coluna date ausente"
        
        print("✅ Data generation: OK")
        return True
        
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Validando setup do ambiente...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Dashboard", test_basic_dashboard), 
        ("Data Generation", test_data_generation)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testando {name}...")
        results.append(test_func())
        print()
    
    if all(results):
        print("🎉 Setup completo! Você está pronto para desenvolver dashboards.")
    else:
        print("⚠️ Alguns testes falharam. Revise a instalação.")
        print("💡 Consulte 00_TROUBLESHOOTING.md para ajuda.")
```

### **Executar Validação**
```bash
# Execute o teste
python test_setup.py

# Se tudo OK, você verá:
# 🎉 Setup completo! Você está pronto para desenvolver dashboards.
```

---

## 🚀 **QUICK START PÓS-SETUP**

### **Primeiro Dashboard (5 minutos)**
```python
# primeiro_dashboard.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Dados exemplo
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Grapes'],
    'Amount': [4, 1, 2, 2]
})

# App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Meu Primeiro Dashboard! 🎉"),
    dcc.Graph(
        figure=px.bar(df, x='Fruit', y='Amount', title="Frutas Favoritas")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
    print("Dashboard rodando em: http://localhost:8050")
```

### **Executar**
```bash
python primeiro_dashboard.py
# Abra browser em: http://localhost:8050
```

---

## 🛠️ **TROUBLESHOOTING SETUP**

### **Problemas Comuns**

**❌ "ModuleNotFoundError: No module named 'dash'"**
```bash
# Solução:
pip install dash

# Se persiste, verificar Python/pip:
which python
which pip
```

**❌ "Port 8050 is already in use"**
```python
# Solução: Mude a porta
app.run_server(debug=True, port=8051)
```

**❌ "Permission denied" no Linux/Mac**
```bash
# Solução: Use virtual environment
python3 -m venv venv_dash
source venv_dash/bin/activate
pip install dash plotly pandas numpy
```

---

## 📋 **CHECKLIST FINAL**

### **✅ Antes de Começar Qualquer Projeto:**
- [ ] Python 3.8+ instalado
- [ ] Virtual environment ativado
- [ ] Core libraries instaladas (dash, plotly, pandas, numpy)
- [ ] Estrutura de pastas criada
- [ ] test_setup.py passou todos os testes
- [ ] primeiro_dashboard.py rodou com sucesso

### **✅ Para Projetos Avançados:**
- [ ] dash-bootstrap-components instalado
- [ ] scikit-learn instalado (se ML)
- [ ] .env configurado
- [ ] .gitignore configurado
- [ ] requirements.txt atualizado

---

**🎯 Com este setup, você está 100% preparado para seguir qualquer tutorial da Knowledge-Base sem problemas de ambiente!**
