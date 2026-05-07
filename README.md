# 💎 Personal Expense Tracker Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.14-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-22c55e?style=for-the-badge)

**A full-stack Python data analytics project that tracks, analyzes, and visualizes personal expenses through a premium dark-themed interactive dashboard.**

[🚀 View Dashboard](#how-to-run) · [📊 See Charts](#screenshots) · [📁 Explore Docs](docs/)

</div>

---

## 📌 Project Overview

Personal Expense Tracker Pro is a complete end-to-end data analytics pipeline built with Python. It simulates real-world personal finance tracking using a synthetic 200-record expense dataset spanning all 12 months of 2024. The project covers everything from raw data generation and cleaning to interactive visualization and automated report generation — without requiring access to any banking system.

---

## ❓ Problem Statement

Most people have no structured visibility into where their money goes each month. Without tracking:
- Overspending goes unnoticed until it's too late
- Budgeting decisions are based on guesswork
- Financial patterns across categories and months remain hidden

This project solves that by building an automated expense analysis system that turns raw transaction data into clear, actionable insights.

---

## 🏭 Industry Relevance

| Role | How This Project Applies |
|---|---|
| 🐍 Python Developer | Modular pipeline, OOP-style functions, file I/O, automation |
| 📊 Data Analyst | EDA, GroupBy aggregations, trend analysis, KPI reporting |
| 💼 Business Analyst | Spend breakdowns, category insights, monthly KPIs |
| ⚙️ Automation Engineer | Auto data generation, cleaning, report export pipeline |
| 💰 Finance Domain | Budgeting logic, payment analysis, overspending detection |

---

## ✨ Features

### 🖥️ Premium Streamlit Dashboard (`app.py`)
- **Dark glassmorphism UI** with gradient KPI cards and Inter font
- **5 KPI Metric Cards** — Total Spend, Avg Monthly, Avg Daily, Top Category, Transactions
- **6 Interactive Plotly Charts** — all with hover tooltips, zoom, and pan
- **Sidebar Filters** — filter by Category, Payment Method, Month Range, Amount Range
- **Add Expense Form** — live sidebar form to log new transactions
- **Smart Insight Pills** — 6 auto-generated insights from filtered data
- **Export Button** — download filtered data as CSV instantly

### ⚙️ CLI Data Pipeline (`main.py`)
- Synthetic 200-record expense dataset generation with realistic Indian ₹ amounts
- Automated data cleaning — date parsing, null removal, type coercion, string normalization
- Category-wise analysis — total, average, count, % share
- Monthly trend analysis across all 12 months of 2024
- Payment method breakdown — Cash, UPI, Credit Card, Debit Card
- Daily spending aggregation
- Auto-generated text report + 3 summary CSVs
- 4 static Matplotlib charts saved to `images/`

---

## 📊 Dashboard Charts

| # | Chart | Type | Insight |
|---|---|---|---|
| 1 | Category-wise Spending | Horizontal Gradient Bar | Ranks all 8 categories by total spend |
| 2 | Payment Method Share | Donut Pie | Shows % split across Cash, UPI, Cards |
| 3 | Monthly Spending Trend | Line + Fill + Peak Annotation | Reveals seasonal patterns |
| 4 | Spending by Day of Week | Gradient Bar | Identifies highest-spend weekdays |
| 5 | Daily Spending Trend | Area Chart | Day-by-day granularity across 2024 |
| 6 | Top 5 Categories Share | Stacked Horizontal Bar | % contribution of top spenders |

---

## 📈 Sample Results (2024 Dataset)

```
──────────────────────────────────────────────
  ANNUAL EXPENSE SUMMARY — 2024
──────────────────────────────────────────────
  Total Spend        :  ₹2,71,123
  Avg Monthly Spend  :  ₹22,593
  Avg Daily Spend    :  ₹1,783
  Highest Category   :  Rent  (42.9%)
  Peak Month         :  August 2024
  Most Used Payment  :  Debit Card (32.2%)
  Total Transactions :  200
──────────────────────────────────────────────

  CATEGORY BREAKDOWN:
  Rent            ₹1,16,379   (42.9%)
  Education       ₹ 67,166   (24.8%)
  Healthcare      ₹ 22,727    (8.4%)
  Shopping        ₹ 20,283    (7.5%)
  Utilities       ₹ 17,446    (6.4%)
  Entertainment   ₹ 14,449    (5.3%)
  Food            ₹  8,151    (3.0%)
  Transport       ₹  4,517    (1.7%)
```

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core language |
| Pandas | 2.0 | Data manipulation, GroupBy, aggregation |
| NumPy | 1.24 | Synthetic data generation |
| Plotly | 5.14 | Interactive dashboard charts |
| Streamlit | 1.30 | Web dashboard framework |
| Matplotlib | 3.7 | Static CLI chart generation |
| Seaborn | 0.12 | Statistical chart support |
| CSV / datetime | stdlib | Data storage and date handling |

---

## 📁 Folder Structure

```
Personal-Expense-Tracker-Visualization/
│
├── data/
│   └── expenses.csv              ← 200-record synthetic expense dataset
│
├── src/                          ← Modular Python scripts
│
├── notebooks/                    ← Jupyter exploration notebooks
│
├── outputs/
│   ├── category_summary.csv      ← Category-wise aggregation
│   ├── monthly_summary.csv       ← Monthly totals
│   └── payment_summary.csv       ← Payment method totals
│
├── images/
│   ├── dashboard_overview.png    ← Full dashboard screenshot
│   ├── category_bar.png          ← Category chart
│   ├── monthly_trend.png         ← Monthly line chart
│   ├── payment_pie.png           ← Payment donut chart
│   ├── weekday_bar.png           ← Weekday bar chart
│   └── daily_trend.png           ← Daily area chart
│
├── reports/
│   └── expense_report_2024.txt   ← Auto-generated annual summary
│
├── docs/
│   ├── architecture.md           ← System design + data flow diagram
│   ├── data_dictionary.md        ← Column definitions + schema
│   ├── setup_guide.md            ← Step-by-step installation guide
│   ├── project_report.md         ← Full academic project report
│   └── api_reference.md          ← All functions documented
│
├── app.py                        ← 💎 Premium Streamlit dashboard
├── main.py                       ← ⚙️  CLI pipeline entry point
├── requirements.txt              ← All dependencies
├── .gitignore                    ← Excludes venv, pycache, etc.
└── README.md                     ← You are here
```

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Personal-Expense-Tracker-Visualization.git
cd Personal-Expense-Tracker-Visualization
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run CLI Pipeline (charts + report)
```bash
python main.py
```

### 5. Run Premium Dashboard
```bash
streamlit run app.py
```
Opens automatically at **http://localhost:8501** 🚀

---

## 🖼️ Screenshots

### 💎 Full Dashboard
![Dashboard Overview](images/dashboard_overview.png)

### 📊 Category-wise Spending
![Category Chart](images/category_bar.png)

### 📈 Monthly Spending Trend
![Monthly Trend](images/monthly_trend.png)

### 💳 Payment Method Distribution
![Payment Pie](images/payment_pie.png)

---

## 📚 Documentation

| Document | Description |
|---|---|
| [🏗️ Architecture](docs/architecture.md) | System design diagram and data flow |
| [📖 Data Dictionary](docs/data_dictionary.md) | Column definitions and data schema |
| [⚙️ Setup Guide](docs/setup_guide.md) | Full installation and run instructions |
| [📝 Project Report](docs/project_report.md) | Academic-style project report |
| [🔧 API Reference](docs/api_reference.md) | Every function documented with examples |

---

## 🎯 Learning Outcomes

- ✅ Real-world CSV data handling with Pandas
- ✅ Data cleaning — type coercion, null handling, string normalization
- ✅ GroupBy aggregations and multi-metric analysis
- ✅ Interactive data visualization with Plotly
- ✅ Premium Streamlit dashboard with custom CSS
- ✅ Dark theme UI design with glassmorphism styling
- ✅ Automated report generation (text + CSV)
- ✅ Modular Python code architecture
- ✅ Professional GitHub project structure and documentation

---

## 🗓️ Development Timeline

| Day | Task |
|---|---|
| Day 1 | Project setup, virtual environment, folder structure |
| Day 2 | Synthetic expense dataset generation |
| Day 3 | Data cleaning and category/monthly analysis |
| Day 4 | Category and monthly Matplotlib charts |
| Day 5 | Payment pie, daily trend, Plotly migration |
| Day 6 | Premium Streamlit dashboard + documentation |

---

