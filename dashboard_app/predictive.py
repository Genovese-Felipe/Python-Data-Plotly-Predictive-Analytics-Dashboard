"""Reproducible predictive demonstration for project schedule delay."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .data import MODEL_FEATURES, validate_projects

NUMERIC_FEATURES = [
    "planned_duration_days",
    "budget",
    "team_size",
    "complexity_score",
    "completion_pct",
]
CATEGORICAL_FEATURES = ["project_type"]


@dataclass(frozen=True)
class PredictionResult:
    """Fitted model, evaluated metrics and enriched project records."""

    model: Pipeline
    projects: pd.DataFrame
    mae_days: float
    r2: float
    train_rows: int
    test_rows: int


def _risk_band(predicted_delay: pd.Series) -> pd.Series:
    return pd.cut(
        predicted_delay,
        bins=[-np.inf, 10, 35, np.inf],
        labels=["Low", "Medium", "High"],
    ).astype(str)


def train_delay_model(frame: pd.DataFrame, seed: int = 42) -> PredictionResult:
    """Train and evaluate a delay model with an explicit holdout set."""
    projects = validate_projects(frame)
    if len(projects) < 40:
        raise ValueError("at least 40 rows are required to train the predictive demo")

    features = projects[list(MODEL_FEATURES)]
    target = projects["delay_days"]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=seed,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", NUMERIC_FEATURES),
            (
                "category",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=160,
                    max_depth=9,
                    min_samples_leaf=2,
                    random_state=seed,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    test_prediction = model.predict(x_test)

    enriched = projects.copy()
    enriched["predicted_delay_days"] = model.predict(features).round(1)
    enriched["predicted_risk"] = _risk_band(enriched["predicted_delay_days"])
    return PredictionResult(
        model=model,
        projects=enriched,
        mae_days=float(mean_absolute_error(y_test, test_prediction)),
        r2=float(r2_score(y_test, test_prediction)),
        train_rows=len(x_train),
        test_rows=len(x_test),
    )
