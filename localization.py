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
            raise ValueError(f"Invalid JSON format in {file_path}")
    else:
        raise FileNotFoundError(f"Translation file for {language} not found.")
        
def set_language(language):
    global CURRENT_LANGUAGE, TRANSLATIONS
    CURRENT_LANGUAGE = language
    TRANSLATIONS = load_translations(language)
    print(f"Loaded translations for {language}: {TRANSLATIONS}")  # Debug statement

def _(text):
    return TRANSLATIONS.get(text, text) if TRANSLATIONS else text

# Default to English
TRANSLATIONS = load_translations(CURRENT_LANGUAGE)
