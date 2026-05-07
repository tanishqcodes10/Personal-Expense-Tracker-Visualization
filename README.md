# 💰 Personal Expense Tracker with Data Visualization

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange) ![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 📌 Project Overview
A complete Python-based **Personal Expense Tracker** that simulates real-world expense management using synthetic data, performs multi-dimensional analysis, and generates professional visualizations and reports — without requiring access to any banking system.

## ❓ Problem Statement
Most people have no clear visibility into where their money goes. This project solves that by:
- Organizing expenses by category, month, and payment method
- Identifying overspending patterns
- Generating actionable insights through charts and summary reports

## 🏭 Industry Relevance
| Domain | Use Case |
|---|---|
| Finance | Personal budgeting and savings tracking |
| Data Analysis | EDA on transactional data |
| Business Analyst | KPI dashboards and spend reports |
| Automation | Auto-report generation from CSV data |

## ✨ Features
- 📊 Synthetic 200-record expense dataset generation
- 🧹 Automated data cleaning and preprocessing
- 📂 Category-wise spending analysis
- 📅 Monthly trend analysis
- 💳 Payment method breakdown
- 📈 4 professional data visualizations
- 📄 Auto-generated text + CSV reports

## 🛠️ Tech Stack
- **Python 3.10+**
- **Pandas** — data manipulation
- **NumPy** — numerical operations
- **Matplotlib** — charting
- **Seaborn** — statistical plots
- **CSV** — lightweight data storage
- **datetime** — date parsing

## 📁 Folder Structure
```
Personal-Expense-Tracker-Visualization/
│
├── data/               ← Raw expense CSV
├── src/                ← Modular Python scripts
├── notebooks/          ← Jupyter notebooks
├── outputs/            ← Analysis CSVs
├── images/             ← Generated charts
├── reports/            ← Text summary reports
├── docs/               ← Documentation
├── main.py             ← Entry point
├── requirements.txt    ← Dependencies
├── .gitignore
└── README.md
```

## ⚙️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/Personal-Expense-Tracker-Visualization.git
cd Personal-Expense-Tracker-Visualization

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the project
python main.py
```

## 📊 Sample Output

```
Total Expenses    : Rs. 2,71,123.15
Avg Daily Spend   : Rs. 1,783.70
Highest Category  : Rent
Highest Month     : 2024-08
```

## 🖼️ Screenshots
| Chart | Description |
|---|---|
| `images/category_bar.png` | Category-wise bar chart |
| `images/monthly_line.png` | Monthly trend line chart |
| `images/payment_pie.png`  | Payment method pie chart |
| `images/daily_trend.png`  | Daily spending area chart |

## 🎯 Learning Outcomes
- Real-world CSV data handling with Pandas
- Data cleaning and type conversion
- GroupBy aggregations and statistical summaries
- Multi-chart data visualization with Matplotlib
- Modular Python code architecture
- Automated report generation
- Professional GitHub project structure

## 📜 License
MIT License — free to use and modify.
