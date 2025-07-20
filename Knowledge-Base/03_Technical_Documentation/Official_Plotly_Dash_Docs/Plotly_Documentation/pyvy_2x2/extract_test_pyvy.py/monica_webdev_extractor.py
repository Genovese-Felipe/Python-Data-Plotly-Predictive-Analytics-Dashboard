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

class MonicaWebDevExtractor:
    def __init__(self):
        self.root = ET.Element('monica_webdev_guide')
        self.root.set('generated_on', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.root.set('version', '3.0')
        self.root.set('description', 'Guia completo de Ambiente de Programação e Ferramentas para Projetos Web - Monica AI')
        
        # Metadados específicos para desenvolvimento web
        self.metadata = ET.SubElement(self.root, 'metadata')
        self._create_metadata()
        
        # Estrutura pedagógica específica para desenvolvimento web
        self.structure = {
            'fundamentals': {
                'name': 'Fundamentos de Programação Web',
                'description': 'Base conceitual e ambiente de desenvolvimento',
                'learning_objectives': [
                    'Configurar ambiente de desenvolvimento web',
                    'Compreender ferramentas essenciais',
                    'Dominar conceitos fundamentais'
                ]
            },
            'tools_setup': {
                'name': 'Configuração de Ferramentas',
                'description': 'Setup e configuração de ferramentas de desenvolvimento',
                'learning_objectives': [
                    'Instalar e configurar IDEs',
                    'Configurar controle de versão',
                    'Setup de ambiente local'
                ]
            },
            'development_practices': {
                'name': 'Práticas de Desenvolvimento',
                'description': 'Metodologias e boas práticas',
                'learning_objectives': [
                    'Aplicar metodologias ágeis',
                    'Implementar boas práticas de código',
                    'Usar ferramentas de colaboração'
                ]
            },
            'advanced_topics': {
                'name': 'Tópicos Avançados',
                'description': 'Conceitos avançados e especialização',
                'learning_objectives': [
                    'Otimizar performance',
                    'Implementar CI/CD',
                    'Dominar frameworks avançados'
                ]
            }
        }
        
        self._create_structure()
        
        # Palavras-chave para classificação
        self.topic_keywords = {
            'fundamentals': ['introdução', 'básico', 'conceito', 'fundamental', 'início', 'primeiro'],
            'tools_setup': ['instalar', 'configurar', 'setup', 'ambiente', 'ferramentas', 'ide'],
            'development_practices': ['prática', 'metodologia', 'processo', 'workflow', 'colaboração'],
            'advanced_topics': ['avançado', 'otimização', 'performance', 'deploy', 'produção']
        }
        
        self.difficulty_keywords = {
            'beginner': ['básico', 'introdução', 'primeiro', 'inicial', 'simples'],
            'intermediate': ['intermediário', 'prática', 'aplicação', 'desenvolvimento'],
            'advanced': ['avançado', 'complexo', 'otimização', 'enterprise', 'produção']
        }

    def _create_metadata(self):
        """Cria metadados específicos para desenvolvimento web"""
        title = ET.SubElement(self.metadata, 'title')
        title.text = 'Guia Completo: Ambiente de Programação e Ferramentas Web - Monica AI'
        
        description = ET.SubElement(self.metadata, 'description')
        description.text = 'Documentação completa sobre ambiente de programação e ferramentas para projetos web'
        
        source = ET.SubElement(self.metadata, 'source')
        source.text = 'Monica AI Chat - Sessões de Desenvolvimento Web'
        
        pedagogy = ET.SubElement(self.metadata, 'pedagogical_approach')
        pedagogy.text = 'Fundamentos → Ferramentas → Práticas → Avançado'
        
        # Características educacionais
        features = ET.SubElement(self.metadata, 'educational_features')
        features.set('structured_learning', 'true')
        features.set('practical_examples', 'true')
        features.set('step_by_step_guides', 'true')
        features.set('tool_recommendations', 'true')

    def _create_structure(self):
        """Cria estrutura XML para desenvolvimento web"""
        for section_id, section_info in self.structure.items():
            section_elem = ET.SubElement(self.root, 'section')
            section_elem.set('id', section_id)
            section_elem.set('name', section_info['name'])
            
            # Descrição da seção
            desc_elem = ET.SubElement(section_elem, 'description')
            desc_elem.text = section_info['description']
            
            # Objetivos de aprendizado
            objectives = ET.SubElement(section_elem, 'learning_objectives')
            for i, objective in enumerate(section_info['learning_objectives'], 1):
                obj_elem = ET.SubElement(objectives, 'objective')
                obj_elem.set('id', f'obj_{i}')
                obj_elem.text = objective
            
            # Documentos (serão preenchidos durante o processamento)
            documents = ET.SubElement(section_elem, 'documents')

    def classify_document_topic(self, filename, content):
        """Classifica o tópico do documento baseado no nome e conteúdo"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        scores = defaultdict(int)
        
        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                scores[topic] += filename_lower.count(keyword) * 2
                scores[topic] += content_lower.count(keyword)
        
        # Heurística baseada na numeração dos arquivos
        if re.search(r'00\s*0[01]', filename):
            scores['fundamentals'] += 5
        elif re.search(r'00\s*0[23]', filename):
            scores['tools_setup'] += 5
        elif re.search(r'00\s*[04-9]', filename):
            scores['development_practices'] += 5
        elif re.search(r'00\s*[1-9][0-9]', filename):
            scores['advanced_topics'] += 5
        
        return max(scores, key=scores.get) if scores else 'fundamentals'

    def classify_difficulty(self, content, filename):
        """Classifica dificuldade do documento"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        scores = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
        
        for level, keywords in self.difficulty_keywords.items():
            for keyword in keywords:
                scores[level] += content_lower.count(keyword)
                scores[level] += filename_lower.count(keyword) * 2
        
        # Heurística baseada no número do arquivo
        if re.search(r'00\s*0[01]', filename):
            scores['beginner'] += 3
        elif re.search(r'00\s*[02-05]', filename):
            scores['intermediate'] += 2
        else:
            scores['advanced'] += 1
            
        return max(scores, key=scores.get)

    def extract_web_concepts(self, content):
        """Extrai conceitos específicos de desenvolvimento web"""
        concepts = []
        
        # Padrões para conceitos de desenvolvimento web
        concept_patterns = [
            r'(?:HTML|CSS|JavaScript|React|Vue|Angular|Node\.js|Express)',
            r'(?:IDE|Visual Studio Code|WebStorm|Sublime)',
            r'(?:Git|GitHub|GitLab|Bitbucket)',
            r'(?:npm|yarn|webpack|gulp|grunt)',
            r'(?:API|REST|GraphQL|AJAX)',
            r'(?:framework|biblioteca|library)',
            r'(?:deployment|deploy|produção|staging)'
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            concepts.extend(matches)
        
        # Remover duplicatas e limitar
        unique_concepts = list(set(concepts))
        return unique_concepts[:5]

    def extract_tools_mentioned(self, content):
        """Extrai ferramentas mencionadas no documento"""
        tools = []
        
        tool_patterns = [
            r'(Visual Studio Code|VS Code|WebStorm|Sublime Text)',
            r'(Git|GitHub|GitLab|Bitbucket|SourceTree)',
            r'(npm|yarn|pnpm)',
            r'(webpack|vite|parcel|rollup)',
            r'(Chrome DevTools|Firefox DevTools)',
            r'(Postman|Insomnia|curl)',
            r'(Docker|Kubernetes|Jenkins)'
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            tools.extend(matches)
        
        return list(set(tools))[:3]

    def read_file_content(self, file_path, filename):
        """Lê conteúdo do PDF"""
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
            else:
                return f"Tipo de arquivo não suportado: {filename}"
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def process_monica_document(self, file_path, filename):
        """Processa documento da Monica com análise específica"""
        content = self.read_file_content(file_path, filename)
        
        # Classificações
        topic = self.classify_document_topic(filename, content)
        difficulty = self.classify_difficulty(content, filename)
        
        # Extrações específicas
        web_concepts = self.extract_web_concepts(content)
        tools_mentioned = self.extract_tools_mentioned(content)
        
        # Encontrar seção correta
        section_elem = self.root.find(f".//section[@id='{topic}']")
        if section_elem is None:
            section_elem = self.root.find(".//section[@id='fundamentals']")  # Default
        
        documents = section_elem.find('documents')
        
        # Criar documento
        doc_name = filename.replace('.pdf', '').strip()
        
        document = ET.SubElement(documents, 'document')
        document.set('name', doc_name)
        document.set('difficulty', difficulty)
        document.set('source_file', filename)
        
        # Extrair número da sessão se existir
        session_match = re.search(r'00\s*(\d+)', filename)
        if session_match:
            document.set('session_number', session_match.group(1))
        
        # Resumo do documento
        summary = ET.SubElement(document, 'summary')
        summary.text = content[:300] + '...' if len(content) > 300 else content
        
        # Conceitos web identificados
        if web_concepts:
            concepts_elem = ET.SubElement(document, 'web_concepts')
            for concept in web_concepts:
                concept_elem = ET.SubElement(concepts_elem, 'concept')
                concept_elem.text = concept
        
        # Ferramentas mencionadas
        if tools_mentioned:
            tools_elem = ET.SubElement(document, 'tools_mentioned')
            for tool in tools_mentioned:
                tool_elem = ET.SubElement(tools_elem, 'tool')
                tool_elem.text = tool
        
        # Conteúdo completo (resumido)
        full_content = ET.SubElement(document, 'full_content')
        full_content.text = content[:1500] + '...' if len(content) > 1500 else content
        
        return doc_name, difficulty, topic

    def process_monica_directory(self, directory_path):
        """Processa diretório da Monica"""
        files = sorted(os.listdir(directory_path))
        processed_stats = defaultdict(int)
        
        for filename in files:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                doc_name, difficulty, topic = self.process_monica_document(file_path, filename)
                
                processed_stats[difficulty] += 1
                processed_stats[topic] += 1
                
                print(f'✅ {doc_name} → {topic} ({difficulty})')
        
        return processed_stats

    def create_web_glossary(self):
        """Cria glossário específico para desenvolvimento web"""
        glossary = ET.SubElement(self.root, 'glossary')
        glossary.set('title', 'Glossário de Desenvolvimento Web')
        
        terms = {
            'IDE': 'Integrated Development Environment - Ambiente integrado de desenvolvimento',
            'Framework': 'Estrutura de software que facilita o desenvolvimento de aplicações',
            'API': 'Application Programming Interface - Interface para comunicação entre sistemas',
            'Git': 'Sistema de controle de versão distribuído',
            'npm': 'Node Package Manager - Gerenciador de pacotes do Node.js',
            'webpack': 'Bundler de módulos para aplicações JavaScript',
            'Deploy': 'Processo de disponibilizar aplicação em ambiente de produção',
            'DevTools': 'Ferramentas de desenvolvimento integradas aos navegadores',
            'CI/CD': 'Continuous Integration/Continuous Deployment - Integração e entrega contínuas',
            'Frontend': 'Parte da aplicação que interage diretamente com o usuário',
            'Backend': 'Parte da aplicação que processa dados no servidor',
            'Full Stack': 'Desenvolvimento que abrange frontend e backend'
        }
        
        for term, definition in terms.items():
            term_elem = ET.SubElement(glossary, 'term')
            term_elem.set('name', term)
            term_elem.text = definition

    def add_final_statistics(self, stats):
        """Adiciona estatísticas finais"""
        statistics = ET.SubElement(self.metadata, 'processing_statistics')
        
        # Stats por dificuldade
        difficulty_stats = ET.SubElement(statistics, 'difficulty_distribution')
        for level in ['beginner', 'intermediate', 'advanced']:
            level_elem = ET.SubElement(difficulty_stats, 'level')
            level_elem.set('name', level)
            level_elem.set('count', str(stats.get(level, 0)))
        
        # Stats por tópico
        topic_stats = ET.SubElement(statistics, 'topic_distribution')
        for topic_id in self.structure.keys():
            topic_elem = ET.SubElement(topic_stats, 'topic')
            topic_elem.set('id', topic_id)
            topic_elem.set('count', str(stats.get(topic_id, 0)))

    def save_monica_guide(self, output_file):
        """Salva guia da Monica"""
        self.create_web_glossary()
        
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f'\n🚀 GUIA MONICA WEB DEV CRIADO: {output_file}')
        return output_file

def main():
    print("🌐 CRIANDO GUIA MONICA - DESENVOLVIMENTO WEB")
    print("Ambiente de Programação e Ferramentas para Projetos Web")
    print("=" * 60)
    
    extractor = MonicaWebDevExtractor()
    
    input_folder = 'Exec_Monica'
    output_file = 'monica_webdev_guide.xml'
    
    # Processar documentos da Monica
    stats = extractor.process_monica_directory(input_folder)
    
    # Adicionar estatísticas
    extractor.add_final_statistics(stats)
    
    # Salvar guia
    extractor.save_monica_guide(output_file)
    
    print("=" * 60)
    print("📊 ESTATÍSTICAS:")
    print(f"  🟢 Iniciante: {stats.get('beginner', 0)} documentos")
    print(f"  🟡 Intermediário: {stats.get('intermediate', 0)} documentos") 
    print(f"  🔴 Avançado: {stats.get('advanced', 0)} documentos")
    print("\n🎯 DISTRIBUIÇÃO POR TÓPICO:")
    for topic_id, topic_info in extractor.structure.items():
        count = stats.get(topic_id, 0)
        print(f"  {topic_info['name']}: {count} documentos")
    
    print(f"\n✨ Guia Monica Web Dev estruturado criado!")

if __name__ == "__main__":
    main()
