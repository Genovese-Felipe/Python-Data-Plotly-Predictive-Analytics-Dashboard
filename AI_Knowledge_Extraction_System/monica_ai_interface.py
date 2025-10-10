"""
A comprehensive interface for the Monica AI knowledge processing system.

This module provides a high-level interface to orchestrate the various components
of the Monica AI system, including local knowledge base extraction, web search
integration, multi-query processing, and the generation of comprehensive
insights and recommendations.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add the parent directory to the Python path to resolve local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))

from core.orchestrator import KnowledgeExtractionOrchestrator
from core.multi_query_handler import MultiQueryHandler
from processors.web_search_processor import WebSearchProcessor


class MonicaAIInterface:
    """
    A comprehensive interface for the Monica AI knowledge processing system.

    This class integrates local knowledge extraction with web search capabilities
    and multi-query processing to provide a complete AI assistance experience.
    It manages the end-to-end workflow from data processing to generating
    actionable insights.
    """

    def __init__(self):
        """Initializes the MonicaAIInterface and its components."""
        self.orchestrator = KnowledgeExtractionOrchestrator()
        self.web_processor = WebSearchProcessor()
        self.multi_query_handler: Optional[MultiQueryHandler] = None
        self.session_data = {
            'start_time': time.time(),
            'queries_processed': 0,
            'knowledge_base_loaded': False,
            'session_id': f"monica_ai_{int(time.time())}"
        }
        print("🤖 Monica AI Interface Initialized")

    def run_comprehensive_analysis(self, custom_queries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Runs a comprehensive AI knowledge analysis.

        This is the main method that orchestrates the entire analysis pipeline, including:
        1. Processing the local knowledge base.
        2. Generating and processing AI-focused queries.
        3. Integrating web search results.
        4. Generating insights and recommendations.
        5. Saving and displaying the final results.

        Args:
            custom_queries: An optional list of custom queries to process. If not
                            provided, default AI-focused queries will be used.

        Returns:
            A dictionary containing the complete analysis results.
        """
        print("\n🚀 Starting Monica AI Comprehensive Knowledge Analysis...")
        start_time = time.time()

        knowledge_summary = self._process_local_knowledge()
        self._initialize_query_handler(knowledge_summary)
        ai_queries = self._generate_ai_queries(custom_queries)
        query_results = self.multi_query_handler.process_multiple_queries(ai_queries, include_web_search=True)
        comprehensive_insights = self._generate_comprehensive_insights(knowledge_summary, query_results)
        recommendations = self._create_recommendations(comprehensive_insights)

        final_results = {
            'monica_ai_analysis': {
                'session_info': {
                    'session_id': self.session_data['session_id'],
                    'timestamp': datetime.now().isoformat(),
                    'total_processing_time': f"{time.time() - start_time:.2f} seconds",
                    'queries_processed': len(ai_queries)
                },
                'local_knowledge_summary': knowledge_summary,
                'multi_query_results': query_results,
                'comprehensive_insights': comprehensive_insights,
                'actionable_recommendations': recommendations,
            }
        }
        self._save_results(final_results)
        self._display_results_summary(final_results)
        return final_results

    def _process_local_knowledge(self) -> Dict[str, Any]:
        """
        Processes the local knowledge base using the orchestrator.

        It first checks for existing processed data to avoid redundant processing.
        If not found, it runs the full extraction process.

        Returns:
            A dictionary summarizing the processed local knowledge.
        """
        print("📚 Processing Local Knowledge Base...")
        try:
            extraction_summary = self.orchestrator.run_full_extraction()
            if extraction_summary.get('status') != 'failed':
                self.session_data['knowledge_base_loaded'] = True
                return {'processing_status': 'newly_processed', 'extraction_summary': extraction_summary}
            return {'processing_status': 'failed', 'error': extraction_summary.get('error')}
        except Exception as e:
            print(f"⚠️ Warning: Could not process knowledge base: {e}")
            return {'processing_status': 'error', 'error': str(e)}

    def _initialize_query_handler(self, knowledge_summary: Dict[str, Any]):
        """
        Initializes the MultiQueryHandler with the processed knowledge base data.

        Args:
            knowledge_summary: A dictionary containing the summary of the local knowledge base.
        """
        print("🔧 Initializing Multi-Query Handler...")
        self.multi_query_handler = MultiQueryHandler(knowledge_summary)
        print("✅ Multi-Query Handler initialized.")

    def _generate_ai_queries(self, custom_queries: Optional[List[str]] = None) -> List[str]:
        """
        Generates a list of AI-focused queries for analysis.

        Uses custom queries if provided; otherwise, falls back to a default set
        of queries relevant to the repository's focus.

        Args:
            custom_queries: An optional list of custom queries.

        Returns:
            A list of strings, where each string is a query.
        """
        print("🎯 Generating AI-Focused Queries...")
        if custom_queries:
            return custom_queries
        
        default_queries = [
            "artificial intelligence implementation best practices",
            "AI-powered data visualization and analytics",
            "machine learning integration with Plotly Dash",
            "predictive analytics dashboard development",
        ]
        print(f"📝 Generated {len(default_queries)} default AI-focused queries.")
        return default_queries

    def _generate_comprehensive_insights(self, knowledge_summary: Dict[str, Any], query_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates comprehensive insights by combining local and web knowledge.

        Args:
            knowledge_summary: A summary of the local knowledge base.
            query_results: The results from processing the AI queries.

        Returns:
            A dictionary of generated insights across various categories.
        """
        print("💡 Generating Comprehensive Insights...")
        # Placeholder for a more sophisticated insight generation engine.
        return {
            'summary': 'Insights generated from local and web knowledge.',
            'local_doc_count': knowledge_summary.get('extraction_summary', {}).get('total_documents_processed', 0),
            'web_source_count': len(query_results.get('web_knowledge', {})),
        }

    def _create_recommendations(self, insights: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Creates actionable recommendations based on the generated insights.

        Args:
            insights: A dictionary of insights.

        Returns:
            A list of dictionaries, where each dictionary is a recommendation.
        """
        print("📋 Creating Actionable Recommendations...")
        recommendations = []
        if insights.get('local_doc_count', 0) < 50:
            recommendations.append({
                'category': 'Knowledge Base',
                'action': 'Expand the local knowledge base with more documents.',
                'priority': 'High'
            })
        if insights.get('web_source_count', 0) < 10:
            recommendations.append({
                'category': 'Web Integration',
                'action': 'Improve web search integration to gather more external context.',
                'priority': 'Medium'
            })
        return recommendations

    def _save_results(self, results: Dict[str, Any]):
        """
        Saves the comprehensive analysis results to the outputs directory.

        Args:
            results: The dictionary of final results to save.
        """
        print("💾 Saving results...")
        try:
            outputs_dir = Path(self.orchestrator.output_dir) / "monica_ai_results"
            outputs_dir.mkdir(exist_ok=True, parents=True)
            results_file = outputs_dir / f"analysis_{self.session_data['session_id']}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not save results: {e}")

    def _display_results_summary(self, results: Dict[str, Any]):
        """
        Displays a summary of the analysis results to the console.

        Args:
            results: The dictionary of final results.
        """
        print("\n" + "="*80)
        print("🎉 MONICA AI ANALYSIS COMPLETE")
        print("="*80)
        analysis = results.get('monica_ai_analysis', {})
        print(f"Session ID: {analysis.get('session_info', {}).get('session_id')}")
        print(f"Processing Time: {analysis.get('session_info', {}).get('total_processing_time')}")
        print("\nTop Recommendations:")
        for rec in analysis.get('actionable_recommendations', []):
            print(f"- ({rec['priority']}) {rec['action']}")
        print("\n" + "="*80)


def main():
    """
    Main function to run the Monica AI interface.
    """
    monica_ai = MonicaAIInterface()
    monica_ai.run_comprehensive_analysis()


if __name__ == "__main__":
    main()