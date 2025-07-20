# 📊 Plotly Python Semantic Guide Extractor

## 🎯 Objetivo
Extrator semântico que converte documentação Plotly em PDF/TXT/MD para uma estrutura XML hierárquica e inteligente, organizando o conhecimento por categorias funcionais e extraindo automaticamente exemplos de código.

## 🚀 Principais Características

### ✨ Estrutura Semântica
- **Categorização Inteligente**: Organiza automaticamente gráficos por tipo (Básicos, Estatísticos, Científicos, etc.)
- **Extração de Código**: Identifica e isola exemplos de código Python automaticamente
- **Detecção de Bibliotecas**: Diferencia entre Plotly Express e Graph Objects
- **Hierarquia Clara**: Estrutura XML organizada semanticamente

### 📈 Estatísticas do Projeto
- **204 gráficos** processados e categorizados
- **912 exemplos de código** extraídos automaticamente
- **7 categorias** funcionais identificadas
- **94.3%** dos códigos com imports válidos
- **Suporte a PDF, TXT, MD** com processamento recursivo

## 📁 Estrutura do Projeto

```
projeto_pyvy_2x2/
├── extract_test_pyvy.py          # Script original básico
├── semantic_plotly_extractor.py  # Extrator semântico avançado
├── analyze_guide.py              # Analisador de qualidade
├── Input/                        # Pasta com documentação fonte
│   ├── *.pdf                     # PDFs do Plotly
│   ├── pyvy_2x*/                 # Subpastas organizadas
│   └── pyvy_main/                # Conteúdo principal
├── output.xml                    # Estrutura simples original
├── plotly_python_guide.xml       # Guia hierárquico básico
└── semantic_plotly_guide.xml     # Guia semântico final
```

## 🔧 Como Usar

### 1. Executar Extração Semântica
```powershell
& "G:/Meu Drive/pyvy_2x2/.venv/Scripts/python.exe" semantic_plotly_extractor.py
```

### 2. Analisar Resultados
```powershell
& "G:/Meu Drive/pyvy_2x2/.venv/Scripts/python.exe" analyze_guide.py
```

### 3. Processar Estrutura Básica (alternativa)
```powershell
& "G:/Meu Drive/pyvy_2x2/.venv/Scripts/python.exe" extract_test_pyvy.py
```

## 📊 Categorias Identificadas

| Categoria | Quantidade | Exemplos |
|-----------|------------|----------|
| **Gráficos Básicos** | 80 | Bar charts, Line charts, Scatter plots |
| **Gráficos Científicos** | 51 | Heatmaps, Contours, Surface plots |
| **Gráficos Estatísticos** | 26 | Histograms, Box plots, Distributions |
| **Mapas e Geo** | 14 | Choropleth, Mapbox, Geographic |
| **Personalização** | 13 | Colors, Themes, Annotations |
| **Financeiros** | 10 | Candlestick, OHLC, Time series |
| **Recursos Avançados** | 10 | Animations, Widgets, Subplots |

## 🛠️ Tecnologias Utilizadas

- **Python 3.13.5**
- **PyPDF2**: Extração de texto de PDFs
- **xml.etree.ElementTree**: Manipulação XML
- **Regular Expressions**: Parsing de código
- **PowerShell**: Automação de comandos

## 📋 Estrutura XML Final

```xml
<plotly_guide version="2.0">
  <metadata>
    <title>Guia Semântico Plotly Python</title>
    <statistics total_charts="204" categories="7"/>
  </metadata>
  
  <common_content>
    <reusable_content id="about_dash" title="Sobre o Dash"/>
  </common_content>
  
  <category id="basic_charts" name="Gráficos Básicos">
    <chart name="Bar charts" source_file="Bar charts in Python.pdf">
      <description>Como fazer Gráficos de Barras...</description>
      <examples>
        <example id="example_1" title="Plotly Express">
          <library>plotly.express</library>
          <code language="python">
            import plotly.express as px
            fig = px.bar(data, x='year', y='pop')
            fig.show()
          </code>
        </example>
      </examples>
      <customization section="Opções de Estilo"/>
    </chart>
  </category>
</plotly_guide>
```

## 🎯 Benefícios da Estrutura Semântica

### ✅ Antes (Estrutura Simples)
- Lista plana de arquivos
- Conteúdo em texto bruto
- Difícil de processar
- Informações redundantes

### 🚀 Depois (Estrutura Semântica)
- Hierarquia organizada por função
- Códigos isolados com metadata
- Fácil busca por categoria/biblioteca
- Conteúdo reutilizável otimizado

## 📈 Métricas de Qualidade

- **Cobertura**: 100% dos arquivos processados
- **Precisão**: 94.3% dos códigos com imports válidos
- **Organização**: 7 categorias semânticas
- **Reutilização**: Sistema de conteúdo comum implementado
- **Escalabilidade**: Processamento recursivo automático

## 🔮 Próximos Passos

1. **🔍 API de Busca**: Sistema de consulta semântica
2. **📱 Interface Web**: Navegação interativa
3. **🤖 IA Integration**: Chatbot especializado em Plotly
4. **📚 Auto-docs**: Geração automática de documentação
5. **🔄 Pipeline CI/CD**: Atualizações automáticas

## 👥 Contribuição

Este projeto demonstra a evolução de uma extração simples de arquivos para um sistema semântico inteligente de organização de conhecimento.

**Desenvolvido em**: Julho 2025  
**Versão**: 2.0  
**Status**: ✅ Implementação Completa

---
*Transformando documentação técnica em conhecimento estruturado e acessível* 🚀
