import React from 'react'
import Plot from 'react-plotly.js'

const SunburstChart = () => {
  const data = [{
    type: "sunburst",
    labels: [
      "Vendas", "Eletrônicos", "Roupas", "Casa & Jardim", "Livros",
      "Smartphones", "Laptops", "Tablets", "Camisetas", "Calças", "Vestidos",
      "Móveis", "Decoração", "Jardim", "Ficção", "Técnicos", "Biografias",
      "iPhone", "Samsung", "Xiaomi", "Dell", "HP", "Lenovo", "iPad", "Samsung Tab"
    ],
    parents: [
      "", "Vendas", "Vendas", "Vendas", "Vendas",
      "Eletrônicos", "Eletrônicos", "Eletrônicos", "Roupas", "Roupas", "Roupas",
      "Casa & Jardim", "Casa & Jardim", "Casa & Jardim", "Livros", "Livros", "Livros",
      "Smartphones", "Smartphones", "Smartphones", "Laptops", "Laptops", "Laptops", "Tablets", "Tablets"
    ],
    values: [
      100, 45, 25, 20, 10,
      20, 15, 10, 12, 8, 5,
      8, 7, 5, 4, 3, 3,
      8, 7, 5, 6, 5, 4, 6, 4
    ],
    branchvalues: "total",
    hovertemplate: '<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percentParent}<extra></extra>',
    maxdepth: 3,
    insidetextorientation: 'radial'
  }]

  const layout = {
    margin: { l: 0, r: 0, b: 0, t: 0 },
    font: { size: 12, family: "Inter, sans-serif" },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    colorway: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316']
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

export default SunburstChart

