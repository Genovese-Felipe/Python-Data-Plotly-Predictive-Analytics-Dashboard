import os
import xml.etree.ElementTree as ET
from datetime import datetime
import re
from collections import defaultdict
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 não está instalado. Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

class AdvancedSemanticPlotlyExtractor:
    def __init__(self):
        self.root = ET.Element('advanced_plotly_guide')
        self.root.set('generated_on', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.root.set('version', '3.0')
        self.root.set('description', 'Guia pedagógico avançado de Plotly baseado em estrutura de aprendizado progressivo')
        
        # Metadados expandidos
        self.metadata = ET.SubElement(self.root, 'metadata')
        self._create_metadata()
        
        # Estrutura pedagógica baseada na revisão
        self.structure = {
            'part_1_fundamentals': {
                'name': 'Parte I: Fundamentos',
                'description': 'Base conceitual e arquitetura do Plotly',
                'learning_objectives': [
                    'Compreender a arquitetura do Plotly',
                    'Diferenciar Express vs Graph Objects',
                    'Preparar dados nos formatos corretos'
                ]
            },
            'part_2_essential_charts': {
                'name': 'Parte II: Gráficos Essenciais',
                'description': 'Gráficos fundamentais para visualização de dados',
                'learning_objectives': [
                    'Criar gráficos de barras completos',
                    'Implementar visualizações geográficas',
                    'Dominar gráficos de linha e dispersão'
                ]
            },
            'part_3_customization': {
                'name': 'Parte III: Customização e Interatividade',
                'description': 'Estilização avançada e recursos interativos',
                'learning_objectives': [
                    'Aplicar estilização profissional',
                    'Implementar interatividade',
                    'Integrar com Dash'
                ]
            },
            'part_4_advanced': {
                'name': 'Parte IV: Tópicos Avançados',
                'description': 'Performance, boas práticas e casos complexos',
                'learning_objectives': [
                    'Otimizar performance',
                    'Aplicar boas práticas de design',
                    'Resolver problemas complexos'
                ]
            }
        }
        
        # Criar estrutura XML
        self._create_structure()
        
        # Dicionários para classificação
        self.difficulty_keywords = {
            'basic': ['basic', 'simple', 'introduction', 'getting started', 'first'],
            'intermediate': ['advanced', 'custom', 'style', 'layout', 'multiple'],
            'advanced': ['performance', 'optimization', 'complex', 'enterprise', 'scalable']
        }
        
        self.topic_mapping = {
            'part_1_fundamentals': ['plotly python', 'getting started', 'introduction', 'basic'],
            'part_2_essential_charts': ['bar chart', 'line chart', 'scatter', 'pie chart', 'geographic'],
            'part_3_customization': ['styling', 'color', 'layout', 'interactive', 'dash', 'annotation'],
            'part_4_advanced': ['performance', 'optimization', 'enterprise', 'large data', 'streaming']
        }

    def _create_metadata(self):
        """Cria metadados expandidos baseados na revisão"""
        title = ET.SubElement(self.metadata, 'title')
        title.text = 'Guia Pedagógico Avançado Plotly Python'
        
        description = ET.SubElement(self.metadata, 'description')
        description.text = 'Guia estruturado pedagogicamente seguindo progressão de aprendizado lógica'
        
        pedagogy = ET.SubElement(self.metadata, 'pedagogical_approach')
        pedagogy.text = 'Fundamentos → Essencial → Customização → Avançado'
        
        # Características pedagógicas
        features = ET.SubElement(self.metadata, 'educational_features')
        features.set('learning_objectives', 'true')
        features.set('difficulty_levels', 'true')
        features.set('side_by_side_examples', 'true')
        features.set('practical_exercises', 'true')
        features.set('glossary', 'true')

    def _create_structure(self):
        """Cria estrutura XML baseada na revisão pedagógica"""
        for part_id, part_info in self.structure.items():
            part_elem = ET.SubElement(self.root, 'part')
            part_elem.set('id', part_id)
            part_elem.set('name', part_info['name'])
            
            # Descrição da parte
            desc_elem = ET.SubElement(part_elem, 'description')
            desc_elem.text = part_info['description']
            
            # Objetivos de aprendizado
            objectives = ET.SubElement(part_elem, 'learning_objectives')
            for i, objective in enumerate(part_info['learning_objectives'], 1):
                obj_elem = ET.SubElement(objectives, 'objective')
                obj_elem.set('id', f'obj_{i}')
                obj_elem.text = objective
            
            # Seções (serão preenchidas durante o processamento)
            sections = ET.SubElement(part_elem, 'sections')

    def classify_difficulty(self, content, filename):
        """Classifica dificuldade baseada no conteúdo"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        scores = {'basic': 0, 'intermediate': 0, 'advanced': 0}
        
        for level, keywords in self.difficulty_keywords.items():
            for keyword in keywords:
                scores[level] += content_lower.count(keyword)
                scores[level] += filename_lower.count(keyword) * 2  # Peso maior para nome do arquivo
        
        # Heurísticas adicionais
        if 'import plotly.express' in content and 'go.' not in content:
            scores['basic'] += 3
        elif 'plotly.graph_objects' in content and 'px.' not in content:
            scores['intermediate'] += 2
        elif 'px.' in content and 'go.' in content:
            scores['advanced'] += 2
            
        # Complexidade do código
        code_lines = len([line for line in content.split('\n') if line.strip().startswith(('fig', 'px.', 'go.'))])
        if code_lines > 10:
            scores['advanced'] += 2
        elif code_lines > 5:
            scores['intermediate'] += 1
        else:
            scores['basic'] += 1
            
        return max(scores, key=scores.get)

    def classify_topic_part(self, content, filename):
        """Classifica em qual parte pedagógica o conteúdo se encaixa"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        scores = defaultdict(int)
        
        for part_id, keywords in self.topic_mapping.items():
            for keyword in keywords:
                scores[part_id] += content_lower.count(keyword)
                scores[part_id] += filename_lower.count(keyword) * 2
        
        # Heurísticas específicas
        if any(word in filename_lower for word in ['basic', 'introduction', 'getting started']):
            scores['part_1_fundamentals'] += 5
        elif any(word in filename_lower for word in ['bar', 'line', 'scatter', 'pie']):
            scores['part_2_essential_charts'] += 5
        elif any(word in filename_lower for word in ['styling', 'color', 'layout', 'interactive']):
            scores['part_3_customization'] += 5
        elif any(word in filename_lower for word in ['performance', 'optimization', 'large']):
            scores['part_4_advanced'] += 5
        
        return max(scores, key=scores.get) if scores else 'part_2_essential_charts'

    def extract_express_vs_objects(self, content):
        """Extrai exemplos de Express vs Graph Objects para comparação lado a lado"""
        express_pattern = r'(import plotly\.express.*?(?=\n\n|\nimport|\Z))'
        objects_pattern = r'(import plotly\.graph_objects.*?(?=\n\n|\nimport|\Z))'
        
        express_examples = re.findall(express_pattern, content, re.DOTALL)
        objects_examples = re.findall(objects_pattern, content, re.DOTALL)
        
        return express_examples, objects_examples

    def extract_learning_concepts(self, content):
        """Extrai conceitos de aprendizado do conteúdo"""
        concepts = []
        
        # Procurar por padrões que indicam conceitos importantes
        concept_patterns = [
            r'(?:conceito|concept|importante|key|fundamental):\s*([^.!?]+)',
            r'(?:lembre-se|remember|note|importante):\s*([^.!?]+)',
            r'(?:dica|tip|hint):\s*([^.!?]+)'
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            concepts.extend(matches)
        
        return concepts[:3]  # Limitar a 3 conceitos por arquivo

    def create_exercise(self, content, chart_name):
        """Cria exercícios práticos baseados no conteúdo"""
        exercises = []
        
        # Templates de exercícios baseados no tipo de gráfico
        if 'bar' in chart_name.lower():
            exercises.append({
                'title': f'Exercício: Criar {chart_name} com seus dados',
                'description': 'Usando o exemplo acima, modifique o código para usar seus próprios dados',
                'difficulty': 'basic',
                'solution_hint': 'Substitua o dataset pelos seus dados e ajuste as colunas x e y'
            })
        
        return exercises

    def read_file_content(self, file_path, filename):
        """Lê conteúdo com processamento aprimorado"""
        try:
            if filename.lower().endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        page_text = page.extract_text()
                        if page_text.strip():
                            content += f"--- Página {page_num} ---\n{page_text}\n\n"
                    return content.strip()
            elif filename.lower().endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"Tipo de arquivo não suportado: {filename}"
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def process_file_advanced(self, file_path, filename):
        """Processa arquivo com análise pedagógica avançada"""
        content = self.read_file_content(file_path, filename)
        
        # Classificações
        difficulty = self.classify_difficulty(content, filename)
        topic_part = self.classify_topic_part(content, filename)
        
        # Extrações avançadas
        express_examples, objects_examples = self.extract_express_vs_objects(content)
        concepts = self.extract_learning_concepts(content)
        
        # Encontrar a parte correta
        part_elem = self.root.find(f".//part[@id='{topic_part}']")
        if part_elem is None:
            part_elem = self.root.find(".//part[@id='part_2_essential_charts']")  # Default
        
        sections = part_elem.find('sections')
        
        # Criar seção do gráfico
        chart_name = filename.replace('.pdf', '').replace('.txt', '').replace('.md', '').replace(' in Python', '').strip()
        
        section = ET.SubElement(sections, 'section')
        section.set('name', chart_name)
        section.set('difficulty', difficulty)
        section.set('source_file', filename)
        
        # Objetivos específicos da seção
        section_objectives = ET.SubElement(section, 'section_objectives')
        obj1 = ET.SubElement(section_objectives, 'objective')
        obj1.text = f'Dominar a criação de {chart_name}'
        obj2 = ET.SubElement(section_objectives, 'objective') 
        obj2.text = f'Aplicar customizações em {chart_name}'
        
        # Conceitos importantes
        if concepts:
            concepts_elem = ET.SubElement(section, 'key_concepts')
            for i, concept in enumerate(concepts, 1):
                concept_elem = ET.SubElement(concepts_elem, 'concept')
                concept_elem.set('id', f'concept_{i}')
                concept_elem.text = concept.strip()
        
        # Comparação lado a lado (se houver ambos)
        if express_examples and objects_examples:
            comparison = ET.SubElement(section, 'side_by_side_comparison')
            comparison.set('title', 'Express vs Graph Objects')
            
            express_elem = ET.SubElement(comparison, 'plotly_express')
            express_elem.set('approach', 'high_level')
            express_elem.text = express_examples[0][:500] + '...' if len(express_examples[0]) > 500 else express_examples[0]
            
            objects_elem = ET.SubElement(comparison, 'graph_objects')
            objects_elem.set('approach', 'low_level')
            objects_elem.text = objects_examples[0][:500] + '...' if len(objects_examples[0]) > 500 else objects_examples[0]
        
        # Exercícios práticos
        exercises = self.create_exercise(content, chart_name)
        if exercises:
            exercises_elem = ET.SubElement(section, 'practical_exercises')
            for i, exercise in enumerate(exercises, 1):
                exercise_elem = ET.SubElement(exercises_elem, 'exercise')
                exercise_elem.set('id', f'exercise_{i}')
                exercise_elem.set('difficulty', exercise['difficulty'])
                
                title_elem = ET.SubElement(exercise_elem, 'title')
                title_elem.text = exercise['title']
                
                desc_elem = ET.SubElement(exercise_elem, 'description')
                desc_elem.text = exercise['description']
                
                hint_elem = ET.SubElement(exercise_elem, 'solution_hint')
                hint_elem.text = exercise['solution_hint']
        
        # Conteúdo original (resumido)
        content_elem = ET.SubElement(section, 'full_content')
        content_elem.text = content[:1000] + '...' if len(content) > 1000 else content
        
        return chart_name, difficulty, topic_part

    def process_directory_advanced(self, directory_path, relative_path=""):
        """Processa diretório com análise pedagógica"""
        items = sorted(os.listdir(directory_path))
        processed_stats = defaultdict(int)
        
        for item in items:
            item_path = os.path.join(directory_path, item)
            current_relative_path = os.path.join(relative_path, item) if relative_path else item
            
            if os.path.isfile(item_path):
                chart_name, difficulty, topic_part = self.process_file_advanced(item_path, item)
                processed_stats[difficulty] += 1
                processed_stats[topic_part] += 1
                
                print(f'✅ {chart_name} → {topic_part} ({difficulty})')
                
            elif os.path.isdir(item_path):
                print(f'📁 Processando: {current_relative_path}')
                sub_stats = self.process_directory_advanced(item_path, current_relative_path)
                for key, value in sub_stats.items():
                    processed_stats[key] += value
        
        return processed_stats

    def create_glossary(self):
        """Cria glossário de termos técnicos"""
        glossary = ET.SubElement(self.root, 'glossary')
        glossary.set('title', 'Glossário de Termos Plotly')
        
        terms = {
            'Figure': 'Container principal que contém todos os elementos visuais',
            'Trace': 'Representação visual dos dados (barras, linhas, pontos)',
            'Layout': 'Configurações visuais da figura (eixos, títulos, cores)',
            'Plotly Express': 'Interface de alto nível para criação rápida de gráficos',
            'Graph Objects': 'Interface de baixo nível para controle detalhado',
            'Long-form data': 'Formato onde cada linha é uma observação',
            'Wide-form data': 'Formato onde colunas representam variáveis',
            'Callback': 'Função que conecta inputs e outputs em Dash'
        }
        
        for term, definition in terms.items():
            term_elem = ET.SubElement(glossary, 'term')
            term_elem.set('name', term)
            term_elem.text = definition

    def add_final_statistics(self, stats):
        """Adiciona estatísticas finais ao guia"""
        statistics = ET.SubElement(self.metadata, 'processing_statistics')
        
        # Stats por dificuldade
        difficulty_stats = ET.SubElement(statistics, 'difficulty_distribution')
        for level in ['basic', 'intermediate', 'advanced']:
            level_elem = ET.SubElement(difficulty_stats, 'level')
            level_elem.set('name', level)
            level_elem.set('count', str(stats.get(level, 0)))
        
        # Stats por parte
        part_stats = ET.SubElement(statistics, 'part_distribution')
        for part_id in self.structure.keys():
            part_elem = ET.SubElement(part_stats, 'part')
            part_elem.set('id', part_id)
            part_elem.set('count', str(stats.get(part_id, 0)))

    def save_advanced_guide(self, output_file):
        """Salva guia com formatação pedagógica"""
        # Adicionar glossário
        self.create_glossary()
        
        # Salvar com indentação
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f'\n🎓 GUIA PEDAGÓGICO AVANÇADO CRIADO: {output_file}')
        return output_file

def main():
    print("🎓 CRIANDO GUIA PLOTLY PEDAGÓGICO AVANÇADO")
    print("Baseado nas sugestões de estrutura de aprendizado")
    print("=" * 60)
    
    extractor = AdvancedSemanticPlotlyExtractor()
    
    input_folder = 'Input'
    output_file = 'advanced_pedagogical_plotly_guide.xml'
    
    # Processar com análise pedagógica
    stats = extractor.process_directory_advanced(input_folder)
    
    # Adicionar estatísticas
    extractor.add_final_statistics(stats)
    
    # Salvar guia
    extractor.save_advanced_guide(output_file)
    
    print("=" * 60)
    print("📊 ESTATÍSTICAS PEDAGÓGICAS:")
    print(f"  📈 Básico: {stats.get('basic', 0)} seções")
    print(f"  📊 Intermediário: {stats.get('intermediate', 0)} seções") 
    print(f"  🎯 Avançado: {stats.get('advanced', 0)} seções")
    print("\n🎯 DISTRIBUIÇÃO POR PARTE:")
    for part_id, part_info in extractor.structure.items():
        count = stats.get(part_id, 0)
        print(f"  {part_info['name']}: {count} seções")
    
    print(f"\n✨ Guia pedagógico estruturado criado com sucesso!")
    print(f"📚 Agora com progressão de aprendizado e exercícios práticos")

if __name__ == "__main__":
    main()
