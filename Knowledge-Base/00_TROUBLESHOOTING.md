# 🔧 TROUBLESHOOTING GUIDE - Guia de Solução de Problemas

Este é seu **guia de emergência** para quando algo der errado. Organizado por sintomas específicos com soluções testadas e validadas.

---

## 🚨 **PROBLEMAS CRÍTICOS - Ação Imediata**

### **💥 "Dashboard não carrega - página em branco"**

#### **Sintomas:**
- Navegador mostra página branca
- Console mostra erros Python
- `app.run_server()` falha

#### **Soluções por ordem de probabilidade:**

**1. Dependências faltando (70% dos casos)**
```bash
# Teste rápido
pip list | grep -E "(dash|plotly|pandas)"

# Se faltando, instale:
pip install dash plotly pandas numpy
```

**2. Erro de sintaxe Python (20% dos casos)**
```python
# Execute diretamente no terminal para ver erro:
python app.py

# Erros comuns:
- Indentação incorreta
- Parênteses não fechados  
- Importações erradas
```

**3. Porta já em uso (10% dos casos)**
```python
# Mude a porta no app.py:
app.run_server(debug=True, port=8051)  # ao invés de 8050
```

---

### **🔴 "Gráficos não aparecem"**

#### **Sintomas:**
- Dashboard carrega mas gráficos são espaços vazios
- Erro: "Invalid property", "Figure is not defined"

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
