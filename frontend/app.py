import streamlit as st

from pages.dashboard import (
    render_dashboard
)

st.set_page_config(
    page_title="Green Bull Rider",
    layout="wide"
)

render_dashboard()
