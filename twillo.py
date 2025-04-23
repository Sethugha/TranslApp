from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Twilio API keys from environment variables
account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')

# Initialize Twilio client
client = Client(account_sid, api_key_sid, api_key_secret)

# A simple structure to manage clients and their conversations
clients = {}

def receive_message():
    """Receives the latest WhatsApp messages via Twilio"""
    messages = client.messages.list(limit=1)
    for message in messages:
        print(f"Message from {message.from_}: {message.body}")
        return message.body, message.from_

def manage_client_conversation(sender, message_body):
    """Checks if a client already exists, and creates a conversation if not"""
    if sender in clients:
        print(f"Client {sender} already exists. Adding message to their conversation.")
        # Append the message to the client's existing conversation
        clients[sender].append(message_body)
    else:
        print(f"New client {sender} created.")
        # Create a new conversation for the client
        clients[sender] = [message_body]

def send_message(to, body):
    """Sends a WhatsApp message to the given number"""
    message = client.messages.create(
        body=body,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{to}'
    )
    print(f"Message sent to {to}: {body}")
