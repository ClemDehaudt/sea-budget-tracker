import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEA Budget Tracker",
    page_icon="🌏",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Space Mono', monospace;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 12px;
    padding: 1rem;
    color: #e0e0ff;
}
[data-testid="metric-container"] label {
    color: #a0a0cc !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Space Mono', monospace;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f23;
    border-right: 1px solid #2d2d4e;
}
[data-testid="stSidebar"] * {
    color: #c0c0ee !important;
}

/* Main background */
.stApp {
    background: #13132b;
    color: #e0e0ff;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6464a0;
    border-bottom: 1px solid #2d2d4e;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

/* Budget status box */
.status-green {
    background: #0d2b1a;
    border: 1px solid #1a5c35;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: #4ade80;
    font-family: 'Space Mono', monospace;
}
.status-red {
    background: #2b0d0d;
    border: 1px solid #5c1a1a;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: #f87171;
    font-family: 'Space Mono', monospace;
}
.status-title {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 0.3rem;
}

/* Table styling */
[data-testid="stDataFrame"] {
    border: 1px solid #2d2d4e;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────
if "expenses" not in st.session_state:
    st.session_state.expenses = []

COUNTRIES = ["Indonesia", "Malaysia", "Thailand", "Vietnam"]
CATEGORIES = ["🏠 Accommodation", "🚌 Transport", "🍜 Food", "🎭 Activities", "🛒 Other"]

# ── Sidebar – Trip Settings ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌏 SEA Budget Tracker")
    st.markdown("---")

    st.markdown('<p class="section-header">Trip Settings</p>', unsafe_allow_html=True)
    total_budget = st.number_input("Total budget (€)", min_value=100, max_value=50000,
                                   value=10000, step=100)
    trip_start   = st.date_input("Trip start date",    value=date(2027, 9, 28))
    trip_end     = st.date_input("Trip end date",      value=date(2027, 12, 28))

    st.markdown("---")
    st.caption("Built for 3 months in Southeast Asia 🛺")

# ── Derived trip info ──────────────────────────────────────────────────────
total_days     = max((trip_end - trip_start).days, 1)
today          = date.today()
days_elapsed   = max((min(today, trip_end) - trip_start).days, 0)
days_remaining = max((trip_end - today).days, 0)

# ── Build DataFrame from expenses ─────────────────────────────────────────
def get_df():
    if not st.session_state.expenses:
        return pd.DataFrame(columns=["Date", "Country", "Category", "Description", "Amount (€)"])
    return pd.DataFrame(st.session_state.expenses)

df = get_df()
total_spent = df["Amount (€)"].sum() if not df.empty else 0.0

# ── Header KPIs ────────────────────────────────────────────────────────────
st.markdown("# SEA Budget Tracker")
st.markdown('<p class="section-header">Overview</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Budget",    f"€{total_budget:,.0f}")
c2.metric("Total Spent",     f"€{total_spent:,.2f}")
c3.metric("Remaining",       f"€{total_budget - total_spent:,.2f}",
          delta=f"€{total_budget - total_spent - total_spent:,.0f}" if total_spent else None)
c4.metric("Trip Duration",   f"{total_days} days")

st.markdown("---")

# ── Two-column layout ─────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ── LEFT – Log an Expense ─────────────────────────────────────────────────
with left:
    st.markdown('<p class="section-header">Log Daily Expense</p>', unsafe_allow_html=True)

    with st.form("expense_form", clear_on_submit=True):
        exp_date    = st.date_input("Date",        value=today)
        exp_country = st.selectbox("Country",      COUNTRIES)
        exp_cat     = st.selectbox("Category",     CATEGORIES)
        exp_desc    = st.text_input("Description", placeholder="e.g. Hostel Chiang Mai")
        exp_amount  = st.number_input("Amount (€)", min_value=0.01, max_value=5000.0,
                                      value=20.0, step=0.5)
        submitted   = st.form_submit_button("➕ Add Expense", use_container_width=True)

    if submitted:
        st.session_state.expenses.append({
            "Date":        str(exp_date),
            "Country":     exp_country,
            "Category":    exp_cat,
            "Description": exp_desc if exp_desc else "—",
            "Amount (€)":  exp_amount,
        })
        df          = get_df()
        total_spent = df["Amount (€)"].sum()
        st.success(f"✔ Added €{exp_amount:.2f} for {exp_cat}")

    # Clear all button
    if st.session_state.expenses:
        if st.button("🗑 Clear all expenses", use_container_width=True):
            st.session_state.expenses = []
            st.rerun()

# ── RIGHT – Budget Calculator ──────────────────────────────────────────────
with right:
    st.markdown('<p class="section-header">Budget Calculator</p>', unsafe_allow_html=True)

    remaining_budget = total_budget - total_spent
    budget_per_day_remaining = remaining_budget / days_remaining if days_remaining > 0 else 0
    actual_daily_avg = total_spent / days_elapsed if days_elapsed > 0 else 0
    projected_total  = actual_daily_avg * total_days if actual_daily_avg > 0 else 0

    # Stats row
    s1, s2 = st.columns(2)
    s1.metric("Days Remaining",        f"{days_remaining}d")
    s2.metric("Days Elapsed",          f"{days_elapsed}d")
    s3, s4 = st.columns(2)
    s3.metric("Budget/Day (remaining)", f"€{budget_per_day_remaining:.2f}")
    s4.metric("Actual Daily Avg",       f"€{actual_daily_avg:.2f}")

    st.markdown("")

    # Green/Red indicator
    if total_spent == 0:
        st.info("📊 Log your first expense to see the budget health indicator.")
    elif remaining_budget >= actual_daily_avg * days_remaining:
        projected_surplus = remaining_budget - (actual_daily_avg * days_remaining)
        st.markdown(f"""
        <div class="status-green">
            <div class="status-title">🟢 Budget on track</div>
            <div style="font-size:1.6rem; font-weight:700;">€{remaining_budget:,.2f} left</div>
            <div style="font-size:0.85rem; margin-top:0.3rem; opacity:0.8;">
                At your current pace of €{actual_daily_avg:.2f}/day,
                you'll finish with <strong>€{projected_surplus:,.2f}</strong> to spare.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        shortfall = (actual_daily_avg * days_remaining) - remaining_budget
        st.markdown(f"""
        <div class="status-red">
            <div class="status-title">🔴 Over budget pace</div>
            <div style="font-size:1.6rem; font-weight:700;">€{remaining_budget:,.2f} left</div>
            <div style="font-size:0.85rem; margin-top:0.3rem; opacity:0.8;">
                At your current pace of €{actual_daily_avg:.2f}/day,
                you'll run out by <strong>~{days_remaining - int(remaining_budget / actual_daily_avg)}
                days early</strong>. Reduce to €{budget_per_day_remaining:.2f}/day to stay safe.
            </div>
        </div>
        """, unsafe_allow_html=True)

    if actual_daily_avg > 0:
        st.markdown("")
        st.caption(f"📈 Projected total spend at current pace: **€{projected_total:,.2f}** / €{total_budget:,.0f}")

# ── Country Summary Table ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">Summary by Country</p>', unsafe_allow_html=True)

if df.empty:
    st.info("No expenses logged yet. Add your first expense above 👆")
else:
    # Build country summary
    summary_rows = []
    for country in COUNTRIES:
        cdf       = df[df["Country"] == country]
        total     = cdf["Amount (€)"].sum()
        days_in   = cdf["Date"].nunique()
        avg_day   = total / days_in if days_in > 0 else 0
        pct       = (total / total_spent * 100) if total_spent > 0 else 0
        summary_rows.append({
            "Country":         country,
            "Expenses logged": len(cdf),
            "Days tracked":    days_in,
            "Total spent (€)": round(total, 2),
            "Avg / day (€)":   round(avg_day, 2),
            "% of budget":     f"{pct:.1f}%",
        })

    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Category breakdown
    st.markdown('<p class="section-header" style="margin-top:1.5rem">Breakdown by Category</p>',
                unsafe_allow_html=True)
    cat_df = (
        df.groupby("Category")["Amount (€)"]
          .sum()
          .reset_index()
          .sort_values("Amount (€)", ascending=False)
    )
    cat_df["% of total"] = (cat_df["Amount (€)"] / total_spent * 100).round(1).astype(str) + "%"
    st.dataframe(cat_df, use_container_width=True, hide_index=True)

    # Raw log
    with st.expander("📋 Full expense log"):
        st.dataframe(df.sort_values("Date", ascending=False),
                     use_container_width=True, hide_index=True)
