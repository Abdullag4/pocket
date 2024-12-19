import streamlit as st
import pandas as pd
from expense import show_add_expense
from income import show_add_income
from overview import show_overview  # Corrected case
from settings import show_settings
from analyze import show_analysis  # For the analysis page
from manage_data import show_manage_data  # For managing data

DB_FILE = "finance_data.csv"

# Load or initialize data
try:
    finance_data = pd.read_csv(DB_FILE)
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Type", "Notes"])
    finance_data.to_csv(DB_FILE, index=False)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
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
