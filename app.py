import streamlit as st
import pandas as pd
from Expense import show_add_expense
from Income import show_add_income
from Settings import show_settings

# Database file path
db_file = "database.csv"

# Load existing data or initialize an empty DataFrame
try:
    finance_data = pd.read_csv(db_file)
    # Ensure the Amount column is numeric
    finance_data["Amount"] = pd.to_numeric(finance_data["Amount"], errors="coerce")
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# Save data to the CSV file
def save_data(data):
    data.to_csv(db_file, index=False)

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Select a Page:", ["Overview", "Add Expense", "Add Income", "Settings"])

# Page logic
if menu == "Overview":
    st.title("Overview")
    st.subheader("Finance Summary")

    # Ensure Amount column is numeric
    finance_data["Amount"] = pd.to_numeric(finance_data["Amount"], errors="coerce")

    # Display finance data with highlighted maximum values
    st.dataframe(finance_data.style.highlight_max(axis=0))

    # Display summary
    total_income = finance_data[finance_data["Amount"] > 0]["Amount"].sum()
    total_expense = finance_data[finance_data["Amount"] < 0]["Amount"].sum()
    balance = total_income + total_expense

    st.write(f"Total Income: {total_income}")
    st.write(f"Total Expense: {total_expense}")
    st.write(f"Current Balance: {balance}")

elif menu == "Add Expense":
    show_add_expense(finance_data, save_data)

elif menu == "Add Income":
    show_add_income(finance_data, save_data)

elif menu == "Settings":
    show_settings()
