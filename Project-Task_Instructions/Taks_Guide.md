# Task\_itens:

---

### 1\. Pesquisar imagem na internet

**Campo:**

Search the internet for an image using the description given. Paste the URL while researching (right-click on image \> copy image address) \*

**Orientação:**  
Pesquise uma imagem na internet usando a descrição fornecida e cole o URL da imagem encontrada.

---

### 2\. Criar prompt para modelo de gráfico

**Campo:**

Create a model prompt for the graph image found (no specific formatting details, only general guidelines) \*

**Orientação:**  
Crie um prompt de modelo para a imagem de gráfico encontrada, usando apenas diretrizes gerais (sem detalhes específicos de formatação).

---

### 3\. Colar script de geração de dados

**Campo:**

Paste the entire contents of the data generation script (data\_gen.py) \*

**Orientação:**  
Cole todo o conteúdo do script de geração de dados chamado `data_gen.py`.

---

### 4\. Colar script de visualização

**Campo:**

Paste the entire contents of the visualization script (viz.py) \*

**Orientação:**  
Cole todo o conteúdo do script de visualização chamado `viz.py`.

---

### 5\. Colar arquivo HTML gerado

**Campo:**

Paste the entire contents of the generated HTML file (dashboard.html) \*

**Orientação:**  
Cole todo o conteúdo do arquivo HTML gerado chamado `dashboard.html`.

---

### 6\. Tipos de gráficos no dashboard

**Campo:**

What kind of plots were seen in the dashboard? (coma separated list ex. bar, line, sankey) \*

**Orientação:**  
Liste, separados por vírgula, os tipos de gráficos vistos no dashboard (ex: bar, line, sankey).

---

### 7\. Bibliotecas adicionais utilizadas

**Campo:**

Have you used any more libraries than plotly dash, numpy, and/or pandas \*

**Orientação:**  
Informe se utilizou outras bibliotecas além de plotly dash, numpy e/ou pandas.

---

Se precisar de exemplos de preenchimento ou de algum desses campos em detalhes, é só avisar\!

---

### Exemplo de Questão

**Create a DASHBOARD. Here are some examples:**

- [https://plotly.com/examples/dashboards/](https://plotly.com/examples/dashboards/)  
- [https://plotly.com/examples/predictive-analytics/](https://plotly.com/examples/predictive-analytics/)

**Requisitos:**

- O dashboard deve ser capaz de contar uma história (deve conter pelo menos 2–3 diagramas complexos).  
- Integração de mapas em um subconjunto do dashboard (cerca de 8% dos dashboards) — por exemplo:  
  - [https://dash.gallery/dash-uber-rides-demo/](https://dash.gallery/dash-uber-rides-demo/)

---

## Dicas e Informações Adicionais

Aqui está um resumo organizado das principais informações e orientações extraídas de imagens enviadas, focando nas instruções, dicas técnicas e contexto do projeto de avaliação Python Data Visualization:

---

## **Resumo das Instruções e Dicas Técnicas**

### **1\. Sobre o Projeto de Avaliação**

- **Objetivo:** Avaliação para integrar o time de produção Python para projetos de visualização de dados.  
- **Tarefas:** Você receberá 2 tarefas (data rows) para completar, podendo fazer mais se desejar. Basta uma tarefa aprovada para ser convidado ao time de produção.  
- **Processo:** Não é necessário subir arquivos; cole o conteúdo dos arquivos diretamente na plataforma.  
- **Dica:** Abra o arquivo HTML em um editor de código para copiar o conteúdo facilmente.  
- **Resultado:** Se aprovado, poderá participar de projetos pagos com alta competitividade.

---

### **2\. Requisitos Técnicos do Dashboard**

- **Bibliotecas permitidas:** Apenas `pandas`, `numpy` e `plotly` (Dash).  
- **Scripts esperados:**  
  - Um script para geração de dados.  
  - Um script de visualização (`viz.py`) que:  
    - Lê os dados gerados.  
    - Gera um dashboard interativo em HTML usando Plotly.  
    - Salva o arquivo em `outputs/dashboard.html`.  
    - Usa boas práticas de tipografia (títulos em negrito, legendas claras).  
    - Organiza o layout com containers visuais (cards, seções).  
    - Utiliza sombras/gradientes para hierarquia visual (evite imagens “chapadas”).

---

### **3\. Dicas para Exportação de HTML com Plotly**

- **Exportando HTML:**  
  - `fig.write_html("path/to/file.html")` salva o gráfico como HTML completo.  
  - Para reduzir o tamanho do arquivo, use o parâmetro:  
    `include_plotlyjs='cdn'`  
    Exemplo:  
      
    fig.write\_html("dashboard.html", include\_plotlyjs='cdn')

    
- **Inserindo em Templates HTML:**  
  - Prefira usar `.to_html(full_html=False)` para obter apenas o conteúdo necessário do gráfico, sem as tags `<html>` e `<body>`, facilitando a inclusão em templates.  
  - Exemplo:  
      
    html\_str \= fig.to\_html(full\_html=False)  
      
  - **Por quê?** Assim, você pode montar um HTML maior, com vários gráficos, cards, etc., e inserir apenas o código dos gráficos onde desejar.

---

### **4\. Outras Informações Importantes**

- **Erros de acesso:** Caso encontre erros de acesso ("Unauthorized to view this asset"), aguarde novas instruções.  
- **Comunicação:** Veja as instruções sempre no início do tópico, conforme orientado pelos moderadores.  
- **Avaliação:** Esta etapa é não remunerada, mas serve para seleção do time fixo.

---

## **Exemplo de Fluxo para o Dashboard**

1. **Gere os dados com seu script de data generation.**  
2. **No script de visualização:**  
   - Leia os dados.  
   - Crie os gráficos com Plotly.  
   - Monte um layout organizado e atraente (cards, seções, títulos em negrito).  
   - Exporte cada gráfico com `.to_html(full_html=False)` e insira no template HTML.  
   - Salve o HTML final em `outputs/dashboard.html`.

---

## **Dicas Finais**

- Use apenas as bibliotecas permitidas.  
- Capriche na estética e organização visual.  
- Prefira exportar gráficos sem o HTML completo para facilitar a montagem do dashboard.  
- Reduza o tamanho do HTML usando `include_plotlyjs='cdn'` se necessário.

---

