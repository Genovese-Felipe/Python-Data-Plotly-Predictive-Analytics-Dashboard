"""Command-line entrypoint for serving or exporting the dashboard."""

from __future__ import annotations

import argparse

from . import create_app, export_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Construction analytics dashboard")
    parser.add_argument("--data", help="Optional CSV using the documented project schema")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8050)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--export", metavar="PATH", help="Export a static HTML snapshot and exit")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.export:
        output = export_dashboard(args.export, csv_path=args.data)
        print(f"Dashboard exported to {output}")
        return 0

    app = create_app(csv_path=args.data)
    print(f"Dashboard available at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
