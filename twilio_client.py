from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')
chat_service_sid = os.getenv('MS_TWILIO_CHAT_SERVICE_SID')

client = Client(api_key_sid, api_key_secret, account_sid)

clients = {}

def receive_message(sender):
    """Simuliert Empfang der letzten Nachricht"""
    try:
        message = client.conversations.v1.services(sender)
        print(f"Message from {sender}: {message.api_key_sid}")
        return message.body, sender
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None

def manage_client_conversation(sender, message_body):
    if sender in clients:
        clients[sender].append(message_body)
    else:
        clients[sender] = [message_body]

def get_or_create_conversation(sender):
    """Create or get existing conversation for a WhatsApp sender"""
    try:
        # First, check if a conversation already exists for the sender
        conversations = client.conversations.conversations.list()
        for convo in conversations:
            if convo.friendly_name == sender:
                return convo

        # If no existing conversation is found, create a new one
        conversation = client.conversations.conversations.create(
            friendly_name=sender  # The name of the conversation
        )

        # Add the WhatsApp user as a participant
        client.conversations.conversations(conversation.sid).participants.create(
            messaging_binding_address=f'whatsapp:{sender}',  # Sender's number
            messaging_binding_proxy_address='whatsapp:+493083795321'  # Your Twilio WhatsApp number
        )

        print(f"New conversation created for {sender}.")
        return conversation
    except Exception as e:
        print(f"Error getting/creating conversation: {e}")
        return None


def send_message_to_conversation(sender, message_body):
    try:
        conversation = get_or_create_conversation(sender)
        client.conversations.conversations(conversation.sid).messages.create(
            author="Bot",
            body=message_body
        )
        print(f"Sent message to {sender} via Conversation.")
    except Exception as e:
        print(f"Error sending message: {e}")
