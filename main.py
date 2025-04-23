import twilio_client as twilio
from translation_api import translate_message

AUTHORIZED_SENDER = "+491719043240"

def run_workflow():
    """Main function that runs the messaging and translation workflow."""
    print("Starting workflow...")

    # Step 1: Receive the latest WhatsApp message
    sender = AUTHORIZED_SENDER
    received_message, sender = twilio.receive_message(sender)
    print(f"Received message from {sender}: {received_message}")

    if received_message:
        # Step 2: Add message to client's conversation (create or append)
        twilio.manage_client_conversation(sender, received_message)

        # Step 3: Translate the message to a preferred language (e.g., German to English)
        translated_message = translate_message(received_message, "de", "en")
        print(f"Translated message: {translated_message}")

        # Step 4: Prompt Person B (user at PyCharm) to reply
        response = input("Type your reply: ")

        # Step 5: Ask for translation target language
        translation_choice = input("Do you want to translate your reply to French, English, or German? (fr/en/de): ").strip().lower()

        # Step 6: Translate the response
        translated_response = translate_message(response, "de", translation_choice)  # Assuming your input is in German
        print(f"Translated response to send: {translated_response}")

        # Step 7: Send the translated message back to the original sender
        twilio.send_message(sender, translated_response)

if __name__ == "__main__":
    run_workflow()
