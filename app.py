import streamlit as st
import pandas as pd
from Expense import show_add_expense
from Income import show_add_income
from Settings import show_settings
from overview import show_overview  # Importing the new Overview module

# Database file path
db_file = "finance_data.csv"

# Load data
try:
    finance_data = pd.read_csv(db_file)
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# App Menu
menu = st.sidebar.selectbox("Menu", ["Overview", "Add Expense", "Add Income", "Settings"])

# Menu Navigation
if menu == "Overview":
    show_overview(finance_data)  # Call the new overview function
elif menu == "Add Expense":
    finance_data = show_add_expense(finance_data, db_file)
elif menu == "Add Income":
    finance_data = show_add_income(finance_data, db_file)
elif menu == "Settings":
    finance_data = show_settings(finance_data, db_file)
