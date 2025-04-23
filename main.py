import twilio_client as twilio
from translation_api import translate_message  # Assuming translation is handled in a separate file


def run_workflow():
    """Main function that runs the workflow"""
    print("Starting workflow...")

    # Step 1: Receive message from Person A (via Twilio)
    received_message, sender = twilio.receive_message()

    if received_message:
        # Step 2: Handle the message, check if client already exists, and update their conversation
        twilio.manage_client_conversation(sender, received_message)

        # Step 3: Translate the message to the receiver's preferred language (if required)
        # For example, translate to English
        translated_message = translate_message(received_message, "en")

        # Step 4: Let Person B reply to the message (simulating input here)
        print(f"Message received from {sender}: {received_message}")
        response = input("Type your reply: ")

        # Step 5: Ask if the response needs to be translated (to French, English, or German)
        translation_choice = input("Do you want the reply in French, English, or German? ")

        # Step 6: Translate the response
        translated_response = translate_message(response, translation_choice)

        # Step 7: Send the translated message to Person A via Twilio
        twilio.send_message(sender, translated_response)


if __name__ == "__main__":
    run_workflow()
