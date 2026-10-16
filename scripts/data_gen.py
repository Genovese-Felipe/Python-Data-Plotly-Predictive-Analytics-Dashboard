"""Generate the canonical sample CSV from any working directory."""

from dashboard_app.data import generate_projects
from dashboard_app.paths import DATA_DIR, ensure_directory


def main() -> None:
    output = ensure_directory(DATA_DIR) / "projects.csv"
    projects = generate_projects()
    projects.to_csv(output, index=False)
    print(f"Generated {len(projects)} synthetic projects at {output}")


if __name__ == "__main__":
    main()
