"""
Configuration Package for the Monica AI System.

This package provides centralized access to all configuration settings and
parameters for the Monica AI Bot System, making it easy to manage and
customize the system's behavior.

Key Components:
- `get_config`: A function to retrieve configuration values.
- `update_config`: A function to update configuration settings at runtime.
- `MONICA_CONFIG`: A dictionary with general settings for the Monica AI system.
- `BOT_CONFIG`: A dictionary with default settings for AI bots.
"""

from .settings import get_config, update_config, MONICA_CONFIG, BOT_CONFIG

# Define the public API for this package.
__all__ = ['get_config', 'update_config', 'MONICA_CONFIG', 'BOT_CONFIG']