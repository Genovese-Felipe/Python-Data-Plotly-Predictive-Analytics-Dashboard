"""
Web Search Processor for AI Knowledge Enhancement
Integrates web search capabilities with the existing Knowledge-Base system
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus
import re

class WebSearchProcessor:
    """
    Processes web search queries to enhance knowledge base information
    Integrates external knowledge with local Knowledge-Base content
    """
    
    def __init__(self):
        self.search_history = []
        self.cache = {}
        
    def search_duckduckgo(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform web search using DuckDuckGo Instant Answer API
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results with title, snippet, and URL
        """
        try:
            # Check cache first
            cache_key = f"{query}_{num_results}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # DuckDuckGo Instant Answer API
            url = f"https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Extract answer if available
                if data.get('Answer'):
                    results.append({
                        'title': 'Direct Answer',
                        'snippet': data['Answer'],
                        'url': data.get('AnswerSource', ''),
                        'type': 'answer'
                    })
                
                # Extract related topics
                if data.get('RelatedTopics'):
                    for topic in data['RelatedTopics'][:num_results-len(results)]:
                        if isinstance(topic, dict) and topic.get('Text'):
                            results.append({
                                'title': topic.get('FirstURL', {}).get('Text', 'Related Topic'),
                                'snippet': topic['Text'],
                                'url': topic.get('FirstURL', {}).get('Result', ''),
                                'type': 'related'
                            })
                
                # Cache results
                self.cache[cache_key] = results
                
                # Add to search history
                self.search_history.append({
                    'query': query,
                    'timestamp': time.time(),
                    'results_count': len(results)
                })
                
                return results
                
        except Exception as e:
            print(f"Web search error: {str(e)}")
            
        return []
    
    def search_multiple_queries(self, queries: List[str], max_results_per_query: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform multiple web searches and aggregate results
        
        Args:
            queries: List of search query strings
            max_results_per_query: Maximum results per query
            
        Returns:
            Dictionary mapping queries to their search results
        """
        all_results = {}
        
        for query in queries:
            print(f"🔍 Searching web for: {query}")
            results = self.search_duckduckgo(query, max_results_per_query)
            all_results[query] = results
            
            # Add small delay between searches to be respectful
            time.sleep(1)
            
        return all_results
    
    def extract_ai_knowledge_queries(self, domain: str = "artificial intelligence") -> List[str]:
        """
        Generate relevant AI knowledge queries based on domain
        
        Args:
            domain: The domain to focus on
            
        Returns:
            List of AI-related search queries
        """
        base_queries = [
            f"{domain} best practices",
            f"{domain} latest developments 2024",
            f"{domain} implementation guide",
            f"{domain} tools and frameworks",
            f"Monica AI {domain} documentation"
        ]
        
        # Add domain-specific queries
        if "data visualization" in domain.lower():
            base_queries.extend([
                "plotly dash AI integration",
                "predictive analytics dashboard AI",
                "AI-powered data visualization techniques"
            ])
        elif "machine learning" in domain.lower():
            base_queries.extend([
                "ML model deployment best practices",
                "AI model monitoring and evaluation",
                "automated machine learning workflows"
            ])
        
        return base_queries
    
    def synthesize_knowledge(self, local_knowledge: Dict[str, Any], web_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Synthesize local knowledge base information with web search results
        
        Args:
            local_knowledge: Knowledge extracted from local Knowledge-Base
            web_results: Results from web searches
            
        Returns:
            Synthesized comprehensive knowledge structure
        """
        synthesis = {
            'overview': {
                'local_sources': len(local_knowledge.get('documents', [])),
                'web_sources': sum(len(results) for results in web_results.values()),
                'total_queries': len(web_results)
            },
            'enhanced_knowledge': {},
            'cross_references': [],
            'comprehensive_insights': []
        }
        
        # Combine local and web knowledge by domain
        for query, web_data in web_results.items():
            domain_key = query.replace(' ', '_').lower()
            
            synthesis['enhanced_knowledge'][domain_key] = {
                'query': query,
                'local_matches': self._find_local_matches(local_knowledge, query),
                'web_insights': web_data,
                'combined_score': self._calculate_relevance_score(local_knowledge, web_data, query)
            }
        
        # Generate comprehensive insights
        synthesis['comprehensive_insights'] = self._generate_insights(synthesis['enhanced_knowledge'])
        
        return synthesis
    
    def _find_local_matches(self, local_knowledge: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """Find local knowledge base entries that match the query"""
        matches = []
        query_terms = query.lower().split()
        
        for doc in local_knowledge.get('documents', []):
            content = doc.get('content', '').lower()
            keywords = doc.get('semantic_analysis', {}).get('keywords', [])
            
            # Simple relevance scoring
            relevance_score = 0
            for term in query_terms:
                if term in content:
                    relevance_score += content.count(term)
                if term in ' '.join(keywords).lower():
                    relevance_score += 2
            
            if relevance_score > 0:
                matches.append({
                    'document': doc.get('file_info', {}).get('filename', 'Unknown'),
                    'relevance_score': relevance_score,
                    'snippet': self._extract_snippet(content, query_terms),
                    'domain': doc.get('semantic_analysis', {}).get('domain_classification', 'unknown')
                })
        
        # Sort by relevance
        matches.sort(key=lambda x: x['relevance_score'], reverse=True)
        return matches[:5]  # Return top 5 matches
    
    def _extract_snippet(self, content: str, query_terms: List[str], max_length: int = 200) -> str:
        """Extract relevant snippet from content"""
        # Find first occurrence of any query term
        content_lower = content.lower()
        for term in query_terms:
            index = content_lower.find(term)
            if index != -1:
                start = max(0, index - 50)
                end = min(len(content), index + max_length - 50)
                snippet = content[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
                return snippet
        
        # If no terms found, return beginning of content
        return content[:max_length].strip() + ("..." if len(content) > max_length else "")
    
    def _calculate_relevance_score(self, local_knowledge: Dict[str, Any], web_data: List[Dict[str, Any]], query: str) -> float:
        """Calculate combined relevance score for local + web knowledge"""
        local_score = len(self._find_local_matches(local_knowledge, query)) * 0.6
        web_score = len(web_data) * 0.4
        return local_score + web_score
    
    def _generate_insights(self, enhanced_knowledge: Dict[str, Any]) -> List[str]:
        """Generate comprehensive insights from combined knowledge"""
        insights = []
        
        # Analyze coverage
        total_sources = sum(
            len(data['local_matches']) + len(data['web_insights']) 
            for data in enhanced_knowledge.values()
        )
        
        insights.append(f"Analyzed {total_sources} total sources across {len(enhanced_knowledge)} domains")
        
        # Find strongest domains
        domain_scores = {
            domain: data['combined_score']
            for domain, data in enhanced_knowledge.items()
        }
        
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])
            insights.append(f"Strongest knowledge coverage in: {best_domain[0].replace('_', ' ').title()}")
        
        # Identify knowledge gaps
        weak_domains = [
            domain for domain, data in enhanced_knowledge.items()
            if len(data['local_matches']) == 0 or len(data['web_insights']) == 0
        ]
        
        if weak_domains:
            insights.append(f"Knowledge gaps identified in: {', '.join(weak_domains[:3])}")
        
        return insights
    
    def get_search_summary(self) -> Dict[str, Any]:
        """Get summary of all search activities"""
        return {
            'total_searches': len(self.search_history),
            'cache_size': len(self.cache),
            'recent_queries': [h['query'] for h in self.search_history[-5:]],
            'search_frequency': len(self.search_history) / max(1, (time.time() - self.search_history[0]['timestamp'] if self.search_history else 1) / 3600)
        }