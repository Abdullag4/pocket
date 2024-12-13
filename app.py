import streamlit as st
import pandas as pd
from sidebar import show_sidebar
from Expense import show_add_expense
from Income import show_add_income
from Setting import show_settings

# Load Finance Data
def load_finance_data(file_path):
    """Load finance data from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        # If file does not exist, create an empty DataFrame
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

def save_finance_data(data, file_path):
    """Save finance data to a CSV file."""
    data.to_csv(file_path, index=False)

# File path for the database
db_file = "database.csv"

# Load or initialize finance data
finance_data = load_finance_data(db_file)

# Sidebar Menu
menu = show_sidebar()

# Debugging: Display the selected menu
st.write(f"Debug: Selected menu - {menu}")

# Page Routing
if menu == "Overview":
    st.title("Overview")
    st.dataframe(finance_data.style.highlight_max(axis=0), use_container_width=True)
elif menu == "Add Expense":
    st.write("Navigating to Add Expense")
    show_add_expense(finance_data, lambda data: save_finance_data(data, db_file))
elif menu == "Add Income":
    st.write("Navigating to Add Income")
    show_add_income(finance_data, lambda data: save_finance_data(data, db_file))
elif menu == "Settings":
    st.write("Navigating to Settings")
    show_settings(finance_data, db_file)

# Footer Debugging
st.write("App execution completed.")
