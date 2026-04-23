import streamlit as st
import pandas as pd
from datetime import date

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEA Journal — Budget Tracker",
    page_icon="🌿",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Karla:wght@300;400;500;600&display=swap');

:root {
    --cream:      #F5EFE0;
    --cream-dark: #EDE4CE;
    --ink:        #2C2416;
    --ink-muted:  #7A6A50;
    --green:      #3D6B4F;
    --green-light:#6FAF82;
    --green-pale: #DCF0E3;
    --terra:      #C45E35;
    --terra-pale: #FAE5D8;
    --gold:       #D4A847;
    --red-pale:   #FDDDD4;
    --red-deep:   #A83220;
    --border:     #D8CDBA;
}

html, body, [class*="css"] {
    font-family: 'Karla', sans-serif;
    background-color: var(--cream) !important;
    color: var(--ink);
}
.stApp { background-color: var(--cream) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }

/* Title */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.page-subtitle {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--ink-muted);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.title-rule {
    border: none;
    border-top: 2px solid var(--ink);
    margin: 1rem 0 1.5rem 0;
    width: 60px;
}

/* Section label */
.section-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ink-muted);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}

/* KPI cards */
.kpi-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.accent-ink::before   { background: var(--ink); }
.kpi-card.accent-terra::before { background: var(--terra); }
.kpi-card.accent-green::before { background: var(--green); }
.kpi-card.accent-gold::before  { background: var(--gold); }
.kpi-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--ink-muted);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--ink);
    line-height: 1;
}
.kpi-sub { font-size: 0.72rem; color: var(--ink-muted); margin-top: 0.3rem; }

/* Progress bar */
.progress-wrap { margin: 1.4rem 0 0.4rem; }
.progress-track {
    background: var(--cream-dark);
    border-radius: 99px;
    height: 7px;
    overflow: hidden;
    margin-bottom: 0.4rem;
}
.progress-fill { height: 100%; border-radius: 99px; }
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: var(--ink-muted);
}

/* Form */
[data-testid="stForm"] {
    background: white;
    border: 1px solid var(--border) !important;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
}
[data-testid="stForm"] label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--ink-muted) !important;
}
[data-testid="stFormSubmitButton"] button {
    background: var(--green) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Karla', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    width: 100%;
}

/* Status boxes */
.status-box {
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
}
.status-box.ok   { background: var(--green-pale); border: 1px solid var(--green-light); }
.status-box.warn { background: var(--red-pale);   border: 1px solid #E8A090; }
.status-flag { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 0.4rem; }
.status-flag.ok   { color: var(--green); }
.status-flag.warn { color: var(--red-deep); }
.status-amount {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 800; color: var(--ink); line-height: 1.1;
}
.status-desc { font-size: 0.82rem; color: var(--ink-muted); margin-top: 0.4rem; line-height: 1.55; }

/* Calc grid */
.calc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin-bottom: 1rem; }
.calc-cell { background: white; border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; }
.calc-cell-label { font-size: 0.6rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-muted); }
.calc-cell-value { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: var(--ink); margin-top: 0.15rem; }

/* Country strip */
.country-strip { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.8rem; }
.country-badge {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--ink-muted);
    display: flex; align-items: center; gap: 0.4rem;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--border); flex-shrink: 0; }
.dot.active { background: var(--terra); }

