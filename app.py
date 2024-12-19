import streamlit as st
import pandas as pd
from expense import show_add_expense
from income import show_add_income
from overview import show_overview
from settings import show_settings
from analyze import show_analysis
from manage_data import show_manage_data  # For managing data

DB_FILE = "finance_data.csv"

# Load or initialize data
try:
    finance_data = pd.read_csv(DB_FILE)
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Type", "Notes"])
    finance_data.to_csv(DB_FILE, index=False)

# Sidebar navigation with summary
st.sidebar.title("📊 Personal Money Manager")
st.sidebar.markdown("---")

# Display summary
total_income = finance_data.loc[finance_data["Type"] == "Income", "Amount"].sum()
total_expenses = finance_data.loc[finance_data["Type"] == "Expense", "Amount"].sum()
balance = total_income - total_expenses

st.sidebar.metric("💰 Total Income", f"${total_income:,.2f}")
st.sidebar.metric("💸 Total Expenses", f"${total_expenses:,.2f}")
st.sidebar.metric("📈 Balance", f"${balance:,.2f}")

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "📂 Pages",
    ["Overview", "Add Expense", "Add Income", "Analyze", "Manage Data", "Settings"]
)


# Page routing
if page == "Overview":
    show_overview(finance_data)
elif page == "Add Expense":
    finance_data = show_add_expense(finance_data, DB_FILE)
elif page == "Add Income":
    finance_data = show_add_income(finance_data, DB_FILE)
elif page == "Analyze":
    show_analysis(finance_data)
elif page == "Manage Data":
    show_manage_data(finance_data, DB_FILE)
elif page == "Settings":
    show_settings(finance_data, DB_FILE)
