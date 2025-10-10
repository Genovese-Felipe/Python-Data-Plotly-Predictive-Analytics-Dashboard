"""
Integrations Package for the Monica AI System.

This package contains modules responsible for connecting the Monica AI System
with various external platforms and services, such as email clients, social
media, and other third-party applications.

Key Components:
- `PlatformManager`: Manages communication and integration with different platforms.
"""

from .platform_manager import PlatformManager

# Define the public API for this package.
__all__ = ['PlatformManager']