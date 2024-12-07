import streamlit as st

def show_sidebar():
    # Sidebar navigation using a selectbox to persist the state
    st.sidebar.title("Navigation")
    
    # Set default value for the menu if not already set
    if "menu" not in st.session_state:
        st.session_state.menu = "Overview"

    # Sidebar selectbox to choose the menu
    menu = st.sidebar.selectbox(
        "Choose an option",
        ["Overview", "Add Expense", "Add Income", "Settings"],
        index=["Overview", "Add Expense", "Add Income", "Settings"].index(st.session_state.menu)
    )
    
    # Update the session state when an option is selected
    st.session_state.menu = menu

    return menu
