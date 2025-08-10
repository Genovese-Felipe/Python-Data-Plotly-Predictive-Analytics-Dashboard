"""
Monica AI Knowledge Management System
====================================

Advanced knowledge upload and semantic enrichment system that provides:
- Multi-format content upload and processing
- Semantic analysis and relationship mapping
- Vector embeddings for similarity search
- Automatic categorization and tagging
- Knowledge graph construction
- Cross-domain knowledge integration
- Real-time knowledge retrieval and synthesis
"""

import os
import json
import hashlib
import mimetypes
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np

# Import from existing AI Knowledge Extraction System
try:
    from AI_Knowledge_Extraction_System.core.orchestrator import KnowledgeExtractionOrchestrator
    from AI_Knowledge_Extraction_System.processors.semantic_processor import SemanticProcessor
except ImportError:
    # Fallback if not available
    KnowledgeExtractionOrchestrator = None
    SemanticProcessor = None

from Monica_AI_System.config.settings import get_config

@dataclass
class KnowledgeDocument:
    """Represents a processed knowledge document."""
    doc_id: str
    filename: str
    file_type: str
    content: str
    metadata: Dict[str, Any]
    semantic_analysis: Dict[str, Any]
    vector_embedding: Optional[List[float]]
    knowledge_domains: List[str]
    related_documents: List[str]
    upload_timestamp: str
    last_updated: str
    owner_id: str
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class KnowledgeRelation:
    """Represents a relationship between knowledge entities."""
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    strength: float
    context: Dict[str, Any]
    created_at: str

