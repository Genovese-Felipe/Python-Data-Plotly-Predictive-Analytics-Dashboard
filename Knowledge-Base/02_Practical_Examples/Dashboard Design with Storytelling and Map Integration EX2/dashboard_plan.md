# Plano do Dashboard de Visualização de Dados

## 1. Layout e Estrutura
- **Grade CSS:** Utilizar uma grade CSS de 12 colunas com largura total (100vw) e sem margens laterais.
- **Responsividade:** Cartões de gráficos devem se ajustar automaticamente ao seu intervalo de colunas e tamanho do visor.
- **Divisão principal:** O dashboard será dividido em seções lógicas para agrupar visualizações relacionadas.

## 2. Posicionamento dos Gráficos e Mapas
- **Gráficos Complexos (2-3):**
  - **Sunburst:** Ideal para hierarquias, talvez no topo ou em uma seção dedicada.
  - **Flow:** Para processos ou fluxos de dados, pode ser uma seção central.
  - **Stackedbar:** Para comparação de categorias ao longo do tempo ou entre grupos.
- **Gráficos Adicionais:**
  - **Bubble:** Para mostrar relações entre três variáveis, bom para insights de dados.
  - **Area:** Para tendências ao longo do tempo.
- **Integração de Mapas (8% do dashboard):** Uma seção dedicada ao mapa, possivelmente interligada com os dados dos gráficos para filtragem ou destaque de regiões.

## 3. Estilo Visual e Tipografia
- **Estilo Distinto:** O estilo visual deve refletir as características do conjunto de dados (a ser definido ou simulado).
- **Tipografia Consistente:** Escolher uma família de fontes para títulos, rótulos e texto, garantindo legibilidade e coesão.
- **Paleta de Cores:** Definir uma paleta de cores que seja esteticamente agradável e funcional para as visualizações, evitando sobrecarga visual.

## 4. Contando uma História com Dados
- Organizar os gráficos de forma que o usuário possa seguir uma narrativa, começando com uma visão geral e progredindo para detalhes mais específicos ou relações complexas.
- Utilizar interatividade (filtros, zoom, tooltips) para permitir que o usuário explore a história por conta própria.

## 5. Tecnologias a Serem Utilizadas
- **HTML5:** Estrutura da página.
- **CSS3:** Estilização e layout responsivo (CSS Grid).
- **JavaScript:** Lógica interativa e bibliotecas de gráficos.
- **Bibliotecas de Gráficos:** Avaliar Plotly.js, Chart.js, D3.js, Highcharts ou outras com base na pesquisa inicial e na complexidade dos gráficos solicitados.
- **Mapas:** Possivelmente Mapbox GL JS ou Leaflet.js para integração de mapas.

