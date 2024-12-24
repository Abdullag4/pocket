import streamlit as st

def show_sidebar(finance_data):
    st.sidebar.title("📊 Navigation")

    # Notifications
    st.sidebar.subheader("🔔 Notifications")
    total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
    total_expense = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    if balance < 0:
        st.sidebar.error("⚠️ Balance is negative!")
    else:
        st.sidebar.success("✅ You're on track!")

    # Overspending alerts
    needs_limit = total_income * 0.50
    needs_expense = finance_data[finance_data["Category"] == "Needs"]["Amount"].sum()
    if needs_expense > needs_limit:
        st.sidebar.warning("⚠️ Overspending on 'Needs'!")

    # Navigation
    menu = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Overview", "➕ Add Expense", "➕ Add Income", "📈 Analyze", "Manage Data", "⚙️ Settings", "💳 Debt Management"]
    )
    return menu
