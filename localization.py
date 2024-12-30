import json
import os

CURRENT_LANGUAGE = "en"
TRANSLATIONS = {}  # Default empty dictionary

def load_translations(language):
    file_path = f"translations/{language}.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}.")
            return {}
    else:
        print(f"Error: Translation file for '{language}' not found. Falling back to default.")
        return {}

def set_language(language):
    global CURRENT_LANGUAGE, TRANSLATIONS
    CURRENT_LANGUAGE = language
    TRANSLATIONS = load_translations(language)
    if TRANSLATIONS:
        print(f"Loaded translations for '{language}'.")
    else:
        print(f"Warning: No translations found for '{language}'. Using default texts.")

def _(text):
    return TRANSLATIONS.get(text, text)  # Return the translation or the original text if not found

# Default to English at startup
TRANSLATIONS = load_translations(CURRENT_LANGUAGE)
