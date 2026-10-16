from dashboard_app import create_app, export_dashboard


def test_dash_app_can_be_constructed():
    app = create_app()
    assert app.layout is not None
    assert app.title == "Construction Analytics Dashboard"


def test_static_export(tmp_path):
    output = export_dashboard(tmp_path / "dashboard.html")
    content = output.read_text(encoding="utf-8")
    assert "Construction Analytics" in content
    assert "Synthetic demonstration dataset" in content
