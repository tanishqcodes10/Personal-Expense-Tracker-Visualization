#!/usr/bin/env python3
"""
Personal Expense Tracker — Premium Streamlit Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Expense Tracker", page_icon="💎",
                   layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.kpi-card {
    background: linear-gradient(135deg, #1e1e3a 0%, #2d2d5e 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px; padding: 22px 20px;
    text-align: center; position: relative; overflow: hidden; margin-bottom: 10px;
}
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.kpi-card-1::before { background: linear-gradient(90deg,#667eea,#764ba2); }
.kpi-card-2::before { background: linear-gradient(90deg,#f093fb,#f5576c); }
.kpi-card-3::before { background: linear-gradient(90deg,#4facfe,#00f2fe); }
.kpi-card-4::before { background: linear-gradient(90deg,#43e97b,#38f9d7); }
.kpi-card-5::before { background: linear-gradient(90deg,#fa709a,#fee140); }
.kpi-icon  { font-size:28px; margin-bottom:8px; }
.kpi-label { font-size:11px; color:#94a3b8; text-transform:uppercase; letter-spacing:1.2px; margin-bottom:6px; }
.kpi-value { font-size:24px; font-weight:700; color:#f1f5f9; }
.kpi-delta { font-size:12px; color:#43e97b; margin-top:4px; }

.section-title {
    font-size:18px; font-weight:600; color:#e2e8f0;
    padding:6px 0 6px 14px; border-left:4px solid #667eea; margin:28px 0 14px 0;
}
.insight-pill {
    display:inline-block; background:rgba(102,126,234,0.12);
    border:1px solid rgba(102,126,234,0.3); border-radius:20px;
    padding:6px 16px; font-size:13px; color:#a5b4fc; margin:4px 4px 4px 0;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
# Safe base layout — ONLY keys that never conflict with per-chart overrides
DARK_BG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#cbd5e1", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
)

AXIS_STYLE = dict(
    gridcolor="rgba(255,255,255,0.05)",
    zerolinecolor="rgba(255,255,255,0.08)",
    tickfont=dict(size=11),
    title_font=dict(size=12),
    linecolor="rgba(255,255,255,0.1)",
)

LEG = dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", font=dict(size=11))
COLORS = ["#667eea","#f5576c","#4facfe","#43e97b","#fa709a","#fee140","#a18cd1","#fbc2eb"]

def apply_dark(fig):
    """Apply dark axis + legend styling cleanly — no dict conflicts."""
    fig.update_layout(**DARK_BG, legend=LEG)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
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
        date = start + timedelta(days=random.randint(0, 364))
        cat  = random.choice(categories)
        lo, hi = cat_amounts[cat]
        rows.append({
            "Date": date.strftime("%Y-%m-%d"), "Category": cat,
            "Amount": round(random.uniform(lo, hi), 2),
            "Payment_Method": random.choice(payment_methods),
            "Note": random.choice(notes[cat])
        })
    return pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)

@st.cache_data
def clean(df):
    df = df.copy()
    df["Date"]           = pd.to_datetime(df["Date"])
    df["Amount"]         = pd.to_numeric(df["Amount"], errors="coerce").abs()
    df.dropna(subset=["Date","Amount","Category"], inplace=True)
    df["Month"]          = df["Date"].dt.to_period("M").astype(str)
    df["Day"]            = df["Date"].dt.date
    df["Weekday"]        = df["Date"].dt.day_name()
    df["Category"]       = df["Category"].str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].str.strip().str.title()
    return df

df = clean(generate_expenses())

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 20px 0;'>
        <div style='font-size:42px'>💎</div>
        <div style='font-size:20px;font-weight:700;color:#e2e8f0;'>Expense Tracker</div>
        <div style='font-size:11px;color:#64748b;letter-spacing:1px;text-transform:uppercase;'> Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🗂 FILTERS**")

    all_cats    = sorted(df["Category"].unique())
    all_methods = sorted(df["Payment_Method"].unique())
    all_months  = sorted(df["Month"].unique())

    sel_cats    = st.multiselect("Category",       all_cats,    default=all_cats)
    sel_methods = st.multiselect("Payment Method", all_methods, default=all_methods)
    min_m, max_m = st.select_slider("Month Range", options=all_months,
                                     value=(all_months[0], all_months[-1]))
    min_a, max_a = float(df["Amount"].min()), float(df["Amount"].max())
    amt = st.slider("Amount Range (₹)", min_a, max_a, (min_a, max_a))

    st.markdown("---")
    st.markdown("**➕ LOG EXPENSE**")
    with st.form("add_form", clear_on_submit=True):
        new_date   = st.date_input("Date", datetime.today())
        new_amt    = st.number_input("Amount (₹)", min_value=1.0, value=100.0, step=10.0)
        new_cat    = st.selectbox("Category", all_cats)
        new_method = st.selectbox("Payment Method", all_methods)
        st.text_input("Note", placeholder="e.g. Lunch at canteen")
        if st.form_submit_button("➕ Add Expense", use_container_width=True):
            st.success(f"✅ {new_cat} · ₹{new_amt:,.0f} added!")

    st.markdown("---")
   

# ══════════════════════════════════════════════════════════════
# FILTER
# ══════════════════════════════════════════════════════════════
fd = df[
    df["Category"].isin(sel_cats) &
    df["Payment_Method"].isin(sel_methods) &
    (df["Month"] >= min_m) & (df["Month"] <= max_m) &
    (df["Amount"] >= amt[0]) & (df["Amount"] <= amt[1])
].copy()

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style='margin-bottom:8px;'>
    <span style='font-size:32px;font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;'>💎 Expense Tracker</span>
    <span style='font-size:14px;color:#64748b;margin-left:12px;'>Personal Finance Dashboard · </span>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════
total     = fd["Amount"].sum() if not fd.empty else 0
avg_mo    = fd.groupby("Month")["Amount"].sum().mean() if not fd.empty else 0
avg_daily = fd.groupby("Day")["Amount"].sum().mean() if not fd.empty else 0
top_cat   = fd.groupby("Category")["Amount"].sum().idxmax() if not fd.empty else "N/A"
top_mo    = fd.groupby("Month")["Amount"].sum().idxmax() if not fd.empty else "N/A"
txn       = len(fd)

cols = st.columns(5)
cards = [
    ("kpi-card-1","💸","TOTAL SPENT",   f"₹{total/1000:.1f}k",  "Annual 2024"),
    ("kpi-card-2","📅","AVG / MONTH",   f"₹{avg_mo/1000:.1f}k", "Monthly avg"),
    ("kpi-card-3","📆","AVG / DAY",     f"₹{avg_daily:,.0f}",   "Daily avg"),
    ("kpi-card-4","🏆","TOP CATEGORY",  top_cat,                 "Highest spend"),
    ("kpi-card-5","🧾","TRANSACTIONS",  str(txn),                f"Peak: {top_mo}"),
]
for col, (cls, icon, label, value, delta) in zip(cols, cards):
    col.markdown(f"""
    <div class="kpi-card {cls}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ROW 1 — CATEGORY BAR + PAYMENT DONUT
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Spending Breakdown</div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2], gap="medium")

