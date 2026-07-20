# Multimedia Audit Service

Este pacote transforma metadados públicos de commits do GitHub em artefatos de auditoria com rastreabilidade:

- outputs/audit/prediction_performance_dossier.xlsx
- outputs/audit/prediction_performance_dossier.pdf
- outputs/audit/coverage_timeline.png
- outputs/audit/audit_cover.png
- outputs/audit/github_activity.gif
- outputs/audit/github_activity.mp4
- app Dash com callbacks: python -m media_audit.dashboard

As janelas são 7 dias, 15 dias, 1/2/3/4/6/8/9/12/16 meses e os marcos de 4/8/12/16 meses. Os dados não são um medidor completo de produtividade: registros ausentes são marcados como no_evidence, nunca como prova de que nada aconteceu.

