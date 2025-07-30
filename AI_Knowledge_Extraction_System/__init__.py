"""
AI Knowledge Extraction System
Expert-level content processing and semantic analysis for Knowledge-Base materials
"""

__version__ = "1.0.0"
__author__ = "AI Knowledge Extraction System"

from .core.orchestrator import KnowledgeExtractionOrchestrator
from .processors.content_extractor import ContentExtractor
from .processors.semantic_processor import SemanticProcessor
from .config.config import config

__all__ = [
    "KnowledgeExtractionOrchestrator",
    "ContentExtractor", 
    "SemanticProcessor",
    "config"
]