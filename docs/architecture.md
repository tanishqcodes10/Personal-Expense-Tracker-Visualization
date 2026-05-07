# 🏗️ Project Architecture

## System Overview

This project follows a classic ETL + EDA pipeline pattern used in real-world data analytics.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                           │
│   Date | Category | Amount | Payment Method | Note          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       STORAGE LAYER                          │
│                   data/expenses.csv                          │
│         (200 records, 5 columns, full year 2024)             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     PROCESSING LAYER                         │
│  ┌─────────────────┐   ┌──────────────────┐                 │
│  │  Data Cleaning  │   │  Data Analysis   │                 │
│  │ - Parse dates   │   │ - GroupBy Cat    │                 │
│  │ - Remove nulls  │──▶│ - GroupBy Month  │                 │
│  │ - Fix types     │   │ - GroupBy Method │                 │
│  │ - Normalize str │   │ - Daily agg      │                 │
│  └─────────────────┘   └──────────────────┘                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                        │
│  category_bar.png | monthly_line.png | payment_pie.png       │
│  daily_trend.png  | Streamlit Dashboard (app.py)            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                            │
│  reports/expense_report_2024.txt                             │
│  outputs/category_summary.csv                                │
│  outputs/monthly_summary.csv                                 │
│  outputs/payment_summary.csv                                 │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **generate_expenses()** → creates synthetic CSV with realistic Indian rupee amounts
2. **load_and_clean()** → parses, validates, and normalizes the raw CSV
3. **category_analysis()** → GroupBy Category → sum, mean, count, % share
4. **monthly_analysis()** → GroupBy Month Period → sum
5. **payment_analysis()** → GroupBy Payment Method → sum
6. **daily_analysis()** → GroupBy Date → sum
7. **plot_*()** → Matplotlib charts saved to images/
8. **generate_report()** → writes .txt and .csv outputs

## Module Responsibilities

| Module | File | Responsibility |
|--------|------|----------------|
| Data Generator | main.py | Creates synthetic expense records |
| Data Cleaner | main.py | Validates and normalizes data |
| Analyzer | main.py | Aggregates and computes metrics |
| Visualizer | main.py | Renders and saves charts |
| Report Engine | main.py | Exports text and CSV reports |
| Dashboard | app.py | Interactive Streamlit web UI |
