"""
A processor to integrate web search capabilities for knowledge enhancement.

This module provides the `WebSearchProcessor` class, which is responsible for
querying external search engines, processing the results, and synthesizing them
with the local knowledge base to provide a more comprehensive and up-to-date
knowledge repository.
"""

import requests
import json
import time
from typing import Dict, List, Any

class WebSearchProcessor:
    """
    Processes web search queries to enhance the local knowledge base.

    This class handles web searches, caches results to avoid redundant queries,
    and provides methods to synthesize web-based information with locally
    extracted knowledge.
    """

    def __init__(self):
        """Initializes the WebSearchProcessor."""
        self.search_history: List[Dict[str, Any]] = []
        self.cache: Dict[str, List[Dict[str, Any]]] = {}

    def search_duckduckgo(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a web search using the DuckDuckGo Instant Answer API.

        Args:
            query: The search query string.
            num_results: The maximum number of results to return.

        Returns:
            A list of search results, each containing a title, snippet, and URL.
        """
        cache_key = f"{query}_{num_results}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if data.get("AbstractText"):
                results.append({"title": data["Heading"], "snippet": data["AbstractText"], "url": data["AbstractURL"]})
            
            for topic in data.get("RelatedTopics", []):
                if len(results) >= num_results:
                    break
                if "Text" in topic:
                    results.append({"title": topic["Text"], "snippet": topic.get("Result", ""), "url": topic.get("FirstURL", "")})
            
            self.cache[cache_key] = results
            self.search_history.append({'query': query, 'timestamp': time.time(), 'results_count': len(results)})
            return results
        except requests.RequestException as e:
            print(f"Web search error: {e}")
            return []

    def search_multiple_queries(self, queries: List[str], max_results_per_query: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """
        Performs multiple web searches and aggregates the results.

        Args:
            queries: A list of search query strings.
            max_results_per_query: The maximum number of results for each query.

        Returns:
            A dictionary mapping each query to its list of search results.
        """
        all_results = {}
        for query in queries:
            print(f"🔍 Searching web for: {query}")
            results = self.search_duckduckgo(query, max_results_per_query)
            all_results[query] = results
            time.sleep(0.5)  # Be respectful to the API
        return all_results

    def synthesize_knowledge(self, local_knowledge: Dict[str, Any], web_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Synthesizes local knowledge with web search results.

        This method provides a basic framework for combining local and web-based
        information. In a real-world scenario, this would involve more complex
        semantic analysis and merging logic.

        Args:
            local_knowledge: A dictionary containing knowledge extracted from local files.
            web_results: A dictionary of web search results.

        Returns:
            A dictionary containing the synthesized knowledge.
        """
        synthesis = {
            'overview': {
                'local_sources_count': len(local_knowledge.get('documents', [])),
                'web_queries_count': len(web_results),
            },
            'enhanced_knowledge': {}
        }

        for query, results in web_results.items():
            synthesis['enhanced_knowledge'][query] = {
                'web_results': results,
                'local_matches': self._find_local_matches(local_knowledge, query)
            }
        return synthesis

    def _find_local_matches(self, local_knowledge: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """
        Finds local documents that are relevant to a given query.

        Args:
            local_knowledge: A dictionary containing local knowledge.
            query: The search query string.

        Returns:
            A list of matching local documents.
        """
        matches = []
        query_terms = set(query.lower().split())
        
        for doc in local_knowledge.get('documents', []):
            content = doc.get('content', '').lower()
            if any(term in content for term in query_terms):
                matches.append({'document': doc.get('file_info', {}).get('filename', 'Unknown')})
        
        return matches[:5] # Return top 5 matches for brevity

    def get_search_summary(self) -> Dict[str, Any]:
        """
        Returns a summary of the web search activities.

        Returns:
            A dictionary with search statistics.
        """
        return {
            'total_searches': len(self.search_history),
            'cache_size': len(self.cache),
            'recent_queries': [h['query'] for h in self.search_history[-5:]],
        }