import React from 'react'
import Plot from 'react-plotly.js'

const FlowChart = () => {
  const data = [{
    type: "sankey",
    orientation: "h",
    node: {
      pad: 15,
      thickness: 30,
      line: {
        color: "black",
        width: 0.5
      },
      label: [
        "Visitantes", "Leads", "Prospects", "Clientes",
        "Orgânico", "Pago", "Social", "Email",
        "Qualificados", "Não Qualificados",
        "Proposta", "Negociação", "Fechamento"
      ],
      color: [
        "#3b82f6", "#10b981", "#8b5cf6", "#f59e0b",
        "#06b6d4", "#84cc16", "#f97316", "#ef4444",
        "#10b981", "#ef4444",
        "#8b5cf6", "#f59e0b", "#10b981"
      ]
    },
    link: {
      source: [0, 0, 0, 0, 1, 1, 2, 2, 8, 8, 8],
      target: [1, 4, 5, 6, 8, 9, 10, 11, 10, 11, 3],
      value: [10000, 4000, 3000, 2000, 6000, 1000, 3000, 2000, 2000, 1500, 800],
      color: [
        "rgba(59, 130, 246, 0.3)",
        "rgba(6, 182, 212, 0.3)",
        "rgba(132, 204, 22, 0.3)",
        "rgba(249, 115, 22, 0.3)",
        "rgba(16, 185, 129, 0.3)",
        "rgba(239, 68, 68, 0.3)",
        "rgba(139, 92, 246, 0.3)",
        "rgba(245, 158, 11, 0.3)",
        "rgba(139, 92, 246, 0.3)",
        "rgba(245, 158, 11, 0.3)",
        "rgba(16, 185, 129, 0.3)"
      ]
    }
  }]

  const layout = {
    title: {
      text: "",
      font: { size: 16, family: "Inter, sans-serif" }
    },
    margin: { l: 0, r: 0, b: 0, t: 0 },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { size: 10, family: "Inter, sans-serif" }
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

export default FlowChart

