# 🤖 Guia Completo de Implementação de IA e Python Coding
## Código Prático e Estratégias Executáveis para Desenvolvimento de IA

"""
Este módulo contém implementações práticas de IA e guias de Python coding
para desenvolvimento de dashboards inteligentes e análise preditiva.

Categorias de implementação:
1. 🔧 Sistema de Embeddings para Knowledge-Base
2. 🧠 RAG (Retrieval-Augmented Generation) 
3. 🎯 Análise Preditiva com ML
4. 📊 Dashboards Inteligentes
5. 🔍 Processamento de Linguagem Natural
6. 🚀 Deploy e Otimização
"""

### 🔧 **1. SISTEMA DE EMBEDDINGS PARA KNOWLEDGE-BASE**

```python
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
import json

class KnowledgeBaseEmbeddings:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("knowledge_base")
        
    def process_knowledge_base(self, kb_path="Knowledge-Base"):
        """Processa toda a Knowledge-Base criando embeddings"""
        documents = []
        metadata = []
        
        for category in Path(kb_path).iterdir():
            if category.is_dir() and not category.name.startswith('.'):
                docs, meta = self.process_category(category)
                documents.extend(docs)
                metadata.extend(meta)
        
        # Criar embeddings
        embeddings = self.model.encode(documents)
        
        # Armazenar no ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadata,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        
        return len(documents)
    
    def process_category(self, category_path):
        """Processa uma categoria específica"""
        documents = []
        metadata = []
        
        for file_path in category_path.rglob("*.md"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Chunking inteligente
            chunks = self.intelligent_chunking(content)
            
            for chunk in chunks:
                documents.append(chunk)
                metadata.append({
                    "category": category_path.name,
                    "file_path": str(file_path),
                    "chunk_type": self.classify_chunk(chunk),
                    "complexity": self.estimate_complexity(chunk),
                    "topics": self.extract_topics(chunk)
                })
        
        return documents, metadata
    
    def intelligent_chunking(self, content, max_chunk_size=512):
        """Chunking inteligente baseado em estrutura"""
        chunks = []
        lines = content.split('\n')
        current_chunk = ""
        current_section = ""
        
        for line in lines:
            if line.startswith('#'):  # Nova seção
                if current_chunk and len(current_chunk) > 100:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
                current_section = line
            else:
                current_chunk += line + '\n'
                
            if len(current_chunk) > max_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = current_section + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def semantic_search(self, query, n_results=5):
        """Busca semântica na Knowledge-Base"""
        query_embedding = self.model.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        
        return results

# Exemplo de uso
kb_embeddings = KnowledgeBaseEmbeddings()
# kb_embeddings.process_knowledge_base()
```

### 🧠 **2. SISTEMA DE CONTEXT AWARENESS**

```python
class ContextAwareAI:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.context_history = []
        self.user_preferences = {}
        self.success_patterns = {}
        
    def analyze_query_context(self, query, conversation_history=None):
        """Análise contextual do query"""
        context = {
            "intent": self.classify_intent(query),
            "complexity": self.estimate_query_complexity(query),
            "domain": self.identify_domain(query),
            "requires_code": self.needs_code_generation(query),
            "learning_level": self.estimate_user_level(query, conversation_history)
        }
        
        return context
    
    def classify_intent(self, query):
        """Classifica a intenção do usuário"""
        intents = {
            "learning": ["aprende", "entenda", "explique", "como funciona"],
            "troubleshooting": ["erro", "problema", "não funciona", "debug"],
            "implementation": ["criar", "fazer", "implementar", "código"],
            "optimization": ["otimizar", "melhorar", "performance", "rápido"],
            "reference": ["documentação", "api", "sintaxe", "parâmetros"]
        }
        
        query_lower = query.lower()
        intent_scores = {}
        
        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            intent_scores[intent] = score
        
        return max(intent_scores, key=intent_scores.get)
    
    def get_contextual_knowledge(self, query, context):
        """Recupera conhecimento contextualmente relevante"""
        # 1. Busca semântica básica
        semantic_results = self.kb.semantic_search(query, n_results=10)
        
        # 2. Filtro por contexto
        filtered_results = self.filter_by_context(semantic_results, context)
        
        # 3. Ranking por relevância
        ranked_results = self.rank_by_relevance(filtered_results, query, context)
        
        # 4. Otimização por token limit
        optimized_results = self.optimize_token_usage(ranked_results, max_tokens=4000)
        
        return optimized_results
    
    def filter_by_context(self, results, context):
        """Filtra resultados baseado no contexto"""
        filtered = []
        
        for result in results['documents'][0]:
            metadata = results['metadatas'][0][results['documents'][0].index(result)]
            
            # Filtros baseados no contexto
            if context['intent'] == 'learning' and metadata.get('chunk_type') == 'example':
                continue
            
            if context['intent'] == 'implementation' and metadata.get('chunk_type') == 'theory':
                continue
            
            if context['complexity'] == 'beginner' and metadata.get('complexity') == 'expert':
                continue
            
            filtered.append((result, metadata))
        
        return filtered
```

