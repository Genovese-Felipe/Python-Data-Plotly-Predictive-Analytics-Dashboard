"""
Core Components Package for the Monica AI System.

This package contains the foundational modules that power the Monica AI Bot
System, including bot management, API integration, and the prompt system.

Key Components:
- `BotManager`: Manages the creation and lifecycle of AI bots.
- `APIIntegrationFramework`: Handles connections to various external APIs.
- `PromptSystem`: Manages and optimizes prompts for the AI models.
"""

from .bot_manager import BotManager
from .api_integration import APIIntegrationFramework
from .prompt_system import PromptSystem

# Define the public API for this package.
__all__ = ['BotManager', 'APIIntegrationFramework', 'PromptSystem']