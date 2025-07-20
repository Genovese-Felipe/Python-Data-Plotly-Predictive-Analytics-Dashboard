<web_content>
  <title>EVALUATION ONLY - Labeling Instructions</title>
  <author>Alignerr</author>
  <publication_date>2025-07-12</publication_date>
  <license>Internal Evaluation Use Only</license>
  <section>
    <title>Objective</title>
    <paragraph>
      This is a Python evaluation focused on data visualization and storytelling. The main task is to recreate a visual similar to a reference image, telling the same story using a dummy dataset. This involves creating Python scripts for data generation and visualization. An input prompt that would naturally produce the created visual must also be written.
    </paragraph>
    <paragraph>
      IMPORTANT UPDATE AS OF JULY 12TH: An upload script is no longer used. The contents of the scripts and HTML file are to be copy-pasted into the Labelbox editor.
    </paragraph>
  </section>
  <section>
    <title>Labeling Steps</title>
    <list type="ordered">
      <item>
        <b>Find and Analyze the Dashboard/Graph:</b> Search the web for a reference image of a business-related dashboard or graph that matches the given chart description. Obtain the direct URL to the image. The objective is to creatively expand on this reference, capturing core features while developing realistic datasets and visualizations.
      </item>
      <item>
        <b>Generate a Prompt:</b> Write a simple, open-ended, natural, and practical user-style question or instruction that the reference image would answer. This prompt frames the data story.
      </item>
      <item>
        <b>Generate Data To Tell the Business Story:</b> Write a data creation script (data_gen.py) using only pandas and numpy. It must generate at least two datasets (as DataFrames or Numpy arrays) that tell a story similar to the reference image.
      </item>
      <item>
        <b>Recreate the Visualization:</b> Write a visualization script (viz.py) using only pandas, numpy, and plotly. This script reads the generated data and outputs a single interactive HTML file (dashboard.html).
      </item>
      <item>
        <b>Upload Files:</b> Copy and paste the contents of the data generation script, visualization script, and the generated HTML file into the Labelbox platform's left side panel. The generated .csv/.npy files are not needed.
      </item>
    </list>
  </section>
  <section>
    <title>Prompt Examples</title>
    <table>
      <row>
        <cell><b>Prompt Topic</b></cell>
        <cell><b>Story &amp; Visuals</b></cell>
      </row>
      <row>
        <cell>"Show how global electric-vehicle (EV) adoption has evolved since 2015 and predict the next five years."</cell>
        <cell>Multi-line time-series of unit sales by region, Stacked area of battery chemistries, Sankey of supply-chain flows, Heat-map of EV market-share by country.</cell>
      </row>
      <row>
        <cell>"Analyze hospital network capacity vs. infectious-disease outbreaks during winter seasons."</cell>
        <cell>Dual-axis line (ICU beds vs. cases), Correlation heat-map of symptoms &amp; test positivity, Box-whisker of LOS by diagnosis group.</cell>
      </row>
      <row>
        <cell>"Contrast same-day vs. two-day e-commerce delivery performance during holiday peaks."</cell>
        <cell>Violin plot of delivery times, Pareto of top delay causes, Time-series forecast of warehouse backlog.</cell>
      </row>
      <row>
        <cell>"Track sustainable-aviation-fuel (SAF) usage across the airline industry and project carbon savings."</cell>
        <cell>Waterfall of CO2 reductions, Treemap of SAF feedstocks, Monte Carlo projection of carbon offset targets.</cell>
      </row>
    </table>
  </section>
  <section>
    <title>Visualization Style Guidelines</title>
    <list type="unordered">
      <item><b>Typography:</b> Titles MUST be bold, with properly formatted legends and labels.</item>
      <item><b>Aesthetics:</b> Organize layout using visual containers (e.g., cards, sections). Use depth thoughtfully via shadows or gradients for visual hierarchy.</item>
      <item><b>Storytelling:</b> Establish a clear narrative flow, starting with high-level KPIs and drilling down into details. Data elements should feel connected.</item>
      <item><b>Complexity:</b> Dashboards must match the visual density and insight variety of provided examples. Avoid oversimplification.</item>
      <item><b>Layout:</b> No overlapping elements or cut-off text. Ensure consistent padding, margin, and spacing.</item>
      <item><b>Legends:</b> Ensure legends are clearly displayed, boxed if appropriate, with well-organized placement.</item>
      <item><b>Color Palette:</b> Use a professional and aesthetically pleasing color scheme that complements the data and enhances readability.</item>
      <item><b>Overall Quality:</b> The final plot should be polished and suitable for a presentation or publication.</item>
    </list>
  </section>
  <visual_elements>
    <image>
      <url>local_file_image</url>
      <dimensions>
        <width>unknown</width>
        <height>unknown</height>
      </dimensions>
      <colors>
        <primary>#2d333b</primary>
        <secondary>#adbac7</secondary>
        <accent>#539bf5</accent>
      </colors>
      <text>
        <![CDATA[
        <data_row_id>/
        |-- data/
        |   |-- sample.npy
        |   |-- dataframe2.csv
        |   |-- dataframe.csv      # Generated .csv and/or npy files
        |-- scripts/
        |   |-- data_gen.py        # Data generation script
        |   |-- viz.py             # Visualization script
        |-- outputs/
        |   |-- dashboard.html     # Interactive html generated using viz.py
        ]]>
      </text>
    </image>
  </visual_elements>
  <summary>
    This document provides evaluation instructions for a Python data visualization task. The goal is to find a reference dashboard/graph, create a relevant prompt, generate synthetic data using pandas/numpy, and build an interactive visualization with Plotly. The final deliverables (data script, visualization script, and HTML output) are to be pasted into the Labelbox editor. The instructions emphasize storytelling, visual quality, and adherence to a specific folder structure and style guidelines.
  </summary>
  <link url="[Evaluation Labeling Walkthrough] Advanced Capabilities v2" type="external">Walkthrough Video</link>
  <link url="full_example_url_placeholder" type="external">A full example is available here.</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Positive Visualization Examples</title>
  <author>Unknown</author>
  <publication_date>Unknown</publication_date>
  <license>Internal Evaluation Use Only</license>
  <summary>
    Este documento é um catálogo visual de exemplos positivos de dashboards e gráficos complexos. Ele serve como uma referência de qualidade para tarefas de visualização de dados, exibindo uma variedade de tipos de gráficos, incluindo painéis financeiros, infográficos de mercado, mapas geográficos, diagramas de Sankey e rodas de sabor, todos demonstrando uma narrativa clara e design polido.
  </summary>
  <visual_elements>
    <dashboard>
      <title>Lending Operations Dashboard</title>
      <visualization>
        Um painel de controle financeiro com tema claro que monitora as operações de empréstimo em tempo real. [cite_start]Ele usa cartões de KPI, gráficos de área, gráficos de linha e um gráfico de funil para apresentar o portfólio de empréstimos, volume de aplicações e o pipeline de aprovação[cite: 1, 2].
      </visualization>
      <metric>
        <label>Total Loan Portfolio</label>
        <value>$25.5M</value>
      </metric>
      <metric>
        <label>Applications</label>
        <value>12K+</value>
      </metric>
      <metric>
        <label>Approval Rate</label>
        <value>81%</value>
      </metric>
      <metric>
        <label>Default Rate</label>
        <value>3.4%</value>
      </metric>
      <chart>
        <type>funnel</type>
        <title>Application Pipeline</title>
      </chart>
      <chart>
        <type>area</type>
        <title>Application Volume</title>
      </chart>
    </dashboard>
    <dashboard>
      <title>Regional Sales Performance</title>
      <visualization>
        Um painel de desempenho de vendas com tema escuro. [cite_start]Ele combina um grande KPI para a cota geral, um gráfico de linha para a tendência de receita mensal, uma lista de melhores desempenhos e um mapa geográfico para o desempenho global de vendas[cite: 13, 16].
      </visualization>
      <metric>
        <label>Overall Quota</label>
        <value>87%</value>
      </metric>
      <chart>
        <type>line</type>
        <title>Monthly Revenue Trend</title>
      </chart>
      <chart>
        <type>map</type>
        <title>Global Sales Performance</title>
      </chart>
    </dashboard>
    <dashboard>
      <title>Social Media Engagement Dashboard</title>
      <visualization>
        Um painel de mídia social com tema escuro que rastreia o alcance global e o engajamento. [cite_start]Ele usa uma combinação de cartões de KPI, um mapa geográfico, um gráfico de radar para interesses dos seguidores, e um gráfico de barras agrupadas para dados demográficos de audiência[cite: 62, 70, 73, 78].
      </visualization>
       <metric>
        <label>Total Likes</label>
        <value>350,809</value>
      </metric>
       <metric>
        <label>Engagement Rate</label>
        <value>48.07%</value>
      </metric>
       <metric>
        <label>Total Users Reached</label>
        <value>840,466</value>
      </metric>
    </dashboard>
    <dashboard>
      <title>SaaS Financial Performance Dashboard</title>
      <visualization>
        Um painel financeiro para um negócio de SaaS, utilizando um tema escuro. Apresenta KPIs chave na parte superior, como MRR e Churn. [cite_start]Os gráficos principais incluem um gráfico de área empilhada para tendências de aquisição, uma análise de cascata do ARR, um funil de aquisição de clientes e um heatmap para análise de retenção de coorte[cite: 87, 88, 89, 90, 91, 104, 95, 110].
      </visualization>
        <metric>
            <label>Monthly Recurring Revenue</label>
            <value>$3.2M</value>
        </metric>
        <metric>
            <label>Net Revenue Retention</label>
            <value>112%</value>
        </metric>
        <metric>
            <label>LTV:CAC Ratio</label>
            <value>4.8x</value>
        </metric>
    </dashboard>
    <chart>
        <type>sankey</type>
        <title>How Nike Inc (NKE) Makes Its Money</title>
        <visualization>
            [cite_start]Um diagrama de Sankey detalhando o fluxo financeiro da Nike em 28-05-2023[cite: 141]. [cite_start]Ele rastreia a receita de diferentes segmentos de produtos (Calçados, Vestuário, etc.) através do Custo dos Produtos Vendidos (COGS) e Despesas Operacionais para chegar ao Lucro Líquido[cite: 140, 143, 153, 159, 149].
        </visualization>
    </chart>
     <dashboard>
      <title>Global Oil Benchmark Infographic</title>
      <visualization>
        [cite_start]Um infográfico complexo sobre o mercado de petróleo, focando na inclusão do WTI Midland no benchmark Dated Brent[cite: 173]. [cite_start]Ele usa um mapa global para mostrar o alcance, gráficos de barras e de bolhas para comparações, e gráficos de linha para sincronia de preços[cite: 218, 178, 179, 197].
      </visualization>
    </dashboard>
    <chart>
      <type>sunburst</type>
      <title>Aroma, Taste, and Mouthfeel Wheel</title>
      <visualization>
        Uma roda de sabor, provavelmente para café ou vinho, que categoriza a experiência sensorial. [cite_start]Ela se divide em Aroma, Sabor e Sensação na Boca, com cada categoria se ramificando em descritores mais específicos de forma hierárquica[cite: 529, 541, 542].
      </visualization>
    </chart>
  </visual_elements>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Data Visualization &amp; Dashboards</title>
  <author>Plotly</author>
  <publication_date>Unknown</publication_date>
  <license>Showcase of Examples</license>
  <summary>
    [cite_start]Este documento apresenta uma galeria de aplicações e painéis interativos construídos com o Plotly Dash[cite: 5]. [cite_start]Os exemplos abrangem uma ampla gama de setores e casos de uso, incluindo a análise de custos de planos de saúde [cite: 13, 14][cite_start], disparidade salarial de gênero [cite: 17, 24][cite_start], análise de dados de filmes do IMDb [cite: 39, 40][cite_start], dados geoespaciais de corridas da Uber [cite: 88, 89][cite_start], visualização de dados climáticos [cite: 92, 93][cite_start], métricas de plataformas de streaming [cite: 207, 208] e muito mais, demonstrando a versatilidade da ferramenta para criar visualizações de dados interativas.
  </summary>
  <visual_elements>
    <dashboard>
      <title>Medical Provider Charges Dashboard</title>
      <author>Plotly</author>
      [cite_start]<visualization>Explora os custos de provedores de saúde em diferentes estados[cite: 14].</visualization>
    </dashboard>
    <dashboard>
      <title>Gender Pay Gap Report</title>
      <author>Ann Marie</author>
      [cite_start]<visualization>Analisa a diferença entre a média e mediana do pagamento por hora entre homens e mulheres[cite: 24].</visualization>
    </dashboard>
    <dashboard>
      <title>IMDb Analysis for Movies &amp; Series</title>
      <author>TFI</author>
      [cite_start]<visualization>Visualiza e analisa dados do IMDb para os principais filmes e séries e obtém recomendações[cite: 40].</visualization>
    </dashboard>
    <dashboard>
      <title>IOT Rainfall App</title>
      <author>Tanima</author>
      [cite_start]<visualization>Explora dados de precipitação neste painel Python IOT[cite: 53].</visualization>
    </dashboard>
    <dashboard>
      <title>Clinical Patient Dashboard</title>
      <author>Plotly</author>
      [cite_start]<visualization>Explora o volume de pacientes da clínica por hora do dia, tempo de espera e pontuação de cuidado[cite: 64].</visualization>
    </dashboard>
    <dashboard>
      <title>Retail Demand Transference</title>
      <author>Plotly</author>
      [cite_start]<visualization>Prevê a demanda de produtos de consumo para varejistas em diferentes localidades de lojas[cite: 81].</visualization>
    </dashboard>
    <dashboard>
      <title>Uber Rides Geospatial Data</title>
      <author>Plotly</author>
      [cite_start]<visualization>Explora os locais de embarque de milhões de corridas da Uber em NYC[cite: 89].</visualization>
    </dashboard>
    <dashboard>
      <title>CBE Climate Visualization App</title>
      <author>Center for the Built Environment (Berkeley)</author>
      [cite_start]<visualization>Visualiza dados climáticos com séries temporais, mapas de calor, mapas, rosas dos ventos e mais[cite: 93].</visualization>
    </dashboard>
    <dashboard>
      <title>HERA Radio Telescope &amp; Weather App</title>
      <author>HERA Reionization Team</author>
      [cite_start]<visualization>Visualiza dados científicos e geoespaciais em tempo real do conjunto de radiotelescópios HERA[cite: 142].</visualization>
    </dashboard>
    <dashboard>
      <title>World Atlas</title>
      <author>Dan Baker</author>
      [cite_start]<visualization>Visualiza centenas de indicadores entre países nesta aplicação de múltiplas páginas[cite: 150].</visualization>
    </dashboard>
    <dashboard>
      <title>Dash Molstar for SARS-COV-2</title>
      <author>Simon Sun</author>
      [cite_start]<visualization>Exemplo de uso do Dash-Molstar para visualizar estruturas moleculares e dados em aplicações web[cite: 169].</visualization>
    </dashboard>
    <dashboard>
      <title>Repair Cafe Dashboard</title>
      <author>Natalia</author>
      [cite_start]<visualization>Visualiza os dados do Repair Café para rastrear e explorar os resultados de reparos de dispositivos[cite: 217].</visualization>
    </dashboard>
     <dashboard>
      <title>An Analytics App on USA Flights Data</title>
      <author>Unknown</author>
      [cite_start]<visualization>Explore esta aplicação web para descobrir dados importantes relacionados a voos de passageiros nos EUA[cite: 227].</visualization>
    </dashboard>
  </visual_elements>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Predictive Analytics, Forecasting</title>
  <author>Plotly</author>
  <publication_date>Unknown</publication_date>
  <license>Showcase of Examples</license>
  <section>
    <title>Predictive Analytics, Forecasting</title>
    <paragraph>
      Enquanto ferramentas de BI tradicionais respondem "O que aconteceu?", o Plotly e o Dash respondem "E se?". [cite_start]Explore estes exemplos de Python em análise preditiva e previsão. [cite: 96, 97]
    </paragraph>
  </section>
  <summary>
    Este documento da Plotly exibe aplicações de análise preditiva e previsão construídas com Dash. Ele destaca dois exemplos principais: um preditor de idade cronológica que utiliza deep learning e uma ferramenta interativa para ajustar modelos de séries temporais SARIMA, demonstrando como o Python pode ser usado para análises avançadas do tipo "E se?".
  </summary>
  <visual_elements>
    <dashboard>
      <title>Harvard Age Prediction</title>
      <author>Theo Vincent</author>
      <visualization>
        [cite_start]Uma aplicação que apresenta preditores de idade cronológica utilizando ferramentas de deep learning. [cite: 107] A interface permite selecionar a forma como uma amostra é definida e exibe o desempenho da previsão.
      </visualization>
      <metric>
        <label>Average R²</label>
        <value>0.611 +- 0.229</value>
      </metric>
    </dashboard>
    <dashboard>
      <title>SARIMA Tuner</title>
      <author>Gabriele</author>
      <visualization>
        [cite_start]Uma aplicação para aprender sobre os passos necessários para trabalhar com dados de séries temporais, ajustando modelos SARIMA para fazer previsões. [cite: 125] [cite_start]A ferramenta guia o usuário através das etapas de "1-Data set up", "2-Stationarity" e "3-Model Selection". [cite: 113, 114, 115]
      </visualization>
    </dashboard>
  </visual_elements>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Model interpretability - Time series</title>
  <author>multidimensionality-of-aging.net project</author>
  <publication_date>2025-07-17</publication_date>
  <license>Research Application</license>
  <summary>
    [cite_start]Este documento exibe um painel de controle interativo da web projetado para a interpretabilidade de um modelo de Rede Neural Convolucional 1D (1DCNN)[cite: 995]. [cite_start]A aplicação permite que os usuários explorem como o modelo analisa dados de séries temporais (especificamente, pressão arterial [cite: 1021, 1032]) para prever métricas relacionadas ao envelhecimento. [cite_start]Os usuários podem filtrar os resultados por várias dimensões de envelhecimento, dados demográficos e taxas de envelhecimento para visualizar o impacto nos dados e nas previsões do modelo[cite: 989, 996, 998, 1000].
  </summary>
  <section>
    <title>Painel de Controle de Interpretabilidade Interativa</title>
    <paragraph>
      Esta aplicação web fornece uma interface para analisar a interpretabilidade de um modelo de previsão de idade baseado em séries temporais. Ela permite a seleção de diferentes coortes e parâmetros para visualizar os dados de entrada e as previsões do modelo correspondentes.
    </paragraph>
    <list type="unordered">
      <item>
        [cite_start]<b>Dimensões de Envelhecimento:</b> Arterial, Cardíaca, Atividade Física[cite: 990].
      </item>
      <item>
        [cite_start]<b>Filtros Demográficos:</b> Sexo (Masculino, Feminino) e Faixa Etária (Jovem, Meia-idade, Idoso)[cite: 996, 997, 998, 999].
      </item>
      <item>
        [cite_start]<b>Filtros de Envelhecimento:</b> Taxa de envelhecimento (Acelerada, Normal, Desacelerada)[cite: 1000, 1001].
      </item>
      <item>
        [cite_start]<b>Seleção de Dados:</b> Permite a seleção de amostras e canais de dados específicos[cite: 1002, 1011].
      </item>
    </list>
  </section>
  <visual_elements>
    <dashboard>
      <title>Model interpretability - Time series</title>
      <metric>
        <label>1DCNN Model Performance (R²)</label>
        <value>0.41 +- 0.004</value>
      </metric>
      <visualization>
        [cite_start]O painel apresenta um gráfico de dispersão que plota a pressão arterial normalizada em função do tempo[cite: 1021, 1030]. Os pontos de dados no gráfico representam a série temporal para a amostra selecionada. A interface é projetada para explorar como diferentes subgrupos de dados influenciam a interpretabilidade do modelo.
      </visualization>
      <chart>
        <type>scatter</type>
        <title>Blood Pressure Over Time</title>
        <data>
          <label>X-Axis</label>
          <value>Time (10 min / unit)</value>
        </data>
        <data>
          <label>Y-Axis</label>
          <value>blood pressure [normalized]</value>
        </data>
      </chart>
    </dashboard>
  </visual_elements>
  <link url="https://www.multidimensionality-of-aging.net/model_interpretability/time_series" type="external">Link para a Aplicação Web</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Sarima Tuner</title>
  <author>Gabriele (inferred), using Plotly Dash</author>
  <publication_date>2025-07-17</publication_date>
  <license>Web Application</license>
  <summary>
    [cite_start]O "Sarima Tuner" é uma aplicação web interativa de 4 etapas, criada com Plotly Dash, que guia os usuários através do processo completo de previsão de séries temporais usando modelos SARIMA[cite: 3, 44, 51]. [cite_start]A ferramenta abrange desde a configuração e visualização inicial dos dados, passando pela transformação para garantir a estacionariedade, até a seleção de modelos por meio de uma busca em grade de hiperparâmetros e, finalmente, a geração e análise de previsões[cite: 53, 56, 59, 61].
  </summary>
  <section>
    <title>Visão Geral e Fluxo de Trabalho da Aplicação</title>
    <paragraph>
      Esta aplicação permite a um usuário passar por todas as etapas necessárias para realizar uma previsão de série temporal com um modelo SARIMA. O processo é dividido em quatro seções principais.
    </paragraph>
    <list type="ordered">
      <item>
        <b>1. Configuração dos Dados:</b> O usuário começa selecionando um conjunto de dados. [cite_start]O padrão é o conjunto de dados "Air passenger", mas qualquer arquivo .csv pode ser usado[cite: 53, 54, 55]. [cite_start]A série temporal inicial é então visualizada em um gráfico de linhas[cite: 687].
      </item>
      <item>
        <b>2. [cite_start]Estacionariedade:</b> Esta etapa fornece ferramentas para transformar os dados para torná-los estacionários[cite: 56]. [cite_start]As transformações disponíveis incluem log e diferenciação[cite: 57]. [cite_start]A estacionariedade é avaliada usando o teste Augmented Dickey-Fuller [cite: 57, 720][cite_start], juntamente com gráficos de Autocorrelação (ACF) e Autocorrelação Parcial (PACF) para ajudar a identificar parâmetros adequados para o modelo[cite: 58].
      </item>
      <item>
        <b>3. [cite_start]Seleção do Modelo:</b> Aqui, uma busca em grade (grid search) de hiperparâmetros é realizada para encontrar o melhor modelo SARIMA(p,d,q; P,D,Q,m)[cite: 12, 59]. [cite_start]O usuário pode definir a porcentagem de divisão para treino [cite: 13, 14] [cite_start]e os intervalos para os parâmetros regulares e sazonais[cite: 17, 20]. [cite_start]A aplicação exibe os 10 modelos de melhor desempenho com base na pontuação AIC (Akaike Information Criterion)[cite: 60].
      </item>
      <item>
        <b>4. [cite_start]Previsão:</b> Na etapa final, o melhor modelo da busca em grade é automaticamente ajustado aos dados de treino para fazer previsões[cite: 62, 64]. [cite_start]A aplicação exibe um gráfico com os valores reais, as previsões para os conjuntos de treino e teste [cite: 64][cite_start], e permite gerar previsões futuras[cite: 639]. [cite_start]Também são mostrados gráficos ACF e PACF para os resíduos do modelo para análise de diagnóstico[cite: 65, 660].
      </item>
    </list>
  </section>
  <visual_elements>
    <dashboard>
      <title>Interface do Sarima Tuner</title>
      <visualization>
        A aplicação é apresentada como uma interface web de múltiplas abas, onde cada aba corresponde a uma etapa do processo de modelagem de séries temporais. Ela utiliza vários componentes interativos, como seletores, campos de entrada numérica e botões, juntamente com uma variedade de gráficos para visualização de dados e resultados do modelo.
      </visualization>
      <chart>
        <type>line</type>
        <title>Dataset Linechart</title>
      </chart>
      <chart>
        <type>line</type>
        <title>Transformed Data Linechart</title>
      </chart>
      <chart>
        <type>bar</type>
        <title>Autocorrelation (ACF)</title>
      </chart>
      <chart>
        <type>bar</type>
        <title>Partial Autocorrelation (PACF)</title>
      </chart>
      <chart>
        <type>line</type>
        <title>Final Model: Fit &amp; Prediction</title>
      </chart>
    </dashboard>
  </visual_elements>
  <link url="https://gabria1.pythonanywhere.com" type="external">URL da Aplicação Principal</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Interactive html export in Python</title>
  <author>Plotly</author>
  <publication_date>2025-07-17</publication_date>
  <license>Documentation</license>
  <summary>
    Este documento é um tutorial da Plotly que explica como exportar figuras interativas para arquivos HTML usando Python. Ele aborda vários métodos, incluindo salvar um arquivo HTML autônomo com o método `write_html`, controlar o tamanho do arquivo, incorporar gráficos em templates HTML personalizados usando Jinja2, e implementar uma funcionalidade de download de HTML em aplicações Dash. O documento fornece exemplos de código detalhados para cada técnica.
  </summary>
  <section>
    <title>Salvando Figuras como um Arquivo HTML Autônomo</title>
    <paragraph>
      [cite_start]Figuras da Plotly podem ser salvas como arquivos HTML que permanecem totalmente interativos quando abertos em um navegador[cite: 421, 426, 431]. [cite_start]Isso é feito usando o método `write_html`[cite: 430]. [cite_start]Por padrão, o arquivo HTML resultante é totalmente autônomo, contendo uma cópia embutida da biblioteca Plotly.js, o que o torna grande (mais de 5MB)[cite: 436, 437].
    </paragraph>
    <code>
      import plotly.express as px
      fig = px.scatter(x=range(10), y=range(10))
      fig.write_html("path/to/file.html")
    </code>
  </section>
  <section>
    <title>Incorporando Saída da Plotly em HTML com Jinja2</title>
    <paragraph>
      [cite_start]É possível inserir a saída da Plotly em templates HTML usando Jinja2[cite: 439]. [cite_start]Para isso, use o método `.to_html(full_html=False)` para gerar apenas o HTML do gráfico, sem a estrutura completa da página, e passe-o para o template[cite: 441, 442]. [cite_start]Primeiro, crie um arquivo de template HTML com um marcador de posição Jinja como `{{ fig }}`[cite: 444, 445].
    </paragraph>
    <code>
      &lt;!DOCTYPE html&gt;
      &lt;html&gt;
      &lt;head&gt;
          &lt;meta charset="utf-8" /&gt;
          &lt;meta name="viewport" content="width=device-width, initial-scale=1.0" /&gt;
      &lt;/head&gt;
      &lt;body&gt;
          &lt;h1&gt;Here's a Plotly graph!&lt;/h1&gt;
          {{ fig }}
          &lt;p&gt;And here's some text after the graph.&lt;/p&gt;
      &lt;/body&gt;
      &lt;/html&gt;
    </code>
    <paragraph>
      [cite_start]Em seguida, use um script Python para ler o template, renderizar o gráfico dentro dele e salvar o resultado em um novo arquivo HTML[cite: 478].
    </paragraph>
    <code>
      import plotly.express as px
      from jinja2 import Template

      # Carregar dados e criar figura
      data_canada = px.data.gapminder().query("country == 'Canada'")
      fig = px.bar(data_canada, x='year', y='pop')

      # Definir caminhos e dados para o template
      output_html_path = r"/path/to/output.html"
      input_template_path = r"/path/to/template.html"
      plotly_jinja_data = {"fig": fig.to_html(full_html=False)}

      # Renderizar o template com a figura
      with open(output_html_path, "w", encoding="utf-8") as output_file:
          with open(input_template_path) as template_file:
              j2_template = Template(template_file.read())
              output_file.write(j2_template.render(plotly_jinja_data))
    </code>
  </section>
  <section>
    <title>Exportação de HTML em Aplicações Dash</title>
    <paragraph>
      [cite_start]Dash é a maneira recomendada para construir aplicações analíticas com figuras da Plotly[cite: 495]. É possível implementar uma funcionalidade de download de HTML dentro de uma aplicação Dash. [cite_start]O exemplo de código a seguir mostra como criar um botão que permite ao usuário baixar o gráfico exibido como um arquivo HTML[cite: 522, 539].
    </paragraph>
    <code>
      from dash import Dash, dcc, html
      import plotly.express as px
      from base64 import b64encode
      import io

      app = Dash(__name__)

      buffer = io.StringIO()
      df = px.data.iris()
      fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
      fig.write_html(buffer)

      html_bytes = buffer.getvalue().encode()
      encoded = b64encode(html_bytes).decode()

      app.layout = html.Div([
          dcc.Graph(id="graph", figure=fig),
          html.A(
              html.Button("Download as HTML"),
              id="download",
              href="data:text/html;base64," + encoded,
              download="plotly_figure.html"
          )
      ])
    </code>
  </section>
  <section>
    <title>Documentação Completa de Parâmetros</title>
    <paragraph>
      [cite_start]A documentação completa para todos os parâmetros do método `write_html` pode ser acessada diretamente em Python usando a função `help()`[cite: 556]. [cite_start]Os parâmetros principais incluem `file` (o caminho do arquivo ou objeto gravável) e `config` (um dicionário para opções de configuração do Plotly.js)[cite: 561, 563].
    </paragraph>
  </section>
  <link url="https://plotly.com/python/interactive-html-export/" type="external">Interactive HTML Export in Python</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>GitHub Issue: Text is cut off on bars where textposition=outside #2001</title>
  <author>RedShift1</author>
  <publication_date>2017-09-13</publication_date>
  <license>GitHub Issue / Bug Report</license>
  <summary>
    [cite_start]Este documento é um relatório de bug do repositório plotly/plotly.js no GitHub, aberto em 13 de setembro de 2017[cite: 1466]. [cite_start]O problema relatado é que os rótulos de texto em gráficos de barras são cortados quando `textposition: 'outside'` é usado nas barras de maior valor[cite: 1467, 1469]. [cite_start]Embora a issue tenha sido fechada rapidamente como uma duplicata[cite: 1488, 1489], os usuários continuaram a encontrar o problema e, ao longo dos anos, contribuíram com várias soluções alternativas eficazes. [cite_start]As soluções incluem usar a opção `cliponaxis: false` [cite: 1497][cite_start], ajustar manualmente o intervalo do eixo ou as margens do gráfico [cite: 1512][cite_start], e usar anotações em vez de texto de barra[cite: 1562].
  </summary>
  <section>
    <title>Relatório de Bug Original</title>
    <paragraph>
      [cite_start]O usuário 'RedShift1' abriu a issue em 13 de setembro de 2017, relatando que, ao desenhar um gráfico de barras com a opção `textposition: 'outside'`, o texto das barras mais altas é cortado pela borda da área do gráfico[cite: 1466, 1467, 1469]. [cite_start]A issue foi fechada no mesmo dia por um mantenedor, que a marcou como uma duplicata da issue #2000, afirmando que a correção resolveria o problema para gráficos de barras e de dispersão[cite: 1488, 1489]. [cite_start]No entanto, os comentários subsequentes indicam que o problema persistiu para os usuários[cite: 1493].
    </paragraph>
    <visual_elements>
      <chart>
        <type>bar</type>
        <title>Exemplo do Bug de Texto Cortado</title>
        [cite_start]<visualization>Um gráfico de barras vertical onde o rótulo de texto da barra mais alta (valor 5900) é visivelmente cortado no topo[cite: 1469, 1502].</visualization>
      </chart>
    </visual_elements>
  </section>
  <section>
    <title>Soluções Alternativas da Comunidade</title>
    <paragraph>
      Ao longo de vários anos, os usuários da comunidade forneceram várias soluções alternativas eficazes para contornar o problema do texto cortado.
    </paragraph>
    <list type="unordered">
      [cite_start]<item><b>Usar `cliponaxis: false`</b>: Um usuário apontou para um Pull Request relacionado e sugeriu usar a opção `cliponaxis: false` no traço do gráfico de barras para evitar que o texto seja cortado pelo eixo[cite: 1497].</item>
      [cite_start]<item><b>Ajustar a Margem Superior</b>: Uma solução alternativa é aumentar manualmente a margem superior do layout do gráfico para criar espaço suficiente para o rótulo de texto[cite: 1512].</item>
      <item><b>Expandir o Intervalo do Eixo</b>: Outra abordagem é estender manualmente o intervalo do eixo y para que ele seja maior que o valor máximo da barra. [cite_start]Isso pode ser feito definindo um valor fixo [cite: 1512] [cite_start]ou calculando dinamicamente um novo máximo (por exemplo, `max_value * 1.1`)[cite: 1559].</item>
      <item><b>Usar Anotações</b>: Uma solução alternativa "à prova de falhas" é adicionar os rótulos como anotações separadas em vez de usar o parâmetro `textposition`. [cite_start]As anotações não são cortadas da mesma forma[cite: 1562].</item>
    </list>
  </section>
  <link url="https://github.com/plotly/plotly.js/issues/2001" type="external">Link para a Issue #2001 no GitHub</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Plotly Python 3D: axes with ticktexts shows only limited numbers of ticks</title>
  <author>bso</author>
  <publication_date>2025-07-11</publication_date>
  <license>Community Forum Post</license>
  <summary>
    [cite_start]Este documento é uma thread do Fórum da Comunidade Plotly onde um usuário relata um problema com gráficos 3D que não exibem todos os rótulos de eixo (`ticktexts`) especificados, mostrando apenas um número limitado[cite: 215, 216]. [cite_start]Outro usuário diagnostica que a causa é o uso de `autorange=False` sem definir manualmente um `range` para o eixo[cite: 253, 256]. [cite_start]A solução, confirmada pelo autor original, é definir explicitamente o `range` do eixo (por exemplo, `range=[0, len(values)]`), o que força a exibição de todos os ticks desejados[cite: 286].
  </summary>
  <section>
    <title>Problema: Exibição Limitada de Ticks em Eixos 3D</title>
    <paragraph>
      [cite_start]Em 11 de julho de 2025, o usuário 'bso' postou um problema que estava enfrentando com a versão 4.2.0 do Plotly[cite: 213, 219]. [cite_start]Ao tentar criar um gráfico 3D com nomes de ticks de eixo definidos individualmente usando `ticktext`, os eixos não exibiam mais do que 5 ou 7 ticks, independentemente do número de ticks fornecidos[cite: 215, 216]. [cite_start]O usuário observou que, embora os ticks não fossem visíveis na figura, os valores corretos do eixo estavam presentes no arquivo HTML bruto ao salvar o gráfico[cite: 217].
    </paragraph>
    <code>
      # Código original com o problema
      def make_axis(id, number):
          return [id+str(i) for i in range(number)]
      def get_3d_axis_dict(values):
          return dict(
              ticktext=[val for val in values],
              nticks=len(values),
              tickmode='array',
              autorange=False,
              tickvals=[i for i in range(len(values))],
          )
      # ... (resto do código de configuração da figura)
    </code>
  </section>
  <section>
    <title>Diagnóstico e Solução</title>
    <paragraph>
      [cite_start]O usuário 'AIMPED' respondeu, diagnosticando que o problema era causado pelo uso de `autorange=False` sem a especificação de um `range` para o eixo[cite: 251, 253, 256]. Quando `autorange` é definido como `False`, o Plotly requer que um intervalo explícito seja fornecido para renderizar o eixo corretamente.
    </paragraph>
    <list type="unordered">
      [cite_start]<item><b>Solução Proposta:</b> Manter `autorange=False` e adicionar um parâmetro `range` explícito ao dicionário de configuração do eixo, como `range=[0, len(values)]`[cite: 271].</item>
      [cite_start]<item><b>Alternativa:</b> Definir `autorange=True`, embora o usuário original tenha notado que isso não atendia à sua necessidade de exibir todos os ticks, pois mostrava apenas os ticks relacionados aos dados[cite: 256, 287].</item>
    </list>
    <code>
        # Código corrigido
        def get_3d_axis_dict(values):
            return dict(
                ticktext=[val for val in values],
                nticks=len(values),
                tickmode='array',
                autorange=False,
                range=[0, len(values)],  # Linha adicionada que corrige o problema
                tickvals=[i for i in range(len(values))],
            )
    </code>
  </section>
  <section>
    <title>Confirmação da Correção</title>
    <paragraph>
      [cite_start]O autor original, 'bso', confirmou que a adição do parâmetro `range` de fato resolveu o problema[cite: 284, 286]. [cite_start]Ele havia presumido incorretamente que, com `autorange=False`, o Plotly exibiria automaticamente todos os `tickvals` fornecidos, mas entendeu a necessidade de definir o intervalo manualmente[cite: 287, 288].
    </paragraph>
  </section>
  <link url="https://community.plotly.com/t/plotly-python-3d-axes-with-ticktexts-shows-only-limited-numbers-of-ticks/93115/print" type="external">Link para a Thread do Fórum</link>
  <language code="en-US">English</language>
