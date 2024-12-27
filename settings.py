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
            _("Most to Do"): 50,
            _("Good to Do"): 30,
            _("Nice to Do"): 15,
            _("Saving Target"): 5,
        },
        "categories": {category: _("Unclassified") for category in EXPENSE_CATEGORIES},
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
        settings["language"] = language
        set_language(language)
        st.experimental_rerun()  # Restart the app to apply changes

    # Display grade percentage allocation
    st.subheader(_("🚦 Grade Percentage Allocation"))
    for grade in settings["grades"]:
        settings["grades"][grade] = st.slider(
            f"{grade} {_('Percentage')}",
            min_value=0,
            max_value=100,
            value=settings["grades"][grade],
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
        save_settings(settings)
        st.success(_("Settings saved successfully!"))
