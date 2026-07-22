import streamlit as st


def metric_card(title, value, color="#2563EB"):
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:16px;
            border-left:6px solid {color};
            box-shadow:0 6px 18px rgba(15,23,42,.08);
            border:1px solid #E2E8F0;
            min-height:120px;
        ">

            <div style="
                font-size:15px;
                color:#64748B;
                font-weight:600;
            ">
                {title}
            </div>

            <div style="
                margin-top:14px;
                font-size:34px;
                font-weight:700;
                color:#0F172A;
            ">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )