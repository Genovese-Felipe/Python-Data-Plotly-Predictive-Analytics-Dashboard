# Roadmap

## Concluído na versão 2

- Ponto de entrada único e wrappers de compatibilidade.
- Caminhos independentes do diretório atual.
- Dados sintéticos explicitamente rotulados.
- CSV externo com validação de esquema.
- Modelo preditivo com holdout, MAE e R².
- Interface e exportação HTML compartilhando gráficos.
- Dependências separadas para dashboard, desenvolvimento e Monica AI.
- Testes, lint, CI e deploy do GitHub Pages.
- Documentação coerente com porta 8050 e Python 3.10+.

## Próximo ciclo

1. Adicionar `data/sample_projects.csv` pequeno e versionado.
2. Criar validação estatística de faixa, nulos e duplicatas.
3. Persistir o modelo com metadados de versão e hash do dataset.
4. Implementar baseline linear para comparação com Random Forest.
5. Adicionar explicabilidade por importância de variáveis e análise de erro por tipo.
6. Medir cobertura de testes e tempo de build.
7. Mover demos antigas para uma release ou repositório de arquivo.

## Antes de usar dados reais

- Definir origem, proprietário, frequência e SLA dos dados.
- Remover ou anonimizar dados pessoais e comerciais sensíveis.
- Criar esquema de validação e política de retenção.
- Avaliar viés, drift e impacto de decisões incorretas.
- Adicionar autenticação e autorização.
- Substituir treinamento durante o startup por pipeline versionado.

## Manutenção do tamanho

Novas saídas HTML, caches, modelos e datasets grandes devem permanecer fora do Git. A redução do histórico existente requer uma migração separada com backup, comunicação aos colaboradores e atualização forçada dos clones; ela não faz parte desta versão por ser destrutiva.

