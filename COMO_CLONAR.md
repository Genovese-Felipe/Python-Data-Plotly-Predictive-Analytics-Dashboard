# Como Clonar e Executar o Dashboard

Este repositório contém um Dashboard Interativo de Análise Preditiva de Dados usando Python, Plotly e Dash.

## 🔧 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 📋 Instruções de Clonagem e Setup

### 1. Clone o Repositório

```bash
git clone https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
cd Python-Data-Plotly-Predictive-Analytics-Dashboard
```

### 2. Configuração Automática (Recomendado)

Execute o script de setup que instala dependências e gera dados:

```bash
python setup.py
```

Este script irá:
- ✅ Verificar a versão do Python
- 📦 Instalar todas as dependências necessárias
- 📊 Gerar dados de exemplo
- 🧪 Testar os componentes do dashboard
- 🚀 Criar script de execução

### 3. Configuração Manual (Alternativa)

Se preferir fazer a configuração manual:

```bash
# Instalar dependências
pip install -r requirements.txt

# Gerar dados de exemplo
python scripts/data_gen_new.py

# Testar setup
python test_setup.py
```

## 🚀 Como Executar o Dashboard

### Opção 1: Script Automático
```bash
python run.py
```

### Opção 2: Execução Direta
```bash
python scripts/viz_new.py
```

### Opção 3: Script Shell (se disponível)
```bash
./run_dashboard.sh
```

## 📊 Acessando o Dashboard

Após executar qualquer dos comandos acima:

1. Abra seu navegador
2. Acesse: **http://localhost:8050**
3. Explore o dashboard interativo!

## 🏗️ Estrutura do Projeto

```
├── data/                  # Dados CSV gerados
│   ├── projects_master.csv
│   ├── project_status.csv
│   └── ...
├── scripts/               # Scripts Python
│   ├── data_gen_new.py   # Geração de dados
│   ├── viz_new.py        # Dashboard principal
│   └── ...
├── outputs/               # Arquivos HTML gerados
│   └── dashboard.html
├── requirements.txt       # Dependências Python
├── setup.py              # Script de configuração
├── run.py                # Script para executar dashboard
└── test_setup.py         # Script de teste
```

## 📈 Funcionalidades do Dashboard

- **Monitoramento de Projetos**: Visualização em tempo real do status dos projetos
- **Análise de Orçamento**: Gráficos de variação orçamentária
- **Gestão de Recursos**: Utilização de recursos por projeto
- **Filtros Interativos**: Filtragem dinâmica por tipo de projeto, responsável, etc.
- **Indicadores KPI**: Medidores de progresso e performance
- **Design Responsivo**: Adaptável a diferentes tamanhos de tela

## 🛠️ Personalização

Para personalizar os dados ou visualizações:

1. **Modificar dados**: Edite `scripts/data_gen_new.py`
2. **Alterar visualizações**: Edite `scripts/viz_new.py`
3. **Regenerar dados**: Execute `python scripts/data_gen_new.py`

## 🔍 Solução de Problemas

### Erro de Porta em Uso
```bash
# Se a porta 8050 estiver em uso, pare outros processos ou use outra porta
# Edite o arquivo viz_new.py e altere port=8050 para port=8051
```

### Dependências em Falta
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

### Dados Não Encontrados
```bash
# Regenere os dados
python scripts/data_gen_new.py
```

## 📞 Suporte

Se encontrar problemas:
1. Verifique se todos os pré-requisitos estão instalados
2. Execute `python test_setup.py` para diagnosticar problemas
3. Consulte os logs de erro para mais detalhes

## 🎯 Próximos Passos

Após o setup bem-sucedido, você pode:
- Explorar o dashboard interativo
- Modificar os dados para seus próprios projetos
- Customizar as visualizações
- Implementar novas funcionalidades

Aproveite seu Dashboard de Análise Preditiva! 🚀