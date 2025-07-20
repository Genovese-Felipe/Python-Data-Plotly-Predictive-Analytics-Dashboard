# ⚡ PROTOCOLO OBRIGATÓRIO - Future Studies Update

> **🚨 ATENÇÃO:** Este protocolo DEVE ser seguido sempre que:
> - ✅ Uma sessão de trabalho for encluída
> - ✅ Um commit/pull request for feito
> - ✅ Novas ideias forem discutidas
> - ✅ Funcionalidades forem planejadas mas não implementadas

---

## 📋 **CHECKLIST OBRIGATÓRIO**

### **Antes de encerrar qualquer sessão de trabalho:**

- [ ] **Atualizar 09_Future_Studies/README.md**
  - Adicionar data da última atualização
  - Resumir principais decisões/discussões
  - Atualizar próximos steps

- [ ] **Revisar FEATURE_BACKLOG.md**
  - Mover itens implementados para "Concluído"
  - Adicionar novos features identificados
  - Ajustar prioridades baseadas em aprendizados

- [ ] **Atualizar TECHNICAL_DEBT.md**
  - Adicionar novos débitos identificados
  - Marcar itens resolvidos
  - Repriorizar baseado em impacto

- [ ] **Documentar em RESEARCH_NOTES.md**
  - Novos experimentos ou hipóteses
  - Descobertas técnicas importantes
  - Links para recursos úteis encontrados

### **Sempre que fazer commit/pull request:**

- [ ] **Commit message deve referenciar Future Studies**
  - Mencionar impacto em roadmap se aplicável
  - Referenciar itens do backlog afetados
  
- [ ] **Atualizar status de implementação**
  - Marcar features como "Em Progresso" → "Concluído"
  - Atualizar estimativas baseadas na experiência real
  
- [ ] **Verificar dependencies**
  - Quais próximos itens foram desbloqueados?
  - Algum item precisa ser re-priorizado?

---

## 🎯 **TEMPLATE RÁPIDO PARA UPDATES**

### **Para adicionar ao final de qualquer README.md em Future Studies:**

```markdown
---
## 📅 **ÚLTIMO UPDATE**
- **Data:** [YYYY-MM-DD]
- **Sessão:** [Breve descrição do que foi trabalhado]
- **Principais adições:**
  - [Item 1]
  - [Item 2] 
  - [Item 3]
- **Próximos steps prioritários:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
```

### **Para novos itens em qualquer backlog:**

```markdown
### **🆕 [TÍTULO DO ITEM]**
**Status:** [Brainstorm/Conceitual/Planejado/Em Progresso]
**Prioridade:** [Crítica/Alta/Média/Baixa] 
**Estimativa:** [X horas/dias/semanas]
**Dependencies:** [O que precisa estar pronto antes]
**Descrição:** [O que precisa ser feito]
**Valor:** [Por que é importante]
**Acceptance Criteria:**
- [ ] Critério 1
- [ ] Critério 2
```

---

## 🔄 **WORKFLOW DE ATUALIZAÇÃO**

### **Inicio da sessão (5 minutos):**
1. Revisar 09_Future_Studies/README.md para contexto
2. Identificar itens relevantes para o trabalho atual
3. Marcar itens que serão trabalhados como "Em Progresso"

### **Durante o trabalho:**
1. Anotar novas ideias que surgirem
2. Identificar débitos técnicos ou problemas
3. Documentar descobertas ou insights importantes

### **Fim da sessão (10 minutos):**
1. Executar checklist obrigatório acima
2. Fazer commit com referência aos Future Studies
3. Atualizar estimativas baseadas no trabalho real

---

## 💡 **DICAS PARA MANTER ATUALIZADO**

### **Use templates:**
- Tenha templates prontos para novos itens
- Copy/paste é seu amigo para manter consistência

### **Seja conciso mas específico:**
- Prefira listas a parágrafos longos
- Use emojis para navegação visual rápida

### **Pense no "futuro você":**
- O que você gostaria de saber daqui 1 mês?
- Que contexto seria útil para retomar o trabalho?

### **Vincule tudo:**
- Reference commits em issues
- Link features para código implementado
- Conecte pesquisa com implementação

---

## 🚨 **CONSEQUÊNCIAS DE NÃO SEGUIR**

### **Problemas que acontecem:**
- ❌ Perda de contexto entre sessões
- ❌ Re-trabalho desnecessário
- ❌ Ideias importantes esquecidas
- ❌ Decisões técnicas não documentadas
- ❌ Dificuldade para priorizar próximos steps

### **Benefícios de seguir religiosamente:**
- ✅ Contexto sempre preservado
- ✅ Decisões rastreáveis e revisitáveis  
- ✅ Roadmap sempre atualizado
- ✅ Progresso visível e mensurável
- ✅ Colaboração mais eficiente

---

## 🎯 **LEMBRETES VISUAIS**

### **Antes de committar:**
```
┌─────────────────────────────────┐
│  🔮 Future Studies Updated?     │
│                                 │
│  [ ] README.md atualizado       │
│  [ ] Backlog revisado           │
│  [ ] Débito técnico documentado │
│  [ ] Research notes atualizados │
│                                 │
│  Se não: PARE e atualize!       │
└─────────────────────────────────┘
```

### **Ao encerrar trabalho:**
```
┌─────────────────────────────────┐
│  📋 Checklist de Encerramento   │
│                                 │
│  [ ] Próximos steps definidos   │
│  [ ] Aprendizados documentados  │
│  [ ] Problemas identificados    │
│  [ ] Prioridades atualizadas    │
│                                 │
│  Sessão completa! 🎉            │
└─────────────────────────────────┘
```

---

**🔥 LEMBRE-SE: Future Studies é nossa memória coletiva. Trate com o cuidado que você gostaria que tratassem a sua memória pessoal!**
