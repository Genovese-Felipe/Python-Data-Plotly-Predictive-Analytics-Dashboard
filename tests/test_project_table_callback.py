"""Regression guard for the Dash project table callback contract.

The component with id="project-table" is an html.Div; the callback must
update children, not a nonexistent data property.
"""
from dashboard_app.app import create_app


def test_project_table_callback_targets_children():
    app = create_app()
    callback_outputs = " | ".join(app.callback_map)
    assert "project-table.children" in callback_outputs
    assert "project-table.data" not in callback_outputs
