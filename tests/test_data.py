from pathlib import Path

import pandas as pd
import pytest

from dashboard_app.data import REQUIRED_COLUMNS, generate_projects, load_dataset, validate_projects


def test_generated_data_is_reproducible_and_complete():
    first = generate_projects(rows=80, seed=7)
    second = generate_projects(rows=80, seed=7)
    pd.testing.assert_frame_equal(first, second)
    assert REQUIRED_COLUMNS.issubset(first.columns)


def test_csv_loader_marks_external_source(tmp_path: Path):
    path = tmp_path / "projects.csv"
    generate_projects(rows=60).to_csv(path, index=False)
    dataset = load_dataset(path)
    assert dataset.is_synthetic is False
    assert dataset.source_label == "CSV: projects.csv"


def test_schema_error_is_actionable():
    with pytest.raises(ValueError, match="missing required columns"):
        validate_projects(pd.DataFrame({"project_id": ["x"]}))
