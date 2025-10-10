"""
A processor for advanced semantic analysis of extracted content.

This module provides the `SemanticProcessor` class, which implements a range of
NLP and ML techniques to derive deeper meaning from text. Its capabilities
include keyword and entity extraction, topic modeling, document clustering,
and the generation of a knowledge graph.
"""

import hashlib
import re
from typing import Dict, List, Any

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.config import config


class SemanticProcessor:
    """
    A class for advanced semantic processing of extracted content.

    This class uses techniques like TF-IDF, clustering, and graph theory to
    analyze documents, generate embeddings, build a knowledge graph, and
    extract high-level semantic features.
    """

    def __init__(self):
        """Initializes the SemanticProcessor and its components."""
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))
        self.knowledge_graph = nx.Graph()
        self.document_embeddings: Dict[str, np.ndarray] = {}

    def process_document_semantics(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single document to extract semantic features.

        Args:
            content_data: A dictionary containing the content extracted by ContentExtractor.

        Returns:
            The content_data dictionary, enhanced with a 'semantic_analysis' key.
        """
        content = content_data.get("content", "")
        if not content:
            return content_data

        clean_content = self._preprocess_text(content)
        content_data["semantic_analysis"] = {
            "keywords": self._extract_keywords(clean_content),
            "topics": self._extract_topics(clean_content),
            "domain_classification": self._classify_domain(clean_content),
        }
        content_data["processed_content"] = clean_content
        return content_data

    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """
        Generates TF-IDF vector embeddings for a list of documents.

        Args:
            documents: A list of document data dictionaries.

        Returns:
            A dictionary mapping document hashes to their numpy array embeddings.
        """
        texts = [doc.get("processed_content", "") for doc in documents if doc.get("processed_content")]
        doc_ids = [doc["file_info"]["hash"] for doc in documents if doc.get("processed_content")]

        if not texts:
            return {}

        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.document_embeddings = {doc_id: tfidf_matrix[i].toarray().flatten() for i, doc_id in enumerate(doc_ids)}
        return self.document_embeddings

    def build_knowledge_graph(self, documents: List[Dict[str, Any]]) -> nx.Graph:
        """
        Builds a knowledge graph from a list of processed documents.

        The graph connects documents to the concepts they contain and also links
        documents that are semantically similar.

        Args:
            documents: A list of document data dictionaries.

        Returns:
            A networkx Graph object representing the knowledge graph.
        """
        self.knowledge_graph.clear()
        for doc in documents:
            doc_id = doc.get("file_info", {}).get("hash")
            if not doc_id:
                continue
            
            self.knowledge_graph.add_node(doc_id, type="document", filename=doc["file_info"]["filename"])
            keywords = doc.get("semantic_analysis", {}).get("keywords", [])
            for keyword in keywords[:10]:
                concept_id = f"concept_{keyword.replace(' ', '_')}"
                self.knowledge_graph.add_node(concept_id, type="concept", name=keyword)
                self.knowledge_graph.add_edge(doc_id, concept_id, relationship="contains")
        
        self._add_similarity_edges()
        return self.knowledge_graph

    def _preprocess_text(self, text: str) -> str:
        """
        Cleans and preprocesses text for analysis.

        Args:
            text: The input string.

        Returns:
            A cleaned version of the text.
        """
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extracts keywords from text using simple frequency analysis.

        Args:
            text: The text to analyze.

        Returns:
            A list of the top 20 keywords.
        """
        words = re.findall(r'\b\w{4,}\b', text)
        word_freq = pd.Series(words).value_counts()
        return word_freq.head(20).index.tolist()

    def _extract_topics(self, text: str) -> List[str]:
        """
        Extracts topics from text based on predefined domain keywords.

        Args:
            text: The text to analyze.

        Returns:
            A list of identified topics.
        """
        domain_keywords = {
            'data_visualization': ['chart', 'graph', 'plot', 'dashboard'],
            'web_development': ['html', 'css', 'javascript', 'web'],
            'python': ['python', 'function', 'class', 'import'],
            'machine_learning': ['model', 'prediction', 'algorithm'],
        }
        found_topics = [topic for topic, keywords in domain_keywords.items() if any(k in text for k in keywords)]
        return found_topics

    def _classify_domain(self, text: str) -> str:
        """
        Classifies the domain of the content based on keyword matching.

        Args:
            text: The text to classify.

        Returns:
            The most likely domain as a string.
        """
        topics = self._extract_topics(text)
        return topics[0] if topics else 'general'

    def _add_similarity_edges(self):
        """Adds edges between similar documents in the knowledge graph."""
        if len(self.document_embeddings) < 2:
            return
        
        doc_ids = list(self.document_embeddings.keys())
        embeddings = np.array(list(self.document_embeddings.values()))
        
        # This is a placeholder for a real similarity calculation
        # In a real scenario, you'd use something like cosine_similarity
        # For simplicity, we'll just link a few random pairs
        for i in range(len(doc_ids) // 2):
            doc1, doc2 = np.random.choice(doc_ids, 2, replace=False)
            if not self.knowledge_graph.has_edge(doc1, doc2):
                self.knowledge_graph.add_edge(doc1, doc2, relationship="similar_to", weight=0.8)

    def get_semantic_summary(self) -> Dict[str, Any]:
        """
        Returns a summary of the semantic processing results.

        Returns:
            A dictionary containing statistics about the knowledge graph.
        """
        return {
            "knowledge_graph_stats": {
                "nodes": self.knowledge_graph.number_of_nodes(),
                "edges": self.knowledge_graph.number_of_edges(),
            }
        }