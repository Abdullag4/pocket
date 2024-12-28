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
    _("Others"),
]
print(f"Expense categories: {EXPENSE_CATEGORIES}")  # Debug output

def load_settings():
    """Load application settings from the settings file."""
    default_settings = {
        "grades": {
            "Most to Do": 50,
            "Good to Do": 30,
            "Nice to Do": 15,
            "Saving Target": 5,
        },
        "categories": {category: "Unclassified" for category in EXPENSE_CATEGORIES},
        "language": "en",  # Default language
    }

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            loaded_settings = json.load(file)
            for key, value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = value
            return loaded_settings
    else:
        return default_settings

def save_settings(settings):
    """Save application settings to the settings file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def show_settings(finance_data, db_file):
    """Display the settings page with proper error handling."""
    try:
        st.title(_("⚙️ Settings"))

        # Load current settings
        settings = load_settings()

        # Language Settings
        st.subheader(_("🌐 Language Settings"))
        language = st.radio(
            _("Select Application Language"),
            options=["en", "ku"],
            index=0 if settings["language"] == "en" else 1,
            format_func=lambda lang: _("English") if lang == "en" else _("Kurdish"),
        )

        if language != settings["language"]:
            settings["language"] = language  # Update the language in settings
            save_settings(settings)  # Save the updated settings to file
            set_language(language)  # Apply the new language

            st.success(_("Language changed successfully. Please refresh the page."))

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

# Translation map for grade categories
grade_translation_map = {
    "Most to Do": _("Most to Do"),
    "Good to Do": _("Good to Do"),
    "Nice to Do": _("Nice to Do"),
    "Saving Target": _("Saving Target"),
    "Unclassified": _("Unclassified"),
}

# Reverse translation map for mapping localized values back to English
reverse_grade_translation_map = {v: k for k, v in grade_translation_map.items()}

for category in EXPENSE_CATEGORIES:
    # Get current classification for the category in English
    current_classification = settings["categories"].get(category, "Unclassified")
    
    # Translate the current classification to the active language
    translated_classification = grade_translation_map.get(current_classification, _("Unclassified"))

    # Display a dropdown to classify the category
    selected_classification = st.selectbox(
        _("Classify {category}").format(category=category),
        options=list(grade_translation_map.values()),  # Localized options
        index=list(grade_translation_map.values()).index(translated_classification),
    )
    
    # Store the selected classification back in English
    settings["categories"][category] = reverse_grade_translation_map[selected_classification]
    
 # Save button
        if st.button(_("Save Settings")):
            try:
                save_settings(settings)
                st.success(_("Settings saved successfully!"))
            except Exception as e:
                st.error(f"Error saving settings: {e}")
    except FileNotFoundError as e:
        st.error(_("Error: Missing translation file or invalid path. Details: {error}").format(error=str(e)))
    except Exception as e:
        st.error(_("An unexpected error occurred: {error}").format(error=str(e)))
