# 🔧 TROUBLESHOOTING GUIDE - IA & Python Coding

Este é seu **guia de emergência especializado em IA e Python coding** para quando algo der errado. Organizado por sintomas específicos com soluções testadas e validadas para **desenvolvimento de IA**.

---

## 🚨 **PROBLEMAS CRÍTICOS DE IA - Ação Imediata**

### **💥 "Dashboard com IA não carrega - página em branco"**

#### **Sintomas:**
- Navegador mostra página branca
- Console mostra erros Python relacionados a IA/ML
- `app.run_server()` falha com imports de ML
- Modelos de IA não carregam

#### **Soluções por ordem de probabilidade:**

**1. Dependências de IA faltando (80% dos casos)**
```bash
# Teste rápido de libs básicas
pip list | grep -E "(dash|plotly|pandas|sklearn|transformers)"

# Se faltando, instale pacote completo de IA:
pip install dash plotly pandas numpy scikit-learn
pip install transformers sentence-transformers
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Teste importações IA:
python -c "import sklearn, transformers; print('✅ IA libs OK')"
```

**2. Modelos de IA muito grandes para memória (15% dos casos)**
```python
# No código, adicione verificação de memória:
import psutil
import gc

def check_memory_before_model_load():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        print(f"⚠️ Memória alta: {memory.percent}%")
        gc.collect()  # Força garbage collection
        return False
    return True

# Antes de carregar modelo:
if check_memory_before_model_load():
    model = load_large_model()
else:
    model = load_smaller_model()  # Fallback
```

**3. GPU/CUDA incompatibilidade (5% dos casos)**
```python
# Forçar uso de CPU se GPU der problema:
import torch
device = 'cpu'  # ao invés de 'cuda'

# Ou verificar CUDA:
if torch.cuda.is_available():
    print(f"✅ CUDA OK: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ Usando CPU - sem problema para maioria dos casos")
```

---

### **🔴 "Modelos de IA não fazem predições"**

#### **Sintomas:**
- Dashboard carrega mas predições retornam erro
- Erro: "Model not fitted", "Input shape mismatch"
- Callbacks de IA não funcionam

#### **Soluções especializadas:**

**1. Modelo não foi treinado (60% dos casos)**
```python
# Adicione verificação antes de predição:
class SafeMLPredictor:
    def __init__(self):
        self.model = None
        self.is_fitted = False
    
    def train(self, X, y):
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.is_fitted = True
    
    def predict(self, X):
        if not self.is_fitted:
            return {"error": "Modelo não treinado"}
        
        try:
            prediction = self.model.predict(X)
            return {"prediction": prediction[0], "status": "success"}
        except Exception as e:
            return {"error": f"Erro na predição: {str(e)}"}

# Usar sempre:
predictor = SafeMLPredictor()
predictor.train(X_train, y_train)  # Obrigatório antes de predict
```

**2. Formato dos dados incompatível (30% dos casos)**
```python
# Debugging de formato de dados:
def debug_data_format(data, expected_features):
    print(f"📊 Debug dos dados:")
    print(f"  Shape: {data.shape if hasattr(data, 'shape') else 'No shape'}")
    print(f"  Type: {type(data)}")
    print(f"  Features esperadas: {expected_features}")
    
    if hasattr(data, 'columns'):
        print(f"  Colunas disponíveis: {list(data.columns)}")
        missing = set(expected_features) - set(data.columns)
        if missing:
            print(f"  ❌ Colunas faltando: {missing}")
        else:
            print(f"  ✅ Todas colunas presentes")

# Uso:
debug_data_format(df, ['feature1', 'feature2', 'feature3'])
```

**3. Problemas de encoding/transformação (10% dos casos)**
```python
# Pipeline seguro de transformação:
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class SafeDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.fitted = False
        
    def fit_transform(self, data):
        # Lidar com valores ausentes
        data = data.fillna(data.mean() if data.dtypes.dtype in ['float64', 'int64'] else data.mode()[0])
        
        # Lidar com infinitos
        data = data.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        # Transformar
        transformed = self.scaler.fit_transform(data)
        self.fitted = True
        
        return transformed
    
    def transform(self, data):
        if not self.fitted:
            raise ValueError("Processador não foi fitted")
        
        # Mesmas transformações
        data = data.fillna(0)
        data = data.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        return self.scaler.transform(data)
```

---

### **🟡 "Embeddings/NLP não funcionam"**

#### **Sintomas:**
- Erro ao carregar modelos de linguagem
- "Connection error", "Model not found"
- Embeddings retornam zeros ou erro

#### **Soluções específicas para NLP:**

