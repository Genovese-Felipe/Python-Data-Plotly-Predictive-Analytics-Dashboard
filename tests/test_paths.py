from dashboard_app.paths import PROJECT_ROOT, resolve_output_path


def test_relative_output_is_anchored_at_project_root():
    path = resolve_output_path("outputs/test-dashboard.html")
    assert path == PROJECT_ROOT / "outputs" / "test-dashboard.html"
