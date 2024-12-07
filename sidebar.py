import streamlit as st

def show_sidebar():
    # Sidebar navigation with buttons
    st.sidebar.title("Navigation")
    menu = None

    if st.sidebar.button("Overview"):
        menu = "Overview"
    elif st.sidebar.button("Add Expense"):
        menu = "Add Expense"
    elif st.sidebar.button("Add Income"):
        menu = "Add Income"
    elif st.sidebar.button("Settings"):
        menu = "Settings"

    return menu
