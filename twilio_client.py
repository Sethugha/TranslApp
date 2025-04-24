import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')
chat_service_sid = os.getenv('MS_TWILIO_CHAT_SERVICE_SID')
conversation_sid = "CH2374ec189a69428bbddd5bb7add0b772"
twilio_number = os.getenv('TWILIO_NUMBER')
sender_number = os.getenv('MY_PHONE_NUMBER')

client = Client(api_key_sid, api_key_secret, account_sid)

def receive_message(sender):
    """Receive the latest message from a specific WhatsApp sender."""
    try:
        messages = client.messages.list(limit=20)
        for message in messages:
            if message.from_ == f'whatsapp:{sender}':
                return message.body, sender, message.sid  # NEU: SID mit zurückgeben
        print("No message from authorized sender found.")
        return None, None, None
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None, None

def get_conversation_id():
    conversation = client.conversations.v1.conversations(conversation_sid).fetch()
    return conversation.sid

def participant_check():
    use_conversation_sid = get_conversation_id()
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
        print("👥 Participant added:")
        print(f"Participant SID: {participant.sid}")
    else:
        print("⚠️ Participant already exists – will not be added again.")

def send_message_to_conversation(to, text):
    """Sends a WhatsApp message to the given number"""
    use_conversation_sid = get_conversation_id()
    try:
        message = client.messages.create(
            body=text,
            from_=twilio_number,
            to=sender_number
        )

        print("📨 WhatsApp message sending ...")
        print(f"\n📨 Message send to {to}:")
        print(f"    → {text}\n")
    except Exception as e:
        print(f"Error sending message: {e}")
