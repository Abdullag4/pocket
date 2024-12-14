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
        data = pd.read_csv(file_path)
        # Ensure 'Amount' is numeric, coercing errors to NaN
        data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
        return data
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

# Page Routing with Debugging
try:
    if menu == "Overview":
    st.title("Overview")

    # Clean the finance data to ensure numeric values
    finance_data['Amount'] = pd.to_numeric(finance_data['Amount'], errors='coerce')

    # Handle potential NaN values
    if finance_data['Amount'].isna().any():
        st.warning("Some entries have invalid amounts. Please review your data.")

    # Display the data
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
except Exception as e:
    st.error("An error occurred while rendering the page.")
    st.write(f"Error details: {e}")

# Footer Debugging
st.write("App execution completed.")
