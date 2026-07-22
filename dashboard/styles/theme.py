# dashboard/styles/theme.py

import streamlit as st
import base64

def load_theme():
    """Load modern dashboard theme with dark/light support"""
    
    # Check if theme is set in session state
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'dark'  # Default to dark mode
    
    # Theme toggle in sidebar
    theme_mode = st.sidebar.radio(
        "🎨 Theme",
        ["🌙 Dark", "☀️ Light"],
        index=0 if st.session_state.theme_mode == 'dark' else 1,
        key="theme_radio"
    )
    
    # Update session state
    if theme_mode == "🌙 Dark":
        st.session_state.theme_mode = 'dark'
    else:
        st.session_state.theme_mode = 'light'
    
    # Apply theme
    if st.session_state.theme_mode == 'dark':
        apply_dark_theme()
    else:
        apply_light_theme()

def apply_dark_theme():
    """Apply dark theme styling"""
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: #0F172A;
        }
        
        /* Main content */
        .main > div {
            background: #1E293B;
            padding: 1.5rem;
            border-radius: 12px;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #F1F5F9 !important;
            font-weight: 600 !important;
        }
        
        /* Text */
        p, li, label, div {
            color: #CBD5E1 !important;
        }
        
        /* Sidebar */
        .css-1d391kg, .css-12oz5g7 {
            background: #0F172A !important;
        }
        
        .css-1d391kg .css-1v0mbdj, .css-12oz5g7 .css-1v0mbdj {
            color: #F1F5F9 !important;
        }
        
        /* Sidebar labels */
        .css-1v0mbdj p, .css-1v0mbdj label {
            color: #CBD5E1 !important;
        }
        
        /* Select box */
        .stSelectbox > div > div {
            background: #1E293B !important;
            color: #F1F5F9 !important;
            border-color: #334155 !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #3B82F6 !important;
        }
        
        /* Text input */
        .stTextInput > div > div > input {
            background: #1E293B !important;
            color: #F1F5F9 !important;
            border-color: #334155 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
        }
        
        /* Slider */
        .stSlider > div > div > div {
            background: #334155 !important;
        }
        
        .stSlider > div > div > div > div {
            background: #3B82F6 !important;
        }
        
        /* Metrics/KPI cards */
        .stMetric {
            background: #1E293B !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            border: 1px solid #334155 !important;
        }
        
        .stMetric > div > div {
            color: #F1F5F9 !important;
        }
        
        .stMetric > div > div:first-child {
            color: #94A3B8 !important;
            font-size: 0.9rem !important;
        }
        
        .stMetric > div > div:last-child {
            color: #3B82F6 !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        /* Divider */
        hr {
            border-color: #334155 !important;
        }
        
        /* Dataframe */
        .stDataFrame {
            background: #1E293B !important;
        }
        
        .stDataFrame > div > div {
            background: #1E293B !important;
            color: #CBD5E1 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: #3B82F6 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background: #2563EB !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        }
        
        /* Info/Warning messages */
        .stAlert {
            background: #1E293B !important;
            border-color: #334155 !important;
        }
        
        .stAlert > div > div {
            color: #F1F5F9 !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #1E293B !important;
            color: #F1F5F9 !important;
            border-color: #334155 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #1E293B !important;
            color: #CBD5E1 !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: #3B82F6 !important;
            color: #FFFFFF !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1E293B;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #3B82F6;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #2563EB;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_light_theme():
    """Apply light theme styling"""
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: #F8FAFC;
        }
        
        /* Main content */
        .main > div {
            background: #FFFFFF;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 600 !important;
        }
        
        /* Text */
        p, li, label, div {
            color: #1E293B !important;
        }
        
        /* Sidebar */
        .css-1d391kg, .css-12oz5g7 {
            background: #F1F5F9 !important;
        }
        
        .css-1d391kg .css-1v0mbdj, .css-12oz5g7 .css-1v0mbdj {
            color: #0F172A !important;
        }
        
        /* Select box */
        .stSelectbox > div > div {
            background: #FFFFFF !important;
            color: #0F172A !important;
            border-color: #E2E8F0 !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #3B82F6 !important;
        }
        
        /* Text input */
        .stTextInput > div > div > input {
            background: #FFFFFF !important;
            color: #0F172A !important;
            border-color: #E2E8F0 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Slider */
        .stSlider > div > div > div {
            background: #E2E8F0 !important;
        }
        
        .stSlider > div > div > div > div {
            background: #3B82F6 !important;
        }
        
        /* Metrics/KPI cards */
        .stMetric {
            background: #F8FAFC !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
        }
        
        .stMetric > div > div:first-child {
            color: #64748B !important;
            font-size: 0.9rem !important;
        }
        
        .stMetric > div > div:last-child {
            color: #3B82F6 !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        /* Divider */
        hr {
            border-color: #E2E8F0 !important;
        }
        
        /* Dataframe */
        .stDataFrame {
            background: #FFFFFF !important;
        }
        
        .stDataFrame > div > div {
            background: #FFFFFF !important;
            color: #1E293B !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: #3B82F6 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background: #2563EB !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }
        
        /* Info/Warning messages */
        .stAlert {
            background: #F8FAFC !important;
            border-color: #E2E8F0 !important;
        }
        
        .stAlert > div > div {
            color: #1E293B !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            background: #F1F5F9 !important;
            color: #64748B !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: #3B82F6 !important;
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)