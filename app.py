import streamlit as st
import pandas as pd
from Expense import show_add_expense
from Income import show_add_income
from Overview import show_overview
from Settings import show_settings
from Analyze import show_analysis  # Import the new analysis page

# Database file
DB_FILE = "finance_data.csv"

# Load or initialize data
try:
    finance_data = pd.read_csv(DB_FILE)
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])
    finance_data.to_csv(DB_FILE, index=False)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Overview", "Add Expense", "Add Income", "Analyze", "Settings"]
)

# Page routing
if page == "Overview":
    show_overview(finance_data)
elif page == "Add Expense":
    finance_data = show_add_expense(finance_data, DB_FILE)
elif page == "Add Income":
    finance_data = show_add_income(finance_data, DB_FILE)
elif page == "Analyze":
    show_analysis(finance_data)  # Call the new analysis function
elif page == "Settings":
    show_settings(finance_data, DB_FILE)
