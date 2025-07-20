<web_content>
  <title>Plotly Python Graphing Library</title>
  <author>Plotly</author>
  <publication_date>2025-07-16</publication_date>
  <license>Plotly.py is free and open source[cite: 12]. Copyright © 2025 Plotly. All rights reserved. [cite: 232]</license>
  <summary>Este documento apresenta a biblioteca de gráficos Python da Plotly, uma ferramenta de código aberto que permite a criação de gráficos interativos e com qualidade de publicação[cite: 11, 12]. Ele detalha uma vasta gama de tipos de gráficos, desde básicos e estatísticos até científicos, financeiros e geoespaciais. Além disso, aborda funcionalidades avançadas como integração com Jupyter, animações, controles personalizados e a criação de aplicações web analíticas com o Dash[cite: 43].</summary>
  <language code="en">English</language>
  
  <section>
    <title>Introdução</title>
    <paragraph>A biblioteca de gráficos Python da Plotly cria gráficos interativos e com qualidade de publicação. Exemplos de como fazer gráficos de linha, gráficos de dispersão, gráficos de área, gráficos de barras, barras de erro, box plots, histogramas, heatmaps, subplots, múltiplos eixos, gráficos polares e gráficos de bolhas. [cite: 11]</paragraph>
    <paragraph>Plotly.py é gratuito e de código aberto [cite: 12] e você pode visualizar o código-fonte, relatar problemas ou contribuir no GitHub. [cite: 12]</paragraph>
  </section>
  
  <section>
    <title>Fundamentos</title>
    <list>
      <item>The Figure Data Structure [cite: 21]</item>
      <item>Creating and Updating Figures [cite: 29]</item>
      <item>Displaying Figures [cite: 28]</item>
      <item>Plotly Express [cite: 41]</item>
      <item>Analytical Apps with Dash [cite: 43]</item>
    </list>
  </section>
  
  <section>
    <title>Gráficos Básicos</title>
    <list>
      <item>Scatter Plots [cite: 25]</item>
      <item>Line Charts [cite: 30]</item>
      <item>Bar Charts [cite: 31]</item>
      <item>Pie Charts [cite: 47]</item>
      <item>Bubble Charts [cite: 49]</item>
    </list>
  </section>
  
  <section>
    <title>Gráficos Estatísticos</title>
    <list>
      <item>Error Bars [cite: 32]</item>
      <item>Box Plots [cite: 33]</item>
      <item>Histograms [cite: 51]</item>
      <item>Distplots [cite: 54]</item>
      <item>2D Histograms [cite: 55]</item>
    </list>
  </section>
  
  <section>
    <title>Gráficos Científicos</title>
    <list>
      <item>Heatmaps [cite: 57]</item>
      <item>Imshow [cite: 58]</item>
      <item>Ternary Plots [cite: 63]</item>
      <item>Log Plots [cite: 64]</item>
    </list>
  </section>
  
  <section>
    <title>Gráficos Financeiros e de Séries Temporais</title>
    <list>
      <item>Time Series and Date Axes [cite: 71]</item>
      <item>Candlestick Charts [cite: 72]</item>
      <item>Waterfall Charts [cite: 84]</item>
      <item>Funnel Chart [cite: 81]</item>
      <item>OHLC Charts [cite: 82]</item>
    </list>
  </section>

  <section>
    <title>Mapas</title>
    <list>
      <item>MapLibre Migration [cite: 98]</item>
      <item>Tile Choropleth Maps [cite: 100]</item>
      <item>Lines on Tile Maps [cite: 103]</item>
      <item>Filled Area on Tile Maps [cite: 104]</item>
      <item>Bubble Maps [cite: 106]</item>
    </list>
  </section>
  
  <section>
    <title>Inteligência Artificial e Machine Learning</title>
    <list>
      <item>ML Regression [cite: 111]</item>
      <item>KNN Classification [cite: 113]</item>
      <item>ROC and PR Curves [cite: 115]</item>
      <item>PCA Visualization [cite: 117]</item>
      <item>AI/ML Apps with Dash [cite: 119]</item>
    </list>
  </section>
  
  <section>
    <title>Bioinformática</title>
    <list>
      <item>Volcano Plot [cite: 121]</item>
      <item>Manhattan Plot [cite: 123]</item>
      <item>Clustergram [cite: 124]</item>
      <item>Alignment Chart [cite: 126]</item>
    </list>
  </section>
  
  <section>
    <title>Gráficos 3D</title>
    <list>
      <item>3D Axes [cite: 131]</item>
      <item>3D Scatter Plots [cite: 133]</item>
      <item>3D Surface Plots [cite: 135]</item>
      <item>3D Subplots [cite: 136]</item>
      <item>3D Camera Controls [cite: 138]</item>
    </list>
  </section>

  <section>
    <title>Interação com Jupyter Widgets</title>
    <list>
      <item>Plotly FigureWidget Overview [cite: 162]</item>
      <item>Jupyter Lab with FigureWidget [cite: 164]</item>
      <item>Interactive Data Analysis with FigureWidget ipywidgets [cite: 166]</item>
      <item>Click Events [cite: 167]</item>
    </list>
  </section>

  <section>
    <title>Controles Personalizados e Animações</title>
    <list>
      <item>Custom Buttons [cite: 173]</item>
      <item>Sliders [cite: 179]</item>
      <item>Dropdown Menus [cite: 188]</item>
      <item>Range Slider and Selector [cite: 189]</item>
      <item>Intro to Animations [cite: 176]</item>
    </list>
  </section>

  <visual_elements>
    <chart>
      <type>bar</type>
      <title>Gráficos de Barras</title>
    </chart>
    <chart>
      <type>line</type>
      <title>Gráficos de Linha</title>
    </chart>
    <chart>
      <type>pie</type>
      <title>Gráficos de Pizza</title>
    </chart>
    <chart>
      <type>scatter</type>
      <title>Gráficos de Dispersão</title>
    </chart>
    <chart>
      <type>heatmap</type>
      <title>Mapas de Calor</title>
    </chart>
    <chart>
      <type>histogram</type>
      <title>Histogramas</title>
    </chart>
    <chart>
      <type>box-plot</type>
      <title>Box Plots</title>
    </chart>
    <chart>
        <type>candlestick</type>
        <title>Gráficos de Candlestick</title>
    </chart>
    <chart>
        <type>3d-surface</type>
        <title>Gráficos de Superfície 3D</title>
    </chart>
    <dashboard>
        <title>Analytical Apps with Dash</title>
        <metric>
            <label>Descrição</label>
            <value>Crie aplicações web analíticas com Dash, sem necessidade de JavaScript. [cite: 43, 206]</value>
        </metric>
    </dashboard>
  </visual_elements>
  
  <link url="https://plotly.com/python/" type="external">Página Principal da Biblioteca Python</link>
  <link url="https://github.com/plotly/plotly.py" type="external">Repositório no GitHub [cite: 12]</link>
  <link url="https://dash.plotly.com/" type="external">Dash [cite: 40, 220]</link>
  <link url="https://plotly.com/studio/?utm.medium-graphing libraries&amp;utm campaign=studio early access&amp;utm content=sidebar" type="external">Plotly Studio Early Access [cite: 14]</link>
  <link url="https://community.plot.ly/" type="external">Suporte da Comunidade [cite: 230]</link>
  <link url="https://plotly.com/graphing-libraries" type="external">Documentação [cite: 2, 230]</link>
