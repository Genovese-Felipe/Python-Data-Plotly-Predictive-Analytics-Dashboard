"""
Monica AI System
================

A comprehensive AI assistant system designed to provide advanced capabilities
for communication, knowledge management, and development assistance. This system
integrates with various platforms and extends the functionality of the main
data analytics dashboard with AI-powered features.

Key Components:
- `BotManager`: For creating and managing custom AI bots.
- `APIIntegrationFramework`: To connect with external APIs and services.
- `PromptSystem`: For managing and generating sophisticated prompts.
- `PlatformManager`: To handle integrations with different platforms like email and social media.
"""

# The version of the Monica AI System package.
__version__ = "1.0.0"

# The designated author of the package.
__author__ = "Monica AI Team"

# Import key classes to make them directly accessible from the package level.
# e.g., from Monica_AI_System import BotManager
from .core.bot_manager import BotManager
from .core.api_integration import APIIntegrationFramework
from .core.prompt_system import PromptSystem
from .integrations.platform_manager import PlatformManager

# Define the public API of the package. When a user writes `from Monica_AI_System import *`,
# only these names will be imported.
__all__ = [
    'BotManager',
    'APIIntegrationFramework',
    'PromptSystem',
    'PlatformManager'
]