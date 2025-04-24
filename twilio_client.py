# Aktuellste Version 2
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Umgebungsvariablen laden
account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')
chat_service_sid = os.getenv('MS_TWILIO_CHAT_SERVICE_SID')
conversation_sid = "CH5b24cd3d6f9b46468c02aa18b1bba2a8"
twilio_number = os.getenv('TWILIO_NUMBER')
sender_number = os.getenv('MY_PHONE_NUMBER')



# Twilio Client initialisieren
client = Client(api_key_sid, api_key_secret, account_sid)

def receive_message(sender):
    """Receive the latest message from a specific WhatsApp sender."""
    try:
        messages = client.messages.list(limit=20)
        for message in messages:
            if message.from_ == f'whatsapp:{sender}':
                print(f"Message from {sender}: {message.body}")
                return message.body, sender
        print("No message from authorized sender found.")
        return None, None

    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None

def get_conversation_id():
    conversation = client.conversations.v1.conversations(conversation_sid).fetch()
    return conversation.sid


def participant_check():
    use_conversation_sid = get_conversation_id()


    # Prüfen ob Teilnehmer schon existiert
    participants = client.conversations \
        .v1.conversations(use_conversation_sid) \
        .participants \
        .list()

    already_exists = any(
        p.messaging_binding.get("address") == sender_number
        for p in participants if p.messaging_binding
    )

    if not already_exists:
        participant = client.conversations \
            .v1.conversations(conversation_sid) \
            .participants \
            .create(
            messaging_binding_address=sender_number,
            messaging_binding_proxy_address=twilio_number
        )
        print("👥 Teilnehmer hinzugefügt:")
        print(f"Participant SID: {participant.sid}")
    else:
        print("⚠️ Teilnehmer existiert bereits – wird nicht erneut hinzugefügt.")



def send_message_to_conversation(to, text):
    """Sends a WhatsApp message to the given number"""
    use_conversation_sid = get_conversation_id()
    try:
        message = client.conversations \
            .v1.conversations(use_conversation_sid) \
            .messages \
            .create(
            author="ChatBenutzer123",
            body=text
        )

        print("📨 WhatsApp-Nachricht gesendet.")
        print(f"Message sent to {to}: {text}")
    except Exception as e:
        print(f"Error sending message: {e}")