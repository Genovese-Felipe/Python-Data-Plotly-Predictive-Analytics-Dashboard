import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const StackedBarChart = () => {
  const data = [
    { periodo: 'Q1 2023', online: 120000, loja: 80000, telefone: 40000, parceiros: 30000 },
    { periodo: 'Q2 2023', online: 140000, loja: 85000, telefone: 45000, parceiros: 35000 },
    { periodo: 'Q3 2023', online: 160000, loja: 90000, telefone: 50000, parceiros: 40000 },
    { periodo: 'Q4 2023', online: 180000, loja: 95000, telefone: 55000, parceiros: 45000 },
    { periodo: 'Q1 2024', online: 200000, loja: 100000, telefone: 60000, parceiros: 50000 },
    { periodo: 'Q2 2024', online: 220000, loja: 105000, telefone: 65000, parceiros: 55000 }
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
      const total = payload.reduce((sum, entry) => sum + entry.value, 0)
      return (
        <div className="bg-white dark:bg-slate-800 p-3 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {formatCurrency(entry.value)}
            </p>
          ))}
          <hr className="my-2 border-slate-200 dark:border-slate-600" />
          <p className="font-medium text-slate-900 dark:text-white text-sm">
            Total: {formatCurrency(total)}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
        <XAxis 
          dataKey="periodo" 
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
        <Legend 
          wrapperStyle={{ fontSize: '12px' }}
          iconType="rect"
        />
        <Bar 
          dataKey="online" 
          stackId="a" 
          fill="#3b82f6" 
          name="Online"
          radius={[0, 0, 0, 0]}
        />
        <Bar 
          dataKey="loja" 
          stackId="a" 
          fill="#10b981" 
          name="Loja Física"
          radius={[0, 0, 0, 0]}
        />
        <Bar 
          dataKey="telefone" 
          stackId="a" 
          fill="#8b5cf6" 
          name="Telefone"
          radius={[0, 0, 0, 0]}
        />
        <Bar 
          dataKey="parceiros" 
          stackId="a" 
          fill="#f59e0b" 
          name="Parceiros"
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  )
}

export default StackedBarChart

