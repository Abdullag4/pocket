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
import json
import base64

def push_to_github(file_path, repo, branch, token):
    """Push local file updates to GitHub."""
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Step 1: Fetch the latest file information
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_info = response.json()
            sha = file_info["sha"]  # Get the latest commit SHA
        elif response.status_code == 404:
            sha = None  # File does not exist, creating it for the first time
        else:
            st.error(f"Error fetching file info: {response.json()}")
            return

        # Step 2: Read the local file content
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        # Step 3: Prepare the payload
        payload = {
            "message": "Update finance_data.csv",
            "content": content,
            "branch": branch,
        }
        if sha:
            payload["sha"] = sha  # Include SHA for updates

        # Step 4: Push the updated file
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            st.success("Data successfully pushed to GitHub.")
        else:
            st.error(f"Error pushing data to GitHub: {response.json()}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


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

# Push data to GitHub
def push_to_github(file_path, data, token):
    headers = {"Authorization": f"Bearer {token}"}
    get_url = f"{GITHUB_API_URL}/repos/{REPO}/contents/{FILE_PATH}"

    # Get file content and SHA
    response = requests.get(get_url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info["sha"]
    else:
        sha = None  # File does not exist, create a new one

    # Prepare content
    content = data.to_csv(index=False).encode("utf-8")
    encoded_content = base64.b64encode(content).decode("utf-8")
    commit_message = "Update finance_data.csv via Streamlit"

    # Prepare payload
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": BRANCH,
    }
    if sha:
        payload["sha"] = sha

    # Push changes
    response = requests.put(get_url, headers=headers, data=json.dumps(payload))
    if response.status_code in [200, 201]:
        st.success("Data successfully pushed to GitHub!")
    else:
        st.error(f"Error pushing data to GitHub: {response.status_code} {response.text}")

# Save data back to the file and sync with GitHub
def save_and_sync(file_path, data):
    try:
        # Save locally
        data.to_csv(file_path, index=False)
        st.success(_("Data saved locally."))

        # Push to GitHub
        push_to_github(file_path, data, st.secrets["GITHUB_POCKET"])
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
    save_and_sync(DB_FILE, st.session_state["finance_data"])  # Save changes and push to GitHub
elif page == _("Add Income") or page == "Add Income":
    st.session_state["finance_data"] = show_add_income(st.session_state["finance_data"], DB_FILE)
    save_and_sync(DB_FILE, st.session_state["finance_data"])  # Save changes and push to GitHub
elif page == _("Analyze") or page == "Analyze":
    show_analysis(st.session_state["finance_data"])
elif page == _("Manage Data") or page == "Manage Data":
    show_manage_data(st.session_state["finance_data"], DB_FILE)
    save_and_sync(DB_FILE, st.session_state["finance_data"])  # Save changes and push to GitHub
elif page == _("Settings") or page == "Settings":
    show_settings(st.session_state["finance_data"], DB_FILE)
elif page == _("Debt Management") or page == "Debt Management":
    show_debt_page(st.session_state["debt_data"], DEBT_FILE)
    save_and_sync(DEBT_FILE, st.session_state["debt_data"])  # Save changes and push to GitHub
