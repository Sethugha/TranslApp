"""import translataion_api
import Twilio
import client"""

import translate_functions

def dummy():
    pass


def main():
    dummy()
    msg = translate_functions.whatsapp_message()
    receiver_lang = translate_functions.detect_language(msg)
    choice = translate_functions.ask_sender_for_translation_choice()
    if choice == "y":
        translated = translate_functions.funktion_api_Gerd()
        translate_functions.send_translated_message()
    else:
        translate_functions.send_translated_message()

if  __name__ == '__main__':
    main()
