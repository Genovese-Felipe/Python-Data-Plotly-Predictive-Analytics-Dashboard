"""
Monica AI-style Interface for Comprehensive Knowledge Processing
Integrates local Knowledge-Base with web search for comprehensive AI assistance
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add the current directory to the Python path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from core.orchestrator import KnowledgeExtractionOrchestrator
from core.multi_query_handler import MultiQueryHandler
from processors.web_search_processor import WebSearchProcessor

class MonicaAIInterface:
    """
    Monica AI-style comprehensive interface for knowledge processing
    Combines local knowledge extraction with web search and multi-query processing
    """
    
    def __init__(self):
        self.orchestrator = KnowledgeExtractionOrchestrator()
        self.web_processor = WebSearchProcessor()
        self.multi_query_handler = None
        self.session_data = {
            'start_time': time.time(),
            'queries_processed': 0,
            'knowledge_base_loaded': False,
            'session_id': f"monica_ai_{int(time.time())}"
        }
        
        print("🤖 Monica AI Interface Initialized")
        print("Comprehensive AI knowledge processing with web integration")
        
    def run_comprehensive_analysis(self, custom_queries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run comprehensive AI knowledge analysis
        
        Args:
            custom_queries: Optional custom queries to process
            
        Returns:
            Comprehensive analysis results
        """
        print("\n" + "="*80)
        print("🚀 MONICA AI - COMPREHENSIVE KNOWLEDGE ANALYSIS")
        print("="*80)
        
        start_time = time.time()
        
        # Step 1: Extract and process local knowledge base
        print("\n📚 Step 1: Processing Local Knowledge Base...")
        knowledge_summary = self._process_local_knowledge()
        
        # Step 2: Initialize multi-query handler with knowledge base
        print("\n🔧 Step 2: Initializing Multi-Query Handler...")
        self._initialize_query_handler(knowledge_summary)
        
        # Step 3: Generate AI-focused queries
        print("\n🎯 Step 3: Generating AI-Focused Queries...")
        ai_queries = self._generate_ai_queries(custom_queries)
        
        # Step 4: Process multiple queries with web integration
        print("\n🌐 Step 4: Processing Queries with Web Integration...")
        query_results = self.multi_query_handler.process_multiple_queries(ai_queries, include_web_search=True)
        
        # Step 5: Generate comprehensive insights
        print("\n💡 Step 5: Generating Comprehensive Insights...")
        comprehensive_insights = self._generate_comprehensive_insights(knowledge_summary, query_results)
        
        # Step 6: Create actionable recommendations
        print("\n📋 Step 6: Creating Actionable Recommendations...")
        recommendations = self._create_recommendations(comprehensive_insights)
        
        total_time = time.time() - start_time
        
        # Compile final results
        final_results = {
            'monica_ai_analysis': {
                'session_info': {
                    'session_id': self.session_data['session_id'],
                    'timestamp': datetime.now().isoformat(),
                    'total_processing_time': f"{total_time:.2f} seconds",
                    'queries_processed': len(ai_queries)
                },
                'local_knowledge_summary': knowledge_summary,
                'multi_query_results': query_results,
                'comprehensive_insights': comprehensive_insights,
                'actionable_recommendations': recommendations,
                'next_steps': self._generate_next_steps(comprehensive_insights)
            }
        }
        
        # Save results
        self._save_results(final_results)
        
        # Display summary
        self._display_results_summary(final_results)
        
        return final_results
    
    def _process_local_knowledge(self) -> Dict[str, Any]:
        """Process local knowledge base using existing orchestrator"""
        try:
            # Try to load existing processed data first
            outputs_dir = Path(self.orchestrator.output_dir)
            processed_docs_file = outputs_dir / "processed_documents" / "documents.json"
            
            if processed_docs_file.exists():
                print("📄 Loading existing processed knowledge base...")
                with open(processed_docs_file, 'r', encoding='utf-8') as f:
                    documents = json.load(f)
                
                summary = {
                    'documents': documents,
                    'total_documents': len(documents),
                    'processing_status': 'loaded_existing',
                    'domains': self._analyze_domains(documents)
                }
                
                self.session_data['knowledge_base_loaded'] = True
                return summary
            else:
                print("📄 No existing processed data found. Processing knowledge base...")
                # Run extraction on a subset for faster processing
                extraction_summary = self.orchestrator.run_full_extraction()
                
                if extraction_summary.get('status') != 'failed':
                    self.session_data['knowledge_base_loaded'] = True
                    return {
                        'processing_status': 'newly_processed',
                        'extraction_summary': extraction_summary
                    }
                else:
                    return {'processing_status': 'failed', 'error': extraction_summary.get('error')}
                    
        except Exception as e:
            print(f"⚠️  Warning: Could not process knowledge base: {str(e)}")
            return {'processing_status': 'error', 'error': str(e)}
    
    def _analyze_domains(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze domain distribution in documents"""
        domains = {}
        for doc in documents:
            domain = doc.get('semantic_analysis', {}).get('domain_classification', 'unknown')
            domains[domain] = domains.get(domain, 0) + 1
        return domains
    
    def _initialize_query_handler(self, knowledge_summary: Dict[str, Any]) -> None:
        """Initialize multi-query handler with knowledge base data"""
        self.multi_query_handler = MultiQueryHandler(knowledge_summary)
        print("✅ Multi-Query Handler initialized with knowledge base")
    
    def _generate_ai_queries(self, custom_queries: Optional[List[str]] = None) -> List[str]:
        """Generate AI-focused queries for comprehensive analysis"""
        if custom_queries:
            return custom_queries
        
        # Default AI knowledge queries based on the repository focus
        ai_queries = [
            "artificial intelligence implementation best practices",
            "AI-powered data visualization and analytics",
            "machine learning integration with Plotly Dash",
            "predictive analytics dashboard development",
            "AI knowledge extraction and processing systems",
            "automated data analysis and visualization techniques"
        ]
        
        print(f"📝 Generated {len(ai_queries)} AI-focused queries")
        return ai_queries
    
    def _generate_comprehensive_insights(self, knowledge_summary: Dict[str, Any], query_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights combining local and web knowledge"""
        insights = {
            'knowledge_integration': {},
            'ai_capabilities_assessment': {},
            'enhancement_opportunities': [],
            'technology_stack_analysis': {},
            'implementation_readiness': {}
        }
        
        # Analyze knowledge integration
        local_docs = knowledge_summary.get('total_documents', 0)
        web_sources = sum(
            len(query_data['processed_response'].get('web_knowledge', {}).get(query, []))
            for query_data in query_results.get('individual_query_results', {}).values()
            for query in query_data['processed_response'].get('web_knowledge', {})
            if isinstance(query_data['processed_response'].get('web_knowledge', {}).get(query), list)
        )
        
        insights['knowledge_integration'] = {
            'local_sources': local_docs,
            'web_sources': web_sources,
            'integration_score': self._calculate_integration_score(local_docs, web_sources),
            'coverage_assessment': 'comprehensive' if (local_docs > 50 and web_sources > 10) else 'partial'
        }
        
        # Assess AI capabilities
        synthesis = query_results.get('comprehensive_synthesis', {})
        avg_confidence = synthesis.get('confidence_distribution', {}).get('average', 0)
        
        insights['ai_capabilities_assessment'] = {
            'average_query_confidence': avg_confidence,
            'knowledge_base_maturity': 'high' if local_docs > 100 else 'medium' if local_docs > 20 else 'low',
            'web_integration_active': web_sources > 0,
            'multi_domain_coverage': len(synthesis.get('domain_analysis', {})) > 1
        }
        
        # Identify enhancement opportunities
        if avg_confidence < 0.7:
            insights['enhancement_opportunities'].append("Improve knowledge base coverage for better query confidence")
        
        if web_sources < 5:
            insights['enhancement_opportunities'].append("Enhance web search integration for broader knowledge access")
        
        common_themes = synthesis.get('common_themes', [])
        if common_themes:
            insights['enhancement_opportunities'].append(f"Develop specialized modules for: {', '.join(common_themes[:2])}")
        
        # Analyze technology stack
        domains = knowledge_summary.get('domains', {})
        insights['technology_stack_analysis'] = {
            'primary_technologies': list(domains.keys()),
            'plotly_dash_coverage': domains.get('data_visualization', 0),
            'ai_ml_coverage': domains.get('machine_learning', 0) + domains.get('artificial_intelligence', 0),
            'python_coverage': domains.get('python_programming', 0)
        }
        
        # Assess implementation readiness
        insights['implementation_readiness'] = {
            'knowledge_base_ready': local_docs > 20,
            'web_integration_ready': web_sources > 0,
            'multi_query_processing_ready': len(query_results.get('individual_query_results', {})) > 1,
            'comprehensive_analysis_ready': avg_confidence > 0.5
        }
        
        return insights
    
    def _calculate_integration_score(self, local_sources: int, web_sources: int) -> float:
        """Calculate knowledge integration score"""
        local_score = min(local_sources / 100, 1.0) * 0.6  # Max 0.6 from local
        web_score = min(web_sources / 20, 1.0) * 0.4       # Max 0.4 from web
        return local_score + web_score
    
    def _create_recommendations(self, insights: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create actionable recommendations based on insights"""
        recommendations = []
        
        # Knowledge base recommendations
        kb_maturity = insights['ai_capabilities_assessment']['knowledge_base_maturity']
        if kb_maturity != 'high':
            recommendations.append({
                'category': 'Knowledge Base',
                'priority': 'High',
                'action': 'Expand knowledge base with more comprehensive documentation',
                'expected_impact': 'Improved query confidence and coverage'
            })
        
        # Web integration recommendations
        if not insights['ai_capabilities_assessment']['web_integration_active']:
            recommendations.append({
                'category': 'Web Integration',
                'priority': 'Medium', 
                'action': 'Implement robust web search integration for real-time knowledge',
                'expected_impact': 'Access to latest information and broader knowledge scope'
            })
        
        # Enhancement opportunities
        for opportunity in insights['enhancement_opportunities']:
            recommendations.append({
                'category': 'Enhancement',
                'priority': 'Medium',
                'action': opportunity,
                'expected_impact': 'Increased system capabilities and user value'
            })
        
        # Technology stack recommendations
        tech_analysis = insights['technology_stack_analysis']
        if tech_analysis['ai_ml_coverage'] < tech_analysis['plotly_dash_coverage']:
            recommendations.append({
                'category': 'Technology Stack',
                'priority': 'Low',
                'action': 'Balance AI/ML content with visualization content',
                'expected_impact': 'More comprehensive AI assistance capabilities'
            })
        
        return recommendations
    
    def _generate_next_steps(self, insights: Dict[str, Any]) -> List[str]:
        """Generate specific next steps based on insights"""
        next_steps = []
        
        integration_score = insights['knowledge_integration']['integration_score']
        
        if integration_score < 0.7:
            next_steps.append("Priority: Expand knowledge base and improve web integration")
        
        if insights['ai_capabilities_assessment']['average_query_confidence'] < 0.6:
            next_steps.append("Focus: Improve query processing accuracy and confidence")
        
        if not insights['implementation_readiness']['comprehensive_analysis_ready']:
            next_steps.append("Develop: Enhanced analysis algorithms and processing pipelines")
        
        # Always include implementation step
        next_steps.append("Implement: Deploy Monica AI interface for production use")
        
        return next_steps
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Save comprehensive results to outputs directory"""
        try:
            outputs_dir = Path(self.orchestrator.output_dir)
            monica_dir = outputs_dir / "monica_ai_results"
            monica_dir.mkdir(exist_ok=True)
            
            # Save main results
            results_file = monica_dir / f"monica_ai_analysis_{self.session_data['session_id']}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Save summary report
            summary_file = monica_dir / f"summary_report_{self.session_data['session_id']}.md"
            self._create_markdown_report(results, summary_file)
            
            print(f"💾 Results saved to: {monica_dir}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not save results: {str(e)}")
    
    def _create_markdown_report(self, results: Dict[str, Any], output_file: Path) -> None:
        """Create a markdown summary report"""
        monica_data = results['monica_ai_analysis']
        
        report = f"""# Monica AI - Comprehensive Knowledge Analysis Report

**Session ID:** {monica_data['session_info']['session_id']}  
**Timestamp:** {monica_data['session_info']['timestamp']}  
**Processing Time:** {monica_data['session_info']['total_processing_time']}  

## Executive Summary

This report presents a comprehensive AI knowledge analysis integrating local knowledge base with web search capabilities, processing {monica_data['session_info']['queries_processed']} queries through Monica AI's multi-query system.

## Knowledge Integration Assessment

**Local Sources:** {monica_data['comprehensive_insights']['knowledge_integration']['local_sources']} documents  
**Web Sources:** {monica_data['comprehensive_insights']['knowledge_integration']['web_sources']} sources  
**Integration Score:** {monica_data['comprehensive_insights']['knowledge_integration']['integration_score']:.2f}/1.0  
**Coverage:** {monica_data['comprehensive_insights']['knowledge_integration']['coverage_assessment']}  

## AI Capabilities Assessment

**Average Query Confidence:** {monica_data['comprehensive_insights']['ai_capabilities_assessment']['average_query_confidence']:.1%}  
**Knowledge Base Maturity:** {monica_data['comprehensive_insights']['ai_capabilities_assessment']['knowledge_base_maturity']}  
**Web Integration:** {'Active' if monica_data['comprehensive_insights']['ai_capabilities_assessment']['web_integration_active'] else 'Inactive'}  
**Multi-Domain Coverage:** {'Yes' if monica_data['comprehensive_insights']['ai_capabilities_assessment']['multi_domain_coverage'] else 'No'}  

## Actionable Recommendations

"""
        
        for i, rec in enumerate(monica_data['actionable_recommendations'], 1):
            report += f"{i}. **{rec['category']}** ({rec['priority']} Priority): {rec['action']}\n"
            report += f"   *Expected Impact:* {rec['expected_impact']}\n\n"
        
        report += f"""## Next Steps

"""
        
        for i, step in enumerate(monica_data['next_steps'], 1):
            report += f"{i}. {step}\n"
        
        report += f"""
## Technology Stack Analysis

**Primary Technologies:** {', '.join(monica_data['comprehensive_insights']['technology_stack_analysis']['primary_technologies'])}  
**Plotly/Dash Coverage:** {monica_data['comprehensive_insights']['technology_stack_analysis']['plotly_dash_coverage']} documents  
**AI/ML Coverage:** {monica_data['comprehensive_insights']['technology_stack_analysis']['ai_ml_coverage']} documents  
**Python Coverage:** {monica_data['comprehensive_insights']['technology_stack_analysis']['python_coverage']} documents  

---
*Generated by Monica AI Knowledge Processing System*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def _display_results_summary(self, results: Dict[str, Any]) -> None:
        """Display comprehensive results summary"""
        monica_data = results['monica_ai_analysis']
        
        print("\n" + "="*80)
        print("🎉 MONICA AI ANALYSIS COMPLETE")
        print("="*80)
        
        print(f"\n📊 Session Summary:")
        print(f"   • Session ID: {monica_data['session_info']['session_id']}")
        print(f"   • Processing Time: {monica_data['session_info']['total_processing_time']}")
        print(f"   • Queries Processed: {monica_data['session_info']['queries_processed']}")
        
        insights = monica_data['comprehensive_insights']
        print(f"\n🧠 Knowledge Integration:")
        print(f"   • Local Sources: {insights['knowledge_integration']['local_sources']}")
        print(f"   • Web Sources: {insights['knowledge_integration']['web_sources']}")
        print(f"   • Integration Score: {insights['knowledge_integration']['integration_score']:.2f}/1.0")
        
        print(f"\n🎯 AI Capabilities:")
        print(f"   • Query Confidence: {insights['ai_capabilities_assessment']['average_query_confidence']:.1%}")
        print(f"   • Knowledge Maturity: {insights['ai_capabilities_assessment']['knowledge_base_maturity']}")
        print(f"   • Web Integration: {'✅' if insights['ai_capabilities_assessment']['web_integration_active'] else '❌'}")
        
        print(f"\n📋 Top Recommendations:")
        for i, rec in enumerate(monica_data['actionable_recommendations'][:3], 1):
            print(f"   {i}. {rec['category']}: {rec['action']}")
        
        print(f"\n🚀 Next Steps:")
        for i, step in enumerate(monica_data['next_steps'][:3], 1):
            print(f"   {i}. {step}")
        
        print(f"\n💾 Results saved in: AI_Knowledge_Extraction_System/outputs/monica_ai_results/")
        print("="*80)

def main():
    """Main function to run Monica AI interface"""
    monica_ai = MonicaAIInterface()
    
    # Run comprehensive analysis
    results = monica_ai.run_comprehensive_analysis()
    
    return results

if __name__ == "__main__":
    results = main()