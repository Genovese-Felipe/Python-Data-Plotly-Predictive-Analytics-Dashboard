"""Compatibility entrypoint for the canonical dashboard application."""

from dashboard_app import create_app

app = create_app()
server = app.server


if __name__ == "__main__":
    print("Compatibility entrypoint: prefer `python -m dashboard_app`.")
    app.run(host="127.0.0.1", port=8050, debug=False)
