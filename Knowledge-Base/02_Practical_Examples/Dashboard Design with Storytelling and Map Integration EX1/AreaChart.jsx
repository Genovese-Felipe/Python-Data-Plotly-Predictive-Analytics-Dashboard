import React from 'react'
import { AreaChart as RechartsAreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const AreaChart = () => {
  const data = [
    { mes: 'Jan', receita: 180000, meta: 200000 },
    { mes: 'Fev', receita: 220000, meta: 210000 },
    { mes: 'Mar', receita: 195000, meta: 220000 },
    { mes: 'Abr', receita: 240000, meta: 230000 },
    { mes: 'Mai', receita: 280000, meta: 240000 },
    { mes: 'Jun', receita: 260000, meta: 250000 },
    { mes: 'Jul', receita: 310000, meta: 260000 },
    { mes: 'Ago', receita: 295000, meta: 270000 },
    { mes: 'Set', receita: 340000, meta: 280000 },
    { mes: 'Out', receita: 320000, meta: 290000 },
    { mes: 'Nov', receita: 380000, meta: 300000 },
    { mes: 'Dez', receita: 420000, meta: 310000 }
  ]

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
  }

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-slate-800 p-3 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white">{`${label} 2024`}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name === 'receita' ? 'Receita' : 'Meta'}: {formatCurrency(entry.value)}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <RechartsAreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="colorReceita" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
          </linearGradient>
          <linearGradient id="colorMeta" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
        <XAxis 
          dataKey="mes" 
          axisLine={false}
          tickLine={false}
          tick={{ fontSize: 12, fill: '#64748b' }}
        />
        <YAxis 
          axisLine={false}
          tickLine={false}
          tick={{ fontSize: 12, fill: '#64748b' }}
          tickFormatter={formatCurrency}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="meta"
          stackId="1"
          stroke="#10b981"
          strokeWidth={2}
          fill="url(#colorMeta)"
          name="meta"
        />
        <Area
          type="monotone"
          dataKey="receita"
          stackId="2"
          stroke="#3b82f6"
          strokeWidth={2}
          fill="url(#colorReceita)"
          name="receita"
        />
      </RechartsAreaChart>
    </ResponsiveContainer>
  )
}

export default AreaChart

