import json
import os

CURRENT_LANGUAGE = "en"
TRANSLATIONS = {}  # Default empty dictionary

def load_translations(language):
    file_path = f"translations/{language}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Translation file for {language} not found.")
        
def set_language(language):
    global CURRENT_LANGUAGE, TRANSLATIONS
    CURRENT_LANGUAGE = language
    TRANSLATIONS = load_translations(language)

def _(text):
    return TRANSLATIONS.get(text, text) if TRANSLATIONS else text

# Default to English
TRANSLATIONS = load_translations(CURRENT_LANGUAGE)
