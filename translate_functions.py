from langdetect import detect
def ask_sender_for_translation_choice():
    while True:
        choice = input("Would you like to translate? (y/n)").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False


def whatsapp_message():
    user_message = funktion_api_Gent()
    if ask_sender_for_translation_choice():
        return funktion_api_Gerd()
    return user_message

def funktion_api_Gerd():
    return "Übersetzen"


def funktion_api_Gent():
    return "translate"


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def send_translated_message():
     pass
