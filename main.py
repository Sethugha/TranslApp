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
    print("\n" + "=" * 75)
    print("🌍  WELCOME TO TRANSLAPP – YOUR WHATSAPP TRANSLATION ASSISTANT  🌍")
    print("-" * 75)
    print("This app helps translate WhatsApp messages between users in their")
    print("preferred languages. Let’s get started! 🚀")
    print("=" * 75 + "\n")

    print("🔍 Checking if the Twilio conversation ID is valid...\n")

    if twilio.get_conversation_id():
        print(f" ✅ Conversation found! \n -> SID: {twilio.get_conversation_id()}\n")
        twilio.participant_check()
        print()

    with open('language_code.txt', 'r') as file:
        language_code = json.load(file)

    while True:
        preferred_language = input("🌐 Enter your preferred language or country code (e.g. en, de, French): ").lower()
        if len(preferred_language) == 2 and preferred_language in language_code.values():
            break
        if preferred_language in language_code:
            preferred_language = language_code[preferred_language]
            break
        print("❌ Invalid input. Please enter a valid language code or full country/language name.")

    last_message_sid = None  # NEU: letzte empfangene Nachricht merken

    while True:
        user_choice = input(f"\n📩 Press Enter to check for new messages or type 'exit' to quit"
                            f"\n or type 'send' to send a message to {sender_number}: ").lower()

        sender = sender_number
        if user_choice == 'exit':
            print("\n👋 Exiting the workflow. See you next time!")
            break
        elif user_choice == 'send':
            print()
            sending_message = input("💬 Type your message to send: ")
            twilio.send_message_to_conversation(sender, sending_message)
            continue
        elif user_choice:
            continue

        print()

        # Step 1: Receive the latest WhatsApp message
        received_message, sender, message_sid = twilio.receive_message(sender)

        if not received_message or message_sid == last_message_sid:
            print("📭 No new messages.")
            print("\n👋 Exiting the workflow. See you next time!")
            break
        last_message_sid = message_sid


        print(f"\n📨 Message received from {sender}:")
        print(f"    → {received_message}\n")

        detected_language = asyncio.run(detect_language(received_message))
        print(f"🧠 Detected language: {detected_language}\n")

        user_translated_language = asyncio.run(translate_message(received_message, preferred_language))
        print(f"🌐 Translated message: {user_translated_language}\n")

        print()
        response = input("💬 Type your reply: ")
        print()

        translated_response = asyncio.run(translate_message(response, detected_language))
        print(f"🔁 Translated reply to sender’s language: {translated_response}\n")

        twilio.send_message_to_conversation(sender, translated_response)



if __name__ == "__main__":
    run_workflow()