</web_content>

<web_content>
  <title>Guia Mestre para Visualização de Dados Profissional com Python</title>
  <author>Sintetizado de Guias de Projeto Alignerr, Plotly, Pandas, Stack Overflow e outros</author>
  <publication_date>2025-07-17</publication_date>
  <license>Guia Instrucional Agregado</license>
  <summary>
    Este guia mestre consolida o conhecimento de múltiplas fontes para fornecer um fluxo de trabalho completo para a criação de visualizações de dados e dashboards de nível profissional usando Python. Ele abrange desde a configuração fundamental do projeto e ambiente, passando pela manipulação avançada de dados com Pandas (usando `groupby` e `melt`), até a criação de visualizações complexas com Plotly, com um foco especial em gráficos sunburst. Adicionalmente, o guia detalha princípios essenciais de design visual, como a seleção de cores acessíveis e o gerenciamento eficaz de rótulos, e conclui com um rigoroso processo de controle de qualidade e submissão final, baseado em um projeto de avaliação do mundo real.
  </summary>
  <section>
    <title>Fase 1: Fundação do Projeto e Fluxo de Trabalho Profissional</title>
    <paragraph>
      Antes de iniciar o desenvolvimento, é crucial estabelecer uma base sólida para o projeto. Um erro comum, como o uso de um ID de projeto compartilhado, levou a falhas sistêmicas em projetos anteriores, resultando em erros de upload e perda de trabalho. A solução é a geração de um Identificador Único Universal (UUID) para cada projeto.
    </paragraph>
    <list type="ordered">
      <item><b>Configuração do Ambiente (VS Code)</b>: É obrigatório verificar se as extensões essenciais como Python, Jupyter e Python Debugger da Microsoft estão instaladas.</item>
      <item><b>Instalação de Bibliotecas</b>: Instale as bibliotecas aprovadas e necessárias. Bibliotecas como `matplotlib` e `seaborn` são frequentemente proibidas em ambientes de avaliação profissional.</item>
      <item><b>Geração de UUID</b>: Acesse uma ferramenta como `uuidtools.com` para gerar um UUID v4 único. Este UUID será usado como o nome da pasta principal do projeto e é vital para uploads bem-sucedidos.</item>
      <item><b>Estrutura de Pastas Obrigatória</b>: Crie uma estrutura de pastas exata para garantir que os scripts encontrem os arquivos corretamente. A estrutura padrão é uma pasta raiz nomeada com o UUID, contendo subpastas `data`, `scripts`, e `outputs`.</item>
    </list>
  </section>
  <section>
    <title>Fase 2: Preparação e Manipulação de Dados com Pandas</title>
    <paragraph>
      A preparação de dados é um pré-requisito para qualquer visualização eficaz. O Pandas é a ferramenta principal para esta fase.
    </paragraph>
    <list type="unordered">
      <item><b>Agrupamento de Dados (`groupby`)</b>: A operação `groupby` envolve dividir o objeto, aplicar uma função e combinar os resultados. É essencial para calcular operações em grandes volumes de dados agrupados.</item>
      <item><b>Remodelagem de Dados (`melt`)</b>: A função `melt` é usada para "despivotar" um DataFrame de um formato largo para um formato longo. Isso é útil para preparar dados para bibliotecas de visualização que esperam colunas de identificador e colunas de valor.</item>
      <item><b>Geração de Dados Realistas</b>: Em vez de usar dados aleatórios sem sentido, crie datasets que contem uma história de negócio coerente. Isso demonstra conhecimento de domínio e resulta em dashboards mais significativos.</item>
    </list>
  </section>
  <section>
    <title>Fase 3: Visualização Principal com Gráficos Sunburst da Plotly</title>
    <paragraph>
      Gráficos sunburst são uma forma elegante e eficaz de visualizar dados hierárquicos usando um layout radial.
    </paragraph>
    <list type="ordered">
      <item>
        <b>Criação Básica (`plotly.express`)</b>: A maneira mais direta de criar um gráfico sunburst é com `px.sunburst`, usando o parâmetro `path` para definir a hierarquia a partir de colunas em um DataFrame retangular.
      </item>
      <item>
        <b>Controle Avançado (`graph_objects`)</b>: Para uma customização mais sofisticada, use `go.Sunburst`. Este método requer uma estrutura de dados explícita com `labels` (os nós) e `parents` (as relações pai-filho), oferecendo maior controle sobre a aparência e o comportamento.
      </item>
      <item>
        <b>Solução de Problemas: Quebra de Texto (Text Wrapping)</b>: Um problema comum é que rótulos de texto longos são cortados. Como o Plotly não suporta quebra de texto automática, a solução é pré-processar os rótulos inserindo a tag HTML `<br>` para criar quebras de linha manuais. Isso pode ser alcançado com uma função que utiliza a biblioteca `textwrap` do Python.
      </item>
    </list>
  </section>
  <section>
    <title>Fase 4: Design, Estética e Acessibilidade</title>
    <paragraph>
      Um bom design visual é crucial para a clareza e o profissionalismo. As escolhas de cores e tipografia devem ser deliberadas e focadas na acessibilidade e na narrativa dos dados.
    </paragraph>
    <list type="unordered">
      <item><b>Seleção de Paletas de Cores</b>: Opte por paletas profissionais e harmoniosas, evitando cores excessivamente brilhantes ou que causam distração. É fundamental usar esquemas de cores que sejam amigáveis para daltônicos; ferramentas como o `Viz Palette` podem ser usadas para testar a acessibilidade.</item>
      <item><b>Tipos de Paletas</b>: Use paletas categóricas para distinguir grupos distintos, sequenciais para dados progressivos e divergentes para dados com um ponto central neutro.</item>
      <item><b>Gerenciamento de Rótulos</b>: Garanta que os rótulos sejam concisos, legíveis e nunca cortados. Use a propriedade `uniformtext` no Plotly com `mode='hide'` para ocultar automaticamente rótulos que não cabem em seus segmentos.</item>
      <item><b>Requisitos de Formatação</b>: Em contextos profissionais, requisitos explícitos como "títulos em negrito" são comuns e devem ser rigorosamente seguidos para evitar penalidades na avaliação.</item>
    </list>
  </section>
  <section>
    <title>Fase 5: Controle de Qualidade e Submissão Final</title>
    <paragraph>
      A fase final é uma verificação rigorosa para garantir que todos os requisitos técnicos e de qualidade foram atendidos antes da entrega.
    </paragraph>
    <list type="ordered">
      <item><b>Checklist de Verificação Técnica</b>: Valide a estrutura de pastas, a geração correta de todos os arquivos (`.csv`, `.json`, `.html`), e a execução sem erros dos scripts `data_gen.py` e `viz.py`.</item>
      <item><b>Processo de Upload</b>: Use o script de upload fornecido, inserindo seu UUID único quando solicitado. Após a conclusão, anote cuidadosamente todos os caminhos `gs://` gerados, pois eles são necessários para a submissão.</item>
      <item><b>Submissão no Labelbox</b>: Preencha cada campo no formulário de submissão com precisão, incluindo a URL da imagem de referência, o prompt do usuário e os URIs `gs://` para cada artefato do projeto. Verifique novamente se o UUID em todos os caminhos está correto.</item>
      <item><b>Erros Fatais a Evitar</b>: Erros como usar um UUID incorreto, ter uma estrutura de pastas errada, ou usar bibliotecas proibidas podem levar à reprovação automática.</item>
    </list>
  </section>
