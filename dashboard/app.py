from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data"

st.set_page_config(page_title="CFPB Credit Card Complaints", layout="wide")
st.title("Credit Card Complaints Dashboard")
st.caption(
    "Source: CFPB Consumer Complaint Database. Credit card complaints received "
    "Oct 5, 2025 to Sep 18, 2026. Later dates are excluded because recent "
    "complaints were still being logged (counts fade to near zero)."
)

monthly = pd.read_csv(DATA / "monthly.csv", parse_dates=["month_start"])
companies = pd.read_csv(DATA / "companies.csv")
issues = pd.read_csv(DATA / "issues.csv")
states = pd.read_csv(DATA / "states.csv")

# Headline numbers
c1, c2, c3 = st.columns(3)
c1.metric("Total complaints", f"{monthly['complaints'].sum():,}")
c2.metric("Companies shown (1,000+ complaints)", len(companies))
c3.metric("Busiest month (per day)", monthly.loc[monthly["per_day"].idxmax(), "month_start"].strftime("%b %Y"))

# Monthly trend
st.subheader("Complaints per day, by month")
st.caption("Per-day averages keep short months (and the partial first and last months) comparable.")
st.line_chart(monthly.set_index("month_start")["per_day"])

# Companies
st.subheader("Company comparison")
metric = st.selectbox(
    "Compare companies by:",
    ["complaints", "pct_relief", "pct_timely"],
    format_func=lambda m: {
        "complaints": "Number of complaints",
        "pct_relief": "% closed with relief",
        "pct_timely": "% answered on time",
    }[m],
)
ranked = companies.sort_values(metric, ascending=False)
st.bar_chart(ranked.set_index("company_name")[metric])
st.dataframe(ranked, hide_index=True, use_container_width=True)
st.caption(
    "Relief rate is a rough measure. Different companies receive different kinds "
    "of complaints, so it does not show which company is better."
)

# Issues and states side by side
left, right = st.columns(2)
with left:
    st.subheader("Top issues")
    st.bar_chart(issues.set_index("issue")["complaints"])
with right:
    st.subheader("Top 15 states")
    st.bar_chart(states.head(15).set_index("state")["complaints"])