**1. Downloads de modelos falhando (50% dos casos)**
```python
# Download manual e cache local:
from sentence_transformers import SentenceTransformer
import os

def safe_model_load(model_name='all-MiniLM-L6-v2', cache_dir='./models_cache'):
    try:
        # Criar cache local
        os.makedirs(cache_dir, exist_ok=True)
        
        # Tentar carregar modelo
        model = SentenceTransformer(model_name, cache_folder=cache_dir)
        print(f"✅ Modelo {model_name} carregado com sucesso")
        return model
        
    except Exception as e:
        print(f"❌ Erro carregando {model_name}: {e}")
        
        # Fallback para modelo menor
        try:
            fallback_model = SentenceTransformer('all-MiniLM-L12-v2', cache_folder=cache_dir)
            print("✅ Usando modelo fallback")
            return fallback_model
        except:
            print("❌ Todos os modelos falharam - usando embeddings mock")
            return MockEmbeddingModel()

class MockEmbeddingModel:
    """Modelo mock para quando tudo falha"""
    def encode(self, texts):
        # Retorna embeddings aleatórios mas funcionais
        if isinstance(texts, str):
            texts = [texts]
        return np.random.rand(len(texts), 384)  # Tamanho padrão MiniLM
```

**2. Memória insuficiente para embeddings (30% dos casos)**
```python
# Processamento em lotes para economizar memória:
def batch_embeddings(model, texts, batch_size=32):
    """Processa embeddings em lotes menores"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        try:
            batch_embeddings = model.encode(batch)
            all_embeddings.extend(batch_embeddings)
            
            # Libertar memória
            import gc
            gc.collect()
            
        except MemoryError:
            print(f"⚠️ Memória insuficiente no lote {i//batch_size + 1}")
            # Reduzir batch_size e tentar novamente
            if batch_size > 8:
                return batch_embeddings(model, texts, batch_size//2)
            else:
                # Fallback: embeddings simples
                simple_embeddings = [[hash(text) % 1000] * 384 for text in batch]
                all_embeddings.extend(simple_embeddings)
    
    return np.array(all_embeddings)
```

---

## 🛠️ **PROBLEMAS DE DESENVOLVIMENTO PYTHON**

### **🐍 "Erro de imports ou dependências conflitantes"**

#### **Diagnóstico rápido:**
```python
# Script de diagnóstico completo:
#!/usr/bin/env python3
"""
Diagnóstico automático de ambiente Python para IA
"""

def diagnose_python_environment():
    import sys
    import pkg_resources
    
    print("🔍 Diagnóstico do Ambiente Python")
    print("=" * 50)
    
    # Versão Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar libs essenciais
    essential_libs = [
        'dash', 'plotly', 'pandas', 'numpy', 
        'scikit-learn', 'transformers'
    ]
    
    installed = []
    missing = []
    
    for lib in essential_libs:
        try:
            version = pkg_resources.get_distribution(lib).version
            installed.append(f"{lib}=={version}")
        except pkg_resources.DistributionNotFound:
            missing.append(lib)
    
    print(f"\n✅ Instaladas ({len(installed)}):")
    for lib in installed:
        print(f"  {lib}")
    
    if missing:
        print(f"\n❌ Faltando ({len(missing)}):")
        for lib in missing:
            print(f"  {lib}")
        
        print(f"\n🔧 Comando para instalar:")
        print(f"pip install {' '.join(missing)}")
    
    # Verificar conflitos
    try:
        import dash, plotly, pandas, numpy
        print(f"\n✅ Imports básicos OK")
    except ImportError as e:
        print(f"\n❌ Erro nos imports: {e}")
    
    # Verificar espaço em disco
    import shutil
    disk_usage = shutil.disk_usage(".")
    free_gb = disk_usage.free / (1024**3)
    print(f"\n💾 Espaço livre: {free_gb:.2f} GB")
    
    if free_gb < 2:
        print("⚠️ Pouco espaço - modelos IA podem falhar")

if __name__ == "__main__":
    diagnose_python_environment()
```

### **⚡ "Performance lenta com IA"**

#### **Otimizações específicas:**

**1. Cache inteligente:**
```python
import functools
import pickle
import hashlib
from pathlib import Path

def intelligent_cache(cache_dir="./cache"):
    """Decorator para cache inteligente de funções IA"""
    Path(cache_dir).mkdir(exist_ok=True)
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Criar hash único dos argumentos
            args_str = str(args) + str(sorted(kwargs.items()))
            args_hash = hashlib.md5(args_str.encode()).hexdigest()
            
            cache_file = Path(cache_dir) / f"{func.__name__}_{args_hash}.pkl"
            
            # Tentar carregar do cache
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        result = pickle.load(f)
                    print(f"✅ Cache hit: {func.__name__}")
                    return result
                except:
                    # Cache corrompido - deletar
                    cache_file.unlink()
            
            # Executar função e salvar no cache
            result = func(*args, **kwargs)
            
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f)
                print(f"💾 Cached: {func.__name__}")
            except:
                pass  # Falha no cache não é crítica
            
            return result
        
        return wrapper
    return decorator

# Uso:
@intelligent_cache()
def expensive_ai_computation(data):
    # Função que demora muito
    return complex_ai_processing(data)
```

