from langdetect import detect
import translation_api


def ask_sender_for_translation_choice():
    """
       Ask the sender whether they would like to proceed with translation.

       Continuously prompts the user with the question "Would you like to translate? (y/n)".
       The input is case-insensitive and only accepts 'y' or 'n' as valid responses.
       Repeats the prompt until a valid input is given.

       Returns:
           bool: True if the user chooses 'y', False if the user chooses 'n'.
       """
    while True:
        choice = input("Would you like to translate? (y/n) ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False


def whatsapp_message():
    """
        Handle a WhatsApp message and optionally translate it.

        This function retrieves a user message via Twilio->`funktion_api_Gent()`.
        It then prompts the user using `ask_sender_for_translation_choice()` to determine
        whether the message should be translated.

        If translation is requested, it returns the translated message via translation_api->`funktion_api_Gerd()`.
        Otherwise, it returns the original message.

        Returns:
            str: The translated message if chosen, or the original user message.
        """
    user_message = funktion_api_Gent()
    if ask_sender_for_translation_choice():
        return funktion_api_Gerd()
    return user_message


def funktion_api_Gerd():
    """
    the code from Gerd
    :return:
    """
    return "Übersetzen"

def detect_language(text):
    """
      Detect the language of the given text.

      Uses a language detection library to determine the language code
      (e.g., 'en' for English, 'de' for German). If detection fails,
      it returns "unknown".

      Args:
          text (str): The input text whose language should be detected.

      Returns:
          str: A two-letter language code if detection is successful,
               or "unknown" if an error occurs.
      """
    try:
        return detect(text)
    except:
        return "unknown"


def send_translated_message():
    pass
