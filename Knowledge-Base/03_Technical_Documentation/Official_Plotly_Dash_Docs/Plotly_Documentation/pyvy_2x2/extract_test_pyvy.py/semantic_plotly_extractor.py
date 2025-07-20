import os
import xml.etree.ElementTree as ET
from datetime import datetime
import re
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 não está instalado. Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

class SemanticPlotlyExtractor:
    def __init__(self):
        self.root = ET.Element('plotly_guide')
        self.root.set('generated_on', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.root.set('version', '2.0')
        self.root.set('description', 'Guia semântico estruturado de Plotly para Python')
        
        # Adicionar metadados
        self.metadata = ET.SubElement(self.root, 'metadata')
        title_elem = ET.SubElement(self.metadata, 'title')
        title_elem.text = 'Guia Semântico Plotly Python'
        description_elem = ET.SubElement(self.metadata, 'description')
        description_elem.text = 'Documentação estruturada semanticamente para visualização de dados com Plotly'
        
        # Seção para conteúdo comum reutilizável
        self.common_content = ET.SubElement(self.root, 'common_content')
        
        # Categorias principais baseadas nos tipos de gráficos
        self.categories = {
            'basic_charts': 'Gráficos Básicos',
            'statistical_charts': 'Gráficos Estatísticos', 
            'scientific_charts': 'Gráficos Científicos',
            'financial_charts': 'Gráficos Financeiros',
            'maps': 'Mapas e Visualizações Geográficas',
            'advanced_features': 'Recursos Avançados',
            'customization': 'Personalização e Estilo',
            'interactivity': 'Interatividade e Widgets'
        }
        
        self.category_elements = {}
        for cat_id, cat_name in self.categories.items():
            cat_elem = ET.SubElement(self.root, 'category')
            cat_elem.set('id', cat_id)
            cat_elem.set('name', cat_name)
            self.category_elements[cat_id] = cat_elem

    def extract_code_blocks(self, text):
        """Extrai blocos de código Python do texto"""
        code_patterns = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'import.*?(?=\n\n|\n[A-Z]|\nPlotly|\n#|\Z)',
            r'fig\s*=.*?(?=\n\n|\n[A-Z]|\nPlotly|\n#|\Z)',
            r'px\..*?(?=\n\n|\n[A-Z]|\nPlotly|\n#|\Z)',
            r'go\..*?(?=\n\n|\n[A-Z]|\nPlotly|\n#|\Z)'
        ]
        
        code_blocks = []
        for pattern in code_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
            for match in matches:
                clean_code = match.strip()
                if len(clean_code) > 20 and ('import' in clean_code or 'fig' in clean_code or 'px.' in clean_code or 'go.' in clean_code):
                    code_blocks.append(clean_code)
        
        return code_blocks

    def detect_library_type(self, code):
        """Detecta se o código usa plotly.express ou plotly.graph_objects"""
        if 'px.' in code or 'plotly.express' in code:
            return 'plotly.express'
        elif 'go.' in code or 'plotly.graph_objects' in code:
            return 'plotly.graph_objects'
        else:
            return 'mixed'

    def extract_descriptions(self, text):
        """Extrai descrições e explicações do texto"""
        # Remove URLs e elementos de navegação
        clean_text = re.sub(r'https?://[^\s]+', '', text)
        clean_text = re.sub(r'\([^)]*\)', '', clean_text)
        
        # Procura por parágrafos descritivos
        paragraphs = re.split(r'\n\s*\n', clean_text)
        descriptions = []
        
        for para in paragraphs:
            para = para.strip()
            # Filtra parágrafos que parecem ser descrições úteis
            if (len(para) > 50 and 
                not para.startswith('import') and 
                not para.startswith('fig') and
                'plotly' in para.lower() and
                not para.startswith('>')):
                descriptions.append(para)
        
        return descriptions

    def categorize_chart_type(self, filename, content):
        """Categoriza o tipo de gráfico baseado no nome do arquivo e conteúdo"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Mapeamento de palavras-chave para categorias
        category_mapping = {
            'basic_charts': ['bar chart', 'line chart', 'scatter plot', 'pie chart', 'basic chart'],
            'statistical_charts': ['histogram', 'box plot', 'violin plot', 'distribution', 'error bar'],
            'scientific_charts': ['heatmap', 'contour', 'surface', '3d', 'scientific'],
            'financial_charts': ['candlestick', 'ohlc', 'financial', 'stock'],
            'maps': ['map', 'choropleth', 'geographic', 'mapbox', 'geo'],
            'advanced_features': ['animation', 'widget', 'subplot', 'facet'],
            'customization': ['styling', 'color', 'theme', 'layout', 'annotation'],
            'interactivity': ['dropdown', 'slider', 'button', 'crossfilter']
        }
        
        for category, keywords in category_mapping.items():
            for keyword in keywords:
                if keyword in filename_lower or keyword in content_lower:
                    return category
        
        return 'basic_charts'  # Categoria padrão

    def create_chart_element(self, category_id, chart_name, source_file, content):
        """Cria um elemento de gráfico estruturado semanticamente"""
        category_elem = self.category_elements[category_id]
        chart_elem = ET.SubElement(category_elem, 'chart')
        chart_elem.set('name', chart_name)
        chart_elem.set('source_file', source_file)
        
        # Extrair e adicionar descrição principal
        descriptions = self.extract_descriptions(content)
        if descriptions:
            desc_elem = ET.SubElement(chart_elem, 'description')
            desc_elem.text = descriptions[0][:500] + '...' if len(descriptions[0]) > 500 else descriptions[0]
        
        # Extrair e estruturar exemplos de código
        code_blocks = self.extract_code_blocks(content)
        if code_blocks:
            examples_elem = ET.SubElement(chart_elem, 'examples')
            
            for i, code in enumerate(code_blocks[:5]):  # Limita a 5 exemplos por gráfico
                example_elem = ET.SubElement(examples_elem, 'example')
                example_elem.set('id', f'example_{i+1}')
                
                # Tentar extrair título do contexto
                title = f"Exemplo {i+1}"
                if 'express' in code.lower():
                    title += " (Plotly Express)"
                elif 'graph_objects' in code.lower():
                    title += " (Graph Objects)"
                
                example_elem.set('title', title)
                
                # Detectar biblioteca
                library_elem = ET.SubElement(example_elem, 'library')
                library_elem.text = self.detect_library_type(code)
                
                # Adicionar código
                code_elem = ET.SubElement(example_elem, 'code')
                code_elem.set('language', 'python')
                code_elem.text = code
        
        # Adicionar seção de personalização se houver conteúdo relevante
        customization_keywords = ['color', 'style', 'layout', 'axis', 'legend', 'title']
        for desc in descriptions[1:3]:  # Verifica as próximas descrições
            if any(keyword in desc.lower() for keyword in customization_keywords):
                custom_elem = ET.SubElement(chart_elem, 'customization')
                custom_elem.set('section', 'Opções de Estilo')
                custom_desc = ET.SubElement(custom_elem, 'description')
                custom_desc.text = desc
                break
        
        return chart_elem

    def read_file_content(self, file_path, filename):
        """Lê o conteúdo de um arquivo baseado na sua extensão"""
        try:
            if filename.lower().endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text.strip():
                            content += page_text + "\n"
                    return content.strip()
            elif filename.lower().endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"Tipo de arquivo não suportado: {filename}"
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def process_directory(self, directory_path, relative_path=""):
        """Processa recursivamente um diretório"""
        items = sorted(os.listdir(directory_path))
        processed_count = 0
        
        for item in items:
            item_path = os.path.join(directory_path, item)
            current_relative_path = os.path.join(relative_path, item) if relative_path else item
            
            if os.path.isfile(item_path):
                content = self.read_file_content(item_path, item)
                
                # Extrair nome do gráfico do filename
                chart_name = item.replace('.pdf', '').replace('.txt', '').replace('.md', '')
                chart_name = chart_name.replace(' in Python', '').strip()
                
                # Categorizar o tipo de gráfico
                category_id = self.categorize_chart_type(item, content)
                
                # Criar elemento estruturado
                self.create_chart_element(category_id, chart_name, current_relative_path.replace('\\', '/'), content)
                
                processed_count += 1
                print(f'✅ Processado: {chart_name} → {self.categories[category_id]}')
                
            elif os.path.isdir(item_path):
                print(f'📁 Processando pasta: {current_relative_path}')
                processed_count += self.process_directory(item_path, current_relative_path)
        
        return processed_count

    def save_guide(self, output_file):
        """Salva o guia estruturado em XML"""
        # Adicionar conteúdo comum reutilizável
        dash_info = ET.SubElement(self.common_content, 'reusable_content')
        dash_info.set('id', 'about_dash')
        dash_info.set('title', 'Sobre o Dash')
        dash_info.text = "Dash é a estrutura original de baixo código para criar rapidamente aplicativos de dados em Python..."
        
        # Adicionar estatísticas
        stats = ET.SubElement(self.metadata, 'statistics')
        total_charts = sum(len(cat.findall('chart')) for cat in self.category_elements.values())
        stats.set('total_charts', str(total_charts))
        stats.set('categories', str(len([cat for cat in self.category_elements.values() if len(cat.findall('chart')) > 0])))
        
        # Salvar com formatação
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f'\n🎉 Guia semântico criado: {output_file}')
        print(f'📊 Total de gráficos: {total_charts}')
        print(f'📁 Categorias ativas: {len([cat for cat in self.category_elements.values() if len(cat.findall("chart")) > 0])}')

def main():
    extractor = SemanticPlotlyExtractor()
    
    input_folder = 'Input'
    output_file = 'semantic_plotly_guide.xml'
    
    print("🚀 Iniciando extração semântica de conteúdo Plotly...")
    print("=" * 60)
    
    total_processed = extractor.process_directory(input_folder)
    extractor.save_guide(output_file)
    
    print("=" * 60)
    print(f"✨ Processamento concluído! {total_processed} arquivos processados")

if __name__ == "__main__":
    main()
