import translation_api as tapi
#import Twilio
from twilio.rest import Client
import asyncio

import translate_functions


def dummy():
    pass


def main():
    message = "Warum sprang der schnelle braune Fuchs über den faulen Hund?"
    translated_message = asyncio.run(tapi.translate_message(message, 'de', 'en'))
    print(translated_message)


if __name__ == '__main__':
    main()
