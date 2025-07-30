# scripts/data_gen.py - Performance Projects Dashboard Data Generation (Proposal 2)
import pandas as pd
import numpy as np
import datetime as dt
import random
import os

# Ensure reproducibility
np.random.seed(42)
random.seed(42)

def gerar_dados_projetos(n_projetos=200):
    """
    Gera dados simulados para projetos de performance.
    
    Parameters:
    -----------
    n_projetos : int
        Número de projetos a serem gerados
        
    Returns:
    --------
    tuple
        Tupla contendo DataFrames (df_projetos, df_marcos, df_financeiro)
    """
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Tipos de projeto e características
    tipos_projeto = ['Residencial', 'Comercial', 'Industrial', 'Infraestrutura']
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    status_opcoes = ['Planejado', 'Em Andamento', 'Concluído', 'Atrasado']
    
    # Datas
    data_inicio_base = dt.datetime(2023, 1, 1)
    data_fim = dt.datetime(2025, 7, 30)
    dias_intervalo = (data_fim - data_inicio_base).days
    
    # Gerar dados básicos dos projetos
    projetos_data = {
        'id_projeto': [f'PROJ-{i:04d}' for i in range(1, n_projetos + 1)],
        'nome_projeto': [f'Projeto {tipo} {i:03d}' for i, tipo in enumerate(np.random.choice(tipos_projeto, n_projetos), 1)],
        'tipo_projeto': np.random.choice(tipos_projeto, n_projetos),
        'regiao': np.random.choice(regioes, n_projetos),
        'gerente': [f'Gerente {chr(65 + i % 15)}' for i in range(n_projetos)],
        'data_inicio': [data_inicio_base + dt.timedelta(days=random.randint(0, dias_intervalo//2)) 
                       for _ in range(n_projetos)],
        'duracao_prevista': np.random.randint(30, 365, n_projetos),
        'orcamento': np.random.randint(100000, 2000000, n_projetos),
        'complexidade': np.random.choice(['Baixa', 'Média', 'Alta', 'Muito Alta'], n_projetos, p=[0.2, 0.4, 0.3, 0.1])
    }
    
    df_projetos = pd.DataFrame(projetos_data)
    
    # Calcular data de conclusão prevista
    df_projetos['data_conclusao_prevista'] = df_projetos.apply(
        lambda row: row['data_inicio'] + dt.timedelta(days=row['duracao_prevista']), axis=1
    )
    
    # Determinar status baseado nas datas
    hoje = dt.datetime.now()
    def determinar_status(row):
        if row['data_inicio'] > hoje:
            return 'Planejado'
        elif row['data_conclusao_prevista'] < hoje:
            return np.random.choice(['Concluído', 'Atrasado'], p=[0.7, 0.3])
        else:
            return 'Em Andamento'
    
    df_projetos['status'] = df_projetos.apply(determinar_status, axis=1)
    
    # Calcular progresso baseado no status
    def calcular_progresso(row):
        if row['status'] == 'Planejado':
            return np.random.randint(0, 10)
        elif row['status'] == 'Concluído':
            return 100
        elif row['status'] == 'Atrasado':
            return np.random.randint(70, 95)
        else:  # Em Andamento
            dias_decorridos = (hoje - row['data_inicio']).days
            progresso_esperado = min(95, (dias_decorridos / row['duracao_prevista']) * 100)
            return max(5, progresso_esperado + np.random.randint(-15, 20))
    
    df_projetos['progresso'] = df_projetos.apply(calcular_progresso, axis=1)
    
    # Calcular atraso em dias
    def calcular_atraso(row):
        if row['status'] in ['Planejado', 'Em Andamento']:
            dias_decorridos = (hoje - row['data_inicio']).days
            progresso_esperado = (dias_decorridos / row['duracao_prevista']) * 100
            if row['progresso'] < progresso_esperado:
                return int((progresso_esperado - row['progresso']) / 100 * row['duracao_prevista'])
            else:
                return 0
        elif row['status'] == 'Atrasado':
            return np.random.randint(15, 60)
        else:
            return 0
    
    df_projetos['atraso'] = df_projetos.apply(calcular_atraso, axis=1)
    
    # Calcular data de conclusão real
    df_projetos['data_conclusao_real'] = df_projetos.apply(
        lambda row: row['data_conclusao_prevista'] + dt.timedelta(days=row['atraso']), axis=1
    )
    
    # Calcular custo adicional
    def calcular_custo_adicional(row):
        if row['status'] == 'Planejado':
            return 0
        elif row['atraso'] > 0:
            return np.random.randint(5, 25)
        else:
            return np.random.randint(0, 10)
    
    df_projetos['custo_adicional_pct'] = df_projetos.apply(calcular_custo_adicional, axis=1)
    df_projetos['custo_real'] = df_projetos['orcamento'] * (1 + df_projetos['custo_adicional_pct'] / 100)
    
    # Calcular satisfação do cliente
    def calcular_satisfacao(row):
        if row['atraso'] == 0 and row['custo_adicional_pct'] < 5:
            return np.random.randint(8, 11)
        elif row['atraso'] < 15 and row['custo_adicional_pct'] < 15:
            return np.random.randint(6, 9)
        else:
            return np.random.randint(3, 7)
    
    df_projetos['satisfacao_cliente'] = df_projetos.apply(calcular_satisfacao, axis=1)
    
    # Calcular área e eficiência
    areas_por_tipo = {
        'Residencial': (50, 300),
        'Comercial': (100, 1000),
        'Industrial': (200, 5000),
        'Infraestrutura': (500, 10000)
    }
    
    df_projetos['area'] = df_projetos.apply(
        lambda row: np.random.randint(*areas_por_tipo[row['tipo_projeto']]), axis=1
    )
    df_projetos['eficiencia'] = df_projetos['custo_real'] / df_projetos['area']
    
    # Calcular qualidade
    df_projetos['qualidade'] = df_projetos.apply(
        lambda row: np.random.randint(80, 101) if row['complexidade'] in ['Baixa', 'Média'] 
                   else np.random.randint(70, 95), axis=1
    )
    
    # Gerar dados de marcos do projeto
    marcos_data = []
    tipos_marco = ['Iniciação', 'Planejamento', 'Execução', 'Monitoramento', 'Encerramento']
    
    for _, projeto in df_projetos.iterrows():
        n_marcos = random.randint(3, 6)
        duracao_total = (projeto['data_conclusao_real'] - projeto['data_inicio']).days
        
        for i in range(n_marcos):
            data_marco = projeto['data_inicio'] + dt.timedelta(
                days=int((i / (n_marcos - 1)) * duracao_total)
            )
            
            tipo_marco = tipos_marco[min(i, len(tipos_marco) - 1)]
            nome_marco = f'{tipo_marco} - {projeto["nome_projeto"]}'
            
            # Status do marco
            if data_marco <= hoje:
                status_marco = np.random.choice(['Concluído', 'Atrasado'], p=[0.8, 0.2])
                atraso_marco = random.randint(0, 10) if status_marco == 'Concluído' else random.randint(5, 20)
            else:
                status_marco = 'Pendente'
                atraso_marco = 0
            
            marcos_data.append({
                'id_projeto': projeto['id_projeto'],
                'nome_marco': nome_marco,
                'tipo_marco': tipo_marco,
                'data_prevista': data_marco,
                'data_real': data_marco + dt.timedelta(days=atraso_marco) if status_marco == 'Concluído' else None,
                'status_marco': status_marco,
                'atraso_marco': atraso_marco
            })
    
    df_marcos = pd.DataFrame(marcos_data)
    
    # Gerar dados financeiros mensais
    financeiro_data = []
    
    for _, projeto in df_projetos.iterrows():
        if projeto['status'] == 'Planejado':
            continue
            
        inicio = projeto['data_inicio']
        fim = projeto['data_conclusao_real'] if projeto['status'] == 'Concluído' else hoje
        
        # Gerar dados mensais
        current_date = inicio.replace(day=1)
        orcamento_mensal = projeto['orcamento'] / max(1, ((fim - inicio).days / 30.44))
        
        while current_date <= fim and current_date <= hoje:
            # Gasto real com variação
            variacao_pct = np.random.uniform(-20, 30)
            gasto_real = orcamento_mensal * (1 + variacao_pct / 100)
            
            financeiro_data.append({
                'id_projeto': projeto['id_projeto'],
                'data': current_date,
                'mes_ano': current_date.strftime('%Y-%m'),
                'orcado': orcamento_mensal,
                'realizado': gasto_real,
                'variacao': variacao_pct
            })
            
            # Próximo mês
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
    
    df_financeiro = pd.DataFrame(financeiro_data)
    
    # Salvar os datasets
    df_projetos.to_csv('data/projetos.csv', index=False)
    df_marcos.to_csv('data/marcos_projeto.csv', index=False)
    df_financeiro.to_csv('data/financeiro_mensal.csv', index=False)
    
    print(f"Dados de performance de projetos gerados com sucesso!")
    print(f"- Projetos: {len(df_projetos)} registros")
    print(f"- Marcos: {len(df_marcos)} registros")
    print(f"- Financeiro: {len(df_financeiro)} registros")
    
    return df_projetos, df_marcos, df_financeiro

def gerar_dados_recursos(df_projetos):
    """
    Gera dados sobre recursos utilizados nos projetos.
    """
    categorias_recursos = [
        'Recursos Humanos',
        'Equipamentos',
        'Materiais',
        'Software',
        'Consultoria',
        'Infraestrutura'
    ]
    
    recursos_data = []
    
    for _, projeto in df_projetos.iterrows():
        n_categorias = random.randint(3, len(categorias_recursos))
        cats_selecionadas = random.sample(categorias_recursos, n_categorias)
        
        # Distribuição percentual
        distribuicao = np.random.dirichlet(np.ones(n_categorias)) * 100
        
        for i, categoria in enumerate(cats_selecionadas):
            valor_orcado = projeto['orcamento'] * (distribuicao[i] / 100)
            valor_realizado = valor_orcado * (1 + projeto['custo_adicional_pct'] / 100 * np.random.uniform(0.5, 1.5))
            
            recursos_data.append({
                'id_projeto': projeto['id_projeto'],
                'categoria_recurso': categoria,
                'alocacao_percentual': distribuicao[i],
                'valor_orcado': valor_orcado,
                'valor_realizado': valor_realizado
            })
    
    df_recursos = pd.DataFrame(recursos_data)
    df_recursos.to_csv('data/recursos_projeto.csv', index=False)
    
    print(f"- Recursos: {len(df_recursos)} registros")
    return df_recursos

if __name__ == "__main__":
    # Gerar todos os dados
    df_projetos, df_marcos, df_financeiro = gerar_dados_projetos(200)
    df_recursos = gerar_dados_recursos(df_projetos)
    print("\nGeração de dados de performance de projetos concluída com sucesso!")