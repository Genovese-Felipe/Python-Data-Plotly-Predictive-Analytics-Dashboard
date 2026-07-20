from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import PillowWriter
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "media_audit" / "data" / "github_audit.json"
OUT = ROOT / "outputs" / "audit"
OUT.mkdir(parents=True, exist_ok=True)


def load_data():
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    periods = pd.DataFrame(payload["periods"])
    commits = pd.DataFrame(payload["commits"])
    commits["created_at"] = pd.to_datetime(commits["created_at"], utc=True)
    return periods, commits, payload["metadata"]


def month_series(commits):
    if commits.empty:
        return pd.DataFrame({"month": [], "commits": []})
    return (
        commits.assign(month=commits["created_at"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .size()
        .rename(columns={"size": "commits"})
    )


def write_xlsx(periods, commits, metadata):
    path = OUT / "prediction_performance_dossier.xlsx"
    commits_excel = commits.copy()
    commits_excel["created_at"] = commits_excel["created_at"].dt.tz_localize(None)
    feedback = pd.DataFrame(
        [
            [
                "Modernização melhorou a execução",
                "confirmed",
                "CI verde em Python 3.10/3.12; 7 testes; exportação e HTTP 200.",
                0.95,
            ],
            [
                "Houve atividade nos últimos 7 dias",
                "not_observed",
                "Nenhum commit entre 13/07/2026 e 20/07/2026.",
                0.90,
            ],
            [
                "O histórico de 16 meses está completo",
                "partial",
                "Consulta limitada aos 100 commits mais recentes.",
                0.70,
            ],
        ],
        columns=["claim", "status", "evidence", "confidence"],
    )
    governance = pd.DataFrame(
        [
            ["Proveniência", "GitHub commit metadata", "Alta", metadata["retrieved_at"]],
            ["Cobertura", "100 commits; 2025-07-29 a 2025-08-27", "Média", "Expandir paginação"],
            [
                "Interpretação",
                "Ausência de commit não prova ausência de trabalho",
                "Alta",
                "Não converter zero em produtividade",
            ],
            ["Multimídia", "GIF/MP4 são visualizações derivadas", "Alta", "Rotular como derivado"],
        ],
        columns=["dimension", "finding", "risk_level", "next_control"],
    )
    media_plan = pd.DataFrame(
        [
            ["GIF", "Evolução cumulativa por mês", "Leitura rápida", "Derivado de commits"],
            [
                "MP4",
                "Narrativa temporal com KPI e cobertura",
                "Apresentação",
                "Derivado de commits",
            ],
            ["PNG", "Mapa de cobertura por janela", "Relatório/PDF", "Derivado de commits"],
            ["Dash", "Filtro por período e evidência", "Exploração", "Dados atualizáveis"],
        ],
        columns=["asset", "story", "use_case", "provenance"],
    )
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        periods.to_excel(writer, sheet_name="Periods", index=False)
        commits_excel.to_excel(writer, sheet_name="Commits", index=False)
        feedback.to_excel(writer, sheet_name="Feedback", index=False)
        governance.to_excel(writer, sheet_name="Governance", index=False)
        media_plan.to_excel(writer, sheet_name="MediaPlan", index=False)
    return path


def write_pdf(periods, commits, metadata):
    path = OUT / "prediction_performance_dossier.pdf"
    monthly = month_series(commits)
    with PdfPages(path) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        fig.text(0.06, 0.85, "Prediction-performance dossier", fontsize=24, weight="bold")
        fig.text(
            0.06, 0.76, "Auditoria multimídia baseada em evidência do histórico GitHub", fontsize=14
        )
        fig.text(0.06, 0.64, f"Repositório: {metadata['repository']}", fontsize=10)
        fig.text(0.06, 0.59, f"Data de corte: {metadata['as_of']}", fontsize=10)
        fig.text(
            0.06,
            0.50,
            f"Registros observados: {len(commits)} commits",
            fontsize=16,
            color="#174A7E",
        )
        fig.text(
            0.06, 0.38, "Ausência de commits não equivale a ausência de trabalho.", fontsize=11
        )
        fig.text(
            0.06, 0.30, "GIFs, MP4s e gráficos são derivados dos dados primários.", fontsize=11
        )
        plt.axis("off")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        colors = [
            "#8C98A4" if s == "no_evidence" else "#D89B3D" for s in periods["coverage_status"]
        ]
        ax.bar(periods["period"], periods["commit_count"], color=colors)
        ax.set_title("Commits observados por janela temporal")
        ax.set_ylabel("Quantidade de commits")
        ax.grid(axis="y", alpha=0.25)
        for i, row in periods.iterrows():
            ax.text(
                i,
                row["commit_count"] + 1,
                row["coverage_status"],
                ha="center",
                fontsize=8,
                rotation=45,
            )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        if monthly.empty:
            ax.text(0.5, 0.5, "Sem dados mensais observados", ha="center")
        else:
            ax.plot(monthly["month"], monthly["commits"], marker="o", color="#174A7E", linewidth=3)
            ax.set_ylabel("Commits")
            ax.set_title("Concentração temporal da atividade observada")
            ax.tick_params(axis="x", rotation=45)
            ax.grid(alpha=0.25)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        ax.axis("off")
        notes = [
            "Confirmado: PR de modernização passou no CI em Python 3.10 e 3.12.",
            "Não confirmado: atividade recente fora do histórico consultado.",
            "Acerto: separar núcleo mantido de legado, adicionar testes e documentar limites.",
            "Correção: lint inicialmente alcançava scripts legados; o CI foi ajustado.",
            "Próximo controle: paginação completa e ingestão opcional de issues, PRs e releases.",
        ]
        ax.text(
            0.03, 0.92, "Feedback, acertos, erros e próximos controles", fontsize=18, weight="bold"
        )
        ax.text(0.03, 0.82, "\n\n".join(notes), va="top", fontsize=13, wrap=True)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    return path


def write_media(periods, commits):
    monthly = month_series(commits)
    png = OUT / "coverage_timeline.png"
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(periods["period"], periods["commit_count"], color="#174A7E")
    ax.set_title("Cobertura observada do histórico GitHub")
    ax.set_ylabel("Commits")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(png, dpi=180)
    plt.close(fig)

    frames = max(len(monthly), 1)
    fig, ax = plt.subplots(figsize=(10, 6))

    def draw(frame):
        ax.clear()
        ax.set_ylim(0, max(int(monthly["commits"].max()) + 5, 10) if not monthly.empty else 10)
        if monthly.empty:
            ax.text(0.5, 0.5, "Sem observações", ha="center", va="center")
        else:
            current = monthly.iloc[: frame + 1]
            ax.bar(current["month"], current["commits"], color="#D89B3D")
            ax.set_title(f"Atividade observada até {current.iloc[-1]['month']}")
            ax.set_ylabel("Commits")
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()

    clip = OUT / "github_activity.mp4"
    gif = OUT / "github_activity.gif"
    ani = animation.FuncAnimation(fig, draw, frames=frames, interval=900, repeat=False)
    ani.save(clip, writer=animation.FFMpegWriter(fps=1))
    ani.save(gif, writer=PillowWriter(fps=1))
    plt.close(fig)
    return png, gif, clip


def main():
    os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".matplotlib"))
    periods, commits, metadata = load_data()
    paths = [
        write_xlsx(periods, commits, metadata),
        write_pdf(periods, commits, metadata),
        *write_media(periods, commits),
    ]
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
