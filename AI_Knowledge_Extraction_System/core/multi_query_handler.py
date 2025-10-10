"""
Multi-Query Handler for AI Knowledge Enhancement
Processes multiple queries and coordinates between local and web knowledge sources
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re

class MultiQueryHandler:
    """Handles the processing of multiple queries against various knowledge sources.

    This class is responsible for taking a list of user queries, processing
    each one against the local knowledge base and optional web search,
    and then synthesizing the results into a comprehensive, actionable response.
    It maintains a context memory to improve understanding across related
    queries.

    Attributes:
        knowledge_base_data (dict): A dictionary containing the processed data
            from the local knowledge base.
        query_history (list): A log of past query sessions.
        response_cache (dict): A cache to store responses for previously seen
            queries to improve performance.
        context_memory (list): A short-term memory to maintain context across
            a series of related queries.
    """

    def __init__(self, knowledge_base_data: Optional[Dict[str, Any]] = None):
        """Initializes the MultiQueryHandler.

        Args:
            knowledge_base_data: An optional dictionary containing the
                pre-processed knowledge base data.
        """
        self.knowledge_base_data = knowledge_base_data or {}
        self.query_history = []
        self.response_cache = {}
        self.context_memory = []

    def process_multiple_queries(
        self, queries: List[str], include_web_search: bool = True
    ) -> Dict[str, Any]:
        """Processes a list of queries and returns a synthesized response.

        This is the main public method of the class. It orchestrates the
        processing of individual queries, synthesizes the results, and
        generates actionable insights and next-step recommendations.

        Args:
            queries: A list of query strings to process.
            include_web_search: If True, the handler will augment local
                knowledge with results from a web search.

        Returns:
            A dictionary containing a comprehensive, multi-layered response
            that includes individual query results, a synthesis, and
            actionable insights.
        """
        print(f"🤖 Processing {len(queries)} queries with Monica AI-like comprehensive analysis...")
        
        start_time = time.time()
        query_results = {}
        
        for i, query in enumerate(queries, 1):
            print(f"📝 Processing Query {i}/{len(queries)}: {query}")
            
            # Process individual query
            result = self.process_single_query(query, include_web_search)
            query_results[f"query_{i}"] = {
                'original_query': query,
                'processed_response': result,
                'processing_time': result.get('processing_time', 0)
            }
            
            # Add to context memory for cross-query understanding
            self._update_context_memory(query, result)
        
        # Generate comprehensive synthesis
        synthesis = self._synthesize_multi_query_results(query_results)
        
        processing_time = time.time() - start_time
        
        comprehensive_response = {
            'meta_information': {
                'total_queries': len(queries),
                'processing_time': f"{processing_time:.2f} seconds",
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'include_web_search': include_web_search
            },
            'individual_query_results': query_results,
            'comprehensive_synthesis': synthesis,
            'actionable_insights': self._generate_actionable_insights(synthesis),
            'next_steps_recommendations': self._generate_next_steps(queries, synthesis)
        }
        
        # Save to query history
        self.query_history.append({
            'queries': queries,
            'timestamp': time.time(),
            'response_summary': synthesis.get('key_findings', [])
        })
        
        return comprehensive_response
    
    def process_single_query(
        self, query: str, include_web_search: bool = True
    ) -> Dict[str, Any]:
        """Processes a single query and returns a detailed response.

        This method coordinates the search for a single query against the local
        knowledge base and, if enabled, web sources. It analyzes the query,
        calculates a confidence score, and caches the response.

        Args:
            query: The query string to process.
            include_web_search: If True, enables web search integration.

        Returns:
            A dictionary containing the detailed results for the query,
            including local and web findings, and a confidence score.
        """
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{query}_{include_web_search}"
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        response = {
            'query': query,
            'local_knowledge': self._search_local_knowledge(query),
            'web_knowledge': {},
            'confidence_score': 0.0,
            'sources_count': 0,
            'query_analysis': self._analyze_query(query)
        }
        
        # Add web search if requested
        if include_web_search:
            try:
                from .web_search_processor import WebSearchProcessor
                web_processor = WebSearchProcessor()
                
                # Generate AI-focused queries
                ai_queries = web_processor.extract_ai_knowledge_queries(query)
                web_results = web_processor.search_multiple_queries([query] + ai_queries[:2])
                
                response['web_knowledge'] = web_results
                
            except Exception as e:
                print(f"Web search unavailable: {str(e)}")
                response['web_knowledge'] = {'error': 'Web search temporarily unavailable'}
        
        # Calculate confidence and sources
        response['sources_count'] = len(response['local_knowledge']) + sum(
            len(results) for results in response.get('web_knowledge', {}).values() if isinstance(results, list)
        )
        response['confidence_score'] = self._calculate_query_confidence(response)
        response['processing_time'] = time.time() - start_time
        
        # Cache the response
        self.response_cache[cache_key] = response
        
        return response
    
    def _search_local_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search local knowledge base for relevant information"""
        if not self.knowledge_base_data:
            return []
        
        results = []
        query_terms = query.lower().split()
        
        # Search through processed documents
        documents = self.knowledge_base_data.get('documents', [])
        
        for doc in documents:
            relevance_score = 0
            content = doc.get('content', '').lower()
            keywords = doc.get('semantic_analysis', {}).get('keywords', [])
            
            # Calculate relevance
            for term in query_terms:
                relevance_score += content.count(term) * 1
                if any(term in keyword.lower() for keyword in keywords):
                    relevance_score += 3
            
            if relevance_score > 0:
                results.append({
                    'filename': doc.get('file_info', {}).get('filename', 'Unknown'),
                    'relevance_score': relevance_score,
                    'content_snippet': self._extract_relevant_content(content, query_terms),
                    'domain': doc.get('semantic_analysis', {}).get('domain_classification', 'unknown'),
                    'keywords': keywords[:5],  # Top 5 keywords
                    'difficulty_level': doc.get('semantic_analysis', {}).get('difficulty_level', 'unknown')
                })
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:10]
    
    def _extract_relevant_content(self, content: str, query_terms: List[str], max_length: int = 300) -> str:
        """Extract the most relevant content snippet"""
        # Find sentences containing query terms
        sentences = re.split(r'[.!?]+', content)
        relevant_sentences = []
        
        for sentence in sentences:
            score = sum(1 for term in query_terms if term in sentence.lower())
            if score > 0:
                relevant_sentences.append((sentence.strip(), score))
        
        if relevant_sentences:
            # Sort by relevance and take top sentences
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            snippet = '. '.join(sent[0] for sent in relevant_sentences[:3])
            
            if len(snippet) > max_length:
                snippet = snippet[:max_length] + "..."
            
            return snippet
        
        # Fallback to beginning of content
        return content[:max_length] + ("..." if len(content) > max_length else "")
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze the query to understand intent and complexity"""
        analysis = {
            'intent': 'informational',  # Default
            'complexity': 'medium',
            'domain_focus': [],
            'query_type': 'general',
            'key_concepts': []
        }
        
        query_lower = query.lower()
        
        # Determine intent
        if any(word in query_lower for word in ['how to', 'tutorial', 'guide', 'implement']):
            analysis['intent'] = 'instructional'
        elif any(word in query_lower for word in ['what is', 'define', 'explain']):
            analysis['intent'] = 'definitional'
        elif any(word in query_lower for word in ['best', 'compare', 'vs', 'better']):
            analysis['intent'] = 'comparative'
        elif any(word in query_lower for word in ['problem', 'error', 'fix', 'debug']):
            analysis['intent'] = 'troubleshooting'
        
        # Determine domain focus
        domain_keywords = {
            'data_visualization': ['plotly', 'dash', 'chart', 'graph', 'visualization'],
            'machine_learning': ['ml', 'ai', 'model', 'prediction', 'algorithm'],
            'web_development': ['web', 'html', 'css', 'javascript', 'frontend'],
            'python_programming': ['python', 'code', 'programming', 'script', 'function']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                analysis['domain_focus'].append(domain)
        
        # Determine complexity
        complex_indicators = ['advanced', 'expert', 'optimization', 'performance', 'scalability']
        simple_indicators = ['basic', 'beginner', 'simple', 'easy', 'start']
        
        if any(indicator in query_lower for indicator in complex_indicators):
            analysis['complexity'] = 'high'
        elif any(indicator in query_lower for indicator in simple_indicators):
            analysis['complexity'] = 'low'
        
        # Extract key concepts (simple keyword extraction)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', query)
        analysis['key_concepts'] = [word.lower() for word in words if word.lower() not in 
                                   ['the', 'and', 'for', 'with', 'how', 'what', 'where', 'when', 'why']][:5]
        
        return analysis
    
    def _calculate_query_confidence(self, response: Dict[str, Any]) -> float:
        """Calculate confidence score for query response"""
        local_sources = len(response.get('local_knowledge', []))
        web_sources = sum(len(results) for results in response.get('web_knowledge', {}).values() 
                         if isinstance(results, list))
        
        # Base confidence on source availability
        confidence = 0.0
        
        if local_sources > 0:
            confidence += min(local_sources * 0.15, 0.6)  # Max 0.6 from local sources
        
        if web_sources > 0:
            confidence += min(web_sources * 0.1, 0.4)  # Max 0.4 from web sources
        
        return min(confidence, 1.0)
    
    def _update_context_memory(self, query: str, result: Dict[str, Any]) -> None:
        """Update context memory for cross-query understanding"""
        context_entry = {
            'query': query,
            'timestamp': time.time(),
            'key_concepts': result.get('query_analysis', {}).get('key_concepts', []),
            'domain_focus': result.get('query_analysis', {}).get('domain_focus', []),
            'sources_found': result.get('sources_count', 0)
        }
        
        self.context_memory.append(context_entry)
        
        # Keep only recent context (last 10 queries)
        if len(self.context_memory) > 10:
            self.context_memory = self.context_memory[-10:]
    
    def _synthesize_multi_query_results(self, query_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple queries into comprehensive insights"""
        synthesis = {
            'key_findings': [],
            'common_themes': [],
            'knowledge_coverage': {},
            'confidence_distribution': {},
            'domain_analysis': {},
            'comprehensive_summary': ""
        }
        
        # Analyze common themes across queries
        all_concepts = []
        all_domains = []
        confidence_scores = []
        
        for query_data in query_results.values():
            result = query_data['processed_response']
            
            # Collect concepts and domains
            query_analysis = result.get('query_analysis', {})
            all_concepts.extend(query_analysis.get('key_concepts', []))
            all_domains.extend(query_analysis.get('domain_focus', []))
            confidence_scores.append(result.get('confidence_score', 0))
        
        # Find common themes
        concept_freq = {}
        for concept in all_concepts:
            concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
        synthesis['common_themes'] = [
            concept for concept, freq in sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)
            if freq > 1
        ][:5]
        
        # Analyze domain coverage
        domain_freq = {}
        for domain in all_domains:
            domain_freq[domain] = domain_freq.get(domain, 0) + 1
        
        synthesis['domain_analysis'] = domain_freq
        
        # Analyze confidence distribution
        if confidence_scores:
            synthesis['confidence_distribution'] = {
                'average': sum(confidence_scores) / len(confidence_scores),
                'min': min(confidence_scores),
                'max': max(confidence_scores),
                'high_confidence_queries': sum(1 for score in confidence_scores if score > 0.7)
            }
        
        # Generate key findings
        synthesis['key_findings'] = self._generate_key_findings(query_results, synthesis)
        
        # Generate comprehensive summary
        synthesis['comprehensive_summary'] = self._generate_comprehensive_summary(synthesis)
        
        return synthesis
    
    def _generate_key_findings(self, query_results: Dict[str, Any], synthesis: Dict[str, Any]) -> List[str]:
        """Generate key findings from multi-query analysis"""
        findings = []
        
        total_queries = len(query_results)
        avg_confidence = synthesis.get('confidence_distribution', {}).get('average', 0)
        
        findings.append(f"Processed {total_queries} queries with average confidence of {avg_confidence:.1%}")
        
        if synthesis['common_themes']:
            findings.append(f"Common themes identified: {', '.join(synthesis['common_themes'][:3])}")
        
        if synthesis['domain_analysis']:
            primary_domain = max(synthesis['domain_analysis'].items(), key=lambda x: x[1])
            findings.append(f"Primary domain focus: {primary_domain[0].replace('_', ' ').title()}")
        
        high_conf_count = synthesis.get('confidence_distribution', {}).get('high_confidence_queries', 0)
        if high_conf_count > 0:
            findings.append(f"{high_conf_count} queries had high confidence responses (>70%)")
        
        return findings
    
    def _generate_comprehensive_summary(self, synthesis: Dict[str, Any]) -> str:
        """Generate a comprehensive summary of all query results"""
        summary_parts = []
        
        if synthesis['key_findings']:
            summary_parts.append("Key findings: " + "; ".join(synthesis['key_findings']))
        
        if synthesis['common_themes']:
            summary_parts.append(f"The analysis revealed recurring themes around {', '.join(synthesis['common_themes'][:3])}")
        
        if synthesis['domain_analysis']:
            domains = list(synthesis['domain_analysis'].keys())
            if len(domains) == 1:
                summary_parts.append(f"All queries focused on {domains[0].replace('_', ' ')}")
            else:
                summary_parts.append(f"Queries spanned multiple domains: {', '.join(domains)}")
        
        return ". ".join(summary_parts) + "."
    
    def _generate_actionable_insights(self, synthesis: Dict[str, Any]) -> List[str]:
        """Generate actionable insights based on the analysis"""
        insights = []
        
        avg_confidence = synthesis.get('confidence_distribution', {}).get('average', 0)
        
        if avg_confidence < 0.5:
            insights.append("Consider expanding the knowledge base or including more web sources for better coverage")
        
        if synthesis['common_themes']:
            insights.append(f"Focus on developing expertise in: {', '.join(synthesis['common_themes'][:2])}")
        
        domain_count = len(synthesis.get('domain_analysis', {}))
        if domain_count > 3:
            insights.append("Queries span multiple domains - consider creating domain-specific knowledge maps")
        
        return insights
    
    def _generate_next_steps(self, original_queries: List[str], synthesis: Dict[str, Any]) -> List[str]:
        """Generate recommended next steps based on query analysis"""
        next_steps = []
        
        # Based on confidence levels
        avg_confidence = synthesis.get('confidence_distribution', {}).get('average', 0)
        if avg_confidence < 0.6:
            next_steps.append("Research additional sources to improve knowledge coverage")
        
        # Based on common themes
        if synthesis['common_themes']:
            theme = synthesis['common_themes'][0]
            next_steps.append(f"Deep dive into {theme} - create comprehensive guide or tutorial")
        
        # Based on domain analysis
        if len(synthesis.get('domain_analysis', {})) > 1:
            next_steps.append("Create cross-domain integration examples or use cases")
        
        # Always suggest follow-up
        next_steps.append("Consider implementing the insights in a practical project or prototype")
        
        return next_steps
    
    def get_query_history_summary(self) -> Dict[str, Any]:
        """Returns a summary of the query processing history.

        This method provides metadata about the handler's activity, including
        the number of query sessions, cache size, and recent themes.

        Returns:
            A dictionary containing a summary of query history and usage.
        """
        return {
            "total_query_sessions": len(self.query_history),
            "cache_size": len(self.response_cache),
            "context_memory_size": len(self.context_memory),
            "recent_themes": [
                entry["key_concepts"][:2] for entry in self.context_memory[-3:]
            ]
            if self.context_memory
            else [],
        }