### 🎯 **3. ERROR PREDICTION E PREVENTION**

```python
class ErrorPreventionSystem:
    def __init__(self):
        self.common_errors = self.load_error_patterns()
        self.code_validator = CodeValidator()
        
    def load_error_patterns(self):
        """Carrega padrões de erro comuns"""
        return {
            "plotly_errors": [
                {
                    "pattern": "fig.show()",
                    "context": "jupyter",
                    "solution": "Use fig.show(renderer='notebook') em Jupyter",
                    "frequency": 0.8
                },
                {
                    "pattern": "callback without Output",
                    "context": "dash",
                    "solution": "Todo callback precisa de pelo menos um Output",
                    "frequency": 0.7
                }
            ],
            "pandas_errors": [
                {
                    "pattern": "SettingWithCopyWarning",
                    "context": "data_manipulation",
                    "solution": "Use .loc[] ou .copy() para evitar warnings",
                    "frequency": 0.9
                }
            ]
        }
    
    def predict_potential_errors(self, code, context):
        """Prediz erros potenciais no código"""
        potential_errors = []
        
        # 1. Pattern matching com erros conhecidos
        for category, errors in self.common_errors.items():
            for error in errors:
                if self.pattern_matches(code, error['pattern'], context):
                    potential_errors.append({
                        "type": "pattern_match",
                        "category": category,
                        "error": error,
                        "confidence": error['frequency']
                    })
        
        # 2. Análise sintática
        syntax_issues = self.code_validator.validate_syntax(code)
        potential_errors.extend(syntax_issues)
        
        # 3. Análise de dependências
        dependency_issues = self.code_validator.check_dependencies(code)
        potential_errors.extend(dependency_issues)
        
        return sorted(potential_errors, key=lambda x: x['confidence'], reverse=True)
    
    def generate_preventive_suggestions(self, code, predicted_errors):
        """Gera sugestões preventivas"""
        suggestions = []
        
        for error in predicted_errors:
            if error['confidence'] > 0.7:  # Alta confiança
                suggestion = {
                    "type": "prevention",
                    "message": f"Possível erro detectado: {error['error']['pattern']}",
                    "solution": error['error']['solution'],
                    "code_fix": self.generate_code_fix(code, error)
                }
                suggestions.append(suggestion)
        
        return suggestions

class CodeValidator:
    def validate_syntax(self, code):
        """Valida sintaxe do código"""
        import ast
        try:
            ast.parse(code)
            return []
        except SyntaxError as e:
            return [{
                "type": "syntax_error",
                "message": str(e),
                "confidence": 1.0
            }]
    
    def check_dependencies(self, code):
        """Verifica dependências e versões"""
        import re
        imports = re.findall(r'import (\w+)|from (\w+)', code)
        issues = []
        
        for imp in imports:
            module = imp[0] or imp[1]
            if module in ['plotly', 'dash']:
                # Verificar compatibilidade de versão
                version_check = self.check_version_compatibility(module, code)
                if version_check:
                    issues.append(version_check)
        
        return issues
```

### 📊 **4. LEARNING ANALYTICS E FEEDBACK**