</web_content>

<web_content>
  <title>Plot CSV Data in Python</title>
  <author>Plotly</author>
  <publication_date>2025-07-16</publication_date>
  <license>Copyright © 2025 Plotly. All rights reserved.</license>
  <summary>Este documento é um tutorial que demonstra como criar gráficos a partir de arquivos de dados CSV em Python utilizando a biblioteca Plotly em conjunto com a biblioteca Pandas. São abordados três métodos principais: o uso do Plotly Express para criação rápida de gráficos, a utilização dos Graph Objects para maior customização e a integração dos gráficos gerados em aplicações analíticas interativas com o framework Dash.</summary>
  <language code="en">English</language>
  
  <section>
    <title>Introdução ao Plot de Dados CSV</title>
    [cite_start]<paragraph>CSV (comma-delimited-values) é um formato muito popular para armazenar dados estruturados[cite: 10]. [cite_start]Neste tutorial, veremos como plotar belos gráficos usando dados de um CSV e a biblioteca Pandas[cite: 11]. [cite_start]Aprenderemos como importar dados CSV de uma fonte externa (uma URL) e plotá-los usando Plotly[cite: 12].</paragraph>
  </section>

  <section>
    <title>Plot a partir de CSV com Plotly Express</title>
    [cite_start]<paragraph>Primeiro, importamos os dados e os visualizamos usando Pandas[cite: 13].</paragraph>
    <code language="python">
      import pandas as pd
      df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
      df.head()
    </code>
    <table>
      <row>
        <cell>""</cell>
        <cell>"AAPL_x"</cell>
        <cell>"AAPL_y"</cell>
      </row>
      <row>
        <cell>"0"</cell>
        <cell>"2014-01-02"</cell>
        <cell>"77.445395"</cell>
      </row>
      <row>
        <cell>"1"</cell>
        <cell>"2014-01-03"</cell>
        <cell>"77.045575"</cell>
      </row>
      <row>
        <cell>"2"</cell>
        <cell>"2014-01-06"</cell>
        <cell>"74.896972"</cell>
      </row>
      <row>
        <cell>"3"</cell>
        <cell>"2014-01-07"</cell>
        <cell>"75.856461"</cell>
      </row>
      <row>
        <cell>"4"</cell>
        <cell>"2014-01-08"</cell>
        <cell>"75.091947"</cell>
      </row>
    </table>
    [cite_start]<paragraph>O código a seguir utiliza a função `line` do Plotly Express para gerar um gráfico de linha a partir dos dados do CSV[cite: 22].</paragraph>
    <code language="python">
      import plotly.express as px
      df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
      fig = px.line(df, x='AAPL_x', y='AAPL_y', title='Apple Share Prices over time (2014)')
      fig.show()
    </code>
  </section>
  
  <section>
    <title>Plot a partir de CSV com graph_objects</title>
    [cite_start]<paragraph>É possível obter um controle mais granular sobre o gráfico utilizando `graph_objects`[cite: 86]. [cite_start]O código abaixo cria uma figura e adiciona um traço do tipo `Scatter`[cite: 90].</paragraph>
    <code language="python">
      import pandas as pd
      import plotly.graph_objects as go
      
      df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
      
      fig = go.Figure(go.Scatter(x = df['AAPL_x'], y = df['AAPL_y'],
                            name='Share Prices (in USD)'))
      
      fig.update_layout(title_dict=dict(text='Apple Share Prices over time (2014)'),
                        plot_bgcolor='rgb(230, 230,230)',
                        showlegend=True)
      
      fig.show()
    </code>
  </section>

  <section>
    <title>Plot a partir de CSV no Dash</title>
    [cite_start]<paragraph>Dash é a melhor maneira de construir aplicações analíticas em Python usando figuras Plotly[cite: 41]. [cite_start]Para exibir uma figura em uma aplicação Dash, basta passá-la para o argumento `figure` do componente `dcc.Graph`[cite: 118, 129].</paragraph>
    <code language="python">
      from dash import Dash, dcc, html, Input, Output
      import plotly.express as px
      import pandas as pd

      app = Dash(__name__)

      app.layout = html.Div([
          html.H4('Simple stock plot with adjustable axis'),
          html.Button("Switch Axis", n_clicks=0, id='button'),
          dcc.Graph(id="graph"),
      ])

      @app.callback(
          Output("graph", "figure"),
          Input("button", "n_clicks"))
      def display_graph(n_clicks):
          df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
          
          if n_clicks % 2 == 0:
              x, y = 'AAPL_x', 'AAPL_y'
          else:
              x, y = 'AAPL_y', 'AAPL_x'

          fig = px.line(df, x=x, y=y)
          return fig

      # app.run(debug=True)
    </code>
  </section>

  <visual_elements>
    <chart>
      <type>line</type>
      <title>Apple Share Prices over time (2014)</title>
      <data>
        <label>Fonte dos Dados</label>
        <value>https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv</value>
      </data>
    </chart>
  </visual_elements>
  
  <link url="https://plotly.com/python/plot-data-from-csv/" type="external">Página do Tutorial</link>
  <link url="https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv" type="external">Fonte de Dados CSV (Ações da Apple 2014)</link>
  <link url="https://plotly.com/dash/" type="external">Documentação do Dash</link>
  <link url="https://github.com/plotly/plotly.py/edit/doc-prod/doc/python/plot-data-from-csv.md" type="external">Sugerir Edição desta Página</link>
