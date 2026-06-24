import streamlit as st
import pandas as pd

from services.api_client import (
    get_dashboard,
    get_top_long_term,
    get_top_swing,
    get_breakout
)


def render_dashboard():

    st.title("🐂 Green Bull Rider V6")

    data = get_dashboard()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Stocks",
        data["total_stocks"]
    )

    c2.metric(
        "Long Term Buy",
        data["long_term_buy"]
    )

    c3.metric(
        "Swing Buy",
        data["swing_buy"]
    )

    c4.metric(
        "Smart Money",
        data["smart_money"]
    )

    st.divider()

    st.subheader("Top Long Term")

    long_term = get_top_long_term()

    st.dataframe(
        pd.DataFrame(long_term)
    )

    st.subheader("Top Swing")

    swing = get_top_swing()

    st.dataframe(
        pd.DataFrame(swing)
    )

    st.subheader("Breakout Radar")

    breakout = get_breakout()

    st.dataframe(
        pd.DataFrame(breakout)
    )
