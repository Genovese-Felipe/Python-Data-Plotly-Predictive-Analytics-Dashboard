# 🤖 **Guia de Prompt Engineering para Desenvolvimento de Dashboards**

> **Como solicitar desenvolvimento de dashboards Plotly/Dash para obter resultados funcionais**

---

## 🎯 **PROMPTS EFETIVOS**

### **✅ PROMPT BOM - Desenvolvimento Incremental:**
```
"Crie um dashboard Dash simples com gráfico Sunburst usando estes dados reais:
[dados específicos]

Requisitos:
1. APENAS 1 gráfico Sunburst funcional
2. Interface minimalista 
3. Testar em cada etapa
4. Executar na porta 8052
5. Garantir que funciona antes de qualquer melhoria

Se funcionar 100%, então podemos adicionar filtros."
```

### **❌ PROMPT RUIM - Tudo de Uma Vez:**
```
"Crie um dashboard complexo com Sunburst, filtros, ML, mapas, múltiplas visualizações, design moderno, tooltips avançados, análise preditiva e interface responsiva."
```

---

## 📋 **TEMPLATE DE PROMPT RECOMENDADO**

```markdown
## CONTEXTO
Preciso de um dashboard [SIMPLES/AVANÇADO] para [DOMÍNIO ESPECÍFICO].

## DADOS DISPONÍVEIS  
[Cole dados reais ou indique arquivo de referência]

## OBJETIVO PRINCIPAL
[1 objetivo específico, não uma lista]

## RESTRIÇÕES
- Comece SEMPRE pelo mínimo funcional
- Use dados reais fornecidos
- Teste em cada etapa
- Máximo de [X] visualizações inicialmente

## CRITÉRIO DE SUCESSO
Dashboard deve carregar sem erros e mostrar dados corretamente.

## EVOLUÇÃO (se V1 funcionar)
[Próximos passos específicos]
```

---

## 🔧 **PALAVRAS-CHAVE EFETIVAS**

### **✅ Use Estas Frases:**
- "Comece com o mínimo funcional"
- "Use dados reais extraídos de [arquivo]"  
- "Teste cada etapa antes de continuar"
- "Se V1 funcionar, então adicione [recurso]"
- "Desenvolvimento incremental obrigatório"
- "Simplifique callbacks ao máximo"

### **❌ Evite Estas Frases:**
- "Dashboard completo e complexo"
- "Com todas as funcionalidades"
- "Design sofisticado" (sem funcionalidade primeiro)
- "Use dados simulados" (quando reais existem)
- "Corrija o código existente" (se muito quebrado)

---

## 📊 **PROMPTS POR NÍVEL DE COMPLEXIDADE**

### **NÍVEL 1 - Dashboard Básico:**
```
"Crie dashboard Dash minimalista:
- 1 gráfico [tipo específico]  
- Layout HTML simples
- Sem filtros ou callbacks
- Apenas validar que dados aparecem
- Porta [número]
- Comentar cada seção do código"
```

### **NÍVEL 2 - Com Interatividade:**
```
"Baseado no V1 funcionando, adicione:
- 1-2 filtros dropdown  
- 1 callback simples
- Manter mesmo gráfico
- Testar que filtros atualizam corretamente
- Não mudar layout atual"
```

### **NÍVEL 3 - Dashboard Complexo:**
```
"Baseado no V2 funcionando, expanda para:
- [Lista específica de 2-3 recursos]
- Manter funcionalidades anteriores
- Design responsivo com cards
- [Requisito específico de ML/mapas se necessário]"
```

---

## 🎨 **PROMPTS PARA DESIGN**

### **✅ Design Incremental:**
```
"Melhore o layout atual mantendo toda funcionalidade:
1. Adicione cards com background branco
2. Use CSS Grid 2x2 para gráficos  
3. Adicione padding e border-radius
4. Mantenha cores atuais funcionando
5. Teste que interatividade continua igual"
```

### **❌ Design Prematuro:**
```
"Crie interface moderna com cores personalizadas, animações, temas, responsividade total, shadows complexos..."
```

---

## 🧠 **PROMPTS PARA MACHINE LEARNING**

