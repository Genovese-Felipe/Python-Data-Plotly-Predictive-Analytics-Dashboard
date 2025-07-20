# 💡 Practical Examples - Exemplos Completos e Funcionais

Esta pasta contém **projetos completos** que você pode executar, estudar e adaptar para seus próprios dashboards.

## 📂 **Projetos Disponíveis**

### **🌍 Dashboard Design with Storytelling and Map Integration EX1/**
- **Dashboard empresarial completo** com mapas interativos
- Integração de múltiplas visualizações
- Geração de dados sintéticos realistas
- Sistema de callbacks avançado
- **Arquivos principais:**
  - `app.py` - Aplicação Dash principal
  - `data_generator.py` - Geração de dados sintéticos
  - `charts.py` - Funções de visualização
  - `main.py` - Ponto de entrada

### **🌍 Dashboard Design with Storytelling and Map Integration EX2/**
- **Segunda versão** com melhorias e variações
- Foco em storytelling com dados
- Diferentes abordagens de layout

### **🤖 predictive_analytics_dash_complete/**
- **Dashboard de Machine Learning** completo
- Usa dataset Iris para classificação
- Modelo de Regressão Logística integrado
- **100% de acurácia** demonstrada
- **Estrutura modular:**
  ```
  predictive_analytics_dash/
  ├── app.py                    # App principal
  ├── models/train_model.py     # Treinamento ML
  ├── data/load_data.py         # Carregamento de dados
  ├── components/               # Componentes UI
  ├── utils/                    # Utilitários
  └── assets/                   # Recursos estáticos
  ```

### **� MOVED_Plotly_Documentation.md**
- **Nota explicativa** sobre reorganização da documentação oficial
- **Plotly_Documentation foi movida** para `03_Technical_Documentation/`
- Melhor categorização: documentação técnica ≠ exemplos práticos

---

## 🚀 **Como Usar os Exemplos**

### **Para Aprender:**
```bash
# 1. Explore a estrutura
cd "Dashboard Design.../EX1/"
ls -la

# 2. Leia o código-fonte
cat app.py
cat data_generator.py

# 3. Execute o exemplo
python app.py
```

### **Para Adaptar:**
```python
# 1. Copie o padrão que funciona
# 2. Modifique dados e visualizações
# 3. Mantenha a estrutura de callbacks
# 4. Teste incrementalmente
```

### **Para Desenvolver:**
```
1. Use EX1 como base para dashboards empresariais
2. Use predictive_analytics_dash para projetos ML
3. Combine elementos de diferentes exemplos
4. Mantenha a modularidade
```

---

## 📊 **Tipos de Visualizações Disponíveis**

| Projeto | Visualizações Incluídas |
|---------|-------------------------|
| **EX1** | Sunburst, Bubble, Area, Stacked Bar, Flow Charts, Mapas |
| **EX2** | Variações dos anteriores com diferentes datasets |
| **ML Complete** | Scatter plots, Histogramas, Confusion Matrix, ROC Curves |
| **Plotly Docs** | Exemplos básicos de todos os tipos de gráficos |

---

## ⚡ **Execução Rápida**

### **Requisitos:**
```bash
pip install dash plotly pandas numpy scikit-learn
```

### **Teste Rápido EX1:**
```bash
cd "Dashboard Design with Storytelling and Map Integration EX1/"
python app.py
# Acesse: http://localhost:8050
```

### **Teste Rápido ML:**
```bash
cd predictive_analytics_dash_complete/predictive_analytics_dash/
python app.py
# Acesse: http://localhost:8050
```

---

**💡 Dica:** Estes exemplos foram testados e funcionam. Use-os como **ponto de partida** para seus projetos, adaptando dados e estilos conforme necessário.
