"""
Monica AI Capabilities
=====================

Specialized capabilities for the Monica AI Bot System including:
- Knowledge Manager: Document processing and semantic analysis
- Writing Assistant: Content generation and writing support
"""

from .knowledge_manager import KnowledgeManager
from .writing_assistant import WritingAssistant

__all__ = ['KnowledgeManager', 'WritingAssistant']