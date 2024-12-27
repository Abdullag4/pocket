import streamlit as st
import json
import os
from localization import set_language, _

def show_settings():
    st.title(_("Settings"))

    # Language Selection
    language = st.selectbox(_("Choose Language"), ["en", "ku"], index=0)
    if "language" not in st.session_state or st.session_state.language != language:
        st.session_state.language = language
        set_language(language)
    
    st.success(_("Language updated successfully!"))

SETTINGS_FILE = "expense_settings.json"
EXPENSE_CATEGORIES = ["Food", "Transport", "Rent", "Clothes", "Restaurants", "Travel & picnic", "Utilities", "Others"]

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        # Default settings in case the settings file is not available
        return {
            "grades": {
                "Most to Do": 50,
                "Good to Do": 30,
                "Nice to Do": 15,
                "Saving Target": 5,
            },
            "categories": {category: "Unclassified" for category in EXPENSE_CATEGORIES},
        }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def show_settings(finance_data, db_file):
    st.title("⚙️ Settings")
    st.subheader("💡 Expense Classification Settings")
    
    # Load current settings
    settings = load_settings()

    # Display grade percentage allocation
    st.subheader("🚦 Grade Percentage Allocation")
    for grade in settings["grades"]:
        settings["grades"][grade] = st.slider(
            f"{grade} Percentage",
            min_value=0,
            max_value=100,
            value=settings["grades"][grade],
            step=1,
        )

    # Normalize percentages to 100% (optional)
    total_percentage = sum(settings["grades"].values())
    if total_percentage != 100:
        st.warning(f"The total percentage is {total_percentage}%. Adjust to make it exactly 100%.")

    # Display and edit expense category classifications
    st.subheader("🗂️ Classify Expense Categories")
    for category in EXPENSE_CATEGORIES:
        settings["categories"][category] = st.selectbox(
            f"Classify {category}",
            options=["Most to Do", "Good to Do", "Nice to Do", "Saving Target", "Unclassified"],
            index=["Most to Do", "Good to Do", "Nice to Do", "Saving Target", "Unclassified"].index(
                settings["categories"].get(category, "Unclassified")
            ),
        )

    # Save button
    if st.button("Save Settings"):
        save_settings(settings)
        st.success("Settings saved successfully!")
