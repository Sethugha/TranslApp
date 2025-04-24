# Aktuellste Version 2.
import asyncio
import json
import os
import twilio_client as twilio
from translation_api import translate_message
from translation_api import detect_language
from dotenv import load_dotenv


load_dotenv()

sender_number = os.getenv('AUTHORIZED_SENDER')


def run_workflow():
    """Main function that runs the messaging and translation workflow."""

    if twilio.get_conversation_id():
        print("✅ Conversation ID is valid."
              f"\n SID: {twilio.get_conversation_id()}")

    with open('language_code.txt', 'r') as file:
        language_code =json.load(file)

    while True:
        preferred_language = input("Please enter your preferred language or country code: ").lower()
        if len(preferred_language) == 2 and preferred_language in language_code.values():
            break
        if preferred_language in language_code:
            preferred_language = language_code[preferred_language]
            break
        print("Error: Please enter a valid language code or country name.")



    while True:
        user_choice = input("Press Enter to check for new messages. "
                            "Type 'exit' to quit ").lower()

        if user_choice == 'exit':
            print("Exiting the workflow.")
            break
        elif user_choice:
            continue

        sender = sender_number

        # Step 1: Receive the latest WhatsApp message
        received_message, sender = twilio.receive_message(sender)
        print(f"Received message from {sender}: {received_message}")

        if received_message:
            detected_language = asyncio.run(detect_language(received_message))
            print(f"Detected language: {detected_language}")


            user_translated_language = asyncio.run(translate_message(received_message, preferred_language))
            print(f"Translated message in your language: {user_translated_language}")
            print()


            # Step 4: Let Person B reply to the message (simulating input here)
            print()
            response = input("Type your reply: ")


            # Step 6: Translate the response
            translated_response = asyncio.run(translate_message(response, detected_language))
            print(f"Translated response: {translated_response}")
            print()

            # Step 7: Send the translated message to Person A via Twilio
            twilio.participant_check()
            twilio.send_message_to_conversation(sender, translated_response)
            print(f"Sent translated message to {sender}: {translated_response}")



if __name__ == "__main__":
    run_workflow()