```python
class LearningAnalytics:
    def __init__(self):
        self.interactions = []
        self.user_profiles = {}
        self.knowledge_effectiveness = {}
        
    def log_interaction(self, user_id, query, response, feedback=None):
        """Log de interação para análise"""
        interaction = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "query": query,
            "response": response,
            "feedback": feedback,
            "context": self.extract_context(query),
            "knowledge_sources": self.extract_sources(response)
        }
        
        self.interactions.append(interaction)
        self.update_user_profile(user_id, interaction)
        
    def analyze_learning_patterns(self, user_id):
        """Analisa padrões de aprendizado do usuário"""
        user_interactions = [i for i in self.interactions if i['user_id'] == user_id]
        
        patterns = {
            "preferred_learning_style": self.identify_learning_style(user_interactions),
            "knowledge_gaps": self.identify_knowledge_gaps(user_interactions),
            "progress_areas": self.identify_progress_areas(user_interactions),
            "common_errors": self.identify_common_errors(user_interactions)
        }
        
        return patterns
    
    def generate_personalized_recommendations(self, user_id):
        """Gera recomendações personalizadas"""
        patterns = self.analyze_learning_patterns(user_id)
        
        recommendations = []
        
        # Baseado em gaps de conhecimento
        for gap in patterns['knowledge_gaps']:
            rec = {
                "type": "knowledge_gap",
                "topic": gap,
                "resources": self.find_resources_for_topic(gap),
                "learning_path": self.create_learning_path(gap, patterns['preferred_learning_style'])
            }
            recommendations.append(rec)
        
        return recommendations
    
    def measure_knowledge_base_effectiveness(self):
        """Mede efetividade da Knowledge-Base"""
        effectiveness = {}
        
        for interaction in self.interactions:
            for source in interaction['knowledge_sources']:
                if source not in effectiveness:
                    effectiveness[source] = {"uses": 0, "positive_feedback": 0, "negative_feedback": 0}
                
                effectiveness[source]["uses"] += 1
                
                if interaction['feedback']:
                    if interaction['feedback']['rating'] > 3:
                        effectiveness[source]["positive_feedback"] += 1
                    else:
                        effectiveness[source]["negative_feedback"] += 1
        
        # Calcular scores
        for source, data in effectiveness.items():
            if data["uses"] > 0:
                data["effectiveness_score"] = (data["positive_feedback"] - data["negative_feedback"]) / data["uses"]
        
        return effectiveness
```

### 🎛️ **5. ADAPTIVE RESPONSE GENERATION**

```python
class AdaptiveResponseGenerator:
    def __init__(self, knowledge_base, learning_analytics):
        self.kb = knowledge_base
        self.analytics = learning_analytics
        self.response_strategies = self.load_response_strategies()
        
    def generate_adaptive_response(self, user_id, query):
        """Gera resposta adaptada ao usuário"""
        # 1. Análise do contexto e usuário
        context = self.analyze_context(query)
        user_profile = self.analytics.user_profiles.get(user_id, {})
        
        # 2. Seleção da estratégia de resposta
        strategy = self.select_response_strategy(context, user_profile)
        
        # 3. Recuperação de conhecimento contextual
        relevant_knowledge = self.get_contextual_knowledge(query, context, user_profile)
        
        # 4. Geração da resposta
        response = self.generate_response(query, relevant_knowledge, strategy)
        
        # 5. Validação e otimização
        validated_response = self.validate_and_optimize(response, context)
        
        return validated_response
    
    def select_response_strategy(self, context, user_profile):
        """Seleciona estratégia de resposta baseada no contexto e perfil"""
        strategies = {
            "beginner": "step_by_step_with_examples",
            "intermediate": "balanced_theory_practice",
            "advanced": "concise_with_references",
            "visual_learner": "diagram_heavy_response",
            "code_focused": "code_first_explanation"
        }
        
        user_level = user_profile.get('level', 'intermediate')
        learning_style = user_profile.get('preferred_style', 'balanced')
        
        # Lógica de seleção baseada em múltiplos fatores
        if context['intent'] == 'troubleshooting':
            return "problem_solution_focused"
        elif user_level == 'beginner' and context['complexity'] == 'high':
            return "simplified_step_by_step"
        elif learning_style == 'visual':
            return "visual_examples_heavy"
        else:
            return strategies.get(user_level, "balanced_theory_practice")
    
    def generate_response(self, query, knowledge, strategy):
        """Gera resposta usando a estratégia selecionada"""
        response_template = self.response_strategies[strategy]
        
        # Construir resposta baseada no template e conhecimento
        response = {
            "introduction": self.generate_introduction(query, strategy),
            "main_content": self.generate_main_content(knowledge, strategy),
            "examples": self.generate_examples(knowledge, strategy),
            "conclusion": self.generate_conclusion(strategy),
            "additional_resources": self.suggest_resources(knowledge)
        }
        
        return response
```

