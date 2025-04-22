from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Credentials and phone numbers
account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
my_number = os.getenv("MY_PHONE_NUMBER")
twilio_number = "whatsapp:+493083795321"

# Initialize Twilio client
client = Client(api_sid, api_secret, account_sid)

# 1. Create a conversation (using Conversations API)
conversation = client.conversations.conversations.create(friendly_name="My WhatsApp Conversation")
print("Conversation created:", conversation.sid)

# 2. Check if the participant already exists before adding
participants = client.conversations.conversations(conversation.sid).participants.list()

# Check if your number is already a participant in the conversation
if not any(p.messaging_binding_address == f"whatsapp:{my_number}" for p in participants):
    participant = client.conversations.conversations(conversation.sid) \
        .participants \
        .create(
            messaging_binding_address=f"whatsapp:{my_number}",
            messaging_binding_proxy_address=twilio_number
        )
    print("Participant added:", participant.sid)
else:
    print("Participant already exists.")

# 3. Send a message in the conversation
message = client.conversations.conversations(conversation.sid) \
    .messages \
    .create(author=f"whatsapp:{my_number}", body="👋 Hello from the Python script!")

print("Message sent:", message.sid)
