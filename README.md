# Python-Data-Plotly-Predictive-Analytics-Dashboard

This repository contains a multifaceted project that combines a professional, interactive construction project management dashboard with a sophisticated AI-powered knowledge processing system named Monica AI.

## Table of Contents

- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Setup and Installation](#-setup-and-installation)
- [Usage](#-usage)
  - [Construction Dashboard](#-construction-dashboard)
  - [Monica AI System](#-monica-ai-system)
- [Documentation](#-documentation)

## ✨ Key Features

### Construction Dashboard
- **Interactive Visualizations**: Dynamic and responsive charts built with Plotly and Dash.
- **Comprehensive Filtering**: Filter projects by type, manager, and other attributes.
- **Key Performance Indicators (KPIs)**: At-a-glance metrics for budget utilization, project duration, and status.
- **Professional Design**: A clean, well-organized layout suitable for professional presentations.

### Monica AI System
- **Advanced Knowledge Extraction**: Processes documents from a local knowledge base to extract semantic information.
- **Web Search Integration**: Augments local knowledge with real-time web search results from DuckDuckGo.
- **Multi-Query Processing**: Handles multiple user queries simultaneously, maintaining context for more accurate responses.
- **Comprehensive Analysis**: Synthesizes information from all sources to provide actionable insights and recommendations.

## 📂 Project Structure

The repository is organized into two main parts: the AI system and the dashboard scripts.

```
/
├── AI_Knowledge_Extraction_System/   # The Monica AI System
│   ├── core/                         # Core logic for orchestration and query handling
│   ├── processors/                   # Modules for content, semantic, and web processing
│   ├── config/                       # Configuration files
│   ├── monica_ai_interface.py        # Main API for the AI system
│   └── run_monica_ai.py              # Script to run the AI system
│
├── scripts/                          # Scripts for the dashboard
│   ├── viz_new.py                    # Main construction dashboard visualization script
│   └── ...
│
├── final_dashboard.py                # A complete, standalone dashboard example
├── run_dashboard.py                  # Runner script for the construction dashboard
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 셋업 및 설치

To get started with this project, you'll need to have Python 3.8 or higher installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
    cd Python-Data-Plotly-Predictive-Analytics-Dashboard
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 사용법

This project has two main components that can be run independently: the Construction Dashboard and the Monica AI System.

### 🏗️ Construction Dashboard

The primary construction dashboard provides a detailed, interactive view of project management data.

**To run the main dashboard:**
```bash
python run_dashboard.py
```
The dashboard will be available at `http://127.0.0.1:8050/`.

#### Other Dashboards

This repository also contains other standalone dashboard examples:
-   `final_dashboard.py`: A complete, professional dashboard with a different design.
-   `simple_dashboard.py`: A basic sales dashboard with KPI cards and filters.
-   `working_dashboard.py`: An intermediate version of the project dashboard.

To run any of these, simply execute the script directly:
```bash
python simple_dashboard.py
```

### 🤖 Monica AI System

The Monica AI System is a powerful tool for knowledge extraction and analysis. It can be run from the command line or used as a Python module.

#### Command-Line Usage

Navigate to the `AI_Knowledge_Extraction_System` directory to run the following commands:
```bash
cd AI_Knowledge_Extraction_System
```

-   **Run a comprehensive analysis with default queries:**
    ```bash
    python run_monica_ai.py
    ```

-   **Run in interactive mode to enter your own queries:**
    ```bash
    python run_monica_ai.py --custom
    ```

-   **Run with specific, one-off queries:**
    ```bash
    python run_monica_ai.py --queries "AI in construction" "data visualization trends"
    ```

-   **Run a basic functionality test:**
    ```bash
    python run_monica_ai.py --test
    ```

Analysis results, including a summary report and detailed JSON output, will be saved in the `AI_Knowledge_Extraction_System/outputs/monica_ai_results/` directory.

#### Programmatic Usage

You can also integrate the Monica AI system into your own Python scripts by using the `MonicaAIInterface`.

```python
from AI_Knowledge_Extraction_System.monica_ai_interface import MonicaAIInterface

# Initialize the interface
monica_ai = MonicaAIInterface()

# Define your queries
my_queries = [
    "How to integrate AI with Plotly Dash?",
    "Best practices for predictive analytics dashboards"
]

# Run the analysis
results = monica_ai.run_comprehensive_analysis(custom_queries=my_queries)

# Print the top-level recommendations
recommendations = results['monica_ai_analysis']['actionable_recommendations']
for rec in recommendations:
    print(f"- {rec['action']} (Priority: {rec['priority']})")
```

## 📄 Documentation

The codebase is thoroughly documented with Google-style Python docstrings. For a deeper understanding of any module, class, or function, please refer directly to the source code.