### 🔄 **6. CONTINUOUS IMPROVEMENT LOOP**

```python
class ContinuousImprovementSystem:
    def __init__(self):
        self.performance_metrics = PerformanceMetrics()
        self.knowledge_updater = KnowledgeUpdater()
        self.model_trainer = ModelTrainer()
        
    def daily_improvement_cycle(self):
        """Ciclo diário de melhoria"""
        # 1. Análise de performance do dia anterior
        daily_metrics = self.performance_metrics.get_daily_metrics()
        
        # 2. Identificação de padrões problemáticos
        problem_patterns = self.identify_problem_patterns(daily_metrics)
        
        # 3. Atualização de conhecimento baseada em gaps identificados
        knowledge_updates = self.knowledge_updater.suggest_updates(problem_patterns)
        
        # 4. Re-treinamento de modelos específicos
        if self.should_retrain_models(daily_metrics):
            self.model_trainer.incremental_training()
        
        # 5. Atualização de estratégias de resposta
        self.update_response_strategies(daily_metrics)
        
        return {
            "metrics": daily_metrics,
            "improvements": knowledge_updates,
            "retraining": self.model_trainer.last_training_results
        }
    
    def weekly_deep_analysis(self):
        """Análise profunda semanal"""
        weekly_data = self.performance_metrics.get_weekly_metrics()
        
        # Análises mais complexas
        trend_analysis = self.analyze_trends(weekly_data)
        user_satisfaction_analysis = self.analyze_user_satisfaction(weekly_data)
        knowledge_gap_analysis = self.analyze_knowledge_gaps(weekly_data)
        
        # Relatório de melhorias
        improvement_report = {
            "trends": trend_analysis,
            "satisfaction": user_satisfaction_analysis,
            "knowledge_gaps": knowledge_gap_analysis,
            "recommendations": self.generate_improvement_recommendations()
        }
        
        return improvement_report

# Sistema de implementação modular
class AIOptimizationSystem:
    def __init__(self, knowledge_base_path="Knowledge-Base"):
        self.embeddings = KnowledgeBaseEmbeddings()
        self.context_ai = ContextAwareAI(self.embeddings)
        self.error_prevention = ErrorPreventionSystem()
        self.analytics = LearningAnalytics()
        self.response_generator = AdaptiveResponseGenerator(
            self.embeddings, self.analytics
        )
        self.improvement_system = ContinuousImprovementSystem()
        
        # Inicialização
        self.initialize_system(knowledge_base_path)
    
    def initialize_system(self, kb_path):
        """Inicializa todo o sistema"""
        print("🚀 Inicializando sistema de otimização de IA...")
        
        # 1. Processar Knowledge-Base
        num_docs = self.embeddings.process_knowledge_base(kb_path)
        print(f"📚 Processados {num_docs} documentos")
        
        # 2. Carregar padrões históricos
        # self.load_historical_patterns()
        
        print("✅ Sistema inicializado com sucesso!")
    
    def process_query(self, user_id, query):
        """Processa query com todas as otimizações"""
        # 1. Log da interação
        start_time = time.time()
        
        # 2. Geração de resposta adaptativa
        response = self.response_generator.generate_adaptive_response(user_id, query)
        
        # 3. Prevenção de erros se código está envolvido
        if self.contains_code(response):
            error_suggestions = self.error_prevention.predict_potential_errors(
                response['code'], response['context']
            )
            response['error_prevention'] = error_suggestions
        
        # 4. Log da interação completa
        processing_time = time.time() - start_time
        self.analytics.log_interaction(user_id, query, response)
        
        return response, processing_time
```

