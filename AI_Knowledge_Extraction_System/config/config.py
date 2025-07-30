"""
AI Knowledge Extraction System Configuration
Enhanced configuration for expert-level content processing
"""

import os
from pathlib import Path
from typing import Dict, List, Any

class KnowledgeExtractionConfig:
    """Configuration class for the Knowledge Extraction System"""
    
    # Base directories
    BASE_DIR = Path(__file__).parent.parent.parent
    KNOWLEDGE_BASE_DIR = BASE_DIR / "Knowledge-Base"
    OUTPUT_DIR = BASE_DIR / "AI_Knowledge_Extraction_System" / "outputs"
    
    # Processing configuration
    PROCESSING_CONFIG = {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "max_file_size_mb": 100,
        "enable_ocr": True,
        "enable_image_analysis": True,
        "enable_vector_embeddings": True,
        "enable_knowledge_graph": True,
        "enable_semantic_labeling": True,
    }
    
    # File type configurations
    SUPPORTED_FILE_TYPES = {
        "documents": [".pdf", ".txt", ".md", ".doc", ".docx"],
        "code": [".py", ".js", ".jsx", ".html", ".css", ".xml", ".json"],
        "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg"],
        "notebooks": [".ipynb"],
        "data": [".csv", ".json", ".xml", ".yaml", ".yml"]
    }
    
    # Metadata schema
    METADATA_SCHEMA = {
        "file_info": {
            "filename": str,
            "file_path": str,
            "file_type": str,
            "file_size": int,
            "creation_date": str,
            "modification_date": str,
            "hash": str
        },
        "content_info": {
            "content_type": str,
            "language": str,
            "char_count": int,
            "word_count": int,
            "line_count": int,
            "encoding": str
        },
        "semantic_info": {
            "topics": List[str],
            "keywords": List[str],
            "entities": List[Dict[str, Any]],
            "sentiment": float,
            "complexity_score": float,
            "domain_classification": str
        },
        "ai_processing": {
            "embedding_model": str,
            "embedding_dimension": int,
            "chunk_count": int,
            "processing_timestamp": str,
            "processing_version": str
        }
    }
    
    # Output structure
    OUTPUT_STRUCTURE = {
        "processed_content": "processed_documents",
        "embeddings": "vector_embeddings", 
        "knowledge_graph": "knowledge_graphs",
        "metadata": "metadata_catalog",
        "indexes": "search_indexes",
        "summaries": "content_summaries",
        "ai_ready": "ai_training_data"
    }
    
    # AI Model configurations
    AI_MODEL_CONFIG = {
        "embedding_model": "all-MiniLM-L6-v2",  # Lightweight but effective
        "chunk_embedding_model": "all-mpnet-base-v2",  # Better for semantic search
        "classification_model": "distilbert-base-uncased",
        "summarization_model": "facebook/bart-large-cnn",
        "max_tokens": 512,
        "similarity_threshold": 0.7
    }
    
    # Knowledge graph configuration
    KNOWLEDGE_GRAPH_CONFIG = {
        "node_types": ["document", "concept", "entity", "topic", "code_snippet", "image"],
        "relationship_types": ["references", "contains", "similar_to", "part_of", "implements", "describes"],
        "min_edge_weight": 0.5,
        "max_nodes_per_document": 50
    }
    
    # Semantic labeling configuration
    SEMANTIC_LABELING_CONFIG = {
        "domain_categories": [
            "data_visualization", "dashboard_development", "plotly_dash",
            "python_programming", "machine_learning", "data_analysis",
            "business_intelligence", "ui_ux_design", "technical_documentation"
        ],
        "content_types": [
            "tutorial", "reference", "example", "best_practice", 
            "troubleshooting", "api_documentation", "code_sample"
        ],
        "difficulty_levels": ["beginner", "intermediate", "advanced", "expert"],
        "auto_tag_threshold": 0.6
    }
    
    # Quality assurance
    QUALITY_CONFIG = {
        "min_content_length": 100,
        "max_processing_time_per_file": 300,  # seconds
        "validation_checks": [
            "content_extraction",
            "metadata_completeness", 
            "embedding_generation",
            "graph_connectivity"
        ]
    }

# Global configuration instance
config = KnowledgeExtractionConfig()