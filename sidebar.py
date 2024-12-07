import streamlit as st

def show_sidebar():
    # Sidebar navigation with buttons
    st.sidebar.title("Navigation")
    
    # Check if a button has been clicked and store the result in session state
    if "menu" not in st.session_state:
        st.session_state.menu = None

    if st.sidebar.button("Overview"):
        st.session_state.menu = "Overview"
    elif st.sidebar.button("Add Expense"):
        st.session_state.menu = "Add Expense"
    elif st.sidebar.button("Add Income"):
        st.session_state.menu = "Add Income"
    elif st.sidebar.button("Settings"):
        st.session_state.menu = "Settings"

    # Return the current menu state
    return st.session_state.menu
