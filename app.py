#!/usr/bin/env python3
"""
Personal Expense Tracker - Streamlit Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os, random
from datetime import datetime, timedelta

# ── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .section-header {
        font-size: 20px; font-weight: 600; color: #1f2937;
        border-left: 4px solid #667eea; padding-left: 10px;
        margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── DATA GENERATION ────────────────────────────────────────
@st.cache_data
def generate_expenses(n=200, seed=42):
    random.seed(seed); np.random.seed(seed)
    categories = ["Food","Transport","Utilities","Entertainment",
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
        date   = start + timedelta(days=random.randint(0, 364))
        cat    = random.choice(categories)
        lo, hi = cat_amounts[cat]
        amount = round(random.uniform(lo, hi), 2)
        rows.append({"Date": date.strftime("%Y-%m-%d"), "Category": cat,
                     "Amount": amount,
                     "Payment_Method": random.choice(payment_methods),
                     "Note": random.choice(notes[cat])})
    return pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)

@st.cache_data
def load_and_clean(df):
    df = df.copy()
    df["Date"]           = pd.to_datetime(df["Date"])
    df["Amount"]         = pd.to_numeric(df["Amount"], errors="coerce").abs()
    df.dropna(subset=["Date","Amount","Category"], inplace=True)
    df["Month"]          = df["Date"].dt.to_period("M").astype(str)
    df["Day"]            = df["Date"].dt.date
    df["Category"]       = df["Category"].str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].str.strip().str.title()
    return df

raw_df = generate_expenses()
df     = load_and_clean(raw_df)

# ── SIDEBAR ────────────────────────────────────────────────
st.sidebar.title("💰 Expense Tracker")
st.sidebar.markdown("---")

all_cats    = sorted(df["Category"].unique())
all_methods = sorted(df["Payment_Method"].unique())
all_months  = sorted(df["Month"].unique())

sel_cats    = st.sidebar.multiselect("📂 Category", all_cats, default=all_cats)
sel_methods = st.sidebar.multiselect("💳 Payment Method", all_methods, default=all_methods)
min_m, max_m = st.sidebar.select_slider("📅 Month Range", options=all_months,
                                         value=(all_months[0], all_months[-1]))
min_amt = float(df["Amount"].min())
max_amt = float(df["Amount"].max())
amt_range = st.sidebar.slider("💵 Amount Range (₹)", min_amt, max_amt, (min_amt, max_amt))

st.sidebar.markdown("---")
st.sidebar.markdown("**➕ Add New Expense**")
with st.sidebar.form("add_expense"):
    new_date   = st.date_input("Date", datetime.today())
    new_cat    = st.selectbox("Category", all_cats)
    new_amt    = st.number_input("Amount (₹)", min_value=1.0, value=100.0, step=10.0)
    new_method = st.selectbox("Payment Method", all_methods)
    new_note   = st.text_input("Note", placeholder="e.g. Lunch at canteen")
    if st.form_submit_button("Add Expense"):
        st.success(f"✅ Added: {new_cat} — ₹{new_amt:.2f}")

# ── FILTER DATA ────────────────────────────────────────────
filtered = df[
    (df["Category"].isin(sel_cats)) &
    (df["Payment_Method"].isin(sel_methods)) &
    (df["Month"] >= min_m) & (df["Month"] <= max_m) &
    (df["Amount"] >= amt_range[0]) & (df["Amount"] <= amt_range[1])
].copy()

# ── HEADER ─────────────────────────────────────────────────
st.title("💰 Personal Expense Tracker Dashboard")
st.markdown("*Filter by category, month, payment method, and amount using the sidebar.*")
st.markdown("---")

# ── KPI METRICS ────────────────────────────────────────────
total       = filtered["Amount"].sum()
avg_monthly = filtered.groupby("Month")["Amount"].sum().mean() if not filtered.empty else 0
max_cat     = filtered.groupby("Category")["Amount"].sum().idxmax() if not filtered.empty else "N/A"
txn_count   = len(filtered)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💸 Total Spending",    f"₹{total:,.0f}")
col2.metric("📅 Avg Monthly",       f"₹{avg_monthly:,.0f}")
col3.metric("🏆 Top Category",      max_cat)
col4.metric("🧾 Transactions",      txn_count)
st.markdown("---")

# ── CHART ROW 1: BAR + PIE ─────────────────────────────────
st.markdown('<div class="section-header">📊 Spending Breakdown</div>', unsafe_allow_html=True)
col_a, col_b = st.columns([3, 2])

with col_a:
    cat_sum = filtered.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    bars = ax1.bar(cat_sum.index, cat_sum.values,
                   color=plt.cm.Set2.colors[:len(cat_sum)], edgecolor="white")
    ax1.bar_label(bars, fmt="₹%.0f", padding=3, fontsize=8)
    ax1.set_title("Category-wise Total Spending", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Category"); ax1.set_ylabel("Amount (₹)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.0f}k"))
    ax1.tick_params(axis="x", rotation=30)
    ax1.spines[["top","right"]].set_visible(False)
    plt.tight_layout(); st.pyplot(fig1); plt.close()

with col_b:
    pay_sum = filtered.groupby("Payment_Method")["Amount"].sum()
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.pie(pay_sum.values, labels=pay_sum.index, autopct="%1.1f%%",
            startangle=140, wedgeprops=dict(width=0.6, edgecolor="white"))
    ax2.set_title("Payment Method Share", fontsize=12, fontweight="bold")
    plt.tight_layout(); st.pyplot(fig2); plt.close()

# ── CHART ROW 2: MONTHLY TREND ─────────────────────────────
st.markdown('<div class="section-header">📈 Monthly Spending Trend</div>', unsafe_allow_html=True)
monthly = filtered.groupby("Month")["Amount"].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(12, 4))
ax3.plot(monthly["Month"], monthly["Amount"], marker="o", color="#2196F3",
         linewidth=2.5, markersize=7, markerfacecolor="white", markeredgewidth=2)
ax3.fill_between(monthly["Month"], monthly["Amount"], alpha=0.15, color="#2196F3")
ax3.set_title("Monthly Spending Trend", fontsize=12, fontweight="bold")
ax3.set_xlabel("Month"); ax3.set_ylabel("Total (₹)")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.0f}k"))
ax3.tick_params(axis="x", rotation=45)
ax3.spines[["top","right"]].set_visible(False)
plt.tight_layout(); st.pyplot(fig3); plt.close()

# ── CHART ROW 3: DAILY TREND ───────────────────────────────
st.markdown('<div class="section-header">📆 Daily Spending Trend</div>', unsafe_allow_html=True)
daily = filtered.groupby("Day")["Amount"].sum().reset_index()
daily["Day"] = pd.to_datetime(daily["Day"])
fig4, ax4 = plt.subplots(figsize=(12, 3))
ax4.plot(daily["Day"], daily["Amount"], color="#4CAF50", linewidth=1.2)
ax4.fill_between(daily["Day"], daily["Amount"], alpha=0.1, color="#4CAF50")
ax4.set_title("Daily Spending Trend", fontsize=12, fontweight="bold")
ax4.set_xlabel("Date"); ax4.set_ylabel("Daily Spend (₹)")
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x/1000:.1f}k"))
ax4.spines[["top","right"]].set_visible(False)
plt.tight_layout(); st.pyplot(fig4); plt.close()

# ── DATA TABLE + DOWNLOAD ──────────────────────────────────
st.markdown('<div class="section-header">📋 Expense Records</div>', unsafe_allow_html=True)
col_x, col_y = st.columns([3, 1])
with col_x:
    st.dataframe(
        filtered[["Date","Category","Amount","Payment_Method","Note"]]
        .sort_values("Date", ascending=False).reset_index(drop=True),
        use_container_width=True, height=300
    )
with col_y:
    st.download_button("⬇️ Download CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_expenses.csv", mime="text/csv")
    st.markdown("**📊 Stats**")
    st.write(f"Min : ₹{filtered['Amount'].min():,.0f}")
    st.write(f"Max : ₹{filtered['Amount'].max():,.0f}")
    st.write(f"Avg : ₹{filtered['Amount'].mean():,.0f}")

# ── FOOTER ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("<center style='color:gray;font-size:13px;'>Personal Expense Tracker | Python + Streamlit | Portfolio Project</center>",
            unsafe_allow_html=True)