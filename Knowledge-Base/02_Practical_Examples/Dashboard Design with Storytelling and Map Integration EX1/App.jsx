import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { BarChart3, PieChart, TrendingUp, Map, Activity, Users, DollarSign, UserPlus, Target, ShoppingCart } from 'lucide-react'
import SunburstChart from './components/SunburstChart.jsx'
import BubbleChart from './components/BubbleChart.jsx'
import AreaChart from './components/AreaChart.jsx'
import StackedBarChart from './components/StackedBarChart.jsx'
import FlowChart from './components/FlowChart.jsx'
import MapChart from './components/MapChart.jsx'
import InteractiveKPI from './components/InteractiveKPI.jsx'
import FilterableChart from './components/FilterableChart.jsx'
import './App.css'

function App() {
  const [selectedFilter, setSelectedFilter] = useState('all')
  const [chartFilters, setChartFilters] = useState({
    sunburst: 'all',
    area: 'receita',
    bubble: 'all',
    stacked: 'all',
    flow: 'all'
  })

  const updateChartFilter = (chart, filter) => {
    setChartFilters(prev => ({
      ...prev,
      [chart]: filter
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white dark:bg-slate-900 shadow-sm border-b">
        <div className="max-w-full px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                Dashboard Analytics
              </h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Visualização Interativa de Dados Empresariais
              </p>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="text-sm">
                <Activity className="w-4 h-4 mr-1" />
                Tempo Real
              </Badge>
              <Button variant="outline" size="sm">
                Exportar Dados
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Filtros */}
      <div className="max-w-full px-6 py-4">
        <div className="flex flex-wrap gap-2">
          {['all', 'vendas', 'marketing', 'operacoes', 'financeiro'].map((filter) => (
            <Button
              key={filter}
              variant={selectedFilter === filter ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedFilter(filter)}
              className="capitalize"
            >
              {filter === 'all' ? 'Todos' : filter}
            </Button>
          ))}
        </div>
      </div>

      {/* Grid Principal do Dashboard */}
      <main className="max-w-full px-6 pb-8">
        <div className="grid grid-cols-12 gap-6">
          
          {/* KPIs - Linha Superior */}
          <div className="col-span-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <InteractiveKPI
              title="Receita Total"
              value={2400000}
              change={12}
              color="from-blue-500 to-blue-600"
              icon={DollarSign}
              isCurrency={true}
            />
            
            <InteractiveKPI
              title="Novos Clientes"
              value={1247}
              change={8}
              color="from-green-500 to-green-600"
              icon={UserPlus}
            />
            
            <InteractiveKPI
              title="Taxa de Conversão"
              value={3.2}
              change={0.4}
              color="from-purple-500 to-purple-600"
              icon={Target}
              isPercentage={true}
            />
            
            <InteractiveKPI
              title="Ticket Médio"
              value={847}
              change={5}
              color="from-orange-500 to-orange-600"
              icon={ShoppingCart}
              isCurrency={true}
            />
          </div>

          {/* Gráfico Sunburst - Hierarquia de Vendas */}
          <div className="col-span-12 lg:col-span-6">
            <FilterableChart
              title="Hierarquia de Vendas por Categoria"
              description="Distribuição hierárquica das vendas por categoria e subcategoria"
              icon={PieChart}
              filters={[
                { label: 'Todas', value: 'all' },
                { label: 'Eletrônicos', value: 'electronics' },
                { label: 'Roupas', value: 'clothing' },
                { label: 'Casa & Jardim', value: 'home' }
              ]}
              activeFilter={chartFilters.sunburst}
              onFilterChange={(filter) => updateChartFilter('sunburst', filter)}
            >
              <div className="h-96">
                <SunburstChart />
              </div>
            </FilterableChart>
          </div>

          {/* Gráfico de Área - Tendências */}
          <div className="col-span-12 lg:col-span-6">
            <FilterableChart
              title="Tendências de Receita"
              description="Evolução da receita ao longo dos últimos 12 meses"
              icon={TrendingUp}
              filters={[
                { label: 'Receita', value: 'receita' },
                { label: 'Meta', value: 'meta' },
                { label: 'Ambos', value: 'both' }
              ]}
              activeFilter={chartFilters.area}
              onFilterChange={(filter) => updateChartFilter('area', filter)}
            >
              <div className="h-96">
                <AreaChart />
              </div>
            </FilterableChart>
          </div>

          {/* Gráfico Bubble - Análise de Performance */}
          <Card className="col-span-12 lg:col-span-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Análise de Performance por Produto
              </CardTitle>
              <CardDescription>
                Relação entre volume de vendas, margem de lucro e satisfação do cliente
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <BubbleChart />
              </div>
            </CardContent>
          </Card>

          {/* Mapa - Distribuição Geográfica */}
          <Card className="col-span-12 lg:col-span-4">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Map className="w-5 h-5" />
                Distribuição Geográfica
              </CardTitle>
              <CardDescription>
                Vendas por região do Brasil
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <MapChart />
              </div>
            </CardContent>
          </Card>

          {/* Gráfico Stacked Bar - Comparação Temporal */}
          <Card className="col-span-12 lg:col-span-7">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Vendas por Canal e Período
              </CardTitle>
              <CardDescription>
                Comparação de vendas por canal de distribuição ao longo do tempo
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <StackedBarChart />
              </div>
            </CardContent>
          </Card>

          {/* Gráfico Flow - Fluxo de Conversão */}
          <Card className="col-span-12 lg:col-span-5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                Fluxo de Conversão
              </CardTitle>
              <CardDescription>
                Jornada do cliente desde o primeiro contato até a compra
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <FlowChart />
              </div>
            </CardContent>
          </Card>

        </div>
      </main>
    </div>
  )
}

export default App

