#!/usr/bin/env python3
"""
Personal Expense Tracker with Data Visualization
================================================
Author   : [Your Name]
Date     : 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import random
from datetime import datetime, timedelta

# ── CONFIGURATION ──────────────────────────────────────────
DATA_PATH   = "data/expenses.csv"
OUTPUT_DIR  = "outputs/"
REPORTS_DIR = "reports/"
IMAGES_DIR  = "images/"

for d in [OUTPUT_DIR, REPORTS_DIR, IMAGES_DIR, "data"]:
    os.makedirs(d, exist_ok=True)

# ── PHASE 1: GENERATE SYNTHETIC DATASET ────────────────────
def generate_expenses(n=200, seed=42):
    """Creates a realistic synthetic expense CSV."""
    random.seed(seed)
    np.random.seed(seed)

    categories     = ["Food","Transport","Utilities","Entertainment",
                      "Healthcare","Shopping","Education","Rent"]
    payment_methods = ["Cash","UPI","Credit Card","Debit Card"]
    notes = {
        "Food":          ["Lunch at canteen","Groceries","Dinner outside","Breakfast","Coffee"],
        "Transport":     ["Auto rickshaw","Bus pass","Petrol","Ola cab","Metro card"],
        "Utilities":     ["Electricity bill","Internet bill","Water bill","Mobile recharge"],
        "Entertainment": ["Movie ticket","OTT subscription","Concert","Gaming","Books"],
        "Healthcare":    ["Medicine","Doctor visit","Gym membership","Vitamins"],
        "Shopping":      ["Clothes","Footwear","Electronics","Stationery","Home decor"],
        "Education":     ["Online course","Books","Exam fee","Study material"],
        "Rent":          ["Monthly rent","PG charges","Hostel fee"]
    }
    cat_amounts = {
        "Food":(80,600),"Transport":(30,400),"Utilities":(200,1200),
        "Entertainment":(100,800),"Healthcare":(50,1500),
        "Shopping":(200,3000),"Education":(500,3000),"Rent":(3000,6000)
    }

    rows = []
    start = datetime(2024, 1, 1)
    for _ in range(n):
        date = start + timedelta(days=random.randint(0, 364))
        cat  = random.choice(categories)
        low, high = cat_amounts[cat]
        amount = round(random.uniform(low, high), 2)
        method = random.choice(payment_methods)
        note   = random.choice(notes[cat])
        rows.append({"Date": date.strftime("%Y-%m-%d"), "Category": cat,
                     "Amount": amount, "Payment_Method": method, "Note": note})

    df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"[✓] Dataset created: {DATA_PATH}  ({len(df)} rows)")
    return df

# ── PHASE 2: LOAD & CLEAN DATA ─────────────────────────────
def load_and_clean(path=DATA_PATH):
    df = pd.read_csv(path)
    df["Date"]           = pd.to_datetime(df["Date"])
    df["Amount"]         = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(subset=["Date","Amount","Category"], inplace=True)
    df["Amount"]         = df["Amount"].abs()
    df["Month"]          = df["Date"].dt.to_period("M").astype(str)
    df["Day"]            = df["Date"].dt.date
    df["Category"]       = df["Category"].str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].str.strip().str.title()
    print(f"[✓] Data cleaned: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# ── PHASE 3: ANALYSIS ──────────────────────────────────────
def category_analysis(df):
    s = df.groupby("Category")["Amount"].agg(["sum","mean","count"])
    s.columns = ["Total","Average","Transactions"]
    s = s.sort_values("Total", ascending=False)
    s["% Share"] = (s["Total"] / s["Total"].sum() * 100).round(1)
    return s

def monthly_analysis(df):
    m = df.groupby("Month")["Amount"].sum().reset_index()
    m.columns = ["Month","Total"]
    return m

def payment_analysis(df):
    p = df.groupby("Payment_Method")["Amount"].sum().reset_index()
    p.columns = ["Method","Total"]
    return p.sort_values("Total", ascending=False)

def daily_analysis(df):
    d = df.groupby("Day")["Amount"].sum().reset_index()
    d.columns = ["Day","Total"]
    d["Day"] = pd.to_datetime(d["Day"])
    return d

# ── PHASE 4: VISUALIZATIONS ────────────────────────────────
def plot_category_bar(cat_summary):
    fig, ax = plt.subplots(figsize=(10,6))
    colors = plt.cm.Set2.colors
    bars = ax.bar(cat_summary.index, cat_summary["Total"],
                  color=colors[:len(cat_summary)], edgecolor="white")
    ax.bar_label(bars, fmt="₹%.0f", padding=4, fontsize=9)
    ax.set_title("Category-wise Total Spending (2024)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Expense Category"); ax.set_ylabel("Total Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.0f}k"))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{IMAGES_DIR}category_bar.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[✓] Chart saved: {IMAGES_DIR}category_bar.png")

def plot_monthly_line(monthly):
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(monthly["Month"], monthly["Total"], marker="o", color="#2196F3",
            linewidth=2.5, markersize=7, markerfacecolor="white", markeredgewidth=2)
    ax.fill_between(monthly["Month"], monthly["Total"], alpha=0.15, color="#2196F3")
    ax.set_title("Monthly Spending Trend (2024)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month"); ax.set_ylabel("Total Spending (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.0f}k"))
    ax.tick_params(axis="x", rotation=45)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{IMAGES_DIR}monthly_line.png", dpi=150, bbox_inches="tight")
    plt.close()

def plot_payment_pie(pay):
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(pay["Total"], labels=pay["Method"], autopct="%1.1f%%", startangle=140,
           wedgeprops=dict(width=0.6, edgecolor="white"))
    ax.set_title("Payment Method Distribution (2024)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{IMAGES_DIR}payment_pie.png", dpi=150, bbox_inches="tight")
    plt.close()

def plot_daily_trend(daily):
    fig, ax = plt.subplots(figsize=(14,4))
    ax.plot(daily["Day"], daily["Total"], color="#4CAF50", linewidth=1.2)
    ax.fill_between(daily["Day"], daily["Total"], alpha=0.1, color="#4CAF50")
    ax.set_title("Daily Spending Trend (2024)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Daily Spend (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.1f}k"))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{IMAGES_DIR}daily_trend.png", dpi=150, bbox_inches="tight")
    plt.close()

# ── PHASE 5: REPORT ────────────────────────────────────────
def generate_report(df, cat_s, monthly, pay, total, avg_d, max_cat, max_mo):
    lines = [
        "PERSONAL EXPENSE TRACKER - ANNUAL REPORT 2024",
        "="*55,
        f"Total Expenses   : Rs. {total:,.2f}",
        f"Avg Daily Spend  : Rs. {avg_d:,.2f}",
        f"Highest Category : {max_cat}",
        f"Highest Month    : {max_mo}",
        "", "CATEGORY BREAKDOWN:", "-"*55
    ]
    for cat, row in cat_s.iterrows():
        lines.append(f"  {cat:<15} Rs. {row['Total']:>10,.2f}  ({row['% Share']:.1f}%)")
    lines += ["", "MONTHLY BREAKDOWN:", "-"*55]
    for _, r in monthly.iterrows():
        lines.append(f"  {r['Month']}    Rs. {r['Total']:>10,.2f}")
    with open(f"{REPORTS_DIR}expense_report_2024.txt","w") as f:
        f.write("\n".join(lines))
    cat_s.to_csv(f"{OUTPUT_DIR}category_summary.csv")
    monthly.to_csv(f"{OUTPUT_DIR}monthly_summary.csv", index=False)
    pay.to_csv(f"{OUTPUT_DIR}payment_summary.csv", index=False)
    print(f"[✓] Report saved!")

# ── MAIN ───────────────────────────────────────────────────
if __name__ == "__main__":
    df          = generate_expenses()
    df          = load_and_clean()
    cat_s       = category_analysis(df)
    monthly     = monthly_analysis(df)
    pay         = payment_analysis(df)
    daily       = daily_analysis(df)
    total       = df["Amount"].sum()
    avg_d       = daily["Total"].mean()
    max_cat     = cat_s.index[0]
    max_mo      = monthly.sort_values("Total",ascending=False).iloc[0]["Month"]
    plot_category_bar(cat_s)
    plot_monthly_line(monthly)
    plot_payment_pie(pay)
    plot_daily_trend(daily)
    generate_report(df, cat_s, monthly, pay, total, avg_d, max_cat, max_mo)
    print("\n[✓] ALL DONE! Check images/ and reports/ folders.")