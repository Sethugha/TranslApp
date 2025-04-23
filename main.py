# Aktuellste Version 2.0
import asyncio
import twilio_client as twilio
from translation_api import translate_message
from translation_api import detect_language

AUTHORIZED_SENDER = "+491719043240"

def run_workflow():
    """Main function that runs the messaging and translation workflow."""
    print("Starting workflow...")

    # Step 1: Receive the latest WhatsApp message
    sender = AUTHORIZED_SENDER
    received_message, sender = twilio.receive_message(sender)
    print(f"Received message from {sender}: {received_message}")

    if received_message:
        twilio.manage_client_conversation(sender, received_message)

        detected_language = asyncio.run(detect_language(received_message))
        print(f"Detected language: {detected_language}")

        # Step 3: Translate the message to the receiver's preferred language (if required)
        # For example, translate to English
        translated_message = asyncio.run(translate_message(received_message, "en"))

        # Step 4: Let Person B reply to the message (simulating input here)
        print()
        response = input("Type your reply: ")

        # Step 5: Ask for the target language for the response
        lang_map = {
            "french": "fr",
            "english": "en",
            "german": "de",
        }
        translation_choice = input("Do you want the reply in French, English, or German? ").lower()
        print("The text get's translated to the target language")

        # Step 6: Translate the response
        translated_response = asyncio.run(translate_message(response, translation_choice))
        print(f"Translated response: {translated_response}")
        print()

        # Step 7: Send the translated message to Person A via Twilio
        twilio.send_message_to_conversation(sender, translated_response)
        print(f"Sent translated message to {sender}: {translated_response}")


if __name__ == "__main__":
    run_workflow()