---

## 🎯 **IMPLEMENTAÇÃO PRÁTICA**

Para implementar essas melhorias na sua Knowledge-Base:

1. **Execute o sistema de embeddings** primeiro
2. **Configure o sistema de analytics** para começar a coletar dados
3. **Implemente gradualmente** os sistemas mais complexos
4. **Monitore métricas** e ajuste conforme necessário

Este sistema transforma a IA de reativa para proativa, aprendendo continuamente e se adaptando ao usuário!


### 🔧 **7. PYTHON CODING BEST PRACTICES PARA IA**

```python
# Guia prático de Python coding para projetos de IA
import asyncio
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass
from pathlib import Path
import logging
from functools import wraps
import time

@dataclass
class AIProjectStructure:
    """Estrutura padrão para projetos de IA em Python"""
    project_name: str
    data_path: Path
    models_path: Path
    logs_path: Path
    config_path: Path
    
    def create_structure(self):
        """Cria estrutura de diretórios"""
        for path_attr in ['data_path', 'models_path', 'logs_path', 'config_path']:
            path = getattr(self, path_attr)
            path.mkdir(parents=True, exist_ok=True)
        
        self._create_gitignore()
        self._create_requirements()
        self._create_config_template()
    
    def _create_gitignore(self):
        gitignore_content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Data files
*.csv
*.xlsx
*.json
*.pkl
*.h5
*.db

# Model files
*.pt
*.pth
*.onnx
*.pb

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
"""
        with open(self.project_name + "/.gitignore", "w") as f:
            f.write(gitignore_content.strip())

def timing_decorator(func):
    """Decorator para medir performance de funções"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger = logging.getLogger(__name__)
        logger.info(f"{func.__name__} executada em {end_time - start_time:.4f}s")
        
        return result
    return wrapper

def error_handler(func):
    """Decorator para tratamento de erros em funções de IA"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Erro em {func.__name__}: {str(e)}")
            
            # Retornar resposta padrão baseada no tipo da função
            if 'predict' in func.__name__:
                return {"error": "Prediction failed", "details": str(e)}
            elif 'train' in func.__name__:
                return {"status": "failed", "error": str(e)}
            else:
                raise e
    return wrapper

class PythonAIBestPractices:
    """Implementa melhores práticas de Python para IA"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Configuração profissional de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_project.log'),
                logging.StreamHandler()
            ]
        )
    
    @timing_decorator
    @error_handler
    def load_data_efficiently(self, file_path: str, chunk_size: int = 10000) -> Any:
        """Carregamento eficiente de dados grandes"""
        import pandas as pd
        
        if file_path.endswith('.csv'):
            # Para arquivos CSV grandes, usar chunksize
            chunks = []
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                # Processamento de cada chunk
                chunk = self.preprocess_chunk(chunk)
                chunks.append(chunk)
            
            return pd.concat(chunks, ignore_index=True)
        
        elif file_path.endswith('.parquet'):
            # Parquet é mais eficiente para dados grandes
            return pd.read_parquet(file_path)
    
    def preprocess_chunk(self, chunk: Any) -> Any:
        """Pré-processamento de chunk de dados"""
        # Implementar lógica específica de pré-processamento
        return chunk
    
    async def async_model_training(self, models: List[Dict]) -> List[Dict]:
        """Treinamento assíncrono de múltiplos modelos"""
        async def train_single_model(model_config):
            # Simulação de treinamento assíncrono
            await asyncio.sleep(model_config.get('training_time', 1))
            return {
                'model_name': model_config['name'],
                'status': 'trained',
                'accuracy': 0.95  # Placeholder
            }
        
        # Treinar modelos em paralelo
        tasks = [train_single_model(model) for model in models]
        results = await asyncio.gather(*tasks)
        
        return results
    
    def memory_efficient_processing(self, data_generator):
        """Processamento eficiente de memória usando generators"""
        for batch in data_generator:
            # Processa batch por batch para economizar memória
            processed_batch = self.process_batch(batch)
            yield processed_batch
    
    def process_batch(self, batch):
        """Processa um batch de dados"""
        # Implementar lógica de processamento
        return batch

# Exemplo de configuração de projeto
def create_ai_project(project_name: str):
    """Cria estrutura completa de projeto de IA"""
    project = AIProjectStructure(
        project_name=project_name,
        data_path=Path(project_name) / "data",
        models_path=Path(project_name) / "models",
        logs_path=Path(project_name) / "logs",
        config_path=Path(project_name) / "config"
    )
    
    project.create_structure()
    return project
```

