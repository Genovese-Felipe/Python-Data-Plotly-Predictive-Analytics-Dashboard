# ⚙️ SETUP IA & PYTHON CODING - Configuração Completa de Ambiente

Este guia garante que você tenha **todo o ambiente de IA e Python configurado corretamente** antes de começar o desenvolvimento. Evite 90% dos problemas seguindo este setup otimizado para **desenvolvimento de IA**.

---

## 🐍 **PYTHON ENVIRONMENT PARA IA**

### **Versão Recomendada para IA**
```bash
# Python 3.8+ (recomendado 3.9+ para melhor compatibilidade com IA)
python --version
# Deve mostrar: Python 3.9.x ou superior (ideal para TensorFlow/PyTorch)
```

### **Virtual Environment Especializado em IA**
```bash
# Criar ambiente virtual específico para IA
python -m venv venv_ai_dashboard

# Ativar (Linux/Mac)
source venv_ai_dashboard/bin/activate

# Ativar (Windows)
venv_ai_dashboard\Scripts\activate

# Verificar ativação
which python  # Deve mostrar path do venv
pip list       # Deve estar limpo
```

---

## 📦 **DEPENDÊNCIAS DE IA E ML**

### **Core Requirements IA**
```bash
# Instalação básica sempre necessária
pip install dash plotly pandas numpy

# Machine Learning essencial
pip install scikit-learn matplotlib seaborn

# IA e NLP
pip install transformers sentence-transformers

# Verificar instalação
python -c "import dash, plotly, pandas, numpy, sklearn; print('✅ Core IA libs OK')"
```

### **Requirements Avançados para IA**
```bash
# Para projetos avançados de IA
pip install dash-bootstrap-components    # UI components
pip install torch torchvision           # Deep Learning (CPU)
pip install chromadb faiss-cpu          # Vector databases
pip install shap lime                   # Explainable AI
pip install optuna                      # Hyperparameter optimization
pip install mlflow                      # ML experiment tracking

# Para deploy de IA
pip install gunicorn uvicorn            # Production servers
pip install redis celery                # Background tasks
pip install docker                      # Containerization
```

### **GPU Acceleration (Opcional)**
```bash
# Para GPU NVIDIA (se disponível)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Verificar GPU
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```
---

## 🗂️ **ESTRUTURA DE PROJETO IA RECOMENDADA**

### **Template de Pastas para Projetos IA**
```
meu_projeto_ai_dashboard/
├── .env                    # Variáveis ambiente (API keys, etc.)
├── .gitignore             # Git ignore (inclui modelos grandes)
├── requirements.txt       # Dependências IA
├── README.md             # Documentação projeto
├── docker-compose.yml     # Para deploy com IA
├── 
├── data/                 # Dados para IA (não versionar se grandes)
│   ├── raw/             # Dados brutos originais
│   ├── processed/       # Dados processados para ML
│   ├── synthetic/       # Dados gerados
│   ├── embeddings/      # Vetores e embeddings
│   └── knowledge_base/  # Base de conhecimento para RAG
├── 
├── models/              # Modelos de IA treinados
│   ├── trained/         # Modelos .pkl, .pt, .h5
│   ├── experiments/     # Experimentos MLflow
│   └── checkpoints/     # Checkpoints de treino
├── 
├── src/                 # Código fonte IA
│   ├── __init__.py
│   ├── app.py          # Aplicação principal com IA
│   ├── config.py       # Configurações (incluindo IA)
│   ├── 
│   ├── ai/             # Módulos de IA
│   │   ├── __init__.py
│   │   ├── models.py   # Classes de modelos ML
│   │   ├── predictors.py # Sistemas de predição
│   │   ├── embeddings.py # Sistema de embeddings
│   │   └── explainer.py  # Explainable AI
│   ├── 
│   ├── components/     # Componentes UI com IA
│   │   ├── __init__.py
│   │   ├── ai_charts.py # Gráficos inteligentes
│   │   ├── ml_widgets.py # Widgets para ML
│   │   └── layouts.py   # Layouts responsivos
│   ├── 
│   ├── callbacks/      # Callbacks com IA
│   │   ├── __init__.py
│   │   ├── prediction_callbacks.py
│   │   └── search_callbacks.py
│   ├── 
│   └── utils/          # Utilitários IA
│       ├── __init__.py
│       ├── data_processor.py
│       ├── ai_helpers.py
│       └── monitoring.py
├── 
├── notebooks/          # Jupyter notebooks para experimentação
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── ai_experiments.ipynb
├── 
├── tests/              # Testes para IA
│   ├── test_models.py
│   ├── test_predictions.py
│   └── test_app.py
├── 
└── outputs/            # Resultados e deploy
    ├── dashboard.html  # Dashboard exportado
    ├── model_reports/  # Relatórios de modelos
    └── monitoring/     # Logs de monitoramento
```

