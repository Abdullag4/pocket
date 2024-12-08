import streamlit as st
from github import Github
from sidebar import show_sidebar
from style import apply_styles
from Expense import show_add_expense
from Income import show_add_income
from Setting import show_settings
import pandas as pd

# Apply Styles
apply_styles()

# Load GitHub Token from Secrets
GITHUB_TOKEN = st.secrets["GITHUB_POCKET"]

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)

# Your repository where the CSV is stored (update with your actual repository details)
REPO_NAME = "your-username/your-repo"
CSV_PATH = "database.csv"

# Load finance data from GitHub
@st.cache_data
def load_data():
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(CSV_PATH)
    data = pd.read_csv(file_content.download_url)
    return data

# Save finance data back to GitHub
def save_data(data):
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(CSV_PATH)
    updated_content = data.to_csv(index=False)
    repo.update_file(
        path=CSV_PATH,
        message="Update finance data",
        content=updated_content,
        sha=file_content.sha,
    )

# Load initial data
try:
    finance_data = load_data()
except Exception as e:
    st.error("Failed to load data from GitHub. Please check your configuration.")
    st.stop()

# Sidebar
menu = show_sidebar()

# Overview Page
if menu == "Overview":
    st.title("Finance Overview")
    st.dataframe(finance_data)

# Add Expense Page
elif menu == "Add Expense":
    show_add_expense(finance_data, save_data)

# Add Income Page
elif menu == "Add Income":
    show_add_income(finance_data, save_data)

# Settings Page
elif menu == "Settings":
    show_settings()
