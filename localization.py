import json

TRANSLATION_FILE = "translations_ku.json"

def load_translations():
    with open(TRANSLATION_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

translations = load_translations()

def _(key):
    return translations.get(key, key)  # Default to the key if translation is missing
