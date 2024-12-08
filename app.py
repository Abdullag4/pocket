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

# Load Finance Data
db_file = "database.csv"
try:
    finance_data = pd.read_csv(db_file)
except FileNotFoundError:
    finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# Display sidebar and select menu
menu = show_sidebar()

# GitHub Authentication
github_client = authenticate_github()

# Page Routing
if menu == "Overview":
    st.title("Overview")
    st.dataframe(finance_data.style.highlight_max(axis=0))
elif menu == "Add Expense":
    show_add_expense(finance_data, save_data)
elif menu == "Add Income":
    show_add_income(finance_data, save_data)
elif menu == "Settings":
    show_settings()

# Save updated finance data to the database
if 'finance_data' in locals():
    finance_data.to_csv(db_file, index=False)
