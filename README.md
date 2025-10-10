# Python-Data-Plotly-Predictive-Analytics-Dashboard

This repository contains a professional construction project management dashboard and an AI-powered knowledge processing system, Monica AI. The dashboard is built with Python and Plotly for interactive data visualization, while Monica AI leverages local and web-based knowledge for intelligent analysis.

🌐 **Live Site**: [View on GitHub Pages](https://genovese-felipe.github.io/Python-Data-Plotly-Predictive-Analytics-Dashboard/)

## 🚀 Key Features

- **Interactive Dashboards**: Dynamic and responsive dashboards built with Plotly and Dash.
- **AI-Powered Knowledge System**: Monica AI combines local documentation with web search for advanced analysis.
- **Construction-Focused Analytics**: The main dashboard is tailored for construction project management.
- **Modular and Extendable**: The repository is organized into distinct modules for dashboards and AI, making it easy to extend.

## 📂 Repository Structure

```
.
├── AI_Knowledge_Extraction_System/ # Monica AI source code
├── data/                           # Sample CSV data for dashboards
├── docs/                           # Documentation and GitHub Pages site
├── outputs/                        # Output files, such as generated dashboards
├── scripts/                        # Data generation and visualization scripts
├── final_dashboard.py              # Main interactive dashboard application
├── run_dashboard.sh                # Script to run the main dashboard
└── requirements.txt                # Python dependencies
```

## 🛠️ Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
   cd Python-Data-Plotly-Predictive-Analytics-Dashboard
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

##  usage

### 📊 Running the Dashboards

There are several dashboards in this repository. Here is how to run the main one:

1. **Run `final_dashboard.py`**:
   ```bash
   python final_dashboard.py
   ```
   This will start a local server, and you can view the dashboard in your web browser at `http://127.0.0.1:8050`.

2. **Run the construction dashboard**:
   ```bash
   python run_construction_dashboard.py
   ```
   This script runs a more specific dashboard focused on construction data.

### 🤖 Using Monica AI

Monica AI is a powerful tool for knowledge extraction and analysis. You can run it from the command line.

1. **Navigate to the Monica AI directory**:
   ```bash
   cd AI_Knowledge_Extraction_System
   ```

2. **Run Monica AI**:
   - **With default queries**:
     ```bash
     python run_monica_ai.py
     ```
   - **With custom queries**:
     ```bash
     python run_monica_ai.py --queries "data visualization" "project management"
     ```
   - **In interactive mode**:
     ```bash
     python run_monica_ai.py --custom
     ```

## ✨ Key Technologies

- **Python**: The core programming language.
- **Plotly & Dash**: For creating interactive dashboards.
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical operations.