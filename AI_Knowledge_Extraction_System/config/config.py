"""
Configuration settings for the AI Knowledge Extraction System.

This module centralizes all configuration parameters for the system,
including file paths, processing settings, AI model identifiers, and output
structures. This approach makes it easy to manage and update the system's
behavior from a single location.
"""

from pathlib import Path
from typing import Dict, List, Any

class KnowledgeExtractionConfig:
    """
    A configuration class for the AI Knowledge Extraction System.

    This class encapsulates all static settings, from directory paths to
    complex dictionaries defining AI model parameters and data schemas.
    """

    # --- Core Paths ---
    # Defines the base directories used throughout the system for input and output.
    BASE_DIR = Path(__file__).parent.parent.parent
    KNOWLEDGE_BASE_DIR = BASE_DIR / "Knowledge-Base"
    OUTPUT_DIR = BASE_DIR / "AI_Knowledge_Extraction_System" / "outputs"

    # --- Document Processing Parameters ---
    # Governs how files are read, chunked, and processed.
    PROCESSING_CONFIG = {
        "chunk_size": 1000,  # Size of text chunks for processing
        "chunk_overlap": 200,  # Overlap between chunks to maintain context
        "max_file_size_mb": 100,  # Maximum file size to process
        "enable_ocr": True,  # Enable Optical Character Recognition for images/PDFs
        "enable_image_analysis": True,  # Enable analysis of image content
        "enable_vector_embeddings": True,  # Generate vector embeddings for text
        "enable_knowledge_graph": True,  # Construct a knowledge graph
        "enable_semantic_labeling": True,  # Automatically label content
    }

    # --- Supported File Types ---
    # A dictionary categorizing all file extensions the system is designed to handle.
    SUPPORTED_FILE_TYPES = {
        "documents": [".pdf", ".txt", ".md", ".doc", ".docx"],
        "code": [".py", ".js", ".jsx", ".html", ".css", ".xml", ".json"],
        "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg"],
        "notebooks": [".ipynb"],
        "data": [".csv", ".json", ".xml", ".yaml", ".yml"]
    }

    # --- Metadata Schema ---
    # Defines the structure and data types for the metadata to be extracted from each file.
    METADATA_SCHEMA = {
        "file_info": {
            "filename": str, "file_path": str, "file_type": str, "file_size": int,
            "creation_date": str, "modification_date": str, "hash": str
        },
        "content_info": {
            "content_type": str, "language": str, "char_count": int,
            "word_count": int, "line_count": int, "encoding": str
        },
        "semantic_info": {
            "topics": List[str], "keywords": List[str], "entities": List[Dict[str, Any]],
            "sentiment": float, "complexity_score": float, "domain_classification": str
        },
        "ai_processing": {
            "embedding_model": str, "embedding_dimension": int, "chunk_count": int,
            "processing_timestamp": str, "processing_version": str
        }
    }

    # --- Output Directory Structure ---
    # Defines the names of the subdirectories for storing processed outputs.
    OUTPUT_STRUCTURE = {
        "processed_content": "processed_documents",
        "embeddings": "vector_embeddings",
        "knowledge_graph": "knowledge_graphs",
        "metadata": "metadata_catalog",
        "indexes": "search_indexes",
        "summaries": "content_summaries",
        "ai_ready": "ai_training_data"
    }

    # --- AI Model Configurations ---
    # Specifies the pre-trained models to be used for various AI tasks.
    AI_MODEL_CONFIG = {
        "embedding_model": "all-MiniLM-L6-v2",  # For generating document embeddings
        "chunk_embedding_model": "all-mpnet-base-v2",  # For more detailed semantic search
        "classification_model": "distilbert-base-uncased",  # For content classification
        "summarization_model": "facebook/bart-large-cnn",  # For generating summaries
        "max_tokens": 512,  # Max tokens for model inputs
        "similarity_threshold": 0.7  # Threshold for semantic similarity searches
    }

    # --- Knowledge Graph Configuration ---
    # Parameters for building the knowledge graph from extracted entities and concepts.
    KNOWLEDGE_GRAPH_CONFIG = {
        "node_types": ["document", "concept", "entity", "topic", "code_snippet", "image"],
        "relationship_types": ["references", "contains", "similar_to", "part_of", "implements", "describes"],
        "min_edge_weight": 0.5,  # Minimum confidence to create a relationship
        "max_nodes_per_document": 50  # Max graph nodes to extract from a single document
    }

    # --- Semantic Labeling Configuration ---
    # Defines the categories and thresholds for automatic content labeling.
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
        "auto_tag_threshold": 0.6  # Confidence threshold for applying a tag
    }

    # --- Quality Assurance Parameters ---
    # Defines rules and checks to ensure the quality of the processed data.
    QUALITY_CONFIG = {
        "min_content_length": 100,  # Minimum characters for a document to be processed
        "max_processing_time_per_file": 300,  # Max seconds per file to prevent hangs
        "validation_checks": [  # List of quality checks to perform
            "content_extraction",
            "metadata_completeness",
            "embedding_generation",
            "graph_connectivity"
        ]
    }

# Create a global instance of the configuration class for easy access
# across the application.
config = KnowledgeExtractionConfig()