import streamlit as st
import json
import os

SETTINGS_FILE = "expense_settings.json"

# Default Settings
DEFAULT_SETTINGS = {
    "grades": {
        "Most to Do": 50,
        "Good to Do": 30,
        "Nice to Do": 15,
        "Saving Target": 5,
    },
    "categories": {
        "Food": "Most to Do",
        "Rent": "Most to Do",
        "Transport": "Good to Do",
        "Utilities": "Good to Do",
    },
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def show_settings(finance_data, db_file):
    st.title("⚙️ Settings")

    # Load current settings
    settings = load_settings()

    # Grade Percentage Settings
    st.subheader("🛠️ Configure Grade Percentages")
    for grade, percentage in settings["grades"].items():
        new_percentage = st.slider(f"{grade} (%)", 0, 100, percentage)
        settings["grades"][grade] = new_percentage

    # Category Classification
    st.subheader("📂 Classify Expense Categories")
    categories = finance_data["Category"].unique() if not finance_data.empty else []
    for category in categories:
        grade = st.selectbox(
            f"Assign grade to {category}:",
            list(settings["grades"].keys()),
            index=list(settings["grades"].keys()).index(
                settings["categories"].get(category, "Nice to Do")
            )
            if category in settings["categories"]
            else 0,
        )
        settings["categories"][category] = grade

    # Save Button
    if st.button("Save Settings"):
        save_settings(settings)
        st.success("Settings saved successfully!")
