"""Canonical application package for the construction analytics dashboard."""

from __future__ import annotations

__version__ = "2.0.0"


def create_app(*args, **kwargs):
    """Create the Dash application without importing Dash at package import time."""
    from .app import create_app as app_factory

    return app_factory(*args, **kwargs)


def export_dashboard(*args, **kwargs):
    """Export the canonical static dashboard snapshot."""
    from .exporter import export_dashboard as exporter

    return exporter(*args, **kwargs)
