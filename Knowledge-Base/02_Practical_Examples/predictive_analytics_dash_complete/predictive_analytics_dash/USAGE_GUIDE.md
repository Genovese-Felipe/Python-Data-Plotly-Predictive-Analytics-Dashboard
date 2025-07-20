# Guia de Uso - Dashboard de Análise Preditiva

## Introdução

Este guia fornece instruções detalhadas sobre como utilizar o Dashboard de Análise Preditiva desenvolvido com Python, Plotly e Dash. O sistema permite explorar dados, visualizar padrões e realizar predições interativas em tempo real.

## Pré-requisitos

### Requisitos de Sistema
- Python 3.11 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexão com internet (para carregamento de bibliotecas JavaScript)

### Dependências Python
Todas as dependências estão listadas no arquivo `requirements.txt`:
- dash
- plotly
- pandas
- numpy
- scikit-learn

## Instalação e Configuração

### Passo 1: Clonar ou Baixar o Projeto
```bash
# Se usando Git
git clone <repository-url>
cd predictive_analytics_dash

# Ou extrair de arquivo ZIP
unzip predictive_analytics_dash.zip
cd predictive_analytics_dash
```

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Executar a Aplicação
```bash
python app.py
```

### Passo 4: Acessar o Dashboard
Abra seu navegador e acesse: `http://localhost:8050`

## Interface do Dashboard

### Visão Geral da Interface

O dashboard é dividido em duas seções principais:

1. **Visualizações Exploratórias** (lado esquerdo)
2. **Predição Interativa** (lado direito)

### Seção de Visualizações Exploratórias

#### Gráfico de Dispersão (Scatter Plot)
- **Título**: "Comprimento vs Largura da Sépala"
- **Eixo X**: Comprimento da sépala (cm)
- **Eixo Y**: Largura da sépala (cm)
- **Cores**: Diferentes cores para cada espécie de íris
- **Funcionalidade**: Permite visualizar a separação entre as espécies

#### Histograma
- **Título**: "Distribuição do Comprimento da Pétala"
- **Eixo X**: Comprimento da pétala (cm)
- **Eixo Y**: Contagem de amostras
- **Cores**: Diferentes cores para cada espécie
- **Funcionalidade**: Mostra a distribuição das medições por espécie

### Seção de Predição Interativa

#### Controles de Entrada

**Slider 1: Comprimento da Sépala (cm)**
- Faixa: 4.3 a 7.9 cm
- Incremento: 0.1 cm
- Valor padrão: Média do dataset

**Slider 2: Largura da Sépala (cm)**
- Faixa: 2.0 a 4.4 cm
- Incremento: 0.1 cm
- Valor padrão: Média do dataset

**Slider 3: Comprimento da Pétala (cm)**
- Faixa: 1.0 a 6.9 cm
- Incremento: 0.1 cm
- Valor padrão: Média do dataset

**Slider 4: Largura da Pétala (cm)**
- Faixa: 0.1 a 2.5 cm
- Incremento: 0.1 cm
- Valor padrão: Média do dataset

#### Área de Resultados

**Predição Principal**
- Exibe a espécie predita pelo modelo
- Formato: "Predição: [nome da espécie]"

**Nível de Confiança**
- Mostra a confiança do modelo na predição
- Formato: "Confiança: [percentual]%"

**Probabilidades Detalhadas**
- Lista as probabilidades para cada uma das três espécies:
  - Setosa: [valor]
  - Versicolor: [valor]
  - Virginica: [valor]

## Como Usar o Dashboard

### Explorando os Dados

1. **Analise as Visualizações**: Comece observando os gráficos na seção esquerda para compreender como as diferentes espécies se distribuem no espaço de características.

2. **Identifique Padrões**: Note como as espécies formam clusters distintos nos gráficos, indicando que são facilmente separáveis.

### Realizando Predições

1. **Ajuste os Sliders**: Use os quatro sliders na seção direita para definir as características da flor que deseja classificar.

2. **Observe os Resultados**: A predição é atualizada automaticamente conforme você ajusta os sliders.

3. **Interprete a Confiança**: Valores de confiança próximos a 100% indicam predições mais confiáveis.

4. **Analise as Probabilidades**: As probabilidades detalhadas mostram quão próxima a amostra está de cada classe.

### Casos de Uso Práticos

#### Caso 1: Identificação de Espécie Conhecida
1. Ajuste os sliders para valores típicos de uma espécie conhecida
2. Verifique se o modelo prediz corretamente a espécie
3. Observe a confiança da predição

#### Caso 2: Exploração de Fronteiras de Decisão
1. Ajuste os sliders gradualmente entre regiões de diferentes espécies
2. Observe como a confiança diminui nas fronteiras
3. Note quando a predição muda de uma espécie para outra

#### Caso 3: Validação de Medições Atípicas
1. Insira valores extremos nos sliders
2. Observe como o modelo responde a medições fora do padrão
3. Use as probabilidades para avaliar a incerteza

## Interpretação dos Resultados

### Compreendendo as Predições

**Alta Confiança (>90%)**
- O modelo está muito confiante na predição
- A amostra está claramente dentro da região de uma espécie
- Predição altamente confiável

**Confiança Moderada (70-90%)**
- O modelo tem boa confiança, mas há alguma incerteza
- A amostra pode estar próxima à fronteira entre espécies
- Predição confiável, mas com cautela

**Baixa Confiança (<70%)**
- O modelo tem incerteza significativa
- A amostra pode ter características atípicas
- Predição deve ser interpretada com cuidado

### Análise das Probabilidades

As probabilidades somam sempre 1.0 (100%) e mostram a distribuição da confiança entre as três espécies. Uma distribuição como [0.95, 0.03, 0.02] indica alta confiança na primeira espécie, enquanto [0.4, 0.35, 0.25] indica incerteza significativa.

## Solução de Problemas

### Problemas Comuns

**Dashboard não carrega**
- Verifique se todas as dependências estão instaladas
- Confirme que a porta 8050 não está sendo usada por outro processo
- Verifique se há erros no terminal

**Sliders não respondem**
- Atualize a página do navegador
- Verifique a conexão com internet
- Limpe o cache do navegador

**Predições não atualizam**
- Verifique se o modelo foi carregado corretamente
- Confirme que os arquivos .pkl estão no diretório models/
- Reinicie a aplicação

### Mensagens de Erro

**ModuleNotFoundError**
- Instale as dependências: `pip install -r requirements.txt`

**FileNotFoundError**
- Execute o script de treinamento: `python models/train_model.py`
- Verifique se todos os arquivos estão no local correto

## Dicas de Uso Avançado

### Personalizando Visualizações
- Os gráficos são interativos - use zoom, pan e hover para explorar
- Clique na legenda para ocultar/mostrar espécies específicas

### Otimizando Performance
- Para melhor performance, feche outras abas do navegador
- Use navegadores modernos para melhor compatibilidade

### Extensões Possíveis
- Adicione novos tipos de gráficos modificando `components/dashboard_layout.py`
- Implemente novos modelos editando `models/train_model.py`
- Adicione novos datasets modificando `data/load_data.py`

## Suporte e Recursos Adicionais

### Documentação Técnica
Consulte `DOCUMENTATION.md` para detalhes técnicos completos sobre a implementação.

### Estrutura do Código
Consulte `README.md` para visão geral da estrutura do projeto.

### Contato
Para suporte técnico ou dúvidas, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

