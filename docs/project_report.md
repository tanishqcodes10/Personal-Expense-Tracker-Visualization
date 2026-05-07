# 📝 Project Report

**Project Title:** Personal Expense Tracker with Data Visualization  
**Technology:** Python, Pandas, Matplotlib, Streamlit  
**Type:** Portfolio / Academic Project  
**Domain:** Data Analysis, Personal Finance, Automation  

---

## 1. Introduction

Managing personal finances is a challenge for students, professionals, and families alike.
Most people have no structured way to track daily expenses or identify overspending patterns.
This project builds a fully automated expense tracking and visualization system using Python.

## 2. Objectives

- Build a Python pipeline to simulate, clean, and analyze expense data
- Generate category-wise, monthly, and payment-method insights
- Visualize findings using professional Matplotlib charts
- Provide an interactive Streamlit dashboard for real-time filtering
- Produce automated summary reports exportable as CSV and text

## 3. Dataset

- **Source:** Synthetically generated using Python (random + NumPy)
- **Size:** 200 expense records
- **Period:** January 2024 – December 2024
- **Columns:** Date, Category, Amount, Payment_Method, Note
- **Categories:** 8 (Food, Transport, Utilities, Entertainment, Healthcare, Shopping, Education, Rent)

## 4. Methodology

### 4.1 Data Generation
Realistic expense amounts per category are drawn from uniform distributions
with category-specific min/max ranges that reflect Indian urban spending patterns.

### 4.2 Data Cleaning
- Date parsing with `pd.to_datetime()`
- Amount coercion with `pd.to_numeric(errors='coerce')`
- Null removal with `.dropna()`
- String normalization with `.str.strip().str.title()`

### 4.3 Analysis
- **Category Analysis:** GroupBy + agg(sum, mean, count) + % share
- **Monthly Analysis:** GroupBy Month Period + sum
- **Payment Analysis:** GroupBy Payment Method + sum
- **Daily Analysis:** GroupBy date + sum

### 4.4 Visualization
Four charts generated with Matplotlib:
1. Horizontal bar chart — category rankings
2. Line + fill chart — monthly trend
3. Donut pie chart — payment method share
4. Area chart — daily granularity

## 5. Key Findings

| Metric | Value |
|--------|-------|
| Total Annual Spend | ₹2,71,123 |
| Avg Daily Spend | ₹1,783 |
| Highest Category | Rent (42.9%) |
| Peak Month | August 2024 |
| Most Used Payment | Debit Card (32.2%) |

## 6. Technologies Used

| Tool | Version | Role |
|------|---------|------|
| Python | 3.10+ | Core language |
| Pandas | 2.0 | Data manipulation |
| NumPy | 1.24 | Random data generation |
| Matplotlib | 3.7 | Visualization |
| Streamlit | 1.30 | Web dashboard |

## 7. Conclusions

This project demonstrates a complete data analysis pipeline from raw data generation
to visual insights and automated reporting. The modular code structure makes it
extensible — future enhancements could include SQLite storage, bank statement parsing,
budget alerts, and Streamlit Cloud deployment.

## 8. Learning Outcomes

- Real-world Pandas GroupBy and aggregation patterns
- Date-time handling in data analysis
- Multi-chart visualization design
- Streamlit dashboard development
- Professional project structuring for GitHub
- Automated report generation
