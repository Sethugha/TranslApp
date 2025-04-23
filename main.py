import asyncio
import twilio_client as twilio
from translation_api import translate_message, detect_language

AUTHORIZED_SENDER = "+491719043240"

def run_workflow():
    print("Starting workflow...")

    sender = AUTHORIZED_SENDER
    received_message, sender = twilio.receive_message(sender)
    print(f"Received message from {sender}: {received_message}")

    if received_message:
        twilio.manage_client_conversation(sender, received_message)

        detected_language = asyncio.run(detect_language(received_message))
        print(f"Detected language: {detected_language}")

        translated_message = asyncio.run(translate_message(received_message, source_lang="auto", target_lang="en"))
        print(f"Translated message: {translated_message}")

        response = input("Type your reply: ")

        lang_map = {
            "french": "fr",
            "english": "en",
            "german": "de",
            "deutsch": "de",
            "französisch": "fr",
            "englisch": "en"
        }
        translation_choice_input = input("Do you want the reply in French, English, or German? ").lower()
        translation_choice = lang_map.get(translation_choice_input, "en")

        translated_response = asyncio.run(translate_message(response, source_lang="auto", target_lang=translation_choice))

        twilio.send_message(sender, translated_response)

if __name__ == "__main__":
    run_workflow()
