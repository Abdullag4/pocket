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

# File paths
DB_FILE = "finance_data.csv"
DEBT_FILE = "debt_data.csv"

# Load or initialize data
@st.cache_data
def load_or_initialize_data(file_path, columns):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        # Initialize with empty DataFrame with specified columns
        data = pd.DataFrame(columns=columns)
        data.to_csv(file_path, index=False)
        return data

finance_data = load_or_initialize_data(DB_FILE, ["Date", "Category", "Amount", "Type", "Notes"])
debt_data = load_or_initialize_data(
    DEBT_FILE, ["Type", "Name", "Amount", "Due Date", "Reason", "Status"]
)

# Apply global theme configuration
configure_theme()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["🏠 Overview", "➕ Add Expense", "➕ Add Income", "📈 Analyze", "Manage Data", "⚙️ Settings", "💳 Debt Management"]
)

# Page routing
if page == "🏠 Overview":
    show_overview(finance_data)
elif page == "➕ Add Expense":
    finance_data = show_add_expense(finance_data, DB_FILE)
elif page == "➕ Add Income":
    finance_data = show_add_income(finance_data, DB_FILE)
elif page == "📈 Analyze":
    show_analysis(finance_data)
elif page == "Manage Data":
    show_manage_data(finance_data, DB_FILE)
elif page == "⚙️ Settings":
    show_settings(finance_data, DB_FILE)
elif page == "💳 Debt Management":
    show_debt_page(debt_data, DEBT_FILE)
