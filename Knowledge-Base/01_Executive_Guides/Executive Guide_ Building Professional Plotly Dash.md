<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Executive Guide: Building Professional Plotly Dash Dashboards with Synthetic Data

This report provides a ready-to-use, eight-step workflow—complete with tested Python scripts, prompting tips, and quality checkpoints—to help beginners produce expert-level interactive dashboards. The included LaTeX file delivers a printable PDF handbook for future reference.

## 1  Overview of the Eight-Step Pipeline

| Step | Goal | Key Outputs |
| :-- | :-- | :-- |
| 1 | Capture a business-grade reference dashboard | Image URL saved for documentation |
| 2 | Draft a concise, open-ended user prompt | One-sentence question driving the story |
| 3 | Design synthetic data schema | ≥ 2 CSV tables mirroring the visual story |
| 4 | Code `data_gen.py` | Reproducible data generator with Faker + NumPy |
| 5 | Code `viz.py` | Dash app containing ≥ 3 complex visuals |
| 6 | Export HTML | Self-contained `dashboard.html` under 1 MB |
| 7 | Screenshot | 1366 × 768 PNG for label-box upload |
| 8 | Upload folder | `data/`, `scripts/`, `outputs/` tree zipped for GCS |

## 2  Prompt Engineering Essentials

### 2.1 Template

```
Role: <domain expert>  
Task: <insight needed>  
Format: <dashboard / KPI / forecast etc.>  
Context: <date-range, regions, constraints>  
```


### 2.2 Best Practices

- Use **action verbs**: *“Compare”, “Forecast”, “Break down”*.
- Avoid strict formatting demands; let the code decide layout.
- Iterate with **chain-of-thought** questions when results misalign.


## 3  Generating High-Quality Synthetic Data

1. **Clean first**: drop or impute nulls before synthesis.
2. **Volume rule**: ≥ 3 000 rows ensures stable visuals.
3. **Privacy**: swap real IDs with `faker.uuid4()`; never copy PII.
4. **Utility test**: train a quick model on synthetic vs. real and compare metrics.

*Tip:* For imbalanced scenarios, oversample minority classes with `sklearn.utils.resample` before writing to CSV.

## 4  Dash App Design Guidelines

### 4.1 Layout \& Story

1. Upper-left: single KPI or indicator (fast cognition).
2. Upper-right: categorical mix (bar or treemap) for context.
3. Bottom: trend + projection (line or area).
4. Keep to **one palette** and max **three chart types** to reduce load.

### 4.2 Code Organization

```
<row_id>/
├─ scripts/
│  ├─ data_gen.py      # data fabrication
│  └─ viz.py           # Dash app
├─ data/               # CSV outputs
└─ outputs/            # HTML + screenshot
```

Split callbacks into `callbacks.py` when apps grow beyond five functions for easier debugging.

## 5  Cross-Check Checklist Before Upload

1. **Lint**: `flake8 *.py` shows zero errors.
2. **Run headless**: `python viz.py` starts without warnings.
3. **Browser test**: open `dashboard.html` in Chrome and Firefox.
4. **Legend boxes**: no overlap with data bars/lines.
5. **File sizes**: HTML < 1 MB, PNG < 500 KB.
6. **Form paths**: copy-paste GCS URLs exactly into the label-box fields.

## 6  Common Pitfalls \& Fixes

| Pitfall | Symptom | Fix |
| :-- | :-- | :-- |
| Silent callbacks | Blank graph | Enable Dash DevTools; check red nodes |
| Oversized HTML | 5 + MB file | `include_plotlyjs='cdn'` in `write_html` |
| Jittery axes | NaNs in data | `df.fillna(method='ffill')` before plotting |
| Slow load | 100 k + rows sent to browser | Aggregate in pandas, down-sample to 5 k |

## 7  Further Learning

- Dash 20-Minute Tutorial (official docs)
- Plotly YouTube series “Dash Best Practices”
- UXPin “Dashboard Design Principles 2025” for modern UX patterns
- YData “Structured Synthetic Data” blog for privacy-safe generation


## 8  Next Steps

