import streamlit as st
from streamlit_option_menu import option_menu

def show_sidebar(finance_data):
    """
    Creates a sidebar navigation menu with financial summary.

    Args:
        finance_data (pd.DataFrame): The finance data to calculate the summary.

    Returns:
        str: The selected menu option.
    """
    with st.sidebar:
        # Sidebar header
        st.title("📊 Financial Summary")

        # Calculate and display financial summary
        total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
        total_expense = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
        net_balance = total_income - total_expense

        st.metric("💰 Total Income", f"${total_income:,.2f}")
        st.metric("💸 Total Expense", f"${total_expense:,.2f}")
        st.metric("🧾 Net Balance", f"${net_balance:,.2f}")

        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=["Overview", "Add Expense", "Add Income", "Analyze", "Manage Data", "Settings", "Debt Management"],
            icons=["house", "plus-circle", "plus-circle", "bar-chart", "table", "gear", "credit-card"],
            menu_icon="list",
            default_index=0,
            orientation="vertical",
        )

    return selected
