import json

def load_translations(language):
    file_path = f"translations_{language}.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Store the active translations globally
translations = {}

def set_language(language):
    global translations
    translations = load_translations(language)

def _(key):
    return translations.get(key, key)  # Default to the key if translation is missing
