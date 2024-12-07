import streamlit as st

def show_sidebar():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Menu", ["Overview", "Add Expense", "Add Income", "Settings"])
    return menu
