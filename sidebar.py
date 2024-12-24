import streamlit as st

def show_sidebar(finance_data):
    """
    Creates a sidebar navigation menu and displays a financial summary.

    Args:
        finance_data (DataFrame): The DataFrame containing financial data.

    Returns:
        str: The selected menu option.
    """
    # Set the title for the sidebar
    st.sidebar.title("Navigation")

    # Ensure session state for the menu persists
    if "menu" not in st.session_state:
        st.session_state.menu = "Overview"  # Default option

    # Sidebar selectbox to navigate between options
    menu = st.sidebar.selectbox(
        "Choose an option",
        ["Overview", "Add Expense", "Add Income", "Settings", "Manage Data"],
        index=["Overview", "Add Expense", "Add Income", "Settings", "Manage Data"].index(st.session_state.menu),
    )

    # Update the session state to reflect the current selection
    st.session_state.menu = menu

    # Financial Summary
    st.sidebar.subheader("Financial Summary")

    if not finance_data.empty:
        total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
        total_expense = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expense

        st.sidebar.metric("Total Income", f"${total_income:,.2f}")
        st.sidebar.metric("Total Expense", f"${total_expense:,.2f}")
        st.sidebar.metric("Balance", f"${balance:,.2f}")
    else:
        st.sidebar.info("No financial data available.")

    # Return the selected menu option
    return menu
