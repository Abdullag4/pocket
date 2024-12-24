import streamlit as st
import pandas as pd
from expense import show_add_expense
from income import show_add_income
from overview import show_overview
from settings import show_settings
from analyze import show_analysis
from theme import configure_theme  # Global Theme Configuration
from manage_data import show_manage_data  # For managing data
from debts import show_debt_page  # For debt management
from sidebar import show_sidebar  # Updated sidebar function

# File paths
DB_FILE = "finance_data.csv"
DEBT_FILE = "debt_data.csv"

# Load or initialize data
def load_data(file_path, columns):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        data = pd.DataFrame(columns=columns)
        data.to_csv(file_path, index=False)
        return data

# Initialize session state for data persistence
if "finance_data" not in st.session_state:
    st.session_state["finance_data"] = finance_data = load_data(DB_FILE, ["Date", "Category", "Amount", "Type", "Notes"])

if "debt_data" not in st.session_state:
    st.session_state["debt_data"] = load_data(
        DEBT_FILE, ["Type", "Name", "Amount", "Due Date", "Reason", "Status"]
    )

# Apply global theme configuration
configure_theme()

# Sidebar navigation with financial summary
page = show_sidebar(st.session_state["finance_data"])  # Pass finance_data to the sidebar function

# Page routing
if page == "Overview":
    show_overview(st.session_state["finance_data"])
elif page == "Add Expense":
    st.session_state["finance_data"] = show_add_expense(st.session_state["finance_data"], DB_FILE)
elif page == "Add Income":
    st.session_state["finance_data"] = show_add_income(st.session_state["finance_data"], DB_FILE)
elif page == "Analyze":
    show_analysis(st.session_state["finance_data"])
elif page == "Manage Data":
    show_manage_data(st.session_state["finance_data"], DB_FILE)
elif page == "Settings":
    show_settings(st.session_state["finance_data"], DB_FILE)
elif page == "Debt Management":
    show_debt_page(st.session_state["debt_data"], DEBT_FILE)
