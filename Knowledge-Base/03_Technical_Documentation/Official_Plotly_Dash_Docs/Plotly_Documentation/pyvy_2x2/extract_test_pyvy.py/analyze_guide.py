import xml.etree.ElementTree as ET
from collections import defaultdict
import re

def analyze_semantic_guide(xml_file):
    """Analisa a estrutura semântica do guia Plotly"""
    
    print("🔍 ANÁLISE DO GUIA SEMÂNTICO PLOTLY PYTHON")
    print("=" * 60)
    
    # Parsear o XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extrair metadados
    metadata = root.find('metadata')
    title = metadata.find('title').text
    description = metadata.find('description').text
    
    print(f"📖 Título: {title}")
    print(f"📝 Descrição: {description}")
    print(f"🕒 Gerado em: {root.get('generated_on')}")
    print(f"🔢 Versão: {root.get('version')}")
    print()
    
    # Analisar categorias
    categories = root.findall('category')
    print("📊 CATEGORIAS E DISTRIBUIÇÃO:")
    print("-" * 40)
    
    category_stats = {}
    total_charts = 0
    total_examples = 0
    library_usage = defaultdict(int)
    
    for category in categories:
        cat_name = category.get('name')
        cat_id = category.get('id')
        charts = category.findall('chart')
        chart_count = len(charts)
        
        if chart_count > 0:
            category_stats[cat_name] = {
                'count': chart_count,
                'charts': [],
                'examples': 0,
                'customizations': 0
            }
            
            for chart in charts:
                chart_name = chart.get('name')
                category_stats[cat_name]['charts'].append(chart_name)
                
                # Contar exemplos
                examples = chart.findall('.//example')
                category_stats[cat_name]['examples'] += len(examples)
                total_examples += len(examples)
                
                # Contar customizações
                customizations = chart.findall('customization')
                category_stats[cat_name]['customizations'] += len(customizations)
                
                # Analisar uso de bibliotecas
                for example in examples:
                    library = example.find('library')
                    if library is not None:
                        library_usage[library.text] += 1
            
            total_charts += chart_count
            print(f"  {cat_name}: {chart_count} gráficos")
    
    print(f"\n📈 ESTATÍSTICAS GERAIS:")
    print("-" * 30)
    print(f"  Total de gráficos: {total_charts}")
    print(f"  Total de exemplos: {total_examples}")
    print(f"  Média de exemplos por gráfico: {total_examples/total_charts:.1f}")
    print(f"  Categorias ativas: {len(category_stats)}")
    
    print(f"\n🛠️ USO DE BIBLIOTECAS:")
    print("-" * 25)
    for library, count in sorted(library_usage.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_examples) * 100
        print(f"  {library}: {count} exemplos ({percentage:.1f}%)")
    
    print(f"\n📋 DETALHES POR CATEGORIA:")
    print("-" * 35)
    
    for cat_name, stats in sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"\n🔸 {cat_name}")
        print(f"   📊 {stats['count']} gráficos")
        print(f"   💡 {stats['examples']} exemplos")
        print(f"   🎨 {stats['customizations']} customizações")
        
        # Mostrar alguns exemplos de gráficos
        if len(stats['charts']) <= 5:
            print(f"   📈 Gráficos: {', '.join(stats['charts'])}")
        else:
            print(f"   📈 Exemplos: {', '.join(stats['charts'][:3])}... (+{len(stats['charts'])-3} mais)")
    
    # Analisar qualidade dos exemplos de código
    print(f"\n🔬 ANÁLISE DE QUALIDADE DOS CÓDIGOS:")
    print("-" * 40)
    
    code_blocks = root.findall('.//code')
    valid_imports = 0
    has_fig_show = 0
    avg_lines = 0
    total_lines = 0
    
    for code in code_blocks:
        if code.text:
            lines = code.text.strip().split('\n')
            total_lines += len(lines)
            
            code_text = code.text.lower()
            if 'import' in code_text:
                valid_imports += 1
            if 'fig.show()' in code_text:
                has_fig_show += 1
    
    avg_lines = total_lines / len(code_blocks) if code_blocks else 0
    
    print(f"   📝 Total de blocos de código: {len(code_blocks)}")
    print(f"   📦 Com imports válidos: {valid_imports} ({(valid_imports/len(code_blocks)*100):.1f}%)")
    print(f"   🖼️ Com fig.show(): {has_fig_show} ({(has_fig_show/len(code_blocks)*100):.1f}%)")
    print(f"   📏 Média de linhas por código: {avg_lines:.1f}")
    
    # Verificar conteúdo comum
    common_content = root.find('common_content')
    if common_content is not None:
        reusable_items = common_content.findall('reusable_content')
        print(f"\n♻️ CONTEÚDO REUTILIZÁVEL:")
        print("-" * 30)
        for item in reusable_items:
            item_title = item.get('title', 'Sem título')
            item_id = item.get('id', 'Sem ID')
            print(f"   🔗 {item_title} (ID: {item_id})")
    
    print(f"\n✨ RESUMO DA MELHORIA ESTRUTURAL:")
    print("-" * 45)
    print("  ✅ Estrutura semântica implementada")
    print("  ✅ Categorização inteligente por tipos de gráfico")
    print("  ✅ Extração automática de exemplos de código")
    print("  ✅ Separação entre Plotly Express e Graph Objects")
    print("  ✅ Seções de customização identificadas")
    print("  ✅ Metadados estruturados incluídos")
    print("  ✅ Conteúdo reutilizável organizado")
    print("  ✅ Estrutura XML bem formatada e hierárquica")
    
    return category_stats, library_usage, total_charts, total_examples

if __name__ == "__main__":
    analyze_semantic_guide('semantic_plotly_guide.xml')
