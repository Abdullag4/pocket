import streamlit as st
from github import Github
from sidebar import show_sidebar
from style import apply_styles
from Expense import show_add_expense
from Income import show_add_income
from Setting import show_settings
import pandas as pd

# Apply custom styles
apply_styles()

# File to store the data
db_file = "database.csv"

# Function to load data
def load_data():
    try:
        return pd.read_csv(db_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# Function to save data
def save_data(data):
    """
    Save the provided DataFrame to the database file (CSV).
    Also logs the saved data for debugging.
    """
    data.to_csv(db_file, index=False)
    st.write("Data successfully saved to file. Current data:")
    st.write(data)

# Authenticate with GitHub using token from Streamlit secrets
def authenticate_github():
    try:
        token = st.secrets["GITHUB_POCKET"]
        github_client = Github(token)
        user = github_client.get_user()
        st.sidebar.success(f"GitHub Authenticated as: {user.login}")
        return github_client
    except Exception as e:
        st.sidebar.error("Failed to authenticate with GitHub.")
        st.sidebar.write(e)
        return None

# Display sidebar and select menu
menu = show_sidebar()

# GitHub Authentication
github_client = authenticate_github()

# Page Routing
if menu == "Overview":
    st.title("Overview")
    finance_data = load_data()  # Reload data from the CSV file
    if not finance_data.empty:
        st.dataframe(finance_data.style.highlight_max(axis=0))
    else:
        st.write("No data available. Add expenses or income to get started!")
elif menu == "Add Expense":
    finance_data = load_data()  # Load data before modifying
    show_add_expense(finance_data, save_data)
elif menu == "Add Income":
    finance_data = load_data()  # Load data before modifying
    show_add_income(finance_data, save_data)
elif menu == "Settings":
    finance_data = load_data()  # Load data before modifying
    show_settings(finance_data, save_data)