### 🎯 **8. IMPLEMENTAÇÃO DE ALGORITMOS ML OTIMIZADOS**

```python
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import joblib
from typing import Tuple, List

class OptimizedMLPipeline:
    """Pipeline otimizado para Machine Learning com Python"""
    
    def __init__(self, model_type: str = "classification"):
        self.model_type = model_type
        self.pipeline = None
        self.feature_importance = None
        self.performance_metrics = {}
    
    def create_preprocessing_pipeline(self) -> Pipeline:
        """Cria pipeline de pré-processamento otimizado"""
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.impute import SimpleImputer
        from sklearn.compose import ColumnTransformer
        
        # Pipeline personalizado baseado no tipo de dados
        numeric_features = self.get_numeric_features()
        categorical_features = self.get_categorical_features()
        
        numeric_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('encoder', LabelEncoder())
        ])
        
        preprocessor = ColumnTransformer([
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
        return preprocessor
    
    def auto_feature_engineering(self, X: pd.DataFrame) -> pd.DataFrame:
        """Feature engineering automatizado"""
        X_engineered = X.copy()
        
        # 1. Criação de features de interação
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                X_engineered[f'{col1}_{col2}_interaction'] = X[col1] * X[col2]
        
        # 2. Features temporais se existirem colunas de data
        date_cols = X.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            X_engineered[f'{col}_year'] = X[col].dt.year
            X_engineered[f'{col}_month'] = X[col].dt.month
            X_engineered[f'{col}_day'] = X[col].dt.day
            X_engineered[f'{col}_weekday'] = X[col].dt.weekday
        
        # 3. Features estatísticas
        for col in numeric_cols:
            X_engineered[f'{col}_log'] = np.log1p(X[col])
            X_engineered[f'{col}_sqrt'] = np.sqrt(np.abs(X[col]))
        
        return X_engineered
    
    def hyperparameter_optimization(self, X, y, model, param_grid):
        """Otimização automática de hiperparâmetros"""
        from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
        
        # Usar RandomizedSearch para espaços grandes de parâmetros
        if len(param_grid) > 50:
            search = RandomizedSearchCV(
                model, param_grid, n_iter=20, cv=5, scoring='accuracy'
            )
        else:
            search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        
        search.fit(X, y)
        
        return search.best_estimator_, search.best_params_
    
    def advanced_model_evaluation(self, model, X, y) -> Dict:
        """Avaliação avançada de modelos"""
        from sklearn.metrics import classification_report, confusion_matrix
        from sklearn.model_selection import learning_curve
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5)
        
        # Learning curves
        train_sizes, train_scores, val_scores = learning_curve(
            model, X, y, cv=5, n_jobs=-1
        )
        
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            self.feature_importance = model.feature_importances_
        
        metrics = {
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'train_scores': train_scores,
            'val_scores': val_scores,
            'train_sizes': train_sizes
        }
        
        return metrics

class RealTimePredictor:
    """Sistema de predição em tempo real otimizado"""
    
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.cache = {}
        self.prediction_history = []
    
    @timing_decorator
    def predict_single(self, features: Dict) -> Dict:
        """Predição única otimizada"""
        # Cache para features similares
        feature_hash = hash(str(sorted(features.items())))
        
        if feature_hash in self.cache:
            return self.cache[feature_hash]
        
        # Converter para formato esperado pelo modelo
        X = self.prepare_features(features)
        
        # Predição
        prediction = self.model.predict(X)[0]
        probability = None
        
        if hasattr(self.model, 'predict_proba'):
            probability = self.model.predict_proba(X)[0].max()
        
        result = {
            'prediction': prediction,
            'probability': probability,
            'timestamp': time.time()
        }
        
        # Armazenar no cache
        self.cache[feature_hash] = result
        self.prediction_history.append(result)
        
        return result
    
    def batch_predict(self, features_list: List[Dict]) -> List[Dict]:
        """Predição em lote otimizada"""
        # Preparar todas as features de uma vez
        X_batch = [self.prepare_features(features) for features in features_list]
        X_batch = np.vstack(X_batch)
        
        # Predição em lote
        predictions = self.model.predict(X_batch)
        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X_batch)
        else:
            probabilities = [None] * len(predictions)
        
        results = []
        for pred, prob in zip(predictions, probabilities):
            result = {
                'prediction': pred,
                'probability': prob.max() if prob is not None else None,
                'timestamp': time.time()
            }
            results.append(result)
        
        return results
    
    def prepare_features(self, features: Dict) -> np.ndarray:
        """Prepara features para o modelo"""
        # Implementar lógica de preparação específica
        feature_vector = list(features.values())
        return np.array(feature_vector).reshape(1, -1)
```

