import streamlit as st

from backend.services.long_term_screener import (
    run_long_term_screener
)

st.title("📈 Long Term Screener")

# ==================================
# SMART SCREENER
# ==================================

st.subheader("Smart Screener")

col1, col2 = st.columns(2)

with col1:
    years = st.number_input(
        "Investment Period (Years)",
        min_value=1,
        max_value=50,
        value=10
    )

with col2:
    expected_return = st.number_input(
        "Expected Return (%)",
        min_value=5,
        max_value=100,
        value=15
    )

# ==================================
# SMART AUTO PARAMETERS
# ==================================

def generate_parameters(
    years,
    expected_return
):

    if expected_return >= 20:

        return {
            "roe": 20,
            "roce": 20,
            "sales_growth": 15,
            "profit_growth": 15,
            "debt_equity": 0.5,
            "promoter_holding": 50,
            "institutional_holding": 10,
            "market_cap": 0
        }

    return {
        "roe": 15,
        "roce": 15,
        "sales_growth": 10,
        "profit_growth": 10,
        "debt_equity": 1,
        "promoter_holding": 40,
        "institutional_holding": 5,
        "market_cap": 0
    }

if "lt_filters" not in st.session_state:

    st.session_state.lt_filters = (
        generate_parameters(
            years,
            expected_return
        )
    )

if st.button("Generate Parameters"):

    st.session_state.lt_filters = (
        generate_parameters(
            years,
            expected_return
        )
    )

# ==================================
# MANUAL SCREENER
# ==================================

st.subheader("Manual Screener")

filters = st.session_state.lt_filters

filters["roe"] = st.number_input(
    "ROE",
    value=float(filters["roe"])
)

filters["roce"] = st.number_input(
    "ROCE",
    value=float(filters["roce"])
)

filters["sales_growth"] = st.number_input(
    "Sales Growth",
    value=float(filters["sales_growth"])
)

filters["profit_growth"] = st.number_input(
    "Profit Growth",
    value=float(filters["profit_growth"])
)

filters["debt_equity"] = st.number_input(
    "Debt Equity",
    value=float(filters["debt_equity"])
)

filters["promoter_holding"] = st.number_input(
    "Promoter Holding",
    value=float(filters["promoter_holding"])
)

filters["institutional_holding"] = st.number_input(
    "Institutional Holding",
    value=float(filters["institutional_holding"])
)

# ==================================
# SEARCH
# ==================================

if st.button("Search Stocks"):

    results = run_long_term_screener(
        filters
    )

    st.subheader("Results")

    st.dataframe(results)