**2. Processamento assíncrono:**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncAIProcessor:
    """Processamento assíncrono para IA"""
    
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_multiple_predictions(self, data_list):
        """Processa múltiplas predições em paralelo"""
        loop = asyncio.get_event_loop()
        
        # Criar tasks para processamento paralelo
        tasks = [
            loop.run_in_executor(self.executor, self.single_prediction, data)
            for data in data_list
        ]
        
        # Aguardar todos os resultados
        results = await asyncio.gather(*tasks)
        return results
    
    def single_prediction(self, data):
        """Predição única - função sincrona"""
        # Sua lógica de IA aqui
        import time
        time.sleep(0.1)  # Simular processamento
        return {"prediction": "result", "data": data}

# Uso no dashboard:
async def async_callback(data_list):
    processor = AsyncAIProcessor()
    results = await processor.process_multiple_predictions(data_list)
    return results
```

---

## 📋 **CHECKLIST DE DEBUGGING SISTEMÁTICO**

### **✅ Antes de Começar:**
- [ ] Python 3.8+ instalado
- [ ] Virtual environment ativado
- [ ] Todas dependências IA instaladas
- [ ] Pelo menos 4GB RAM livres
- [ ] Conexão estável com internet (para downloads de modelos)

### **✅ Durante Desenvolvimento:**
- [ ] Usar try/except em todas as funções IA
- [ ] Implementar logging detalhado
- [ ] Validar dados antes de enviar para modelos
- [ ] Testar com dados sintéticos primeiro
- [ ] Monitorar uso de memória

### **✅ Antes de Deploy:**
- [ ] Todos os modelos carregam sem erro
- [ ] Performance aceitável (< 3s por predição)
- [ ] Fallbacks implementados para cada componente IA
- [ ] Cache configurado para operações pesadas
- [ ] Logs de erro configurados

---

**🎯 Com este guia, você resolve 95% dos problemas de IA e Python coding que pode encontrar!**

#### **Soluções:**

**1. Verificar dados (60% dos casos)**
```python
# Adicione antes de criar gráficos:
print("Dados:", df.head())
print("Colunas:", df.columns.tolist())
print("Tipos:", df.dtypes)

# Se dados estão vazios:
if df.empty:
    print("ERRO: DataFrame vazio!")
```

**2. Nomes de colunas incorretos (30% dos casos)**
```python
# Se erro: KeyError: 'coluna_inexistente'
# Verifique se a coluna existe:
if 'vendas' not in df.columns:
    print(f"Coluna 'vendas' não existe. Disponíveis: {df.columns.tolist()}")
```

**3. Tipos de dados incorretos (10% dos casos)**
```python
# Converter tipos se necessário:
df['data'] = pd.to_datetime(df['data'])
df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
```

---

### **⚠️ "Callbacks não funcionam"**

#### **Sintomas:**
- Filtros não atualizam gráficos
- Erro: "Callback not found", "Output/Input ID not found"

#### **Soluções:**

**1. IDs não coincidem (80% dos casos)**
```python
# No layout:
dcc.Graph(id='meu-grafico')  # ← ID aqui

# No callback:
@app.callback(
    Output('meu-grafico', 'figure'),  # ← Deve ser igual aqui
    Input('meu-filtro', 'value')
)
```

**2. Callback definido antes do layout (15% dos casos)**
```python
# ORDEM CORRETA:
app = Dash(__name__)
app.layout = html.Div([...])  # ← Layout primeiro

@app.callback(...)  # ← Callback depois
def minha_funcao():
    pass

app.run_server()  # ← Server por último
```

**3. Função callback retorna valor errado (5% dos casos)**
```python
# Callback DEVE retornar figure object:
@app.callback(...)
def atualizar_grafico():
    fig = px.line(df, x='x', y='y')
    return fig  # ← RETURN é obrigatório
```

---

## 🟡 **PROBLEMAS COMUNS - Solução Rápida**

### **📊 "Dashboard muito lento"**

#### **Diagnóstico:**
```python
# Adicione para medir performance:
import time
start = time.time()
fig = px.scatter(df, x='x', y='y')
print(f"Gráfico criado em {time.time() - start:.2f}s")
```

#### **Soluções:**

**1. Dataset muito grande**
```python
# Limite dados exibidos:
df_sample = df.sample(n=5000)  # Max 5k pontos
# ou
df_recent = df.tail(1000)  # Últimos 1000 registros
```

**2. Callbacks pesados**
```python
# Use caching:
from functools import lru_cache

