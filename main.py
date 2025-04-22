"""import translataion_api
import Twilio
import client"""

import translate_functions


def dummy():
    pass


def main():
    dummy()
    print("The text language is :",
          translate_functions.detect_language(translate_functions.funktion_api_Gerd()))
    print(translate_functions.whatsapp_message())


if __name__ == '__main__':
    main()
