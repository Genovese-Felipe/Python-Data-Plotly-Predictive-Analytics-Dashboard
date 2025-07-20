# Dashboard Analytics - Visualização de Dados com Python/Dash

Um dashboard interativo e responsivo desenvolvido com Python, Pandas, Numpy e Plotly/Dash para análise de dados empresariais em tempo real.

## 🚀 Funcionalidades Implementadas

### Visualizações Complexas
- **Gráfico Sunburst**: Hierarquia de vendas por categoria e subcategoria
- **Gráfico Bubble**: Análise multivariável de performance de produtos
- **Gráfico de Área**: Tendências de receita com comparação de metas
- **Gráfico Stacked Bar**: Vendas por canal de distribuição ao longo do tempo
- **Gráfico Flow (Sankey)**: Fluxo de conversão de clientes
- **Mapa Interativo**: Distribuição geográfica de vendas no Brasil

### Interatividade e Filtros
- ✅ **Filtros Globais**: Por departamento e período de tempo
- ✅ **Cross-filtering**: Cliques em um gráfico filtram outros automaticamente
- ✅ **Hover Interativo**: Informações detalhadas ao passar o mouse
- ✅ **Atualizações em Tempo Real**: Simulação de dados dinâmicos
- ✅ **Exportação de Dados**: Download de dados filtrados em CSV

### Design Responsivo
- ✅ **Grade CSS Flexível**: Layout adaptativo para diferentes telas
- ✅ **Mobile-First**: Otimizado para dispositivos móveis
- ✅ **Animações Suaves**: Transições e micro-interações
- ✅ **Tema Moderno**: Gradientes, sombras e tipografia profissional

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem principal
- **Dash 3.1.1** - Framework web para Python
- **Plotly 6.2.0** - Biblioteca de visualização
- **Pandas 2.3.1** - Manipulação de dados
- **Numpy 2.3.1** - Computação numérica

### Dados
- **33.958 registros** de vendas simulados
- **10 regiões** do Brasil com coordenadas geográficas
- **5 categorias** de produtos com subcategorias
- **4 canais** de distribuição
- **12 meses** de dados históricos

## 📊 Estrutura dos Dados

### Dataset Principal (sales_data.csv)
```
- date: Data da venda
- category: Categoria do produto
- subcategory: Subcategoria do produto
- channel: Canal de venda
- region: Região geográfica
- latitude/longitude: Coordenadas para o mapa
- quantity: Quantidade vendida
- unit_price: Preço unitário
- total_revenue: Receita total
- margin_percent: Margem de lucro
- customer_satisfaction: Satisfação do cliente
```

### Funil de Conversão (funnel_data.csv)
```
- stage: Estágio do funil
- count: Número de prospects
- conversion_rate: Taxa de conversão
```

### Performance de Produtos (product_performance.csv)
```
- product: Nome do produto
- sales_volume: Volume de vendas
- profit_margin: Margem de lucro
- customer_satisfaction: Satisfação
- total_revenue: Receita total
```

## 🎯 KPIs Principais

1. **Receita Total**: R$ 2.4M (+12% vs mês anterior)
2. **Novos Clientes**: 1.247 (+8% vs mês anterior)
3. **Taxa de Conversão**: 3.2% (+0.4% vs mês anterior)
4. **Ticket Médio**: R$ 847 (+5% vs mês anterior)

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- pip ou conda

### Instalação
```bash
# Clonar o projeto
cd dashboard-dash-analytics

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Gerar dados (se necessário)
python src/data_generator.py

# Executar aplicação
python src/app.py
```

### Acesso
- **URL Local**: http://localhost:8050
- **Modo Debug**: Habilitado para desenvolvimento

## 📱 Layout Responsivo

### Desktop (> 1024px)
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

### Tablet (768px - 1024px)
- Layout em 2 colunas
- KPIs em grade 2x2
- Gráficos empilhados verticalmente

### Mobile (< 768px)
- Layout em coluna única
- KPIs em linha única
- Gráficos em stack vertical

## 🎨 Paleta de Cores

### Cores Principais
- **Azul**: #3b82f6 (Receita, Primário)
- **Verde**: #10b981 (Crescimento, Sucesso)
- **Roxo**: #8b5cf6 (Conversão, Destaque)
- **Laranja**: #f59e0b (Ticket Médio, Atenção)

### Gradientes
- **Background**: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)
- **Header**: linear-gradient(135deg, #1e293b 0%, #334155 100%)
- **Cards**: Gradientes específicos por KPI

## 🔧 Arquitetura do Código

```
src/
├── app.py                 # Aplicação principal Dash
├── charts.py              # Funções para criar gráficos
├── data_generator.py      # Gerador de dados simulados
├── advanced_callbacks.py  # Callbacks para interações
├── assets/
│   └── style.css         # Estilos CSS customizados
└── data/
    ├── sales_data.csv    # Dados de vendas
    ├── funnel_data.csv   # Dados do funil
    ├── lead_sources.csv  # Fontes de leads
    └── product_performance.csv # Performance produtos
```

## 🌟 Funcionalidades Avançadas

### Callbacks Interativos
1. **Cross-filtering**: Clique no Sunburst filtra Bubble e Area
2. **Hover Details**: Informações detalhadas em tempo real
3. **Real-time Updates**: Simulação de atualizações automáticas
4. **Data Export**: Exportação de dados filtrados

### Filtros Dinâmicos
- **Departamento**: Vendas, Marketing, Operações, Financeiro
- **Período**: Seletor de data range
- **Região**: Filtro por clique no mapa
- **Categoria**: Filtro por clique no Sunburst

### Otimizações
- **Lazy Loading**: Carregamento sob demanda
- **Data Caching**: Cache de dados para performance
- **Responsive Design**: Adaptação automática de layout
- **Error Handling**: Tratamento robusto de erros

## 📈 Métricas de Performance

### Dados Processados
- **33.958 registros** de vendas processados
- **10 regiões** geográficas mapeadas
- **17 produtos** analisados
- **6 estágios** do funil de conversão

### Visualizações
- **6 tipos** de gráficos diferentes
- **4 KPIs** principais
- **Tempo real** de atualização
- **100% responsivo** em todos os dispositivos

## 🔒 Segurança e Boas Práticas

- **Validação de Dados**: Verificação de integridade
- **Error Boundaries**: Tratamento de erros gracioso
- **Performance Monitoring**: Callbacks otimizados
- **Code Organization**: Modularização clara

## 📄 Dependências Principais

```
dash==3.1.1
plotly==6.2.0
pandas==2.3.1
numpy==2.3.1
gunicorn==23.0.0
```

## 🚀 Deploy

### Preparação
```bash
# Atualizar requirements
pip freeze > requirements.txt

# Criar Procfile
echo "web: gunicorn src.app:server" > Procfile
```

### Plataformas Suportadas
- **Heroku**: Deploy direto via Git
- **Railway**: Deploy automático
- **Render**: Deploy com Docker
- **Local**: Desenvolvimento e testes

## 📞 Suporte

Para dúvidas ou sugestões sobre o dashboard:
- Verifique a documentação dos gráficos em `charts.py`
- Analise os callbacks em `app.py`
- Consulte os dados gerados em `data/`

---

**Desenvolvido com ❤️ usando Python + Dash + Plotly**

*Dashboard Analytics - Transformando dados em insights acionáveis*

