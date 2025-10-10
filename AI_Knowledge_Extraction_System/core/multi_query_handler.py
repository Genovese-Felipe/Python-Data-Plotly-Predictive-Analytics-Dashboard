"""
A handler for processing multiple queries and coordinating knowledge sources.

This module provides the `MultiQueryHandler` class, which is responsible for
managing a sequence of queries, fetching information from both local and web
sources, and synthesizing the results into a comprehensive, coherent response.
"""

import time
from typing import Dict, List, Any, Optional

# Import WebSearchProcessor dynamically to avoid circular dependencies
# if it's in the same directory or a submodule.
web_search_processor_instance = None

def get_web_search_processor():
    """Lazily imports and returns a WebSearchProcessor instance."""
    global web_search_processor_instance
    if web_search_processor_instance is None:
        try:
            from processors.web_search_processor import WebSearchProcessor
            web_search_processor_instance = WebSearchProcessor()
        except ImportError:
            print("Warning: WebSearchProcessor could not be imported. Web search will be disabled.")
            # Create a dummy class if the import fails
            class DummyWebSearchProcessor:
                def search_multiple_queries(self, queries, **kwargs): return {q: [] for q in queries}
            web_search_processor_instance = DummyWebSearchProcessor()
    return web_search_processor_instance

class MultiQueryHandler:
    """
    Handles multiple queries and coordinates responses from various knowledge sources.

    This class orchestrates the processing of a list of queries, integrating
    local knowledge base search with optional web search, and then synthesizes
    the findings to provide insights and recommendations.
    """

    def __init__(self, knowledge_base_data: Optional[Dict[str, Any]] = None):
        """
        Initializes the MultiQueryHandler.

        Args:
            knowledge_base_data: A dictionary containing the processed local
                                 knowledge base data.
        """
        self.knowledge_base_data = knowledge_base_data or {}
        self.query_history: List[Dict[str, Any]] = []
        self.response_cache: Dict[str, Dict[str, Any]] = {}

    def process_multiple_queries(self, queries: List[str], include_web_search: bool = True) -> Dict[str, Any]:
        """
        Processes a list of queries and returns a comprehensive, synthesized response.

        Args:
            queries: A list of query strings to process.
            include_web_search: A flag to determine whether to include web search results.

        Returns:
            A dictionary containing the synthesized results from all queries.
        """
        print(f"🤖 Processing {len(queries)} queries with comprehensive analysis...")
        start_time = time.time()
        query_results = {}

        for i, query in enumerate(queries, 1):
            print(f"📝 Processing Query {i}/{len(queries)}: {query}")
            result = self.process_single_query(query, include_web_search)
            query_results[f"query_{i}"] = {'original_query': query, 'processed_response': result}

        synthesis = self._synthesize_multi_query_results(query_results)
        
        return {
            'meta_information': {
                'total_queries': len(queries),
                'processing_time': f"{time.time() - start_time:.2f} seconds",
            },
            'individual_query_results': query_results,
            'comprehensive_synthesis': synthesis,
        }

    def process_single_query(self, query: str, include_web_search: bool = True) -> Dict[str, Any]:
        """
        Processes a single query against local and (optionally) web knowledge sources.

        Args:
            query: The query string to process.
            include_web_search: A flag to include web search results.

        Returns:
            A dictionary with the processed response for the single query.
        """
        cache_key = f"{query}_{include_web_search}"
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]

        response = {
            'query': query,
            'local_knowledge': self._search_local_knowledge(query),
            'web_knowledge': {},
        }

        if include_web_search:
            web_processor = get_web_search_processor()
            response['web_knowledge'] = web_processor.search_multiple_queries([query])

        response['confidence_score'] = self._calculate_query_confidence(response)
        self.response_cache[cache_key] = response
        return response

    def _search_local_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches the local knowledge base for information relevant to the query.

        Args:
            query: The search query string.

        Returns:
            A list of the most relevant documents found in the local knowledge base.
        """
        if not self.knowledge_base_data:
            return []
        
        # This is a placeholder for a more advanced search algorithm.
        # A real implementation would use vector search (e.g., FAISS) on embeddings.
        results = []
        query_terms = set(query.lower().split())
        documents = self.knowledge_base_data.get('documents', [])

        for doc in documents:
            content = doc.get('content', '').lower()
            if any(term in content for term in query_terms):
                results.append({'filename': doc.get('file_info', {}).get('filename', 'Unknown')})
        
        return results[:5] # Return top 5 matches

    def _calculate_query_confidence(self, response: Dict[str, Any]) -> float:
        """
        Calculates a confidence score for the query response based on the number of sources found.

        Args:
            response: The response dictionary for a single query.

        Returns:
            A confidence score between 0.0 and 1.0.
        """
        local_sources_count = len(response.get('local_knowledge', []))
        web_sources_count = sum(len(res) for res in response.get('web_knowledge', {}).values())
        
        # Simple confidence calculation based on source count.
        confidence = min(1.0, (local_sources_count * 0.2) + (web_sources_count * 0.1))
        return round(confidence, 2)

    def _synthesize_multi_query_results(self, query_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes results from multiple queries to find common themes and insights.

        Args:
            query_results: A dictionary of results from individual queries.

        Returns:
            A dictionary containing the synthesized analysis.
        """
        # Placeholder for a more complex synthesis engine.
        all_local_matches = []
        for res in query_results.values():
            all_local_matches.extend(res['processed_response']['local_knowledge'])
        
        common_files = pd.Series([m['filename'] for m in all_local_matches]).value_counts()
        
        return {
            'key_findings': ["Synthesis complete."],
            'common_documents': common_files.head(3).to_dict()
        }

    def get_query_history_summary(self) -> Dict[str, Any]:
        """
        Returns a summary of the query history.

        Returns:
            A dictionary with statistics about the query history.
        """
        return {
            'total_query_sessions': len(self.query_history),
            'cache_size': len(self.response_cache),
        }