/* Sidebar */
[data-testid="stSidebar"] { background: var(--ink) !important; border-right: none !important; }
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] label {
    color: #9A8A70 !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem; font-weight: 600; font-style: italic; color: var(--cream);
}
.sidebar-sub { font-size: 0.68rem; color: #7A6A50; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.5rem; }

/* DataFrames */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] thead tr th {
    background: var(--cream-dark) !important;
    color: var(--ink-muted) !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "expenses" not in st.session_state:
    st.session_state.expenses = []

COUNTRIES  = ["Indonesia 🇮🇩", "Malaysia 🇲🇾", "Thailand 🇹🇭", "Vietnam 🇻🇳"]
CATEGORIES = ["🏠 Accommodation", "🚌 Transport", "🍜 Food", "🎭 Activities", "🛒 Other"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">SEA Journal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Budget Tracker · 2027</div>', unsafe_allow_html=True)
    st.markdown("---")
    total_budget = st.number_input("Total budget (€)", min_value=100, max_value=50000, value=10000, step=100)
    trip_start   = st.date_input("Departure", value=date(2027, 9, 28))
    trip_end     = st.date_input("Return",    value=date(2027, 12, 28))
    st.markdown("---")
    st.caption("Indonesia · Malaysia · Thailand · Vietnam")
    st.caption("Sept → Dec 2027 · ~92 jours")

# ── Derived values ────────────────────────────────────────────────────────────
total_days     = max((trip_end - trip_start).days, 1)
today          = date.today()
days_elapsed   = max((min(today, trip_end) - trip_start).days, 0)
days_remaining = max((trip_end - today).days, 0)

def get_df():
    if not st.session_state.expenses:
        return pd.DataFrame(columns=["Date","Country","Category","Description","Amount (€)"])
    return pd.DataFrame(st.session_state.expenses)

df          = get_df()
total_spent = df["Amount (€)"].sum() if not df.empty else 0.0
remaining   = total_budget - total_spent
pct_spent   = min(total_spent / total_budget * 100, 100) if total_budget else 0
actual_daily = total_spent / max(days_elapsed, 1)
budget_per_day = remaining / max(days_remaining, 1)
avg_ideal    = total_budget / total_days

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Budget Journal</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Southeast Asia · September – December 2027</div>', unsafe_allow_html=True)
st.markdown('<hr class="title-rule">', unsafe_allow_html=True)

# Country badges
spent_by = df.groupby("Country")["Amount (€)"].sum().to_dict() if not df.empty else {}
badges = "".join(
    f'<div class="country-badge"><span class="dot{"" if c not in spent_by else " active"}"></span>{c}</div>'
    for c in COUNTRIES
)
st.markdown(f'<div class="country-strip">{badges}</div>', unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-card accent-ink"><div class="kpi-label">Total Budget</div><div class="kpi-value">€{total_budget:,.0f}</div><div class="kpi-sub">{total_days} days planned</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card accent-terra"><div class="kpi-label">Spent so far</div><div class="kpi-value">€{total_spent:,.2f}</div><div class="kpi-sub">{pct_spent:.1f}% of budget</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card accent-green"><div class="kpi-label">Remaining</div><div class="kpi-value">€{remaining:,.2f}</div><div class="kpi-sub">{days_remaining} days left</div></div>', unsafe_allow_html=True)
with k4:
    delta_color = "var(--green)" if actual_daily <= avg_ideal else "var(--terra)"
    st.markdown(f'<div class="kpi-card accent-gold"><div class="kpi-label">Daily Average</div><div class="kpi-value" style="color:{delta_color}">€{actual_daily:,.2f}</div><div class="kpi-sub">target ≤ €{avg_ideal:.2f}/day</div></div>', unsafe_allow_html=True)

# Progress bar
bar_color = "var(--green)" if pct_spent < 75 else ("var(--gold)" if pct_spent < 100 else "var(--terra)")
st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-track">
        <div class="progress-fill" style="width:{pct_spent:.1f}%; background:{bar_color};"></div>
    </div>
    <div class="progress-label">
        <span>€0</span>
        <span style="color:{bar_color}; font-weight:600">{pct_spent:.1f}% used</span>
        <span>€{total_budget:,}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1.05, 1], gap="large")

# ── LEFT : Log expense ────────────────────────────────────────────────────────
with left:
    st.markdown('<div class="section-label">Log a Daily Expense</div>', unsafe_allow_html=True)
    with st.form("expense_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            exp_date    = st.date_input("Date", value=today)
        with col_b:
            exp_country = st.selectbox("Country", COUNTRIES)
        col_c, col_d = st.columns(2)
        with col_c:
            exp_cat = st.selectbox("Category", CATEGORIES)
        with col_d:
            exp_amount = st.number_input("Amount (€)", min_value=0.01, max_value=5000.0, value=25.0, step=0.5)
        exp_desc  = st.text_input("Description (optional)", placeholder="e.g. Night bus Bangkok → Chiang Mai")
        submitted = st.form_submit_button("＋ Add to journal", use_container_width=True)

    if submitted:
        st.session_state.expenses.append({
            "Date":        str(exp_date),
            "Country":     exp_country,
            "Category":    exp_cat,
            "Description": exp_desc if exp_desc else "—",
            "Amount (€)":  exp_amount,
        })
        df = get_df()
        total_spent = df["Amount (€)"].sum()
        st.success(f"✔ €{exp_amount:.2f} · {exp_cat} · {exp_country}")

    if st.session_state.expenses:
        if st.button("🗑 Clear all entries", use_container_width=True):
            st.session_state.expenses = []
            st.rerun()

    if not df.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recent Entries</div>', unsafe_allow_html=True)
        recent = df.sort_values("Date", ascending=False).head(6)[["Date","Country","Category","Amount (€)"]]
        st.dataframe(recent, use_container_width=True, hide_index=True)

# ── RIGHT : Budget health ─────────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-label">Budget Health</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="calc-grid">
        <div class="calc-cell">
            <div class="calc-cell-label">Days elapsed</div>
            <div class="calc-cell-value">{days_elapsed}d</div>
        </div>
        <div class="calc-cell">
            <div class="calc-cell-label">Days remaining</div>
            <div class="calc-cell-value">{days_remaining}d</div>
        </div>
        <div class="calc-cell">
            <div class="calc-cell-label">Budget/day left</div>
            <div class="calc-cell-value">€{budget_per_day:.2f}</div>
        </div>
        <div class="calc-cell">
            <div class="calc-cell-label">Actual daily avg</div>
            <div class="calc-cell-value">€{actual_daily:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if total_spent == 0:
        st.info("📊 Log your first expense to see budget health.")
    elif remaining >= actual_daily * days_remaining:
        surplus = remaining - (actual_daily * days_remaining)
        st.markdown(f"""
        <div class="status-box ok">
            <div class="status-flag ok">🟢 On track</div>
            <div class="status-amount">€{remaining:,.2f} remaining</div>
            <div class="status-desc">
                At <strong>€{actual_daily:.2f}/day</strong>, you finish with
                <strong>€{surplus:,.2f}</strong> to spare. Budget holds.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        days_of_cash = int(remaining / actual_daily) if actual_daily > 0 else 0
        shortfall    = (actual_daily * days_remaining) - remaining
        st.markdown(f"""
        <div class="status-box warn">
            <div class="status-flag warn">🔴 Over pace</div>
            <div class="status-amount">€{remaining:,.2f} remaining</div>
            <div class="status-desc">
                At <strong>€{actual_daily:.2f}/day</strong>, cash lasts ~<strong>{days_of_cash} more days</strong>.
                Reduce to <strong>€{budget_per_day:.2f}/day</strong> to cover {days_remaining} days.
                Shortfall: <strong>€{shortfall:,.2f}</strong>.
            </div>
        </div>""", unsafe_allow_html=True)

    if actual_daily > 0:
        proj = actual_daily * total_days
        st.caption(f"📈 Projected total at current pace: **€{proj:,.2f}** / €{total_budget:,.0f}")

# ── Country summary ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Summary by Country</div>', unsafe_allow_html=True)

if df.empty:
    st.info("No expenses yet. Start logging above 👆")
else:
    rows = []
    for c in COUNTRIES:
        cdf   = df[df["Country"] == c]
        total = cdf["Amount (€)"].sum()
        days_ = cdf["Date"].nunique()
        avg   = total / days_ if days_ > 0 else 0
        pct   = total / total_spent * 100 if total_spent > 0 else 0
        rows.append({
            "Country":         c,
            "Entries":         len(cdf),
            "Days tracked":    days_,
            "Total spent (€)": round(total, 2),
            "Avg/day (€)":     round(avg, 2),
            "% of budget":     f"{pct:.1f}%",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-label">By Category</div>', unsafe_allow_html=True)
        cat_df = (df.groupby("Category")["Amount (€)"].sum()
                    .reset_index().sort_values("Amount (€)", ascending=False))
        cat_df["% of total"] = (cat_df["Amount (€)"] / total_spent * 100).round(1).astype(str) + "%"
        st.dataframe(cat_df, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown('<div class="section-label">Full Log</div>', unsafe_allow_html=True)
        with st.expander("View all entries"):
            st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