</web_content>

<web_content>
  <title>Random Walk in Python</title>
  <author>Plotly</author>
  <publication_date>2025-07-16</publication_date>
  <license>Copyright © 2025 Plotly. All rights reserved.</license>
  <summary>Este documento é um tutorial que explica o conceito de 'random walk' (passeio aleatório) e demonstra como simular e visualizar exemplos em 1D e 2D utilizando Python, com as bibliotecas NumPy e Plotly. [cite: 9, 10] O conteúdo aborda a teoria, a implementação prática com blocos de código, a visualização dos resultados com gráficos de dispersão e a conexão entre passeios aleatórios e o fenômeno da difusão, ilustrada com histogramas. [cite: 15, 128] Adicionalmente, apresenta uma seção com a fundamentação matemática do valor esperado de um passeio aleatório. [cite: 205, 213]</summary>
  <language code="en">English</language>
  
  <section>
    <title>Introdução ao Random Walk (Passeio Aleatório)</title>
    <paragraph>Um passeio aleatório (random walk) pode ser entendido como um processo aleatório no qual um marcador é movido aleatoriamente por algum espaço. [cite: 13] É mais comumente conceituado em uma dimensão ($\mathbb{Z}$), duas dimensões ($\mathbb{Z}^2$) ou três dimensões ($\mathbb{Z}^3$) no espaço Cartesiano, onde $\mathbb{Z}$ representa o conjunto dos inteiros. [cite: 14] As visualizações neste tutorial utilizam gráficos de dispersão com uma escala de cores para denotar a sequência temporal do passeio. [cite: 15]</paragraph>
  </section>

  <section>
    <title>Random Walk em 1D</title>
    <paragraph>A flutuação (jitter) nos pontos de dados ao longo dos eixos x e y tem como objetivo iluminar onde os pontos estão sendo desenhados e qual é a tendência do passeio aleatório. [cite: 17]</paragraph>
    <code language="python">
      import plotly.graph_objects as go
      import numpy as np

      np.random.seed(1)
      l = 100
      steps = np.random.choice([-1, 1], size=l) + 0.05 * np.random.randn(l)
      position = np.cumsum(steps)
      y = 0.05 * np.random.randn(l)

      fig = go.Figure(data=go.Scatter(
          x = position,
          y = y,
          mode = 'markers',
          name = 'Random Walk in 1D',
          marker = dict(
              color=np.arange(l),
              size=7,
              colorscale='Reds',
              showscale=True,
          )
      ))
      fig.update_layout(yaxis_range=[-1,1])
      fig.show()
    </code>
  </section>
  
  <section>
    <title>Random Walk em 2D</title>
    <paragraph>O conceito é estendido para duas dimensões, onde passos são dados tanto na direção x quanto na y.</paragraph>
    <code language="python">
      import plotly.graph_objects as go
      import numpy as np

      l = 1000
      x_steps = np.random.choice([-1, 1], size=l) + 0.2 * np.random.randn(l)
      y_steps = np.random.choice([-1, 1], size=l) + 0.2 * np.random.randn(l)
      x_position = np.cumsum(x_steps)
      y_position = np.cumsum(y_steps)

      fig = go.Figure(data=go.Scatter(
          x = x_position,
          y = y_position,
          mode = 'markers',
          name = 'Random Walk',
          marker = dict(
              color=np.arange(l),
              size=8,
              colorscale='Greens',
              showscale=True
          )
      ))
      fig.show()
    </code>
  </section>

  <section>
    <title>Random Walk e Difusão</title>
    <paragraph>Esta seção mostra a ligação entre passeios aleatórios e difusão. [cite: 128] Um grande número de passeios aleatórios é computado, representando, por exemplo, moléculas em uma pequena gota de um químico. [cite: 129] Embora todas as trajetórias comecem em 0, após algum tempo, a distribuição espacial dos pontos se torna uma distribuição Gaussiana. [cite: 130] Além disso, a distância média da origem cresce como $\sqrt{t}$. [cite: 131]</paragraph>
    <code language="python">
      # Histograma das posições finais
      import plotly.graph_objects as go
      import numpy as np

      l = 1000
      N = 10000
      steps = np.random.choice([-1,1], size=(N, l)) + 0.05*np.random.standard_normal((N, l))
      position = np.cumsum(steps, axis=1)
      
      fig = go.Figure(data=go.Histogram(x=position[:, -1]))
      fig.show()
    </code>
  </section>

  <section>
    <title>Dica Avançada: Fundamentação Matemática</title>
    <paragraph>Podemos pensar formalmente em um passeio aleatório 1D como um ponto saltando ao longo da linha de números inteiros. [cite: 206] Seja $Z_i$ uma variável aleatória que assume os valores +1 e -1. [cite: 207] Considere a soma $S_{n}=\sum_{i=0}^{n}Z_{i}$, onde S_n representa o ponto final do passeio após n passos. [cite: 211, 212] Para encontrar o valor esperado de $S_n$, podemos calculá-lo diretamente. [cite: 213] Como cada $Z_i$ é independente, temos $E(S_{n})=\sum_{i=0}^{n}E(Z_{i})$. [cite: 218] Uma vez que $Z_i$ assume os valores +1 e -1 com probabilidade de $\frac{1}{2}$ cada, $E(Z_i) = 1 \cdot P(Z_i=1) + (-1) \cdot P(Z_i=-1) = \frac{1}{2} - \frac{1}{2} = 0$. [cite: 209, 214, 219, 220] Isso resulta em $E(S_n)=0$, o que significa que esperamos que o passeio aleatório paire em torno de 0, independentemente de quantos passos damos. [cite: 221]</paragraph>
  </section>
  
  <visual_elements>
    <chart>
      <type>scatter</type>
      <title>Visualização de um Random Walk em 1D</title>
    </chart>
    <chart>
      <type>scatter</type>
      <title>Visualização de um Random Walk em 2D</title>
    </chart>
    <chart>
      <type>histogram</type>
      <title>Distribuição Espacial das Posições Finais (Difusão)</title>
    </chart>
     <chart>
      <type>line</type>
      <title>Distância Média e Quadrática Média vs. Tempo na Difusão</title>
    </chart>
  </visual_elements>
  
  <link url="https://plotly.com/python/random-walk/" type="external">Página do Tutorial</link>
  <link url="https://en.wikipedia.org/wiki/Random_walk" type="external">Artigo da Wikipedia sobre Random Walk</link>
  <link url="https://dash.plot.ly/" type="external">Documentação do Dash</link>
  <link url="https://github.com/plotly/plotly.py/edit/doc-prod/doc/python/random-walk.md" type="external">Sugerir Edição desta Página</link>
