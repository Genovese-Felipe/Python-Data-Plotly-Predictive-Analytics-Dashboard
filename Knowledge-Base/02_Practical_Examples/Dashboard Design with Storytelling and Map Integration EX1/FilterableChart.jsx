import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'

const FilterableChart = ({ title, description, icon: Icon, children, filters, onFilterChange, activeFilter }) => {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <Card className="transition-all duration-300 hover:shadow-lg">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Icon className="w-5 h-5" />
            <div>
              <CardTitle className="text-lg">{title}</CardTitle>
              <CardDescription className="text-sm">{description}</CardDescription>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-slate-500 hover:text-slate-700"
          >
            {isExpanded ? '−' : '+'}
          </Button>
        </div>
        
        {/* Filtros */}
        {filters && (
          <div className={`transition-all duration-300 overflow-hidden ${isExpanded ? 'max-h-20 opacity-100' : 'max-h-0 opacity-0'}`}>
            <div className="flex flex-wrap gap-2 pt-3 border-t border-slate-200">
              {filters.map((filter) => (
                <Button
                  key={filter.value}
                  variant={activeFilter === filter.value ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => onFilterChange(filter.value)}
                  className="text-xs"
                >
                  {filter.label}
                </Button>
              ))}
            </div>
          </div>
        )}
      </CardHeader>
      <CardContent>
        <div className="transition-all duration-300">
          {children}
        </div>
      </CardContent>
    </Card>
  )
}

export default FilterableChart

