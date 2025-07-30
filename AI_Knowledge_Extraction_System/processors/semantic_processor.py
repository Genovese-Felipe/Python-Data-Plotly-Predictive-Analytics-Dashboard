"""
Semantic Processor - Advanced semantic analysis, embeddings, and knowledge graph generation
Implements expert-level NLP and ML techniques for knowledge extraction
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Text processing
import unicodedata
from collections import Counter, defaultdict

# Configuration
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import config

class SemanticProcessor:
    """Advanced semantic processing for extracted content"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.knowledge_graph = nx.Graph()
        self.document_embeddings = {}
        self.semantic_clusters = {}
        self.topic_model = None
        
    def process_document_semantics(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single document for semantic understanding
        
        Args:
            content_data: Extracted content data from ContentExtractor
            
        Returns:
            Enhanced content data with semantic analysis
        """
        
        content = content_data.get("content", "")
        if not content or len(content.strip()) < config.QUALITY_CONFIG["min_content_length"]:
            return content_data
        
        # Clean and preprocess text
        clean_content = self._preprocess_text(content)
        
        # Generate semantic features
        semantic_features = {
            "keywords": self._extract_keywords(clean_content),
            "entities": self._extract_entities(clean_content),
            "topics": self._extract_topics(clean_content),
            "domain_classification": self._classify_domain(clean_content),
            "complexity_score": self._calculate_complexity(content),
            "semantic_tags": self._generate_semantic_tags(clean_content),
            "content_type": self._classify_content_type(content),
            "difficulty_level": self._assess_difficulty(content)
        }
        
        # Add to content data
        content_data["semantic_analysis"] = semantic_features
        content_data["processed_content"] = clean_content
        
        return content_data
    
    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """
        Generate vector embeddings for documents using TF-IDF
        In a full implementation, this would use sentence-transformers
        """
        
        # Extract clean content from documents
        texts = []
        doc_ids = []
        
        for doc in documents:
            content = doc.get("processed_content", doc.get("content", ""))
            if content and len(content.strip()) >= config.QUALITY_CONFIG["min_content_length"]:
                texts.append(content)
                doc_ids.append(doc["file_info"]["hash"])
        
        if not texts:
            return {}
        
        # Generate TF-IDF embeddings
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Store embeddings
            embeddings = {}
            for i, doc_id in enumerate(doc_ids):
                embeddings[doc_id] = tfidf_matrix[i].toarray().flatten()
            
            self.document_embeddings.update(embeddings)
            return embeddings
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return {}
    
    def build_knowledge_graph(self, documents: List[Dict[str, Any]]) -> nx.Graph:
        """
        Build a knowledge graph from processed documents
        """
        
        # Clear existing graph
        self.knowledge_graph.clear()
        
        # Add document nodes
        for doc in documents:
            file_info = doc.get("file_info", {})
            semantic_info = doc.get("semantic_analysis", {})
            
            doc_id = file_info.get("hash", "")
            if not doc_id:
                continue
            
            # Add document node
            self.knowledge_graph.add_node(
                doc_id,
                type="document",
                filename=file_info.get("filename", ""),
                file_type=file_info.get("file_type", ""),
                domain=semantic_info.get("domain_classification", ""),
                keywords=semantic_info.get("keywords", []),
                topics=semantic_info.get("topics", []),
                complexity=semantic_info.get("complexity_score", 0),
                content_type=semantic_info.get("content_type", "")
            )
            
            # Add concept nodes from keywords and entities
            for keyword in semantic_info.get("keywords", [])[:10]:  # Limit to top 10
                concept_id = f"concept_{hashlib.md5(keyword.encode()).hexdigest()[:8]}"
                
                if not self.knowledge_graph.has_node(concept_id):
                    self.knowledge_graph.add_node(
                        concept_id,
                        type="concept",
                        name=keyword,
                        documents=[]
                    )
                
                # Add relationship
                self.knowledge_graph.add_edge(
                    doc_id, concept_id,
                    relationship="contains",
                    weight=1.0
                )
                
                # Update concept's document list
                if 'documents' in self.knowledge_graph.nodes[concept_id]:
                    self.knowledge_graph.nodes[concept_id]['documents'].append(doc_id)
        
        # Add similarity edges between documents
        self._add_similarity_edges()
        
        return self.knowledge_graph
    
    def perform_clustering(self, documents: List[Dict[str, Any]], n_clusters: int = 5) -> Dict[str, Any]:
        """
        Cluster documents based on semantic similarity
        """
        
        if not self.document_embeddings:
            self.generate_embeddings(documents)
        
        if len(self.document_embeddings) < n_clusters:
            n_clusters = max(1, len(self.document_embeddings) // 2)
        
        # Prepare embedding matrix
        doc_ids = list(self.document_embeddings.keys())
        embeddings = np.array([self.document_embeddings[doc_id] for doc_id in doc_ids])
        
        if len(embeddings) == 0:
            return {}
        
        # Perform clustering
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Organize results
            clusters = defaultdict(list)
            for doc_id, cluster_id in zip(doc_ids, cluster_labels):
                clusters[int(cluster_id)].append(doc_id)
            
            # Generate cluster summaries
            cluster_summaries = {}
            for cluster_id, doc_ids_in_cluster in clusters.items():
                # Find representative documents for this cluster
                cluster_docs = [doc for doc in documents if doc["file_info"]["hash"] in doc_ids_in_cluster]
                
                # Extract common keywords
                all_keywords = []
                all_topics = []
                for doc in cluster_docs:
                    semantic_info = doc.get("semantic_analysis", {})
                    all_keywords.extend(semantic_info.get("keywords", []))
                    all_topics.extend(semantic_info.get("topics", []))
                
                keyword_counts = Counter(all_keywords)
                topic_counts = Counter(all_topics)
                
                cluster_summaries[cluster_id] = {
                    "document_count": len(doc_ids_in_cluster),
                    "top_keywords": dict(keyword_counts.most_common(10)),
                    "top_topics": dict(topic_counts.most_common(5)),
                    "document_files": [doc["file_info"]["filename"] for doc in cluster_docs]
                }
            
            self.semantic_clusters = {
                "clusters": dict(clusters),
                "summaries": cluster_summaries,
                "n_clusters": n_clusters
            }
            
            return self.semantic_clusters
            
        except Exception as e:
            print(f"Error in clustering: {e}")
            return {}
    
    def extract_topics(self, documents: List[Dict[str, Any]], n_topics: int = 10) -> Dict[str, Any]:
        """
        Extract topics using Latent Dirichlet Allocation
        """
        
        # Prepare text data
        texts = []
        doc_metadata = []
        
        for doc in documents:
            content = doc.get("processed_content", doc.get("content", ""))
            if content and len(content.strip()) >= config.QUALITY_CONFIG["min_content_length"]:
                texts.append(content)
                doc_metadata.append(doc["file_info"])
        
        if len(texts) < n_topics:
            n_topics = max(1, len(texts) // 2)
        
        try:
            # Vectorize with different parameters for topic modeling
            topic_vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words='english',
                ngram_range=(1, 1),
                min_df=2,
                max_df=0.7
            )
            
            tfidf_matrix = topic_vectorizer.fit_transform(texts)
            
            # Perform LDA
            lda = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=100
            )
            
            lda.fit(tfidf_matrix)
            
            # Extract topics
            feature_names = topic_vectorizer.get_feature_names_out()
            topics = {}
            
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_words_idx]
                word_weights = [topic[i] for i in top_words_idx]
                
                topics[f"topic_{topic_idx}"] = {
                    "words": top_words,
                    "weights": word_weights.tolist(),
                    "description": self._generate_topic_description(top_words)
                }
            
            # Assign documents to topics
            doc_topics = lda.transform(tfidf_matrix)
            
            topic_assignments = {}
            for i, (doc_meta, topic_dist) in enumerate(zip(doc_metadata, doc_topics)):
                dominant_topic = np.argmax(topic_dist)
                topic_assignments[doc_meta["hash"]] = {
                    "dominant_topic": f"topic_{dominant_topic}",
                    "topic_distribution": topic_dist.tolist(),
                    "confidence": float(np.max(topic_dist))
                }
            
            self.topic_model = {
                "topics": topics,
                "document_assignments": topic_assignments,
                "n_topics": n_topics
            }
            
            return self.topic_model
            
        except Exception as e:
            print(f"Error in topic modeling: {e}")
            return {}
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Remove control characters
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
        
        # Basic cleaning
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]{}"\']+', '', text)
        
        return text.strip()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords using simple frequency and length filtering"""
        
        # Tokenize
        words = re.findall(r'\b\w+\b', text, re.IGNORECASE)
        
        # Filter words
        stop_words = STOP_WORDS
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, freq in word_freq.most_common(20)]
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Simple entity extraction using patterns"""
        
        entities = []
        
        # Extract Python-related entities
        python_patterns = {
            'library': r'\b(pandas|numpy|matplotlib|plotly|dash|flask|django|scikit-learn|tensorflow|pytorch)\b',
            'function': r'\b\w+\(\)',
            'file_extension': r'\.[a-zA-Z0-9]+\b',
            'url': r'https?://[^\s]+',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
        for entity_type, pattern in python_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "text": match.group(),
                    "type": entity_type,
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities[:50]  # Limit to 50 entities
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topic-related keywords"""
        
        domain_keywords = {
            'data_visualization': ['chart', 'graph', 'plot', 'visualization', 'dashboard', 'figure'],
            'web_development': ['html', 'css', 'javascript', 'web', 'browser', 'frontend', 'backend'],
            'python': ['python', 'function', 'class', 'import', 'def', 'return'],
            'machine_learning': ['model', 'prediction', 'algorithm', 'training', 'feature', 'dataset'],
            'data_analysis': ['data', 'analysis', 'statistics', 'correlation', 'trend']
        }
        
        text_lower = text.lower()
        found_topics = []
        
        for topic, keywords in domain_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_topics.append(topic)
        
        return found_topics
    
    def _classify_domain(self, text: str) -> str:
        """Classify the domain of the content"""
        
        domain_indicators = {
            'data_visualization': ['plotly', 'dash', 'chart', 'graph', 'visualization', 'dashboard'],
            'python_programming': ['python', 'def', 'import', 'class', 'function'],
            'machine_learning': ['model', 'prediction', 'algorithm', 'sklearn', 'tensorflow'],
            'web_development': ['html', 'css', 'javascript', 'web', 'frontend'],
            'data_analysis': ['pandas', 'numpy', 'data', 'analysis', 'statistics'],
            'documentation': ['guide', 'tutorial', 'documentation', 'readme', 'manual']
        }
        
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, indicators in domain_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate content complexity score"""
        
        if not text:
            return 0.0
        
        # Simple complexity metrics
        words = text.split()
        sentences = text.split('.')
        
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        avg_sentence_length = np.mean([len(sentence.split()) for sentence in sentences]) if sentences else 0
        
        # Technical term density
        technical_terms = ['function', 'class', 'algorithm', 'implementation', 'optimization', 'configuration']
        tech_density = sum(1 for term in technical_terms if term.lower() in text.lower()) / len(words) if words else 0
        
        # Normalize to 0-1 scale
        complexity = (avg_word_length / 10 + avg_sentence_length / 20 + tech_density * 10) / 3
        return min(1.0, complexity)
    
    def _generate_semantic_tags(self, text: str) -> List[str]:
        """Generate semantic tags for content"""
        
        tags = []
        text_lower = text.lower()
        
        # Content type tags
        if any(word in text_lower for word in ['tutorial', 'guide', 'how-to']):
            tags.append('tutorial')
        if any(word in text_lower for word in ['example', 'demo', 'sample']):
            tags.append('example')
        if any(word in text_lower for word in ['reference', 'documentation', 'api']):
            tags.append('reference')
        if any(word in text_lower for word in ['troubleshoot', 'error', 'debug']):
            tags.append('troubleshooting')
        
        # Technology tags
        if 'plotly' in text_lower:
            tags.append('plotly')
        if 'dash' in text_lower:
            tags.append('dash')
        if 'python' in text_lower:
            tags.append('python')
        if any(word in text_lower for word in ['javascript', 'js', 'jsx']):
            tags.append('javascript')
        
        return list(set(tags))
    
    def _classify_content_type(self, text: str) -> str:
        """Classify the type of content"""
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['tutorial', 'guide', 'how-to', 'step-by-step']):
            return 'tutorial'
        elif any(word in text_lower for word in ['example', 'demo', 'sample']):
            return 'example'
        elif any(word in text_lower for word in ['api', 'reference', 'documentation']):
            return 'reference'
        elif any(word in text_lower for word in ['def ', 'class ', 'function', 'import ']):
            return 'code'
        elif text_lower.startswith('#') or '##' in text:
            return 'documentation'
        else:
            return 'general'
    
    def _assess_difficulty(self, text: str) -> str:
        """Assess the difficulty level of content"""
        
        complexity = self._calculate_complexity(text)
        
        if complexity < 0.3:
            return 'beginner'
        elif complexity < 0.6:
            return 'intermediate'
        elif complexity < 0.8:
            return 'advanced'
        else:
            return 'expert'
    
    def _add_similarity_edges(self):
        """Add edges between similar documents in the knowledge graph"""
        
        if len(self.document_embeddings) < 2:
            return
        
        doc_ids = list(self.document_embeddings.keys())
        embeddings = np.array([self.document_embeddings[doc_id] for doc_id in doc_ids])
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Add edges for similar documents
        for i, doc_id1 in enumerate(doc_ids):
            for j, doc_id2 in enumerate(doc_ids):
                if i < j:  # Avoid duplicate edges
                    similarity = similarity_matrix[i][j]
                    if similarity > config.AI_MODEL_CONFIG["similarity_threshold"]:
                        self.knowledge_graph.add_edge(
                            doc_id1, doc_id2,
                            relationship="similar_to",
                            weight=float(similarity)
                        )
    
    def _generate_topic_description(self, words: List[str]) -> str:
        """Generate a human-readable description for a topic"""
        
        if not words:
            return "Unknown topic"
        
        # Simple heuristic to create topic descriptions
        primary_words = words[:3]
        return f"Topic related to {', '.join(primary_words)}"
    
    def get_semantic_summary(self) -> Dict[str, Any]:
        """Get a summary of all semantic processing results"""
        
        return {
            "total_documents_processed": len(self.document_embeddings),
            "knowledge_graph_stats": {
                "nodes": self.knowledge_graph.number_of_nodes(),
                "edges": self.knowledge_graph.number_of_edges(),
                "density": nx.density(self.knowledge_graph) if self.knowledge_graph.number_of_nodes() > 0 else 0
            },
            "clustering_stats": self.semantic_clusters,
            "topic_modeling_stats": self.topic_model if self.topic_model else {},
            "processing_timestamp": datetime.now().isoformat()
        }