import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { TrendingUp, TrendingDown } from 'lucide-react'

const InteractiveKPI = ({ title, value, change, color, icon: Icon, isPercentage = false, isCurrency = false }) => {
  const [animatedValue, setAnimatedValue] = useState(0)
  const [isHovered, setIsHovered] = useState(false)
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedValue(value)
    }, 100)
    return () => clearTimeout(timer)
  }, [value])

  const formatValue = (val) => {
    if (isCurrency) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: val >= 1000000 ? 1 : 0,
        maximumFractionDigits: val >= 1000000 ? 1 : 0
      }).format(val)
    }
    if (isPercentage) {
      return `${val}%`
    }
    return new Intl.NumberFormat('pt-BR').format(val)
  }

  const isPositive = change >= 0

  return (
    <Card 
      className={`bg-gradient-to-r ${color} text-white transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium opacity-90 flex items-center justify-between">
          {title}
          <Icon className={`w-5 h-5 transition-transform duration-300 ${isHovered ? 'scale-110' : ''}`} />
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className={`text-2xl font-bold transition-all duration-500 ${isHovered ? 'scale-110' : ''}`}>
          {formatValue(animatedValue)}
        </div>
        <div className="flex items-center mt-1 opacity-80">
          {isPositive ? (
            <TrendingUp className="w-4 h-4 mr-1" />
          ) : (
            <TrendingDown className="w-4 h-4 mr-1" />
          )}
          <p className="text-xs">
            {isPositive ? '+' : ''}{change}% vs mês anterior
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

export default InteractiveKPI

