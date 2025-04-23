# Aktuellste Version 2.0
from twilio.rest import Client
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()


account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')
chat_service_sid = os.getenv('MS_TWILIO_CHAT_SERVICE_SID')

client = Client(api_key_sid, api_key_secret, account_sid)

clients = {}

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


def manage_client_conversation(sender, message_body):
    if sender in clients:
        clients[sender].append(message_body)
    else:
        clients[sender] = [message_body]

def get_or_create_conversation(sender):
    """Create or get existing conversation for a WhatsApp sender"""
    try:
        # Check for existing conversation inside the right chat service
        conversations = client.conversations.services(chat_service_sid).conversations.list()
        for convo in conversations:
            if convo.friendly_name == sender:
                return convo

        # Create new conversation within the chat service
        conversation = client.conversations.services(chat_service_sid).conversations.create(
            friendly_name=sender
        )

        # Check if the participant is already in the conversation
        participants = client.conversations.services(chat_service_sid) \
            .conversations(conversation.sid) \
            .participants.list()

        # Only add participant if they are not already in the conversation
        if not any(p.messaging_binding_address == f'whatsapp:{sender}' for p in participants):
            client.conversations.services(chat_service_sid) \
                .conversations(conversation.sid) \
                .participants \
                .create(
                    messaging_binding_address=f'whatsapp:{sender}',
                    messaging_binding_proxy_address='whatsapp:+493083795321'
                )

            print(f"New participant added for {sender}.")
        else:
            print(f"Participant {sender} already exists in the conversation.")

        return conversation
    except Exception as e:
        print(f"Error getting/creating conversation: {e}")
        return None


def send_message_to_conversation(sender, message_body):
    try:
        conversation = get_or_create_conversation(sender)

        if conversation is None:
            print(f"Error: No valid conversation found for {sender}.")
            return

        # Debugging: SID der Conversation ausgeben
        print(f"Using conversation SID: {conversation.sid}")

        # Nachricht senden
        message = client.conversations \
            .services(chat_service_sid) \
            .conversations(conversation.sid) \
            .messages \
            .create(author='system', body=message_body)

        print(f"Sent message to {sender} via Twilio.")
    except Exception as e:
        print(f"Error sending message: {e}")


"""
        client.conversations.conversations(conversation.sid).messages.create(
            author="Bot",
            body=message_body
        )
        """