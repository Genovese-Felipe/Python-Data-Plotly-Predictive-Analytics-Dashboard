# Dashboard Analytics - Visualização de Dados Interativa

Um dashboard moderno e responsivo para análise de dados empresariais, desenvolvido com React, TypeScript e bibliotecas de visualização avançadas.

## 🚀 Funcionalidades

### Visualizações Implementadas
- **Gráfico Sunburst**: Hierarquia de vendas por categoria e subcategoria
- **Gráfico Bubble**: Análise de performance por produto (volume, margem, satisfação)
- **Gráfico de Área**: Tendências de receita ao longo do tempo
- **Gráfico Stacked Bar**: Vendas por canal de distribuição
- **Gráfico Flow (Sankey)**: Fluxo de conversão de clientes
- **Mapa Interativo**: Distribuição geográfica de vendas no Brasil

### Características Técnicas
- ✅ **Responsivo**: Grade CSS de 12 colunas com largura total (100vw)
- ✅ **Interativo**: KPIs animados, filtros funcionais, hover states
- ✅ **Moderno**: Design com gradientes, sombras e micro-interações
- ✅ **Acessível**: Tooltips informativos e navegação intuitiva

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React 19** - Framework principal
- **Tailwind CSS** - Estilização e responsividade
- **shadcn/ui** - Componentes de interface
- **Lucide React** - Ícones

### Visualizações
- **Plotly.js** - Gráficos Sunburst, Bubble e Flow
- **Recharts** - Gráficos de Área e Stacked Bar
- **React Leaflet** - Mapas interativos

### Ferramentas
- **Vite** - Build tool e dev server
- **pnpm** - Gerenciador de pacotes

## 📊 Estrutura do Dashboard

### KPIs Principais
1. **Receita Total**: R$ 2.4M (+12%)
2. **Novos Clientes**: 1,247 (+8%)
3. **Taxa de Conversão**: 3.2% (+0.4%)
4. **Ticket Médio**: R$ 847 (+5%)

### Layout Responsivo
```
┌─────────────────────────────────────────────────────────┐
│                    Header + Filtros                     │
├─────────────┬─────────────┬─────────────┬─────────────┤
│    KPI 1    │    KPI 2    │    KPI 3    │    KPI 4    │
├─────────────────────────────┬───────────────────────────┤
│        Sunburst             │         Area Chart        │
├─────────────────────────────┼───────────────────────────┤
│           Bubble Chart      │         Map               │
├─────────────────────────────┼───────────────────────────┤
│        Stacked Bar          │         Flow Chart        │
└─────────────────────────────┴───────────────────────────┘
```

## 🎯 Funcionalidades Interativas

### Filtros Globais
- Todos os departamentos
- Vendas
- Marketing
- Operações
- Financeiro

### Filtros por Gráfico
- **Sunburst**: Todas categorias, Eletrônicos, Roupas, Casa & Jardim
- **Área**: Receita, Meta, Ambos
- **Outros gráficos**: Filtros específicos por contexto

### Animações e Micro-interações
- KPIs com animação de contagem
- Hover effects nos cartões
- Transições suaves entre estados
- Botões de expansão para filtros

## 🚀 Como Executar

### Desenvolvimento
```bash
cd dashboard-analytics
pnpm install
pnpm run dev --host
```

### Produção
```bash
pnpm run build
pnpm run preview
```

## 📱 Responsividade

O dashboard foi desenvolvido com mobile-first approach:

- **Mobile** (< 768px): Layout em coluna única
- **Tablet** (768px - 1024px): Layout em 2 colunas
- **Desktop** (> 1024px): Layout completo em grade

## 🎨 Design System

### Cores Principais
- **Azul**: #3b82f6 (Receita, Primário)
- **Verde**: #10b981 (Crescimento, Sucesso)
- **Roxo**: #8b5cf6 (Conversão, Destaque)
- **Laranja**: #f59e0b (Ticket Médio, Atenção)

### Tipografia
- **Família**: Inter (sistema)
- **Tamanhos**: 12px (small), 14px (base), 16px (lg), 24px (xl)

## 📈 Dados Simulados

O dashboard utiliza dados simulados realistas para demonstração:
- Vendas por categoria e região
- Métricas de performance temporal
- Fluxo de conversão de clientes
- Distribuição geográfica no Brasil

## 🔧 Estrutura de Componentes

```
src/
├── components/
│   ├── SunburstChart.jsx      # Gráfico hierárquico
│   ├── BubbleChart.jsx        # Análise multivariável
│   ├── AreaChart.jsx          # Tendências temporais
│   ├── StackedBarChart.jsx    # Comparação por canal
│   ├── FlowChart.jsx          # Fluxo de conversão
│   ├── MapChart.jsx           # Distribuição geográfica
│   ├── InteractiveKPI.jsx     # KPIs animados
│   └── FilterableChart.jsx    # Container com filtros
├── App.jsx                    # Componente principal
└── App.css                    # Estilos globais
```

## 🌟 Destaques Técnicos

1. **Performance**: Componentes otimizados com lazy loading
2. **Acessibilidade**: ARIA labels e navegação por teclado
3. **SEO**: Meta tags e estrutura semântica
4. **PWA Ready**: Configuração para Progressive Web App

## 📄 Licença

Este projeto foi desenvolvido como demonstração de capacidades técnicas em visualização de dados e desenvolvimento frontend moderno.

---

**Desenvolvido com ❤️ usando React + Vite**

