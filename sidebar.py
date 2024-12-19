import streamlit as st

def show_sidebar():
    """
    Creates a sidebar navigation menu and manages its state.

    Returns:
        str: The selected menu option.
    """
    # Set the title for the sidebar
    st.sidebar.title("Navigation")

    st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["🏠 Overview", "➕ Add Expense", "➕ Add Income", "📈 Analyze", "⚙️ Settings"]
)

    # Ensure session state for the menu persists
    if "menu" not in st.session_state:
        st.session_state.menu = "Overview"  # Default option

    # Sidebar selectbox to navigate between options
    menu = st.sidebar.selectbox(
        "Choose an option",
        ["Overview", "Add Expense", "Add Income", "Settings"],
        index=["Overview", "Add Expense", "Add Income", "Settings"].index(st.session_state.menu)
    )

    # Update the session state to reflect the current selection
    st.session_state.menu = menu

    # Return the selected menu option
    return menu