### 🚀 **9. DEPLOY E PRODUÇÃO DE MODELOS IA**

```python
from flask import Flask, request, jsonify
import redis
import pickle
from celery import Celery
import monitoring

class ProductionAISystem:
    """Sistema de IA para produção com Python"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.celery = Celery('ai_system')
        self.setup_routes()
        self.setup_monitoring()
    
    def setup_routes(self):
        """Configura rotas da API"""
        
        @self.app.route('/predict', methods=['POST'])
        def predict():
            try:
                data = request.json
                
                # Validação de entrada
                if not self.validate_input(data):
                    return jsonify({'error': 'Invalid input'}), 400
                
                # Predição
                prediction = self.make_prediction(data)
                
                # Log da predição
                self.log_prediction(data, prediction)
                
                return jsonify(prediction)
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/batch_predict', methods=['POST'])
        def batch_predict():
            data_list = request.json
            
            # Processar em background se for lote grande
            if len(data_list) > 100:
                task = self.process_large_batch.delay(data_list)
                return jsonify({'task_id': task.id, 'status': 'processing'})
            
            predictions = [self.make_prediction(data) for data in data_list]
            return jsonify(predictions)
    
    @celery.task
    def process_large_batch(self, data_list):
        """Processa lotes grandes em background"""
        predictions = []
        for data in data_list:
            pred = self.make_prediction(data)
            predictions.append(pred)
        
        # Armazenar resultado no Redis
        result_id = f"batch_result_{time.time()}"
        self.redis_client.set(result_id, pickle.dumps(predictions))
        
        return result_id
    
    def setup_monitoring(self):
        """Configura monitoramento do sistema"""
        
        @self.app.before_request
        def before_request():
            request.start_time = time.time()
        
        @self.app.after_request
        def after_request(response):
            request_time = time.time() - request.start_time
            
            # Log de performance
            monitoring.log_request_time(request.endpoint, request_time)
            
            # Monitor de saúde do sistema
            monitoring.check_system_health()
            
            return response
    
    def validate_input(self, data):
        """Validação de entrada robusta"""
        required_fields = ['feature1', 'feature2']  # Definir campos obrigatórios
        
        for field in required_fields:
            if field not in data:
                return False
        
        return True
    
    def make_prediction(self, data):
        """Faz predição com cache e fallback"""
        # Tentar cache primeiro
        cache_key = f"pred_{hash(str(data))}"
        cached_result = self.redis_client.get(cache_key)
        
        if cached_result:
            return pickle.loads(cached_result)
        
        # Fazer predição
        try:
            prediction = self.model.predict([data])[0]
            
            # Armazenar no cache
            result = {'prediction': prediction, 'confidence': 0.95}
            self.redis_client.setex(cache_key, 3600, pickle.dumps(result))
            
            return result
        
        except Exception as e:
            # Fallback para modelo simples
            return self.fallback_prediction(data)
    
    def fallback_prediction(self, data):
        """Predição de fallback quando modelo principal falha"""
        # Implementar lógica de fallback simples
        return {'prediction': 'default', 'confidence': 0.5, 'fallback': True}
```