class KnowledgeManager:
    """
    Advanced knowledge management system for Monica AI.
    
    Handles knowledge upload, processing, enrichment, and retrieval
    with sophisticated semantic analysis and relationship mapping.
    """
    
    def __init__(self):
        self.config = get_config("knowledge")
        self.monica_config = get_config("monica")
        self.documents: Dict[str, KnowledgeDocument] = {}
        self.relations: Dict[str, KnowledgeRelation] = {}
        self.knowledge_graph: Dict[str, Set[str]] = {}
        self.categories: Dict[str, List[str]] = {}
        self.vector_index: Dict[str, List[float]] = {}
        
        # Initialize knowledge extraction system if available
        self.extractor = None
        if KnowledgeExtractionOrchestrator:
            try:
                self.extractor = KnowledgeExtractionOrchestrator()
            except Exception:
                pass
        
        self._initialize_categories()
    
    def _initialize_categories(self):
        """Initialize knowledge categories and domains."""
        self.categories = {
            "technical": ["programming", "data_science", "artificial_intelligence", "web_development", "databases"],
            "business": ["strategy", "marketing", "finance", "operations", "management"],
            "academic": ["research", "papers", "documentation", "tutorials", "references"],
            "creative": ["design", "content", "media", "writing", "arts"],
            "personal": ["notes", "ideas", "projects", "tasks", "learning"]
        }
    
    def upload_knowledge(
        self,
        file_path: str = None,
        content: str = None,
        filename: str = "",
        owner_id: str = "default_user",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, str]:
        """
        Upload and process knowledge content.
        
        Args:
            file_path: Path to file to upload
            content: Direct content string (if not file_path)
            filename: Name for the content
            owner_id: Owner of this knowledge
            tags: Optional tags for categorization
            metadata: Additional metadata
            
        Returns:
            Tuple[bool, str, str]: (success, doc_id, message)
        """
        
        try:
            # Determine content and file info
            if file_path and os.path.exists(file_path):
                # File upload
                file_size = os.path.getsize(file_path)
                if file_size > self.config["max_file_size_mb"] * 1024 * 1024:
                    return False, "", f"File too large. Max size: {self.config['max_file_size_mb']}MB"
                
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext not in self.config["supported_file_types"]:
                    return False, "", f"Unsupported file type: {file_ext}"
                
                filename = filename or os.path.basename(file_path)
                
                # Read content based on file type
                content = self._extract_content_from_file(file_path)
                if not content:
                    return False, "", "Failed to extract content from file"
                
            elif content:
                # Direct content upload
                file_ext = self._detect_content_type(content)
                filename = filename or f"content_{int(datetime.now().timestamp())}.txt"
            else:
                return False, "", "No content or file provided"
            
            # Generate document ID
            doc_id = hashlib.md5(f"{filename}_{owner_id}_{int(datetime.now().timestamp())}".encode()).hexdigest()[:16]
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "file_size": len(content),
                "upload_method": "file" if file_path else "direct",
                "processing_version": "1.0"
            })
            
            # Process content with semantic analysis
            semantic_analysis = self._analyze_content_semantics(content, file_ext)
            
            # Generate vector embedding
            vector_embedding = self._generate_vector_embedding(content)
            
            # Determine knowledge domains
            knowledge_domains = self._classify_knowledge_domains(content, semantic_analysis)
            
            # Create knowledge document
            current_time = datetime.now().isoformat()
            document = KnowledgeDocument(
                doc_id=doc_id,
                filename=filename,
                file_type=file_ext,
                content=content,
                metadata=metadata,
                semantic_analysis=semantic_analysis,
                vector_embedding=vector_embedding,
                knowledge_domains=knowledge_domains,
                related_documents=[],
                upload_timestamp=current_time,
                last_updated=current_time,
                owner_id=owner_id,
                tags=tags or []
            )
            
            # Store document
            self.documents[doc_id] = document
            
            # Update vector index
            if vector_embedding:
                self.vector_index[doc_id] = vector_embedding
            
            # Find and create relationships
            if self.config["enable_relationship_mapping"]:
                self._create_knowledge_relationships(doc_id)
            
            # Auto-categorize if enabled
            if self.config["enable_auto_categorization"]:
                auto_tags = self._auto_categorize_content(content, semantic_analysis)
                document.tags.extend(auto_tags)
            
            return True, doc_id, "Knowledge uploaded and processed successfully"
            
        except Exception as e:
            return False, "", f"Error processing knowledge: {str(e)}"
    
    def _extract_content_from_file(self, file_path: str) -> str:
        """Extract text content from various file types."""
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext in [".txt", ".md", ".py", ".js", ".html", ".css", ".sql", ".yaml", ".json"]:
                # Text-based files
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_ext == ".pdf":
                # PDF extraction (simplified - in production use pdfplumber)
                return f"[PDF Content from {os.path.basename(file_path)}]"
            
            elif file_ext in [".docx", ".doc"]:
                # Document extraction (simplified - in production use python-docx)
                return f"[Document Content from {os.path.basename(file_path)}]"
            
            elif file_ext == ".csv":
                # CSV files
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return f"CSV Data:\n{content[:1000]}..." if len(content) > 1000 else content
            
            else:
                return ""
                
        except Exception:
            return ""
    
    def _detect_content_type(self, content: str) -> str:
        """Detect content type from content analysis."""
        
        content_lower = content.lower()
        
        # Programming languages
        if any(keyword in content_lower for keyword in ["def ", "function", "class ", "import ", "from "]):
            if "import " in content and "def " in content:
                return ".py"
            elif "function" in content and "{" in content:
                return ".js"
        
        # Markup languages
        if content.strip().startswith("#") or "##" in content:
            return ".md"
        elif "<html" in content_lower or "<!doctype" in content_lower:
            return ".html"
        elif content.strip().startswith("{") and content.strip().endswith("}"):
            return ".json"
        
        # Default to text
        return ".txt"
    
    def _analyze_content_semantics(self, content: str, file_type: str) -> Dict[str, Any]:
        """Perform semantic analysis on content."""
        
        # Basic semantic analysis (in production, use advanced NLP)
        words = content.lower().split()
        word_count = len(words)
        unique_words = len(set(words))
        
        # Extract keywords (simplified)
        keyword_candidates = [word for word in words if len(word) > 4 and word.isalpha()]
        keywords = list(set(keyword_candidates))[:20]  # Top 20 unique keywords
        
        # Detect programming languages
        programming_indicators = {
            "python": ["def ", "import ", "python", "django", "flask", "pandas"],
            "javascript": ["function", "var ", "let ", "const ", "react", "node"],
            "java": ["public class", "private", "package", "import java"],
            "sql": ["select ", "from ", "where ", "join ", "database"]
        }
        
        detected_languages = []
        content_lower = content.lower()
        for lang, indicators in programming_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                detected_languages.append(lang)
        
        # Complexity assessment
        complexity_indicators = {
            "high": ["algorithm", "optimization", "architecture", "framework", "advanced"],
            "medium": ["implementation", "development", "analysis", "design"],
            "low": ["basic", "introduction", "simple", "tutorial"]
        }
        
        complexity_score = 0.5  # Default medium
        for level, indicators in complexity_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in content_lower)
            if level == "high" and matches > 2:
                complexity_score = 0.8
            elif level == "low" and matches > 2:
                complexity_score = 0.2
        
        return {
            "word_count": word_count,
            "unique_words": unique_words,
            "keywords": keywords,
            "detected_languages": detected_languages,
            "complexity_score": complexity_score,
            "content_type": file_type,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _generate_vector_embedding(self, content: str) -> Optional[List[float]]:
        """Generate vector embedding for content similarity."""
        
        if not self.config["enable_semantic_enrichment"]:
            return None
        
        try:
            # Simplified TF-IDF based embedding (in production, use sentence-transformers)
            words = content.lower().split()
            
            # Create simple word frequency vector
            word_freq = {}
            for word in words:
                if word.isalpha() and len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Convert to fixed-size vector (simplified)
            vocab_size = self.config["vector_embedding"]["dimension"]
            vector = [0.0] * vocab_size
            
            # Hash words to vector positions
            for word, freq in word_freq.items():
                position = hash(word) % vocab_size
                vector[position] += freq
            
            # Normalize vector
            magnitude = sum(x*x for x in vector) ** 0.5
            if magnitude > 0:
                vector = [x / magnitude for x in vector]
            
            return vector
            
        except Exception:
            return None
    
    def _classify_knowledge_domains(self, content: str, semantic_analysis: Dict[str, Any]) -> List[str]:
        """Classify content into knowledge domains."""
        
        domains = []
        content_lower = content.lower()
        
        # Technical domains
        if any(lang in semantic_analysis.get("detected_languages", []) for lang in ["python", "javascript", "java"]):
            domains.append("programming")
        
        if any(keyword in content_lower for keyword in ["data", "analysis", "statistics", "machine learning", "ai"]):
            domains.append("data_science")
        
        if any(keyword in content_lower for keyword in ["dashboard", "visualization", "chart", "graph", "plotly"]):
            domains.append("data_visualization")
        
        # Business domains
        if any(keyword in content_lower for keyword in ["business", "strategy", "market", "finance", "revenue"]):
            domains.append("business")
        
        # Academic domains
        if any(keyword in content_lower for keyword in ["research", "study", "analysis", "paper", "academic"]):
            domains.append("research")
        
        # Default domain if none found
        if not domains:
            if semantic_analysis.get("complexity_score", 0.5) > 0.7:
                domains.append("advanced_technical")
            else:
                domains.append("general")
        
        return domains
    
    def _auto_categorize_content(self, content: str, semantic_analysis: Dict[str, Any]) -> List[str]:
        """Automatically generate tags for content."""
        
        auto_tags = []
        content_lower = content.lower()
        
        # Complexity tags
        complexity = semantic_analysis.get("complexity_score", 0.5)
        if complexity > 0.7:
            auto_tags.append("advanced")
        elif complexity < 0.3:
            auto_tags.append("beginner")
        else:
            auto_tags.append("intermediate")
        
        # Content type tags
        detected_languages = semantic_analysis.get("detected_languages", [])
        auto_tags.extend(detected_languages)
        
        # Topic tags based on keywords
        topic_keywords = {
            "tutorial": ["tutorial", "guide", "how to", "step by step"],
            "documentation": ["documentation", "docs", "api", "reference"],
            "example": ["example", "sample", "demo", "code"],
            "theory": ["theory", "concept", "principle", "background"]
        }
        
        for tag, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                auto_tags.append(tag)
        
        return auto_tags
    
    def _create_knowledge_relationships(self, doc_id: str):
        """Find and create relationships with existing documents."""
        
        document = self.documents.get(doc_id)
        if not document or not document.vector_embedding:
            return
        
        # Find similar documents using vector similarity
        similarities = []
        for other_id, other_doc in self.documents.items():
            if other_id == doc_id or not other_doc.vector_embedding:
                continue
            
            similarity = self._calculate_cosine_similarity(
                document.vector_embedding,
                other_doc.vector_embedding
            )
            
            if similarity > self.config["vector_embedding"]["similarity_threshold"]:
                similarities.append((other_id, similarity))
        
        # Sort by similarity and create relationships
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        for other_id, similarity in similarities[:5]:  # Top 5 similar documents
            # Create bidirectional relationship
            self._create_relation(doc_id, other_id, "similar_content", similarity)
            self._create_relation(other_id, doc_id, "similar_content", similarity)
            
            # Update document relationships
            if other_id not in document.related_documents:
                document.related_documents.append(other_id)
            
            other_doc = self.documents[other_id]
            if doc_id not in other_doc.related_documents:
                other_doc.related_documents.append(doc_id)
    
    def _create_relation(self, source_id: str, target_id: str, relation_type: str, strength: float):
        """Create a knowledge relationship."""
        
        relation_id = hashlib.md5(f"{source_id}_{target_id}_{relation_type}".encode()).hexdigest()[:12]
        
        relation = KnowledgeRelation(
            relation_id=relation_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=strength,
            context={},
            created_at=datetime.now().isoformat()
        )
        
        self.relations[relation_id] = relation
        
        # Update knowledge graph
        if source_id not in self.knowledge_graph:
            self.knowledge_graph[source_id] = set()
        self.knowledge_graph[source_id].add(target_id)
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def search_knowledge(
        self,
        query: str,
        owner_id: str = None,
        domains: List[str] = None,
        tags: List[str] = None,
        max_results: int = 10
    ) -> List[Tuple[KnowledgeDocument, float]]:
        """
        Search knowledge base with semantic matching.
        
        Args:
            query: Search query
            owner_id: Filter by owner
            domains: Filter by knowledge domains
            tags: Filter by tags
            max_results: Maximum results to return
            
        Returns:
            List of (document, relevance_score) tuples
        """
        
        # Generate query vector
        query_vector = self._generate_vector_embedding(query)
        if not query_vector:
            return []
        
        # Calculate relevance scores
        results = []
        for doc_id, document in self.documents.items():
            # Apply filters
            if owner_id and document.owner_id != owner_id:
                continue
            
            if domains and not any(domain in document.knowledge_domains for domain in domains):
                continue
            
            if tags and not any(tag in document.tags for tag in tags):
                continue
            
            # Calculate semantic similarity
            if document.vector_embedding:
                similarity = self._calculate_cosine_similarity(query_vector, document.vector_embedding)
                
                # Boost score based on keyword matches
                query_lower = query.lower()
                content_lower = document.content.lower()
                keyword_boost = sum(1 for word in query_lower.split() if word in content_lower) * 0.1
                
                final_score = similarity + keyword_boost
                
                if final_score > 0.1:  # Minimum relevance threshold
                    results.append((document, final_score))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]
    
    def get_related_knowledge(self, doc_id: str, max_results: int = 5) -> List[KnowledgeDocument]:
        """Get related documents for a given document."""
        
        document = self.documents.get(doc_id)
        if not document:
            return []
        
        related_docs = []
        for related_id in document.related_documents[:max_results]:
            if related_id in self.documents:
                related_docs.append(self.documents[related_id])
        
        return related_docs
    
    def get_knowledge_graph_data(self) -> Dict[str, Any]:
        """Get knowledge graph data for visualization."""
        
        nodes = []
        edges = []
        
        # Create nodes
        for doc_id, document in self.documents.items():
            nodes.append({
                "id": doc_id,
                "name": document.filename,
                "type": "document",
                "domains": document.knowledge_domains,
                "tags": document.tags,
                "size": len(document.content) / 1000  # Size based on content length
            })
        
        # Create edges
        for relation_id, relation in self.relations.items():
            edges.append({
                "id": relation_id,
                "source": relation.source_id,
                "target": relation.target_id,
                "type": relation.relation_type,
                "strength": relation.strength
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_documents": len(self.documents),
                "total_relations": len(self.relations),
                "knowledge_domains": list(set(
                    domain for doc in self.documents.values() 
                    for domain in doc.knowledge_domains
                ))
            }
        }
    
    def get_knowledge_statistics(self, owner_id: str = None) -> Dict[str, Any]:
        """Get comprehensive knowledge base statistics."""
        
        documents = list(self.documents.values())
        if owner_id:
            documents = [doc for doc in documents if doc.owner_id == owner_id]
        
        if not documents:
            return {"total_documents": 0}
        
        # Basic statistics
        total_content_length = sum(len(doc.content) for doc in documents)
        
        # Domain distribution
        domain_counts = {}
        for doc in documents:
            for domain in doc.knowledge_domains:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # File type distribution
        type_counts = {}
        for doc in documents:
            type_counts[doc.file_type] = type_counts.get(doc.file_type, 0) + 1
        
        # Tag distribution
        tag_counts = {}
        for doc in documents:
            for tag in doc.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_documents": len(documents),
            "total_content_length": total_content_length,
            "average_document_size": total_content_length / len(documents),
            "domain_distribution": domain_counts,
            "file_type_distribution": type_counts,
            "tag_distribution": tag_counts,
            "total_relationships": len(self.relations),
            "knowledge_graph_density": len(self.relations) / max(len(documents), 1)
        }