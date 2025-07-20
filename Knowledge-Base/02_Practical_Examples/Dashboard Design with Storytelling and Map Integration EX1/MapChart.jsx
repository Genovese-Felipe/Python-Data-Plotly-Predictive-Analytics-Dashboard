import React, { useEffect } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

// Dados simulados de vendas por cidade brasileira
const salesData = [
  { city: 'São Paulo', lat: -23.5505, lng: -46.6333, sales: 2400000, color: '#ef4444' },
  { city: 'Rio de Janeiro', lat: -22.9068, lng: -43.1729, sales: 1800000, color: '#f97316' },
  { city: 'Belo Horizonte', lat: -19.9167, lng: -43.9345, sales: 950000, color: '#f59e0b' },
  { city: 'Brasília', lat: -15.7942, lng: -47.8822, sales: 1200000, color: '#eab308' },
  { city: 'Salvador', lat: -12.9714, lng: -38.5014, sales: 850000, color: '#84cc16' },
  { city: 'Fortaleza', lat: -3.7319, lng: -38.5267, sales: 720000, color: '#22c55e' },
  { city: 'Recife', lat: -8.0476, lng: -34.8770, sales: 680000, color: '#10b981' },
  { city: 'Porto Alegre', lat: -30.0346, lng: -51.2177, sales: 1100000, color: '#06b6d4' },
  { city: 'Curitiba', lat: -25.4284, lng: -49.2733, sales: 980000, color: '#0ea5e9' },
  { city: 'Manaus', lat: -3.1190, lng: -60.0217, sales: 450000, color: '#3b82f6' },
  { city: 'Belém', lat: -1.4558, lng: -48.5044, sales: 380000, color: '#6366f1' },
  { city: 'Goiânia', lat: -16.6869, lng: -49.2648, sales: 520000, color: '#8b5cf6' }
]

// Componente para ajustar a visualização do mapa
const MapController = () => {
  const map = useMap()
  
  useEffect(() => {
    // Ajustar o mapa para mostrar o Brasil
    map.setView([-14.2350, -51.9253], 4)
  }, [map])
  
  return null
}

const MapChart = () => {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
  }

  const getRadius = (sales) => {
    // Calcular o raio baseado nas vendas (entre 8 e 40 pixels)
    const minSales = Math.min(...salesData.map(d => d.sales))
    const maxSales = Math.max(...salesData.map(d => d.sales))
    const normalized = (sales - minSales) / (maxSales - minSales)
    return 8 + (normalized * 32)
  }

  return (
    <div className="h-full w-full relative">
      <MapContainer
        center={[-14.2350, -51.9253]}
        zoom={4}
        style={{ height: '100%', width: '100%' }}
        className="rounded-lg"
      >
        <MapController />
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {salesData.map((location, index) => (
          <CircleMarker
            key={index}
            center={[location.lat, location.lng]}
            radius={getRadius(location.sales)}
            fillColor={location.color}
            color="white"
            weight={2}
            opacity={1}
            fillOpacity={0.7}
          >
            <Popup>
              <div className="text-center">
                <h3 className="font-bold text-lg text-slate-900">{location.city}</h3>
                <p className="text-slate-600">
                  Vendas: {formatCurrency(location.sales)}
                </p>
                <p className="text-sm text-slate-500">
                  {((location.sales / salesData.reduce((sum, d) => sum + d.sales, 0)) * 100).toFixed(1)}% do total
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      
      {/* Legenda */}
      <div className="absolute bottom-4 left-4 bg-white dark:bg-slate-800 p-3 rounded-lg shadow-lg border border-slate-200 dark:border-slate-700">
        <h4 className="font-medium text-sm text-slate-900 dark:text-white mb-2">Vendas por Região</h4>
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-slate-600 dark:text-slate-400">&gt; R$ 2M</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-slate-600 dark:text-slate-400">R$ 1M - R$ 2M</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-slate-600 dark:text-slate-400">&lt; R$ 1M</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MapChart

