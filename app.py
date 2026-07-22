# app.py

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="Workforce Analytics Platform",
    page_icon="👥",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("👥 Workforce Analytics")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "📌 Navigation",
    ["📊 Executive Dashboard", "🧠 Predictive Analytics", "📈 Performance Analytics", "📋 Report Center"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("v2.0.0 | Powered by AI")

def load_page(page_name):
    page_path = os.path.join("pages", f"{page_name}.py")
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())
    else:
        st.error(f"Page not found: {page_path}")

# Page routing - EXACT match
if page == "📊 Executive Dashboard":
    load_page("1_Home")
elif page == "🧠 Predictive Analytics":
    load_page("2_ML_Analytics")
elif page == "📈 Performance Analytics":
    load_page("3_Performance_Analytics")
elif page == "📋 Report Center":
    load_page("4_Export")