</web_content>

<web_content>
  <title>Peak Finding in Python</title>
  <author>Plotly</author>
  <publication_date>2025-07-16</publication_date>
  <license>Copyright © 2025 Plotly. All rights reserved.</license>
  <summary>Este documento é um tutorial que ensina como encontrar picos e vales em conjuntos de dados utilizando Python. O processo utiliza a biblioteca SciPy, especificamente a função `find_peaks`, para a lógica de detecção, a biblioteca Pandas para manipulação de dados e a Plotly para visualização. O guia demonstra como carregar dados de séries temporais, aplicar a detecção de picos básica, e subsequentemente filtrar os resultados para identificar apenas os picos mais significativos utilizando um limiar (threshold).</summary>
  <language code="en">English</language>
  
  <section>
    <title>Introdução e Importação de Dados</title>
    [cite_start]<paragraph>Para começar a detectar picos, o tutorial utiliza dados sobre a produção mensal de leite. [cite: 16] [cite_start]As bibliotecas necessárias são Pandas para manipulação de dados e SciPy para a função de detecção de picos. [cite: 12]</paragraph>
    <code language="python">
      # Importação de bibliotecas e dados
      import pandas as pd
      from scipy.signal import find_peaks
      import plotly.graph_objects as go

      # Leitura dos dados de um arquivo CSV
      milk_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/monthly-milk-production-pounds.csv')
      time_series = milk_data['Monthly milk production (pounds per cow)']

      # Plot inicial da série temporal
      fig = go.Figure(data=go.Scatter(
          y = time_series,
          mode = 'lines'
      ))
      fig.show()
    </code>
  </section>

  <section>
    <title>Detecção de Picos</title>
    [cite_start]<paragraph>Para localizar os picos, utilizamos a função `find_peaks` da SciPy, que retorna os índices do eixo x onde os picos ocorrem. [cite: 53] [cite_start]Em seguida, esses picos detectados são plotados sobre o gráfico original para visualização. [cite: 67, 75]</paragraph>
    <code language="python">
      # Encontra os picos na série temporal
      indices, _ = find_peaks(time_series)

      # Cria a figura e adiciona o plot original
      fig = go.Figure()
      fig.add_trace(go.Scatter(
          y=time_series,
          mode='lines+markers',
          name='Original Plot'
      ))

      # Adiciona os picos detectados ao gráfico
      fig.add_trace(go.Scatter(
          x=indices,
          y=[time_series[j] for j in indices],
          mode='markers',
          marker=dict(
              size=8,
              color='red',
              symbol='cross'
          ),
          name='Detected Peaks'
      ))
      fig.show()
    </code>
  </section>
  
  <section>
    <title>Filtrando Apenas os Picos Mais Altos</title>
    [cite_start]<paragraph>É possível ajustar um limiar (threshold) para identificar apenas os picos mais significativos. [cite: 91] [cite_start]O parâmetro `threshold` na função `find_peaks` pode ser usado para este propósito. [cite: 109]</paragraph>
    <code language="python">
      # Encontra os picos com um threshold
      indices, _ = find_peaks(time_series, threshold=20)

      # Plot com os picos filtrados
      fig = go.Figure()
      fig.add_trace(go.Scatter(
          y=time_series,
          mode='lines+markers',
          name='Original Plot'
      ))
      fig.add_trace(go.Scatter(
          x=indices,
          y=[time_series[j] for j in indices],
          mode='markers',
          marker=dict(
              size=8,
              color='red',
              symbol='cross'
          ),
          name='Detected Peaks'
      ))
      fig.show()
    </code>
  </section>

  <visual_elements>
    <chart>
      <type>line</type>
      <title>Série Temporal da Produção Mensal de Leite</title>
      <data>
        <label>Fonte dos Dados</label>
        <value>https://raw.githubusercontent.com/plotly/datasets/master/monthly-milk-production-pounds.csv</value>
      </data>
    </chart>
    <chart>
      <type>line</type>
      <title>Série Temporal com Picos Detectados</title>
      <data>
        <label>Legenda</label>
        <value>Original Plot (Linha Azul), Detected Peaks (Cruzes Vermelhas)</value>
      </data>
    </chart>
  </visual_elements>
  
  <link url="https://plotly.com/python/peak-finding/" type="external">Página do Tutorial</link>
  <link url="https://raw.githubusercontent.com/plotly/datasets/master/monthly-milk-production-pounds.csv" type="external">Fonte de Dados CSV (Produção de Leite)</link>
  <link url="https://pandas.pydata.org/docs/user_guide/10min.html" type="external">Documentação do Pandas</link>
  <link url="https://www.scipy.org/" type="external">Documentação do SciPy</link>
  <link url="https://dash.plot.ly/" type="external">Documentação do Dash</link>
