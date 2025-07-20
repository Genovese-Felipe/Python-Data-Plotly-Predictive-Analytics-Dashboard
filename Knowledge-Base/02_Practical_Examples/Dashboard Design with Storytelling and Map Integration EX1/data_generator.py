import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data():
    """Gera dados de vendas simulados realistas"""
    
    # Configurar seed para reprodutibilidade
    np.random.seed(42)
    random.seed(42)
    
    # Datas dos últimos 12 meses
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Categorias e subcategorias
    categories = {
        'Eletrônicos': ['Smartphones', 'Laptops', 'Tablets', 'Fones de Ouvido', 'Smartwatches'],
        'Roupas': ['Camisetas', 'Calças', 'Vestidos', 'Jaquetas', 'Sapatos'],
        'Casa & Jardim': ['Móveis', 'Decoração', 'Jardim', 'Cozinha', 'Banheiro'],
        'Livros': ['Ficção', 'Técnicos', 'Biografias', 'Infantis', 'Acadêmicos'],
        'Esportes': ['Equipamentos', 'Roupas Esportivas', 'Suplementos', 'Acessórios', 'Calçados']
    }
    
    # Canais de venda
    channels = ['Online', 'Loja Física', 'Telefone', 'Parceiros']
    
    # Regiões do Brasil
    regions = {
        'São Paulo': {'lat': -23.5505, 'lon': -46.6333, 'population': 12000000},
        'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729, 'population': 6700000},
        'Belo Horizonte': {'lat': -19.9167, 'lon': -43.9345, 'population': 2500000},
        'Brasília': {'lat': -15.7942, 'lon': -47.8822, 'population': 3000000},
        'Salvador': {'lat': -12.9714, 'lon': -38.5014, 'population': 2900000},
        'Fortaleza': {'lat': -3.7319, 'lon': -38.5267, 'population': 2700000},
        'Recife': {'lat': -8.0476, 'lon': -34.8770, 'population': 1650000},
        'Porto Alegre': {'lat': -30.0346, 'lon': -51.2177, 'population': 1500000},
        'Curitiba': {'lat': -25.4284, 'lon': -49.2733, 'population': 1950000},
        'Manaus': {'lat': -3.1190, 'lon': -60.0217, 'population': 2200000}
    }
    
    # Gerar dados de vendas
    sales_data = []
    
    for date in date_range:
        # Sazonalidade (mais vendas no final do ano)
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365 + np.pi/2)
        
        # Tendência de crescimento
        days_from_start = (date - start_date).days
        growth_factor = 1 + 0.001 * days_from_start
        
        for category, subcategories in categories.items():
            for subcategory in subcategories:
                for channel in channels:
                    for region in regions.keys():
                        # Probabilidade de venda baseada na população da região
                        pop_factor = regions[region]['population'] / 12000000
                        
                        if random.random() < 0.3 * pop_factor:  # 30% chance base ajustada por população
                            # Quantidade vendida
                            base_quantity = random.randint(1, 50)
                            quantity = int(base_quantity * seasonal_factor * growth_factor * pop_factor)
                            
                            # Preço baseado na categoria
                            price_ranges = {
                                'Eletrônicos': (200, 3000),
                                'Roupas': (30, 300),
                                'Casa & Jardim': (50, 1000),
                                'Livros': (20, 150),
                                'Esportes': (40, 500)
                            }
                            
                            min_price, max_price = price_ranges[category]
                            unit_price = random.uniform(min_price, max_price)
                            
                            # Margem de lucro (varia por categoria e canal)
                            margin_base = {
                                'Eletrônicos': 0.15,
                                'Roupas': 0.45,
                                'Casa & Jardim': 0.35,
                                'Livros': 0.25,
                                'Esportes': 0.30
                            }
                            
                            channel_margin_modifier = {
                                'Online': 1.2,
                                'Loja Física': 1.0,
                                'Telefone': 0.9,
                                'Parceiros': 0.8
                            }
                            
                            margin = margin_base[category] * channel_margin_modifier[channel]
                            margin += random.uniform(-0.05, 0.05)  # Variação aleatória
                            
                            # Satisfação do cliente (correlacionada com margem)
                            satisfaction = min(10, max(1, 7 + margin * 5 + random.uniform(-1, 1)))
                            
                            sales_data.append({
                                'date': date,
                                'category': category,
                                'subcategory': subcategory,
                                'channel': channel,
                                'region': region,
                                'latitude': regions[region]['lat'],
                                'longitude': regions[region]['lon'],
                                'quantity': quantity,
                                'unit_price': round(unit_price, 2),
                                'total_revenue': round(quantity * unit_price, 2),
                                'margin_percent': round(margin * 100, 1),
                                'customer_satisfaction': round(satisfaction, 1)
                            })
    
    return pd.DataFrame(sales_data)

