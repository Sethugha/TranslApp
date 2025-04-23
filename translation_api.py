import asyncio
from deep_translator import GoogleTranslator


async def detect_language(text):
    """
    Detect the language of the given text.
    """
    translator = GoogleTranslator()
    detected_lang = translator.detect(text)
    return detected_lang


async def translate_message(message, source_lang, target_lang):
    """Fetches the translation of 'text'
    :param
    :return: translated text
    """
    await asyncio.sleep(0)
    translated = GoogleTranslator().translate(message)
    return translated




