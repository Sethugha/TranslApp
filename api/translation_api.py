# Aktuellste Version (fertig)
from deep_translator import GoogleTranslator
from langdetect import detect
import asyncio

async def detect_language(text):
    """Detect the language of a given text using langdetect."""
    return detect(text)

async def translate_message(message, target_lang='en', source_lang='auto'):
    """Translate a message from source_lang to target_lang using GoogleTranslator.

    Args:
        message (str): The text to be translated.
        target_lang (str): The target language code (e.g., 'en', 'de', 'fr').
        source_lang (str): The source language code (default is 'auto').

    Returns:
        str: The translated text.
    """
    await asyncio.sleep(0)  # simulate async behavior
    translated = GoogleTranslator(source=source_lang, target=target_lang).translate(message)
    return translated
