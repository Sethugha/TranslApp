from deep_translator import GoogleTranslator
from langdetect import detect
import asyncio

async def detect_language(text):
    """Erkennt die Sprache mit langdetect"""
    return detect(text)

async def translate_message(message, source_lang = 'de', target_lang = 'en'):
    """Fetches the translation of 'text'
    :param
    :return: translated text
    """
    await asyncio.sleep(0)
    translated = GoogleTranslator().translate(message)
    return translated


