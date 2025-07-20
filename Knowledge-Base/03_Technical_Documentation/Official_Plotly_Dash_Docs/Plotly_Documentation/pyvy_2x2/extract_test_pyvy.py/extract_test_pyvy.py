import os
import xml.etree.ElementTree as ET
from datetime import datetime
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 não está instalado. Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

def read_file_content(file_path, filename):
    """Lê o conteúdo de um arquivo baseado na sua extensão"""
    try:
        if filename.lower().endswith('.pdf'):
            # Ler arquivo PDF
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text.strip():  # Só adiciona se a página tem conteúdo
                        content += f"--- Página {page_num} ---\n{page_text}\n\n"
                return content.strip()
        elif filename.lower().endswith(('.txt', '.md')):
            # Ler arquivo de texto comum
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Tipo de arquivo não suportado: {filename}"
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def process_directory(directory_path, parent_element, relative_path=""):
    """Processa recursivamente um diretório e seus subdiretórios"""
    items = sorted(os.listdir(directory_path))
    
    for item in items:
        item_path = os.path.join(directory_path, item)
        current_relative_path = os.path.join(relative_path, item) if relative_path else item
        
        if os.path.isfile(item_path):
            # Processar arquivo
            content = read_file_content(item_path, item)
            
            # Criar elemento do arquivo
            file_elem = ET.SubElement(parent_element, 'file')
            file_elem.set('name', item)
            file_elem.set('path', current_relative_path.replace('\\', '/'))
            file_elem.set('type', item.split('.')[-1].lower() if '.' in item else 'unknown')
            
            content_elem = ET.SubElement(file_elem, 'content')
            content_elem.text = content
            
            print(f'Processado: {current_relative_path}')
            
        elif os.path.isdir(item_path):
            # Processar subdiretório
            category_elem = ET.SubElement(parent_element, 'category')
            category_elem.set('name', item)
            category_elem.set('path', current_relative_path.replace('\\', '/'))
            
            print(f'Processando pasta: {current_relative_path}')
            process_directory(item_path, category_elem, current_relative_path)

input_folder = 'Exec_Monica'
output_file = 'monica_webdev_guide.xml'

# Criar estrutura XML do guia Monica Web Dev
root = ET.Element('monica_webdev_guide')
root.set('generated_on', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
root.set('description', 'Guia completo de Ambiente de Programação e Ferramentas para Projetos Web - Monica AI')

# Adicionar metadados
metadata = ET.SubElement(root, 'metadata')
title_elem = ET.SubElement(metadata, 'title')
title_elem.text = 'Guia Completo Monica - Desenvolvimento Web'
description_elem = ET.SubElement(metadata, 'description')
description_elem.text = 'Documentação sobre Ambiente de Programação e Ferramentas para Projetos Web da Monica AI'

# Processar conteúdo
content_root = ET.SubElement(root, 'content')

print("Iniciando processamento recursivo dos arquivos...")
process_directory(input_folder, content_root)

# Salvar o arquivo XML com formatação adequada
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)  # Adiciona indentação para melhor legibilidade
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'\n� Guia Monica Web Dev criado com sucesso: {output_file}')
print(f'📊 Arquivo XML estruturado com documentação de desenvolvimento web')
print(f'🔍 Use este arquivo para navegar pela documentação da Monica AI')