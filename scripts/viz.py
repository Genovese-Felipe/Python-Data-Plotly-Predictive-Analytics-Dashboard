"""Legacy script wrapper for the canonical dashboard CLI."""

from dashboard_app.__main__ import main

if __name__ == "__main__":
    print("Compatibility entrypoint: prefer `python -m dashboard_app`.")
    raise SystemExit(main())