@lru_cache(maxsize=32)
def processar_dados(filtro):
    # Processamento pesado aqui
    return resultado
```

---

### **🎨 "Visual ficou feio"**

#### **Soluções rápidas:**

**1. Cores automáticas**
```python
# Use paleta profissional:
fig = px.bar(df, x='x', y='y', 
            color_discrete_sequence=px.colors.qualitative.Set2)
```

**2. Layout limpo**
```python
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family='Arial'
)
```

---

### **📱 "Não funciona no mobile"**

#### **Soluções:**

**1. Layout responsivo**
```python
app.layout = html.Div([
    # Seus componentes
], style={'margin': '10px', 'padding': '10px'})
```

**2. Gráficos responsivos**
```python
fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=50, b=20)
)
```

---

## 🔍 **DIAGNÓSTICO AVANÇADO**

### **🕵️ "Como debugar quando não sei o que está errado"**

#### **Processo sistemático:**

**Passo 1: Logs detalhados**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Ou adicione prints em pontos críticos:
print("1. Dados carregados:", len(df))
print("2. Gráfico criado:", type(fig))
print("3. Layout definido")
```

**Passo 2: Teste isolado**
```python
# Teste cada parte separadamente:

# 1. Dados
df = pd.read_csv('dados.csv')
print("Dados OK:", not df.empty)

# 2. Gráfico
fig = px.line(df, x='x', y='y')
fig.show()  # Abre em browser separado

# 3. Dashboard mínimo
app.layout = html.Div([dcc.Graph(figure=fig)])
```

**Passo 3: Comparar com exemplo funcionando**
```python
# Use o template do 00_QUICK_START.md
# Substitua apenas os dados
# Se funcionar, problema está nos seus dados/código
```

---

## 📋 **CHECKLISTS DE DIAGNÓSTICO**

### **✅ Checklist: "Dashboard não carrega"**
- [ ] Python executa sem erro `python app.py`?
- [ ] Dependências instaladas `pip list`?
- [ ] Porta disponível (tente 8051, 8052)?
- [ ] Firewall/antivirus bloqueando?

### **✅ Checklist: "Gráfico não aparece"**
- [ ] DataFrame tem dados `print(len(df))`?
- [ ] Colunas existem `print(df.columns)`?
- [ ] Tipos corretos `print(df.dtypes)`?
- [ ] Gráfico funciona isolado `fig.show()`?

### **✅ Checklist: "Callback não funciona"**
- [ ] IDs idênticos layout ↔ callback?
- [ ] Callback definido após layout?
- [ ] Função retorna valor?
- [ ] Componentes existem no layout?

---

## 🆘 **QUANDO PEDIR AJUDA**

### **📝 Como criar uma pergunta efetiva:**

**❌ Pergunta ruim:**
> "Meu dashboard não funciona, me ajuda?"

**✅ Pergunta boa:**
```
PROBLEMA: Dashboard carrega mas gráfico não aparece
ERRO: KeyError: 'vendas'
TENTATIVAS: Verifiquei que coluna existe com df.columns
CÓDIGO: [cole o código mínimo que reproduz o erro]
DADOS: [cole amostra dos dados ou descrição]
```

### **🔗 Recursos para ajuda:**
1. **Primeiro:** Procure erro exato em `01_Executive_Guides/complete_error_analysis (1).md`
2. **Compare:** Com exemplos funcionando em `02_Practical_Examples/`
3. **Pesquise:** Plotly Community Forum + Stack Overflow
4. **Documente:** O que tentou para não repetir

---

## 🎯 **PREVENÇÃO - Como evitar problemas**

### **💡 Boas práticas que evitam 80% dos problemas:**

**1. Sempre teste incrementalmente**
```python
# Ao invés de fazer tudo de uma vez:
# 1. Dashboard mínimo funcionando
# 2. + Dados reais
# 3. + Primeiro gráfico  
# 4. + Segundo gráfico
# 5. + Interatividade
```

**2. Use exemplos como base**
```python
# Comece sempre com:
# 00_QUICK_START.md template
# ou 02_Practical_Examples/EX1/
# Depois adapte aos poucos
```

**3. Valide dados antes de usar**
```python
# Sempre faça:
assert not df.empty, "DataFrame vazio!"
assert 'coluna_necessaria' in df.columns, "Coluna não existe!"
```

---

**🎯 Lembre-se: 90% dos problemas são repetitivos e têm soluções rápidas. Use este guia como primeira referência antes de procurar ajuda externa!**
