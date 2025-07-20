# 🔢 Data Generation - Geração de Dados Sintéticos

Esta pasta contém **recursos especializados** para criar datasets sintéticos realistas que alimentem seus dashboards com dados convincentes.

## 📋 **Recursos Disponíveis**

### **📅 Geração de Datas e Séries Temporais**
- `Gerando datas sintéticas com NumPy e pandas para d.pdf`
- `Geração de Datas Sintéticas com NumPy & Pandas par.pdf`
- `Geração de Datas Sintéticas com NumPy + Pandas par.pdf` 
- `Geração de datas sintéticas com NumPy & Pandas par (1).pdf`
- `Geração de datas sintéticas com NumPy & Pandas par (2).pdf`
- **Múltiplas abordagens** para criar cronogramas realistas
- Padrões sazonais, tendências, outliers controlados

### **🧬 Synthetic Data Generation**
- `Synthetic data generation (Part 1).pdf`
- **Técnicas avançadas** de geração sintética
- Preservação de distribuições estatísticas
- Correlações e dependências entre variáveis

### **🧹 Limpeza e Otimização de Dados**
- `CoClean_ Collaborative Data Cleaning.pdf` - Métodos colaborativos
- `Bibliotecas Python e Uso de IAs para Limpeza e Oti.pdf`
- `Ferramentas Gratuitas em Python e Soluções com IA.pdf`
- **IA aplicada** à preparação de dados

---

## 🎯 **Casos de Uso por Tipo de Dashboard**

### **📈 Dashboards Financeiros**
```python
# Use recursos de datas sintéticas para:
- Séries temporais de vendas
- Fluxos de caixa mensais  
- Projeções e forecasting
- Dados de multiple anos com sazonalidade
```

### **🏢 Dashboards Empresariais**
```python
# Combine técnicas para criar:
- Dados de funcionários (fake mas realistas)
- KPIs departamentais correlacionados
- Métricas de performance balanceadas
- Distribuições demográficas coerentes
```

### **🌍 Dashboards Geográficos**
```python
# Gere dados sintéticos para:
- Coordenadas realistas por região
- Populações proporcionais às cidades
- Dados econômicos correlacionados por estado
- Padrões climáticos sazonais
```

---

## ⚡ **Padrões de Implementação**

### **Estrutura Base Recomendada:**
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker

def generate_synthetic_data():
    """Template base para geração de dados sintéticos"""
    fake = Faker('pt_BR')  # Localização brasileira
    
    # 1. Definir período temporal
    start_date = datetime.now() - timedelta(days=365)
    date_range = pd.date_range(start=start_date, 
                              end=datetime.now(), 
                              freq='D')
    
    # 2. Gerar dados base
    # 3. Aplicar correlações realistas
    # 4. Adicionar ruído controlado
    # 5. Validar distribuições
    
    return dataframe

# Sempre validar com:
# df.describe(), df.info(), correlações
```

### **Boas Práticas:**
- **Volume mínimo:** 3.000+ registros para estabilidade visual
- **Correlações realistas:** Vendas ↔ Sazonalidade ↔ Região
- **Outliers controlados:** 2-5% dos dados para realismo
- **Tipos variados:** Categóricos, numéricos, temporais, geográficos

---

## 📊 **Tipos de Dados Sintéticos Suportados**

| Tipo | Bibliotecas | Casos de Uso |
|------|-------------|--------------|
| **Temporais** | pandas, NumPy | Séries históricas, forecasting |
| **Categóricos** | Faker, random | Departamentos, regiões, produtos |
| **Numéricos** | NumPy distributions | KPIs, métricas, valores financeiros |
| **Geográficos** | Faker providers | Endereços, coordenadas, CEPs |
| **Pessoas** | Faker profiles | Funcionários, clientes (anonimizados) |

---

## 🔍 **Validação de Qualidade**

### **Checklist Obrigatório:**
```python
# 1. Distribuições estatísticas
df.describe()  # Média, mediana, quartis coerentes?

# 2. Correlações esperadas
df.corr()  # Vendas vs sazonalidade fazem sentido?

# 3. Valores ausentes controlados
df.isnull().sum()  # NAs intencionais ou bugs?

# 4. Tipos de dados corretos
df.dtypes  # Datas como datetime, números como float?

# 5. Volume adequado
len(df) >= 3000  # Suficiente para visualizações estáveis?
```

---

**💡 Dica Principal:** Use os PDFs desta pasta para entender **padrões temporais realistas** - eles são fundamentais para dashboards convincentes com dados que "contam uma história" coerente.
