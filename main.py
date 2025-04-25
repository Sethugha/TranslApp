import time
import asyncio
import json
import os
from app import twilio_client as twilio
import threading
from api.translation_api import translate_message
from api.translation_api import detect_language
from dotenv import load_dotenv
from utils.colors import Colors as c

load_dotenv()
sender_number = os.getenv('AUTHORIZED_SENDER')
stop_event = threading.Event()
pause_event = threading.Event()
user_choice = None  # Global variable to store the user input
conversation_id = twilio.get_conversation_id()
prompt = f"{c.green}📩 Press Enter to send a message or type 'exit' to quit: {c.reset}"
def run_workflow():
    """Main function that runs the messaging and translation workflow."""
    print(f"{c.orange}\n" + "=" * 75)
    print("🌍  WELCOME TO TRANSLAPP – YOUR WHATSAPP TRANSLATION ASSISTANT  🌍")
    print("-" * 75)
    print("This app helps translate WhatsApp messages between users in their")
    print("preferred languages. Let’s get started! 🚀")
    print("=" * 75 + f"\n{c.reset}")

    print(f"{c.blue}🔍 Checking if the Twilio conversation ID is valid...{c.reset}")
    print()

    if conversation_id:
        print(f"{c.blue} ✅ Conversation found!{c.reset} \n "
              f"-> SID: {c.cyan}{conversation_id}{c.reset}")
        print()
        twilio.participant_check(conversation_id)
        print()

    with open('language_code.txt', 'r') as file:
        language_code = json.load(file)
    while True:
        preferred_language = input(f"{c.green}🌐 Enter your preferred language or country code"
                                   f" (e.g. en, de, French): {c.reset}").lower()
        if len(preferred_language) == 2 and preferred_language in language_code.values():
            break
        if preferred_language in language_code:
            preferred_language = language_code[preferred_language]
            break
        print(f"{c.red}❌ Invalid input. "
              f"Please enter a valid language code or full country/language name.{c.reset}")
    t = threading.Thread(target=parallel_message_check, args=(preferred_language,))
    t.start()

    # Start the user input thread
    input_thread = threading.Thread(target=user_input_thread)
    input_thread.start()

    while not stop_event.is_set():
        time.sleep(1)

    # Clean up threads before exit
    input_thread.join()
    t.join()
    twilio.delete_conversation(conversation_id)
    print(f"{c.orange}\n👋 Exiting the workflow. See you next time!{c.reset}")


def parallel_message_check(preferred_language):
    global user_choice
    global prompt
    old_message = ""

    while not stop_event.is_set():
        if pause_event.is_set():
            time.sleep(1)
            continue

        time.sleep(2)
        # Step 1: Receive the latest WhatsApp message
        received_message, sender = twilio.receive_message(sender_number)

        if received_message and received_message != old_message:
            detected_language = asyncio.run(detect_language(received_message))
            print()
            print(f"{c.orange} You have a new message!{c.reset}")
            time.sleep(0.5)
            print()
            print(f"Received message: {c.bold}{c.cyan}{received_message}{c.reset}")
            print(f"🧠 Detected language: {c.cyan}{detected_language}{c.reset}")
            print()

            user_translated_language = asyncio.run(
                translate_message(received_message, preferred_language))
            print(f"🌐 Translated message: {c.bold}{c.cyan}{user_translated_language}{c.reset}\n")
            print("💬 You received a translated message, now it's your turn to reply.")
            print()
            print(f"{c.cyan}💬 Please type your reply: {c.reset}", end="")
            prompt = ""
            if user_choice != "Reply":
                while not user_choice:
                    time.sleep(0.1)
            response = user_choice
            stop_event.set()
            get_user_message_input(sender, detected_language, response)
            prompt = f"{c.green}📩 Press Enter to send a message or type 'exit' to quit: {c.reset}"
            print(prompt, end="", flush=True)


            old_message = received_message
        elif user_choice == "Reply":
            while True:
                print(f"{c.green}💬 Please type your message: {c.reset}", end="", flush=True)
                reply = input()
                if reply:
                    stop_event.set()
                    break
            get_user_message_input(sender_number, "en", reply)
            user_choice = None
            time.sleep(1)
            input_thread = threading.Thread(target=user_input_thread)
            input_thread.start()


def user_input_thread():
    """Handles user input in a separate thread."""
    global user_choice
    global prompt

    while not stop_event.is_set():
        print(prompt, end="", flush=True)
        user_choice = input()

        if user_choice == 'exit':
            stop_event.set()  # Stop all threads if exit is chosen
            break
        elif not user_choice: # If Enter is pressed without text, we allow the user to reply
            stop_event.set()
            user_choice = "Reply"

    time.sleep(1)

def get_user_message_input(sender, detected_language, response):
    """Get a message from the user and send it after translation."""

    print(f"💬 You replied: {c.bold}{c.cyan}{response}{c.reset}")
    # Step 6: Translate the response
    try:
        translated_response = asyncio.run(translate_message(response, detected_language))
        print("🔁 Translated reply to sender’s language: "
              f"{c.bold}{c.cyan}{translated_response}{c.reset}")
        print()

        # Step 7: Send the translated message to Person A via Twilio
        print("📨 WhatsApp message sending ...")
        twilio.send_message_to_conversation(sender, translated_response, conversation_id)

    except Exception as e:
        print(f"{c.red}❌ Error during translation: {str(e)}{c.reset}")
    finally:
        time.sleep(1)
        stop_event.clear()
        pause_event.clear()



if __name__ == "__main__":
    run_workflow()
