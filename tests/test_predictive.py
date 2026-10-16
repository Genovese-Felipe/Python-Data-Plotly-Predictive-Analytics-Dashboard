from dashboard_app.data import generate_projects
from dashboard_app.predictive import train_delay_model


def test_predictive_pipeline_uses_holdout_and_enriches_rows():
    frame = generate_projects(rows=120, seed=13)
    result = train_delay_model(frame, seed=13)
    assert result.train_rows == 96
    assert result.test_rows == 24
    assert result.mae_days >= 0
    assert -1 <= result.r2 <= 1
    assert result.projects["predicted_delay_days"].notna().all()
    assert set(result.projects["predicted_risk"]).issubset({"Low", "Medium", "High"})
