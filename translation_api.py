from deep_translator import GoogleTranslator
from langdetect import detect

async def detect_language(text):
    """
    Detect the language of the given text using langdetect.
    """
    try:
        return detect(text)
    except Exception as e:
        print(f"Fehler bei der Spracherkennung: {e}")
        return None

async def translate_message(message, source_lang, target_lang):
    """
    Übersetzt die Nachricht vom Quell- in die Zielsprache mit Google Translate.
    """
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(message)
        return translated
    except Exception as e:
        print(f"Fehler bei der Übersetzung: {e}")
        return None
