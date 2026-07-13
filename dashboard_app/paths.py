"""Path helpers that are independent from the caller's working directory."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def ensure_directory(path: Path) -> Path:
    """Create *path* and return it for fluent use."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_output_path(value: str | Path) -> Path:
    """Resolve a user path, anchoring relative paths at the project root."""
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    ensure_directory(path.parent)
    return path