### **Comando para Criar Estrutura IA**
```bash
# Script automático para criar estrutura
python -c "
import os
dirs = [
    'data/raw', 'data/processed', 'data/synthetic', 'data/embeddings', 'data/knowledge_base',
    'models/trained', 'models/experiments', 'models/checkpoints',
    'src/ai', 'src/components', 'src/callbacks', 'src/utils',
    'notebooks', 'tests', 'outputs/model_reports', 'outputs/monitoring', 'assets'
]
for d in dirs:
    os.makedirs(d, exist_ok=True)
    with open(f'{d}/__init__.py', 'w') as f:
        f.write('# AI Dashboard Module\\n')
print('✅ Estrutura IA criada!')
"
```

---

## 🔧 **CONFIGURAÇÃO DE DESENVOLVIMENTO IA**

### **IDE Setup para IA**
```bash
# VS Code extensions recomendadas para IA
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter  
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.pylint

# Configurar Python path para IA
echo 'export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"' >> ~/.bashrc
source ~/.bashrc
```

### **Environment Variables para IA**
Crie arquivo `.env`:
```bash
# API Keys para serviços de IA
OPENAI_API_KEY=your_openai_key_here
HUGGINGFACE_API_KEY=your_hf_key_here

# Configurações de modelos
MODEL_CACHE_DIR=./models/cache
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
MAX_SEQUENCE_LENGTH=512

# Configurações de performance
USE_GPU=False
BATCH_SIZE=32
N_WORKERS=4

# Redis para cache (se usando)
REDIS_URL=redis://localhost:6379

# Monitoramento
MLFLOW_TRACKING_URI=./models/experiments
LOG_LEVEL=INFO
```

### **Git Configuration para IA**
Crie `.gitignore` especializado:
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.Python
venv_ai_dashboard/

# Dados e modelos grandes
data/raw/*
!data/raw/.gitkeep
models/trained/*.pkl
models/trained/*.pt
models/trained/*.h5
*.onnx

# Notebooks checkpoints
.ipynb_checkpoints/

# Logs e experimentos
*.log
mlruns/
outputs/monitoring/*

# Environment
.env
.env.local

# Cache de modelos
models/cache/
.cache/

# GPU specific
*.cuda
```

---

## 🧪 **TESTES DE CONFIGURAÇÃO IA**

### **Teste Completo do Environment**
Crie `test_ai_setup.py`:
```python
#!/usr/bin/env python3
"""
Teste completo de configuração para IA e Python coding
"""

def test_basic_imports():
    """Testa imports básicos"""
    try:
        import dash, plotly, pandas, numpy
        print("✅ Core libraries OK")
        return True
    except ImportError as e:
        print(f"❌ Error importing core libs: {e}")
        return False

def test_ml_imports():
    """Testa imports de ML"""
    try:
        import sklearn
        from sklearn.linear_model import LinearRegression
        print("✅ Scikit-learn OK")
        return True
    except ImportError as e:
        print(f"❌ Error importing ML libs: {e}")
        return False

def test_ai_imports():
    """Testa imports de IA avançada"""
    try:
        import transformers
        from sentence_transformers import SentenceTransformer
        print("✅ Advanced AI libraries OK")
        return True
    except ImportError as e:
        print(f"⚠️  Advanced AI libs not available: {e}")
        return False

def test_gpu_availability():
    """Testa disponibilidade de GPU"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  GPU not available (CPU only)")
        return True
    except ImportError:
        print("⚠️  PyTorch not installed")
        return False

def test_project_structure():
    """Testa estrutura do projeto"""
    import os
    required_dirs = ['data', 'models', 'src', 'outputs']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory {dir_name} exists")
        else:
            print(f"❌ Directory {dir_name} missing")

def main():
    print("🧪 Testing AI & Python Coding Setup...")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_ml_imports, 
        test_ai_imports,
        test_gpu_availability,
        test_project_structure
    ]
    
    for test in tests:
        test()
        print()
    
    print("🎯 Setup test completed!")

if __name__ == "__main__":
    main()
```

Execute o teste:
```bash
python test_ai_setup.py
```

---

## 📋 **CHECKLIST DE SETUP COMPLETO**

### **✅ Ambiente Base**
- [ ] Python 3.9+ instalado
- [ ] Virtual environment criado e ativado
- [ ] Core libraries instaladas (dash, plotly, pandas, numpy)
- [ ] Estrutura de projeto criada

### **✅ IA e Machine Learning**
- [ ] Scikit-learn instalado e funcionando
- [ ] Transformers library instalada
- [ ] Sentence-transformers funcionando
- [ ] Teste de modelo simples executado

### **✅ Desenvolvimento Avançado**
- [ ] IDE configurado com extensions
- [ ] Environment variables configuradas
- [ ] Git configurado com .gitignore adequado
- [ ] Teste de setup executado com sucesso

### **✅ Opcional (Produção)**
- [ ] Docker instalado
- [ ] Redis configurado
- [ ] GPU setup (se aplicável)
- [ ] Monitoring tools configurados

---

**🎯 Com este setup, você está pronto para desenvolver dashboards inteligentes com IA e Python coding profissional!**
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
