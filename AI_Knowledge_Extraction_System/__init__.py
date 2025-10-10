"""
AI Knowledge Extraction System
==============================

A comprehensive system for expert-level content processing, semantic analysis,
and knowledge extraction from a variety of file formats.

This package provides the core components for building a sophisticated
knowledge pipeline, including content extraction, semantic processing, and
overall orchestration.

Key Components:
- `KnowledgeExtractionOrchestrator`: The main coordinator for the entire pipeline.
- `ContentExtractor`: For extracting text and metadata from files.
- `SemanticProcessor`: For advanced NLP and semantic analysis.
- `config`: A centralized configuration object for all system settings.
"""

# The version of the AI Knowledge Extraction System package.
__version__ = "1.0.0"

# The designated author of the package.
__author__ = "AI Knowledge Extraction System"

# Import key classes and objects to make them directly accessible from the package level.
# e.g., from AI_Knowledge_Extraction_System import KnowledgeExtractionOrchestrator
from .core.orchestrator import KnowledgeExtractionOrchestrator
from .processors.content_extractor import ContentExtractor
from .processors.semantic_processor import SemanticProcessor
from .config.config import config

# Define the public API of the package. When a user writes `from AI_Knowledge_Extraction_System import *`,
# only these names will be imported.
__all__ = [
    "KnowledgeExtractionOrchestrator",
    "ContentExtractor",
    "SemanticProcessor",
    "config"
]