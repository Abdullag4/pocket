import streamlit as st

def apply_styles():
    # Custom styling for the app
    st.markdown("""
    <style>
    .css-18e3th9 {
        background-color: #f0f4f8;
    }
    .css-1d391kg {
        color: #2c3e50;
    }
    .css-ffhzg2 {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