</web_content>

<web_content>
  <title>Um Guia Prático para Cores em Visualização de Dados</title>
  <author>Sintetizado da Documentação da Simplified Science Publishing e PatternFly</author>
  <publication_date>2025-07-17</publication_date>
  <license>Guia Instrucional</license>
  <summary>
    Este guia aborda os princípios para selecionar paletas de cores eficazes e acessíveis para visualização de dados. Ele detalha a importância da cor para a narrativa e acessibilidade, apresenta ferramentas como Viz Palette e Color Brewer para testes, explica as propriedades das cores (matiz, saturação, luminosidade) e fornece um processo passo a passo e exemplos concretos de esquemas de cores profissionais.
  </summary>
  <section>
    <title>Por Que a Cor é Importante: Narrativa e Acessibilidade</title>
    <paragraph>
      [cite_start]A cor é um elemento crucial no design de gráficos e visualizações de dados, pois é uma ferramenta poderosa para contar histórias[cite: 1207]. [cite_start]A escolha certa das cores melhora a compreensão do público e torna o trabalho acessível a pessoas com Deficiência de Visão de Cores (CVD), também conhecida como daltonismo[cite: 1206]. [cite_start]A CVD é uma ocorrência comum, afetando aproximadamente 1 em cada 12 homens e 1 em cada 200 mulheres[cite: 1216].
    </paragraph>
  </section>
  <section>
    <title>Princípios para a Seleção Eficaz de Cores</title>
    <list type="unordered">
      [cite_start]<item><b>Contraste</b>: Você pode usar qualquer combinação de cores, desde que sejam altamente contrastantes[cite: 1227]. [cite_start]O contraste pode ser criado ajustando as três principais características da cor: matiz, saturação e luminosidade[cite: 1228]. [cite_start]Ao usar escala de cinza, é fundamental garantir que haja uma diferença de saturação de aproximadamente 15-30% entre as cores[cite: 1497].</item>
      [cite_start]<item><b>Cores Opostas</b>: Escolher cores de lados opostos do círculo cromático é uma das melhores maneiras de criar combinações de cores que são acessíveis para pessoas com daltonismo e outras dificuldades de percepção de cores[cite: 1221, 1222].</item>
      [cite_start]<item><b>Códigos de Cores</b>: Para garantir consistência entre diferentes plataformas e ferramentas (como Adobe Illustrator, Excel, PowerPoint, etc.), é importante usar códigos de cores[cite: 1241]. [cite_start]O código "HEX" é um código de seis dígitos que pode ser usado para identificar as cores exatas que você deseja manter consistentes[cite: 1241].</item>
    </list>
  </section>
  <section>
    <title>Um Fluxo de Trabalho Prático para Escolher Paletas</title>
    <paragraph>
      [cite_start]O processo a seguir pode ser usado para criar sua própria paleta de cores científica[cite: 1508]:
    </paragraph>
    <list type="ordered">
      [cite_start]<item><b>Passo 1</b>: Escolha uma paleta de cores que pareça boa para você e que melhor represente sua história de dados[cite: 1510].</item>
      [cite_start]<item><b>Passo 2</b>: Teste as cores em uma ferramenta como o **Viz Palette** para ver como elas afetarão um público com deficiência de visão de cores[cite: 1511, 1248]. [cite_start]O **Color Brewer** é outra ferramenta excelente para testar paletas de cores, especialmente para mapas e dados cartográficos[cite: 1450, 1451, 1452].</item>
      [cite_start]<item><b>Passo 3</b>: Ajuste a cor, matiz e saturação no Viz Palette até que não haja conflitos de cores[cite: 1512].</item>
      [cite_start]<item><b>Passo 4</b>: Aplique as cores finais à sua plataforma de visualização de dados, destacando o ponto principal de seus dados[cite: 1513].</item>
    </list>
  </section>
  <section>
    <title>Exemplos de Paletas e Casos de Uso</title>
    <list type="unordered">
      <item><b>Paletas de Sistemas Padrão</b>: Alguns sistemas de design, como o PatternFly, fornecem um ciclo de cores padrão para gráficos. [cite_start]Por exemplo, quando há mais de 6 grupos, o PatternFly usa automaticamente um ciclo de cores que inclui azul, verde, azul-petróleo, roxo e amarelo[cite: 503].</item>
      <item><b>Paletas Sequenciais</b>: Ideal para dados que têm uma progressão (por exemplo, de baixo para alto). [cite_start]Um exemplo é uma combinação de azul claro, médio e escuro[cite: 1279, 1303].</item>
      <item><b>Paletas Qualitativas/Categóricas</b>: Usadas para categorias distintas sem uma ordem inerente. [cite_start]Um exemplo inclui uma combinação de Azul, Laranja e Cinza[cite: 1299, 1300].</item>
      [cite_start]<item><b>Paletas Divergentes</b>: Adequadas para dados com um ponto médio neutro, como destacar desvios[cite: 1325].</item>
      [cite_start]<item><b>Escala de Cinza</b>: Uma ótima opção padrão quando usada com contraste suficiente[cite: 1495, 1496]. [cite_start]Exemplos de códigos HEX para uma paleta de cinza são `#b8b8b8` (cinza claro) e `#707070` (cinza escuro)[cite: 1276].</item>
    </list>
  </section>
  <link url="https://projects.susielu.com/viz-palette" type="external">Viz Palette Tool</link>
  <link url="https://colorbrewer2.org/" type="external">Color Brewer Tool</link>
</web_content>

