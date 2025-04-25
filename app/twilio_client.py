# Aktuellste Version (fertig)
import os
from twilio.rest import Client
from dotenv import load_dotenv
from utils.colors import Colors as c

load_dotenv()

# Umgebungsvariablen laden
account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')
chat_service_sid = os.getenv('MS_TWILIO_CHAT_SERVICE_SID')
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
                return message.body, sender
        return None, None

    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None

def get_conversation_id():

    conversation = client.conversations \
        .v1.services(chat_service_sid) \
        .conversations \
        .create(friendly_name="My Conversation")
    return conversation.sid


def participant_check(use_conversation_sid):

    try:
        participants = client.conversations \
            .v1.services(chat_service_sid) \
            .conversations(use_conversation_sid) \
            .participants \
            .list()

        already_exists = any(
            p.messaging_binding.get("address") == sender_number
            for p in participants if p.messaging_binding
        )

        if not already_exists:
            participant = client.conversations \
                .v1.services(chat_service_sid) \
                .conversations(use_conversation_sid) \
                .participants \
                .create(
                messaging_binding_address=sender_number,
                messaging_binding_proxy_address=twilio_number
            )
            print(f"{c.blue}👥 Participant added:{c.reset}")
            print(f"Participant SID: {c.cyan}{participant.sid}{c.reset}")
        else:
            print("⚠️ Participant already exists – will not be added again.")

    except Exception as e:
        print(f"❌ Error in participant_check: {e}")

    except Exception as e:
        print(f"❌ Error in participant_check: {e}")


def send_message_to_conversation(to, text, use_conversation_sid):
    """Sends a WhatsApp message to the given number"""

    try:
        message = client.conversations \
            .v1.services(chat_service_sid) \
            .conversations(use_conversation_sid) \
            .messages \
            .create(
            author="User123",
            body=text
        )
        print(f"\n📨 Message sent to {c.cyan}{to}{c.reset}:")
        print(f"    → {c.bold}{c.cyan}{text}\n{c.reset}")

    except Exception as e:
        print(f"{c.red}❌ Error sending message: {e}{c.reset}")


def delete_conversation(conversation_sid):

    try:
        # Delete the conversation
        client.conversations \
            .v1.services(chat_service_sid) \
            .conversations(conversation_sid) \
            .delete()

        print(f"{c.blue}✅ Conversation {conversation_sid} deleted successfully.{c.reset}")

    except Exception as e:
        print(f"{c.red}❌ Error deleting conversation {conversation_sid}: {e}{c.reset}")