with c1:
    cat_sum = fd.groupby("Category")["Amount"].sum().sort_values(ascending=True).reset_index()
    fig1 = go.Figure(go.Bar(
        x=cat_sum["Amount"], y=cat_sum["Category"], orientation="h",
        marker=dict(color=list(range(len(cat_sum))),
                    colorscale=[[0,"#1e1e3a"],[0.5,"#667eea"],[1,"#764ba2"]],
                    showscale=False, line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[f"₹{v/1000:.1f}k" for v in cat_sum["Amount"]],
        textposition="outside", textfont=dict(size=11, color="#94a3b8"),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>"
    ))
    apply_dark(fig1)
    fig1.update_layout(title=dict(text="Category-wise Spending", font=dict(size=14, color="#e2e8f0"), x=0),
                       height=340, xaxis_title="Amount (₹)", yaxis_title="", showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    pay_sum = fd.groupby("Payment_Method")["Amount"].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=pay_sum["Payment_Method"], values=pay_sum["Amount"], hole=0.65,
        marker=dict(colors=COLORS, line=dict(color="#0f0f1a", width=3)),
        textinfo="percent", textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>"
    ))
    fig2.add_annotation(text=f"₹{total/1000:.0f}k<br>Total",
                        x=0.5, y=0.5, showarrow=False,
                        font=dict(size=16, color="#f1f5f9"), align="center")
    apply_dark(fig2)
    fig2.update_layout(title=dict(text="Payment Methods", font=dict(size=14, color="#e2e8f0"), x=0),
                       height=340, showlegend=True,
                       legend=dict(orientation="v", x=1.0, y=0.5, bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ROW 2 — MONTHLY TREND + WEEKDAY BAR
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Time-based Analysis</div>', unsafe_allow_html=True)
c3, c4 = st.columns([3, 2], gap="medium")

with c3:
    monthly = fd.groupby("Month")["Amount"].sum().reset_index()
    fig3 = go.Figure(go.Scatter(
        x=monthly["Month"], y=monthly["Amount"],
        mode="lines+markers",
        line=dict(color="#667eea", width=3),
        marker=dict(size=8, color="#764ba2", line=dict(color="#667eea", width=2)),
        fill="tozeroy", fillcolor="rgba(102,126,234,0.15)",
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        name="Monthly Spend"
    ))
    if not monthly.empty:
        pi = monthly["Amount"].idxmax()
        pv, pm = monthly.loc[pi, "Amount"], monthly.loc[pi, "Month"]
        fig3.add_annotation(x=pm, y=pv, text=f"Peak ₹{pv/1000:.1f}k",
                            showarrow=True, arrowhead=2, arrowcolor="#f5576c",
                            font=dict(color="#f5576c", size=11),
                            bgcolor="#1e1e3a", bordercolor="#f5576c", borderwidth=1)
    apply_dark(fig3)
    fig3.update_layout(title=dict(text="Monthly Spending Trend (2024)", font=dict(size=14, color="#e2e8f0"), x=0),
                       height=340, xaxis_title="Month", yaxis_title="Amount (₹)", showlegend=False)
    fig3.update_xaxes(tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    wd = fd.groupby("Weekday")["Amount"].sum().reindex(weekday_order).fillna(0).reset_index()
    fig4 = go.Figure(go.Bar(
        x=wd["Weekday"], y=wd["Amount"],
        marker=dict(color=list(range(len(wd))),
                    colorscale=[[0,"#1e1e3a"],[0.5,"#4facfe"],[1,"#00f2fe"]],
                    showscale=False, line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[f"₹{v/1000:.1f}k" for v in wd["Amount"]],
        textposition="outside", textfont=dict(size=10, color="#94a3b8"),
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"
    ))
    apply_dark(fig4)
    fig4.update_layout(title=dict(text="Spending by Day of Week", font=dict(size=14, color="#e2e8f0"), x=0),
                       height=340, xaxis_title="", yaxis_title="Amount (₹)", showlegend=False)
    fig4.update_xaxes(tickangle=-20,
                      ticktext=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                      tickvals=weekday_order)
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ROW 3 — DAILY TREND + TOP 5 STACKED
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📆 Transaction Detail</div>', unsafe_allow_html=True)
c5, c6 = st.columns([3, 2], gap="medium")

with c5:
    daily_grp = fd.groupby("Day")["Amount"].sum().reset_index()
    daily_grp["Day"] = pd.to_datetime(daily_grp["Day"])
    fig5 = go.Figure(go.Scatter(
        x=daily_grp["Day"], y=daily_grp["Amount"],
        mode="lines", line=dict(color="#43e97b", width=1.8),
        fill="tozeroy", fillcolor="rgba(67,233,123,0.12)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.0f}<extra></extra>",
        name="Daily Spend"
    ))
    apply_dark(fig5)
    fig5.update_layout(title=dict(text="Daily Spending Trend (2024)", font=dict(size=14, color="#e2e8f0"), x=0),
                       height=300, xaxis_title="Date", yaxis_title="Daily Spend (₹)", showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    top5 = fd.groupby("Category")["Amount"].sum().nlargest(5).reset_index()
    t5_total = top5["Amount"].sum()
    top5["pct"] = (top5["Amount"] / t5_total * 100).round(1)
    fig6 = go.Figure()
    for i, row in top5.iterrows():
        fig6.add_trace(go.Bar(
            x=[row["Amount"]], y=[row["Category"]], orientation="h",
            name=row["Category"],
            marker_color=COLORS[i % len(COLORS)],
            text=f"{row['pct']}%",
            textposition="inside", textfont=dict(size=12, color="white"),
            hovertemplate=f"<b>{row['Category']}</b><br>₹{row['Amount']:,.0f} ({row['pct']}%)<extra></extra>"
        ))
    apply_dark(fig6)
    fig6.update_layout(title=dict(text="Top 5 Categories Share", font=dict(size=14, color="#e2e8f0"), x=0),
                       barmode="stack", height=300, showlegend=False,
                       xaxis_title="Amount (₹)", yaxis_title="")
    fig6.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# INSIGHT PILLS
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">💡 Smart Insights</div>', unsafe_allow_html=True)
if not fd.empty:
    cat_pct = fd.groupby("Category")["Amount"].sum() / total * 100
    top_pay = fd.groupby("Payment_Method")["Amount"].sum().idxmax()
    max_day = fd.groupby("Day")["Amount"].sum().idxmax()
    insights = [
        f"🏠 {cat_pct.idxmax()} = {cat_pct.max():.1f}% of total spend",
        f"💳 {top_pay} is most used payment method",
        f"📅 Highest spend day: {max_day}",
        f"📊 {len(sel_cats)} categories · {len(sel_methods)} payment types active",
        f"🧾 Avg transaction: ₹{fd['Amount'].mean():,.0f}",
        f"📈 Peak month: {fd.groupby('Month')['Amount'].sum().idxmax()}",
    ]
    st.markdown("".join([f'<span class="insight-pill">{i}</span>' for i in insights]),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA TABLE + DOWNLOAD
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📋 Expense Records</div>', unsafe_allow_html=True)
c7, c8 = st.columns([4, 1], gap="medium")
with c7:
    disp = fd[["Date","Category","Amount","Payment_Method","Note"]].sort_values(
        "Date", ascending=False).reset_index(drop=True).copy()
    disp["Amount"] = disp["Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(disp, use_container_width=True, height=320)
with c8:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("⬇️ Export CSV", fd.to_csv(index=False).encode(),
                       "expenses_filtered.csv", "text/csv", use_container_width=True)
    st.markdown("---")
    if not fd.empty:
        st.markdown(f"<div style='color:#94a3b8;font-size:13px;'>📌 <b style='color:#e2e8f0'>{txn}</b> records</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#94a3b8;font-size:13px;'>Min: <b style='color:#43e97b'>₹{fd['Amount'].min():,.0f}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#94a3b8;font-size:13px;'>Max: <b style='color:#f5576c'>₹{fd['Amount'].max():,.0f}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#94a3b8;font-size:13px;'>Avg: <b style='color:#667eea'>₹{fd['Amount'].mean():,.0f}</b></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:20px;border-top:1px solid rgba(255,255,255,0.06);
            color:#475569;font-size:12px;'>
    💎 <b style='color:#667eea'>Expense Tracker </b> &nbsp;·&nbsp;
    Python + Streamlit + Plotly &nbsp;·&nbsp; Portfolio Project · 
</div>""", unsafe_allow_html=True)

