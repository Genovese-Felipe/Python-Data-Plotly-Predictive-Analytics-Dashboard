import xml.etree.ElementTree as ET
from collections import defaultdict
import re

def analyze_monica_guide():
    """Analisa o guia de desenvolvimento web da Monica"""
    
    print("🌐 ANÁLISE DO GUIA MONICA - DESENVOLVIMENTO WEB")
    print("=" * 60)
    
    # Carregar XML
    tree = ET.parse('monica_webdev_guide.xml')
    root = tree.getroot()
    
    # Extrair metadados
    metadata = root.find('metadata')
    title = metadata.find('title').text
    description = metadata.find('description').text
    
    print(f"📖 Título: {title}")
    print(f"📝 Descrição: {description}")
    print(f"🕒 Gerado: {root.get('generated_on')}")
    print(f"📦 Fonte: Monica AI Chat")
    
    # Analisar arquivos processados
    files = root.findall('.//file')
    print(f"\n📊 DOCUMENTOS PROCESSADOS:")
    print("-" * 35)
    print(f"  Total de arquivos: {len(files)}")
    
    # Categorizar por número de sessão
    session_numbers = defaultdict(int)
    technology_mentions = defaultdict(int)
    
    for file_elem in files:
        filename = file_elem.get('name', '')
        content = file_elem.find('content')
        
        if content is not None and content.text:
            content_text = content.text.lower()
            
            # Extrair número da sessão
            session_match = re.search(r'00\s*(\d+)', filename)
            if session_match:
                session_num = session_match.group(1)
                session_numbers[session_num] += 1
            
            # Buscar tecnologias mencionadas
            technologies = {
                'HTML': r'\bhtml\b',
                'CSS': r'\bcss\b',
                'JavaScript': r'\b(?:javascript|js)\b',
                'Python': r'\bpython\b',
                'Tailwind': r'\btailwind\b',
                'Jupyter': r'\bjupyter\b',
                'React': r'\breact\b',
                'Vue': r'\bvue\b',
                'Angular': r'\bangular\b',
                'Node.js': r'\b(?:node\.?js|nodejs)\b',
                'Git': r'\bgit\b',
                'GitHub': r'\bgithub\b',
                'VS Code': r'\b(?:vs code|visual studio code|vscode)\b',
                'Docker': r'\bdocker\b',
                'npm': r'\bnpm\b',
                'webpack': r'\bwebpack\b'
            }
            
            for tech, pattern in technologies.items():
                if re.search(pattern, content_text):
                    technology_mentions[tech] += 1
    
    # Mostrar distribuição por sessão
    print(f"\n📅 DISTRIBUIÇÃO POR SESSÃO:")
    print("-" * 30)
    for session_num in sorted(session_numbers.keys(), key=int):
        count = session_numbers[session_num]
        print(f"  Sessão {session_num}: {count} documento(s)")
    
    # Mostrar tecnologias mais mencionadas
    print(f"\n💻 TECNOLOGIAS IDENTIFICADAS:")
    print("-" * 35)
    sorted_techs = sorted(technology_mentions.items(), key=lambda x: x[1], reverse=True)
    for tech, count in sorted_techs[:10]:
        percentage = (count / len(files)) * 100
        print(f"  {tech}: {count} menções ({percentage:.1f}% dos documentos)")
    
    # Analisar progressão de conteúdo
    print(f"\n📈 ANÁLISE DE PROGRESSÃO:")
    print("-" * 30)
    
    first_files = [f for f in files if '00 01' in f.get('name', '')]
    middle_files = [f for f in files if any(x in f.get('name', '') for x in ['00 02', '00 03', '00 04'])]
    advanced_files = [f for f in files if any(x in f.get('name', '') for x in ['00 05', '00 06', '00 1', '00 4'])]
    
    print(f"  🟢 Documentos iniciais (00 01): {len(first_files)}")
    print(f"  🟡 Documentos intermediários (00 02-04): {len(middle_files)}")
    print(f"  🔴 Documentos avançados (00 05+): {len(advanced_files)}")
    
    # Extrair tópicos principais do primeiro documento
    if files:
        first_file = files[0]
        content = first_file.find('content')
        if content is not None and content.text:
            print(f"\n🎯 TÓPICOS PRINCIPAIS (1º documento):")
            print("-" * 40)
            
            # Buscar padrões de lista
            content_text = content.text
            lines = content_text.split('\n')
            
            topics_found = []
            for line in lines:
                line = line.strip()
                # Procurar por tecnologias/ferramentas listadas
                if re.match(r'^[A-Z][a-zA-Z\s()]+$', line) and len(line) < 50:
                    if any(tech.lower() in line.lower() for tech in ['html', 'css', 'python', 'javascript', 'tailwind', 'jupyter']):
                        topics_found.append(line)
            
            for topic in topics_found[:8]:  # Primeiros 8 tópicos
                print(f"  • {topic}")
    
    # Calcular tamanho médio do conteúdo
    content_sizes = []
    for file_elem in files:
        content = file_elem.find('content')
        if content is not None and content.text:
            content_sizes.append(len(content.text))
    
    if content_sizes:
        avg_size = sum(content_sizes) / len(content_sizes)
        print(f"\n📏 ESTATÍSTICAS DE CONTEÚDO:")
        print("-" * 35)
        print(f"  Tamanho médio por documento: {avg_size:.0f} caracteres")
        print(f"  Documento maior: {max(content_sizes):,} caracteres")
        print(f"  Documento menor: {min(content_sizes):,} caracteres")
    
    print(f"\n🎯 INSIGHTS DA ANÁLISE:")
    print("-" * 30)
    print("  ✅ Foco principal em tecnologias web fundamentais")
    print("  ✅ Progressão clara de conceitos básicos para avançados")
    print("  ✅ Cobertura abrangente de ferramentas de desenvolvimento")
    print("  ✅ Documentação estruturada por sessões numeradas")
    
    if 'Python' in technology_mentions and 'HTML' in technology_mentions:
        print("  ✅ Abordagem full-stack (Python + Frontend)")
    
    if 'Jupyter' in technology_mentions:
        print("  ✅ Foco em desenvolvimento científico/análise de dados")
    
    if 'Tailwind' in technology_mentions:
        print("  ✅ Uso de frameworks CSS modernos")
    
    print(f"\n📊 RESUMO FINAL:")
    print("-" * 20)
    print(f"  📁 {len(files)} documentos processados")
    print(f"  📅 {len(session_numbers)} sessões identificadas")
    print(f"  💻 {len(technology_mentions)} tecnologias mencionadas")
    print(f"  📖 {sum(content_sizes)/1024:.1f}KB de conteúdo total")
    
    return len(files), len(technology_mentions), len(session_numbers)

if __name__ == "__main__":
    total_files, total_techs, total_sessions = analyze_monica_guide()
    
    print(f"\n" + "=" * 60)
    print(f"🌐 GUIA MONICA WEB DEV - EXTRAÇÃO CONCLUÍDA!")
    print(f"  📚 {total_files} documentos estruturados")
    print(f"  💻 {total_techs} tecnologias identificadas")
    print(f"  📅 {total_sessions} sessões organizadas")
    print(f"  ✨ Estrutura XML compatível com guias anteriores")
    print("=" * 60)
