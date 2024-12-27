import streamlit as st
import json
import os
from localization import set_language, _

SETTINGS_FILE = "expense_settings.json"
EXPENSE_CATEGORIES = [
    _("Food"),
    _("Transport"),
    _("Rent"),
    _("Clothes"),
    _("Restaurants"),
    _("Travel & picnic"),
    _("Utilities"),
    _("Others")
]

def load_settings():
    default_settings = {
        "grades": {
            "Most to Do": 50,
            "Good to Do": 30,
            "Nice to Do": 15,
            "Saving Target": 5,
        },
        "categories": {category: "Unclassified" for category in ["Food", "Transport", "Rent", "Clothes", "Restaurants", "Travel & picnic", "Utilities", "Others"]},
        "language": "en",  # Default language
    }

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            loaded_settings = json.load(file)
            # Ensure default keys exist in loaded settings
            for key, value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = value
            return loaded_settings
    else:
        return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def show_settings(finance_data, db_file):
    st.title(_("⚙️ Settings"))

    # Load current settings
    settings = load_settings()

    # Language Settings
    st.subheader(_("🌐 Language Settings"))
    language = st.radio(
        _("Select Application Language"),
        options=["en", "ku"],
        index=0 if settings["language"] == "en" else 1,
        format_func=lambda lang: _("English") if lang == "en" else _("Kurdish")
    )

    if language != settings["language"]:
        # Save the new language setting
        settings["language"] = language
        save_settings(settings)

        # Apply the new language
        set_language(language)

        # Trigger a Streamlit rerun using a success message
        st.set_query_params(language_changed="true")

    # Check query parameters for language change
    query_params = st.query_params
    if query_params.get("language_changed"):
        st.success(_("Language changed successfully. Reloading..."))
        st.set_query_params()  # Clear the query parameter
        return  # Exit to allow the app to rerun cleanly

    # Display grade percentage allocation
    st.subheader(_("🚦 Grade Percentage Allocation"))
    for grade_key, grade_value in settings["grades"].items():
        settings["grades"][grade_key] = st.slider(
            f"{_(grade_key)} {_('Percentage')}",
            min_value=0,
            max_value=100,
            value=grade_value,
            step=1,
        )

    # Normalize percentages to 100% (optional)
    total_percentage = sum(settings["grades"].values())
    if total_percentage != 100:
        st.warning(_("The total percentage is {total_percentage}%. Adjust to make it exactly 100%.").format(total_percentage=total_percentage))

    # Display and edit expense category classifications
    st.subheader(_("🗂️ Classify Expense Categories"))
    for category in EXPENSE_CATEGORIES:
        settings["categories"][category] = st.selectbox(
            _("Classify {category}").format(category=category),
            options=[_("Most to Do"), _("Good to Do"), _("Nice to Do"), _("Saving Target"), _("Unclassified")],
            index=[
                _("Most to Do"), _("Good to Do"), _("Nice to Do"), _("Saving Target"), _("Unclassified")
            ].index(settings["categories"].get(category, _("Unclassified")))
        )

    # Save button
    if st.button(_("Save Settings")):
        try:
            save_settings(settings)
            st.success(_("Settings saved successfully!"))
        except Exception as e:
            st.error(f"Error saving settings: {e}")