def generate_customer_funnel_data():
    """Gera dados do funil de conversão de clientes"""
    
    # Dados do funil
    funnel_data = {
        'stage': ['Visitantes', 'Leads', 'Prospects Qualificados', 'Propostas', 'Negociação', 'Clientes'],
        'count': [10000, 3500, 1800, 900, 600, 320],
        'conversion_rate': [100, 35, 18, 9, 6, 3.2]
    }
    
    # Dados de origem dos leads
    lead_sources = {
        'source': ['Orgânico', 'Pago', 'Social Media', 'Email', 'Referência', 'Direto'],
        'leads': [1200, 800, 600, 400, 300, 200],
        'cost_per_lead': [0, 45, 25, 15, 0, 0],
        'conversion_rate': [4.2, 3.8, 2.1, 5.5, 6.8, 3.9]
    }
    
    return pd.DataFrame(funnel_data), pd.DataFrame(lead_sources)

def generate_product_performance_data():
    """Gera dados de performance de produtos para gráfico bubble"""
    
    products = [
        'iPhone 15', 'Samsung Galaxy S24', 'MacBook Pro', 'Dell XPS 13', 'iPad Pro',
        'Nike Air Max', 'Adidas Ultraboost', 'Sony WH-1000XM5', 'AirPods Pro',
        'Kindle Oasis', 'Echo Dot', 'Ring Doorbell', 'Nest Thermostat',
        'Camiseta Premium', 'Jeans Levi\'s', 'Tênis Allstar', 'Vestido Zara'
    ]
    
    performance_data = []
    
    for product in products:
        # Volume de vendas (unidades)
        volume = random.randint(50, 500)
        
        # Margem de lucro (%)
        margin = random.uniform(10, 60)
        
        # Satisfação do cliente (1-10)
        satisfaction = random.uniform(6, 10)
        
        # Receita total (correlacionada com volume)
        revenue = volume * random.uniform(100, 2000)
        
        performance_data.append({
            'product': product,
            'sales_volume': volume,
            'profit_margin': round(margin, 1),
            'customer_satisfaction': round(satisfaction, 1),
            'total_revenue': round(revenue, 2)
        })
    
    return pd.DataFrame(performance_data)

def save_all_data():
    """Salva todos os dados gerados em arquivos CSV"""
    
    print("Gerando dados de vendas...")
    sales_df = generate_sales_data()
    sales_df.to_csv('/home/ubuntu/dashboard-dash-analytics/src/data/sales_data.csv', index=False)
    print(f"Dados de vendas salvos: {len(sales_df)} registros")
    
    print("Gerando dados do funil de conversão...")
    funnel_df, sources_df = generate_customer_funnel_data()
    funnel_df.to_csv('/home/ubuntu/dashboard-dash-analytics/src/data/funnel_data.csv', index=False)
    sources_df.to_csv('/home/ubuntu/dashboard-dash-analytics/src/data/lead_sources.csv', index=False)
    print(f"Dados do funil salvos: {len(funnel_df)} estágios, {len(sources_df)} fontes")
    
    print("Gerando dados de performance de produtos...")
    products_df = generate_product_performance_data()
    products_df.to_csv('/home/ubuntu/dashboard-dash-analytics/src/data/product_performance.csv', index=False)
    print(f"Dados de produtos salvos: {len(products_df)} produtos")
    
    print("Todos os dados foram gerados e salvos com sucesso!")
    
    return sales_df, funnel_df, sources_df, products_df

if __name__ == "__main__":
    # Criar diretório de dados se não existir
    import os
    os.makedirs('/home/ubuntu/dashboard-dash-analytics/src/data', exist_ok=True)
    
    # Gerar e salvar todos os dados
    save_all_data()

