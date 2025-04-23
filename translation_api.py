import asyncio
from deep_translator import GoogleTranslator


async def detect_language(text):
    await asyncio.sleep(0)
    result = GoogleTranslator(source=source_lang, target=target_lang).detect(message)
    return result


async def translate_message(message, source_lang, target_lang):
    """Fetches the translation of 'text'
    :param
    :return: translated text
    """
    await asyncio.sleep(0)
    translated = GoogleTranslator().translate(message)
    return translated



def main():
    result = asyncio.run(translate_message("Más vale tarde que nunca", 'es', 'de'))

    print(result)


if __name__ == '__main__':
    main()

#phonenum1 = "+493083795321", phonenum2 = "+491775252784"
