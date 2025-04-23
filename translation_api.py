from deep_translator import GoogleTranslator
from langdetect import detect

async def detect_language(text):
    """Erkennt die Sprache mit langdetect"""
    return detect(text)

async def translate_message(message, source_lang, target_lang):
    """Übersetzt die Nachricht"""
    return GoogleTranslator(source=source_lang, target=target_lang).translate(message)
