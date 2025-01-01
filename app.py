import streamlit as st
import pandas as pd
from expense import show_add_expense
from income import show_add_income
from overview import show_overview
from settings import show_settings, load_settings
from analyze import show_analysis
from theme import configure_theme
from manage_data import show_manage_data
from debts import show_debt_page
from sidebar import show_sidebar
from localization import set_language, _
import requests
import base64

# Load settings
settings = load_settings()

# Initialize language from settings or default
if "language" not in st.session_state:
    st.session_state["language"] = settings.get("language", "en")

# Apply language
set_language(st.session_state["language"])

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

# Save data back to the file
def save_data(file_path, data):
    try:
        data.to_csv(file_path, index=False)
        st.success(_("Data saved successfully."))
    except Exception as e:
        st.error(_("Error saving data: {error}").format(error=str(e)))

# Initialize session state for data persistence
if "finance_data" not in st.session_state:
    st.session_state["finance_data"] = load_data(DB_FILE, ["Date", "Category", "Amount", "Type", "Notes"])

if "debt_data" not in st.session_state:
    st.session_state["debt_data"] = load_data(DEBT_FILE, ["Type", "Name", "Amount", "Due Date", "Reason", "Status"])

# Apply global theme configuration
configure_theme()

# Sidebar navigation with financial summary
page = show_sidebar(st.session_state["finance_data"])  # Pass finance_data to the sidebar function

# Debugging translations
st.write(f"Current page: {page}")  # Debugging
st.write(f"Translated Overview: {_('Overview')}")  # Debugging

# Page routing with fallback for missing translations
if page == _("Overview") or page == "Overview":  # Fallback for untranslated string
    show_overview(st.session_state["finance_data"])
elif page == _("Add Expense") or page == "Add Expense":
    st.session_state["finance_data"] = show_add_expense(st.session_state["finance_data"], DB_FILE)
    save_data(DB_FILE, st.session_state["finance_data"])  # Save changes
elif page == _("Add Income") or page == "Add Income":
    st.session_state["finance_data"] = show_add_income(st.session_state["finance_data"], DB_FILE)
    save_data(DB_FILE, st.session_state["finance_data"])  # Save changes
elif page == _("Analyze") or page == "Analyze":
    show_analysis(st.session_state["finance_data"])
elif page == _("Manage Data") or page == "Manage Data":
    show_manage_data(st.session_state["finance_data"], DB_FILE)
    save_data(DB_FILE, st.session_state["finance_data"])  # Save changes
elif page == _("Settings") or page == "Settings":
    show_settings(st.session_state["finance_data"], DB_FILE)
elif page == _("Debt Management") or page == "Debt Management":
    show_debt_page(st.session_state["debt_data"], DEBT_FILE)
    save_data(DEBT_FILE, st.session_state["debt_data"])  # Save changes
