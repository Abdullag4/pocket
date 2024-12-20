import streamlit as st

def configure_theme():
    st.markdown(
        """
        <style>
        .title {
            font-size:40px;
            font-weight:bold;
            text-align:center;
            color:#1f77b4;
            margin-bottom:20px;
        }
        .section-title {
            font-size:30px;
            font-weight:bold;
            color:#1f77b4;
            margin-top:20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
