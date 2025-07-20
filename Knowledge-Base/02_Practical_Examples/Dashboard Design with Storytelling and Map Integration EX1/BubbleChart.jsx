import React from 'react'
import Plot from 'react-plotly.js'

const BubbleChart = () => {
  const data = [{
    x: [85, 92, 78, 88, 95, 82, 90, 87, 93, 79, 86, 91],
    y: [25, 35, 15, 30, 45, 20, 40, 28, 42, 18, 32, 38],
    mode: 'markers',
    marker: {
      size: [120, 180, 90, 150, 220, 100, 200, 140, 210, 95, 160, 190],
      sizemode: 'diameter',
      sizeref: 2,
      color: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      colorscale: [
        [0, '#3b82f6'],
        [0.2, '#10b981'],
        [0.4, '#8b5cf6'],
        [0.6, '#f59e0b'],
        [0.8, '#ef4444'],
        [1, '#06b6d4']
      ],
      showscale: true,
      colorbar: {
        title: "Satisfação",
        titleside: "right"
      },
      line: {
        color: 'rgba(255, 255, 255, 0.8)',
        width: 2
      }
    },
    text: [
      'Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E', 'Produto F',
      'Produto G', 'Produto H', 'Produto I', 'Produto J', 'Produto K', 'Produto L'
    ],
    hovertemplate: '<b>%{text}</b><br>' +
                   'Volume de Vendas: %{x}<br>' +
                   'Margem de Lucro: %{y}%<br>' +
                   'Tamanho da bolha: Receita<br>' +
                   '<extra></extra>',
    type: 'scatter'
  }]

  const layout = {
    title: {
      text: '',
      font: { size: 16, family: "Inter, sans-serif" }
    },
    xaxis: {
      title: 'Volume de Vendas (unidades)',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      zeroline: false,
      font: { family: "Inter, sans-serif" }
    },
    yaxis: {
      title: 'Margem de Lucro (%)',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      zeroline: false,
      font: { family: "Inter, sans-serif" }
    },
    margin: { l: 60, r: 60, b: 60, t: 20 },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: "Inter, sans-serif" },
    showlegend: false
  }

  const config = {
    displayModeBar: false,
    responsive: true
  }

  return (
    <Plot
      data={data}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '100%' }}
      useResizeHandler={true}
    />
  )
}

export default BubbleChart

