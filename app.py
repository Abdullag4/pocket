import streamlit as st
from sidebar import show_sidebar
from Overview import show_overview
from Expense import show_add_expense
from Income import show_add_income
from analyze import show_analysis
from manage_data import show_manage_data
import pandas as pd
import os

# Define the database file path
db_file = "finance_data.csv"

# Load existing data or initialize a new DataFrame
if os.path.exists(db_file):
    finance_data = pd.read_csv(db_file)
else:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])

# Set up the app
st.set_page_config(page_title="Pocket Finance Manager", layout="wide")

# Display the sidebar for navigation
selected_page = show_sidebar()

# Page navigation
if selected_page == "Overview":
    show_overview(finance_data)
elif selected_page == "Add Expense":
    finance_data = show_add_expense(finance_data, db_file)
elif selected_page == "Add Income":
    finance_data = show_add_income(finance_data, db_file)
elif selected_page == "Analyze Data":
    show_analysis(finance_data)
elif selected_page == "Manage Data":
    show_manage_data(finance_data, db_file)
