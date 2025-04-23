from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables Atuell
load_dotenv()

# Retrieve Twilio API credentials from environment variables
account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')

# Debug: Print credentials to ensure they are correctly loaded
print(f"Account SID: {account_sid}")
print(f"API Key SID: {api_key_sid}")
print(f"API Key Secret: {api_key_secret}")

# Initialize Twilio client with API Key SID, API Key Secret, and Account SID
try:
    client = Client(api_key_sid, api_key_secret, account_sid)
    print("Twilio Client initialized successfully!")
except Exception as e:
    print(f"Error initializing Twilio Client: {e}")

# A simple structure to manage clients and their conversations
clients = {}

def receive_message():
    """Receives the latest WhatsApp messages via Twilio"""
    try:
        messages = client.messages.list(limit=1)
        for message in messages:
            print(f"Message from {message.from_}: {message.body}")
            return message.body, message.from_
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None, None

def manage_client_conversation(sender, message_body):
    """Checks if a client already exists and creates a conversation if not"""
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
    try:
        message = client.messages.create(
            body=body,
            from_='whatsapp:+14155238886',  # Your Twilio WhatsApp number
            to=f'whatsapp:{to}'  # The recipient's WhatsApp number
        )
        print(f"Message sent to {to}: {body}")
    except Exception as e:
        print(f"Error sending message: {e}")