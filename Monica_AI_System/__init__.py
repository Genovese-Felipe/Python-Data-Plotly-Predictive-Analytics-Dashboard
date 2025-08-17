"""
Monica AI Bot System
====================

A comprehensive AI assistant system with advanced capabilities including:
- Custom bot creation and management
- Multi-platform integration (Gmail, Outlook, YouTube, Social Media)
- Intelligent writing and communication assistance
- Advanced search and analysis capabilities
- Knowledge management and semantic enrichment
- Full-stack development companion features

This system extends the existing Python Data Analytics Dashboard with AI capabilities.
"""

__version__ = "1.0.0"
__author__ = "Monica AI Team"

from .core.bot_manager import BotManager
from .core.api_integration import APIIntegrationFramework
from .core.prompt_system import PromptSystem
from .integrations.platform_manager import PlatformManager

__all__ = [
    'BotManager',
    'APIIntegrationFramework', 
    'PromptSystem',
    'PlatformManager'
]