</web_content>

<web_content>
  <title>LaTeX in Python</title>
  <author>Plotly</author>
  <publication_date>2025-07-16</publication_date>
  <license>Copyright © 2025 Plotly. [cite_start]All rights reserved. [cite: 988]</license>
  <summary>Este documento é um tutorial que explica como adicionar e renderizar expressões matemáticas e notações complexas usando LaTeX em gráficos Plotly. Ele detalha que a funcionalidade depende da biblioteca MathJax e que as diretivas LaTeX devem ser envolvidas por cifrões ($...$). O guia fornece exemplos de código práticos para adicionar LaTeX a títulos de gráficos, rótulos de eixos e nomes de legendas, tanto com o Plotly Express quanto com os Graph Objects.</summary>
  
  <language code="en">English</language>
  
  <section>
    <title>Tipografia LaTeX em Gráficos Plotly</title>
    [cite_start]<paragraph>Títulos de figuras, rótulos de eixos e anotações aceitam diretivas LaTeX para renderizar fórmulas matemáticas e notações quando todo o rótulo está entre cifrões ($...$)[cite: 876]. [cite_start]Essa renderização é gerenciada pela biblioteca MathJax, que deve ser carregada no ambiente onde as figuras estão sendo exibidas[cite: 877]. [cite_start]O MathJax é incluído por padrão em ambientes do tipo Jupyter, mas pode exigir o carregamento separado em outros contextos, como através de uma tag &lt;script&gt;[cite: 878].</paragraph>
  </section>

  <section>
    <title>Exemplo com Plotly Express</title>
    <paragraph>O exemplo a seguir demonstra como adicionar títulos e rótulos de eixos formatados com LaTeX a um gráfico de linha criado com Plotly Express.</paragraph>
    <code language="python">
      import plotly.express as px

      fig = px.line(x=[1, 2, 3, 4], y=[1, 4, 9, 16], 
                    title=r'$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$')
      
      fig.update_layout(
          xaxis_title=r'$\sqrt{(n_\text{c}(t|T_\text{early}))}$',
          yaxis_title=r'$d, r \text{ (solar radius)}$'
      )
      
      fig.show()
    </code>
  </section>
  
  <section>
    <title>Exemplo com Graph Objects e Múltiplas Traces</title>
    <paragraph>Este exemplo usa `graph_objects` para criar um gráfico com duas 'traces' (séries de dados), onde o nome de cada uma é uma expressão LaTeX, que será renderizada na legenda do gráfico.</paragraph>
    <code language="python">
      import plotly.graph_objects as go

      fig = go.Figure()

      fig.add_trace(go.Scatter(
          x=[1, 2, 3, 4],
          y=[1, 4, 9, 16],
          name=r'$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$'
      ))

      fig.add_trace(go.Scatter(
          x=[1, 2, 3, 4],
          y=[0.5, 2, 4.5, 8],
          name=r'$\beta_{1c} = 25 \pm 11 \text{ km s}^{-1}$'
      ))

      fig.update_layout(
          xaxis_title=r'$\sqrt{(n_\text{c}(t|T_\text{early}))}$',
          yaxis_title=r'$d, r \text{ (solar radius)}$'
      )

      fig.show()
    </code>
  </section>

  <visual_elements>
    <chart>
      <type>line</type>
      <title>Gráfico com Título e Eixos em LaTeX</title>
      <data>
        <label>Título</label>
        <value>$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$</value>
      </data>
      <data>
        <label>Eixo X</label>
        <value>$\sqrt{(n_\text{c}(t|T_\text{early}))}$</value>
      </data>
      <data>
        <label>Eixo Y</label>
        <value>$d, r \text{ (solar radius)}$</value>
      </data>
    </chart>
    <chart>
      <type>line</type>
      <title>Gráfico com Legendas em LaTeX</title>
      <data>
        <label>Legenda 1</label>
        <value>$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$</value>
      </data>
       <data>
        <label>Legenda 2</label>
        <value>$\beta_{1c} = 25 \pm 11 \text{ km s}^{-1}$</value>
      </data>
    </chart>
  </visual_elements>
  
  [cite_start]<link url="https://plotly.com/python/LaTeX/" type="external">Página do Tutorial [cite: 900, 961, 994]</link>
  [cite_start]<link url="https://www.npmjs.com/package/mathjax?activeTab=versions" type="external">Biblioteca MathJax [cite: 877]</link>
  [cite_start]<link url="https://dash.plot.ly/" type="external">Documentação do Dash [cite: 945]</link>
</web_content>

