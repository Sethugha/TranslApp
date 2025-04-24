# Aktuellste Version (fertig)
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
    print("\n" + "=" * 75)
    print("🌍  WELCOME TO TRANSLAPP – YOUR WHATSAPP TRANSLATION ASSISTANT  🌍")
    print("-" * 75)
    print("This app helps translate WhatsApp messages between users in their")
    print("preferred languages. Let’s get started! 🚀")
    print("=" * 75 + "\n")

    print("🔍 Checking if the Twilio conversation ID is valid...")
    print()

    conversation_id = twilio.get_conversation_id()

    if conversation_id:
        print(f" ✅ Conversation found! \n -> SID: {conversation_id}")
        print()
        twilio.participant_check(conversation_id)
        print()

    with open('language_code.txt', 'r') as file:
        language_code =json.load(file)

    while True:
        preferred_language = input("🌐 Enter your preferred language or country code (e.g. en, de, French): ").lower()
        if len(preferred_language) == 2 and preferred_language in language_code.values():
            break
        if preferred_language in language_code:
            preferred_language = language_code[preferred_language]
            break
        print("❌ Invalid input. Please enter a valid language code or full country/language name.")


    while True:
        user_choice = input("\n📩 Press Enter to check for new messages or type 'exit' to quit: ").lower()

        if user_choice == 'exit':
            twilio.delete_conversation(conversation_id)
            print("\n👋 Exiting the workflow. See you next time!")
            break
        elif user_choice:
            continue

        sender = sender_number

        print()
        # Step 1: Receive the latest WhatsApp message
        received_message, sender = twilio.receive_message(sender)
        if not received_message:
            print("📭 No new messages.")
        else:
            print(f"\n📨 Message received from {sender}:")
            print(f"    → {received_message}\n")



        if received_message:
            detected_language = asyncio.run(detect_language(received_message))
            print(f"🧠 Detected language: {detected_language}")
            print()


            user_translated_language = asyncio.run(translate_message(received_message, preferred_language))
            print(f"🌐 Translated message: {user_translated_language}\n")


            # Step 4: Let Person B reply to the message (simulating input here)
            print()
            response = input("💬 Type your reply: ")
            print()


            # Step 6: Translate the response
            translated_response = asyncio.run(translate_message(response, detected_language))
            print(f"🔁 Translated reply to sender’s language: {translated_response}")
            print()

            # Step 7: Send the translated message to Person A via Twilio
            twilio.send_message_to_conversation(sender, translated_response, conversation_id)




if __name__ == "__main__":
    run_workflow()