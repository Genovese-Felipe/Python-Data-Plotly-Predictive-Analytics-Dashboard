"""Synthetic data generation and optional CSV loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_TYPES = ("Residential", "Commercial", "Infrastructure", "Industrial")
STATUSES = ("Planning", "In Progress", "Review", "Completed", "On Hold")

MODEL_FEATURES = (
    "planned_duration_days",
    "budget",
    "team_size",
    "complexity_score",
    "completion_pct",
    "project_type",
)

REQUIRED_COLUMNS = {
    "project_id",
    "project_name",
    "project_type",
    "status",
    "planned_duration_days",
    "budget",
    "team_size",
    "complexity_score",
    "completion_pct",
    "delay_days",
}


@dataclass(frozen=True)
class Dataset:
    """Projects plus transparent source metadata."""

    projects: pd.DataFrame
    source_label: str
    is_synthetic: bool


def generate_projects(rows: int = 240, seed: int = 42) -> pd.DataFrame:
    """Generate a reproducible portfolio suitable for analytics demonstrations."""
    if rows < 40:
        raise ValueError("rows must be at least 40 for a meaningful train/test split")

    rng = np.random.default_rng(seed)
    project_type = rng.choice(PROJECT_TYPES, size=rows, p=[0.34, 0.28, 0.22, 0.16])
    complexity = rng.integers(1, 11, size=rows)
    planned_duration = rng.integers(90, 900, size=rows)
    team_size = rng.integers(4, 48, size=rows)
    budget = rng.integers(180_000, 8_500_000, size=rows)
    completion = np.clip(rng.normal(63, 26, size=rows), 0, 100).round(1)

    type_effect = (
        pd.Series(project_type)
        .map(
            {
                "Residential": 2.0,
                "Commercial": 6.0,
                "Infrastructure": 15.0,
                "Industrial": 10.0,
            }
        )
        .to_numpy()
    )
    schedule_pressure = (
        complexity * 3.4
        + planned_duration * 0.025
        - team_size * 0.72
        - completion * 0.08
        + type_effect
    )
    delay_days = np.rint(schedule_pressure + rng.normal(0, 9, size=rows)).astype(int)
    delay_days = np.clip(delay_days, -25, 120)

    status = np.select(
        [completion >= 97, completion >= 70, completion >= 25, completion < 8],
        ["Completed", "Review", "In Progress", "Planning"],
        default="In Progress",
    )
    hold_mask = (delay_days > 70) & (completion < 70)
    status[hold_mask] = "On Hold"

    start_dates = pd.Timestamp("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 720, size=rows), unit="D"
    )

    frame = pd.DataFrame(
        {
            "project_id": [f"PRJ-{index:04d}" for index in range(1, rows + 1)],
            "project_name": [
                f"{kind} Project {index}" for index, kind in enumerate(project_type, 1)
            ],
            "project_type": project_type,
            "status": status,
            "start_date": start_dates,
            "planned_duration_days": planned_duration,
            "budget": budget,
            "team_size": team_size,
            "complexity_score": complexity,
            "completion_pct": completion,
            "delay_days": delay_days,
        }
    )
    frame["budget_spent"] = (
        frame["budget"] * (frame["completion_pct"] / 100) * rng.uniform(0.82, 1.18, size=rows)
    ).round(2)
    return frame


def validate_projects(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the schema needed by the dashboard and predictive pipeline."""
    missing = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    if missing:
        raise ValueError(f"project data is missing required columns: {', '.join(missing)}")
    if frame.empty:
        raise ValueError("project data must contain at least one row")
    return frame.copy()


def load_dataset(csv_path: str | Path | None = None, rows: int = 240) -> Dataset:
    """Load a user CSV or fall back to the documented synthetic dataset."""
    if csv_path is None:
        return Dataset(generate_projects(rows=rows), "Synthetic demonstration dataset", True)

    path = Path(csv_path).expanduser().resolve()
    frame = pd.read_csv(path)
    return Dataset(validate_projects(frame), f"CSV: {path.name}", False)