1. Clone the provided folder skeleton.
2. Replace the synthetic-data section with your own schema.
3. Swap the figure titles and colour palette to match your company branding.
4. Re-run the eight-step pipeline, export, and upload.

You now have a battle-tested blueprint to deliver professional dashboards—even as a beginner—while meeting the strict technical-instruction checklist. Follow each checkpoint, and your submissions will align with expert standards every time.

<div style="text-align: center">⁂</div>

[^1]: Visual-capabilities-technical-instructions-2.pdf

[^2]: Visual-capabilities-technical-instructions-1.pdf

[^3]: Screenshot_20250705_023748.jpg

[^4]: https://community.plotly.com/t/design-approach-for-large-scale-apps/70394

[^5]: https://plotly.com/python/interactive-html-export/

[^6]: https://github.com/daanknoors/synthetic_data_generation

[^7]: https://www.v7labs.com/blog/prompt-engineering-guide

[^8]: https://community.plotly.com/t/best-practices-to-improve-dash-performance/64883

[^9]: https://stackoverflow.com/questions/50192080/export-plotly-as-self-contained-html-in-javascript

[^10]: https://www.w3resource.com/python-exercises/advanced/python-synthetic-data-generation-tool.php

[^11]: https://botpenguin.com/blogs/techniques-for-effective-ai-prompt-engineering

[^12]: https://community.plotly.com/t/best-practices-in-dash/85078

[^13]: https://github.com/plotly/plotly.py/blob/master/doc/python/interactive-html-export.md

[^14]: https://stackoverflow.com/questions/68087729/python-synthetic-data-generation-by-sampling-column-values-for-a-new-row

[^15]: https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-prompt-engineering/

[^16]: https://community.plotly.com/t/structuring-a-large-dash-application-best-practices-to-follow/62739

[^17]: https://fossies.org/linux/plotly.py/doc/python/interactive-html-export.md

[^18]: https://stackoverflow.com/questions/66668873/pandas-dataframe-synthetic-data-generation/78486242

[^19]: https://www.hostinger.com/tutorials/ai-prompt-engineering

[^20]: https://www.youtube.com/watch?v=JkFyQvQia1U

[^21]: https://stackoverflow.com/questions/60097577/how-to-export-a-plotly-dashboard-app-into-a-html-standalone-file-to-share-with-t

[^22]: https://cookbook.openai.com/examples/sdg1

[^23]: https://cloud.google.com/discover/what-is-prompt-engineering

[^24]: https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash

[^25]: https://www.numberanalytics.com/blog/plotly-for-data-storytelling

[^26]: https://research.aimultiple.com/synthetic-data-generation/

[^27]: https://www.rib-software.com/en/blogs/bi-dashboard-design-principles-best-practices

[^28]: https://dash.plotly.com/tutorial

[^29]: https://www.youtube.com/watch?v=tj_7_5SdrE0

[^30]: https://www.reddit.com/r/Python/comments/1c7tkg1/project_an_interactive_python_dashboard_for_data/

[^31]: https://docs.gretel.ai/create-synthetic-data/safe-synthetics/evaluate/tips-improve-synthetic-data-accuracy

[^32]: https://asana.com/pt/resources/executive-dashboard

[^33]: https://www.youtube.com/watch?v=XOFrvzWFM7Y

[^34]: https://johnloewen.substack.com/p/the-art-of-data-storytelling-an-actionable-guide-with-python-plotly-aa1e6e75ced6

[^35]: https://dev.to/rahulbhave/using-faker-and-pandas-python-libraries-to-create-synthetic-data-for-testing-4gn4

[^36]: https://www.uxpin.com/studio/blog/dashboard-design-principles/

[^37]: https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4/

[^38]: https://community.plotly.com/t/dash-callbacks-best-practice/51167

[^39]: https://plotly.com

[^40]: https://ydata.ai/resources/synthetic-data-generation-best-practices

[^41]: https://www.qlik.com/us/dashboard-examples/dashboard-design

[^42]: https://www.youtube.com/watch?v=Qx5eFVUdDxk

[^43]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/14664039951ec64781e0c3b99c15a214/259376fa-798b-4292-ba21-a6551afa9979/fd9d19dc.tex