### **✅ ML Simples e Funcional:**
```
"Adicione análise ML simples ao dashboard atual:
- Usar LinearRegression do sklearn
- Features: [listar 2-3 colunas específicas]
- Target: [coluna específica]
- Visualizar importância com bar chart horizontal
- Manter todos os gráficos atuais funcionando"
```

### **❌ ML Complexo Demais:**
```
"Implemente modelo preditivo completo com feature engineering, cross-validation, múltiplos algoritmos, hyperparameter tuning, métricas avançadas..."
```

---

## 🗺️ **PROMPTS PARA MAPAS**

### **✅ Mapas Diretos:**
```
"Adicione mapa geográfico usando coordenadas existentes:
- scatter_geo com lat/lon das colunas [X] e [Y]
- Size baseado em [coluna específica]
- Color por [categoria específica]  
- Projection 'albers usa' para dados EUA
- Manter outros gráficos funcionando"
```

---

## 🔄 **PROMPTS DE DEBUGGING**

### **Quando Algo Não Funciona:**
```
"O dashboard atual tem erro [erro específico].

Ao invés de corrigir, faça:
1. Analise o código que funcionava antes
2. Identifique exatamente o que quebrou
3. Reverta para última versão funcional
4. Aplique mudança mínima necessária
5. Teste que funciona antes de continuar

Não tente múltiplas correções simultâneas."
```

---

## 📚 **PROMPTS PARA DOCUMENTAÇÃO**

### **README Automático:**
```
"Crie README.md para este dashboard incluindo:
- Breve descrição (1-2 frases)
- Como executar (comandos exatos)
- Porta de acesso
- Screenshot ou descrição visual
- 3-5 recursos principais
- Tecnologias usadas (versões)
- Estrutura de dados resumida"
```

---

## 🚨 **SINAIS DE ALERTA NOS PROMPTS**

### **🔴 Pare se Você Escreveu:**
- "Crie dashboard com 5+ funcionalidades diferentes"
- "Corrija todos os erros do código atual"  
- "Implemente arquitetura complexa"
- "Use os dados mais realistas possível" (sem especificar)
- "Dashboard production-ready completo"

### **✅ Reescreva Como:**
- "Crie 1 funcionalidade específica que funcione perfeitamente"
- "Recrie funcionalidade [X] do zero de forma simples"
- "Use estrutura mínima para [objetivo específico]"
- "Use exatamente estes dados: [dados específicos]"  
- "Dashboard funcional básico, expandível depois"

---

## 📊 **EXEMPLOS DE SESSÕES BEM-SUCEDIDAS**

### **Sessão Eficaz - 3 Prompts:**
```
1. "Crie Sunburst simples com dados [específicos]"
   → Resultado: V1 funcional

2. "Adicione 2 filtros dropdown ao V1"  
   → Resultado: V2 com interatividade

3. "Expanda V2 com mapa geográfico usando lat/lon"
   → Resultado: V3 completo
```

### **Sessão Ineficaz - 1 Prompt:**
```
1. "Crie dashboard completo com Sunburst + filtros + mapas + ML + design"
   → Resultado: Código complexo e quebrado
```

---

## 🎓 **RESUMO PARA PROMPT ENGINEERING**

### **FÓRMULA DE SUCESSO:**
```
CONTEXTO + DADOS ESPECÍFICOS + OBJETIVO ÚNICO + RESTRIÇÃO DE SIMPLICIDADE + CRITÉRIO CLARO
```

### **ITERAÇÃO OBRIGATÓRIA:**
```
Prompt1 (V1) → Validar → Prompt2 (V2) → Validar → Prompt3 (V3)
```

### **PALAVRAS MÁGICAS:**
- "Simples"
- "Funcional"  
- "Incremental"
- "Testar"
- "Mínimo"
- "Específico"
- "Se funcionar"

### **PALAVRAS PROIBIDAS:**
- "Completo"
- "Complexo"
- "Sofisticado"
- "Todos"
- "Geral"
- "Avançado" (no primeiro prompt)

---

**🎯 Use este guia para obter dashboards funcionais rapidamente, evitando horas de debugging desnecessário!**
