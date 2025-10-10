"""
Capabilities Package for the Monica AI System.

This package contains modules that define the specialized skills and
capabilities of the Monica AI bots, such as knowledge management and
writing assistance.

Key Components:
- `KnowledgeManager`: Provides functionalities for document processing and analysis.
- `WritingAssistant`: Offers support for content generation and writing tasks.
"""

from .knowledge_manager import KnowledgeManager
from .writing_assistant import WritingAssistant

# Define the public API for this package.
__all__ = ['KnowledgeManager', 'WritingAssistant']