import translataion_api
import Twilio
import client
from langdetect import detect


def should_be_message_translate(receiver_lang = "DE"):
    #return receiver_lang != profile_lang()
    pass

def ask_sender_for_translation_choice():
    return input("Would you like to translate? (y/n)").lower()


def whatsapp_message():

    user_message = funktion_api_Gent()
    if should_be_message_translate():
        funktion_api_Gerd()
    return user_message

def funktion_api_Gerd():
    pass


def funktion_api_Gent():
    return "translate"


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def send_translated_message():
     pass

def dummy():
    pass


def main():
    dummy()
    msg = whatsapp_message()
    receiver_lang = detect_language(msg)
    choice = ask_sender_for_translation_choice()
    if choice == "y":
        translated = funktion_api_Gerd()
        send_translated_message()
    else:
        send_translated_message()

if  __name__ == '__main__':
    main()
