from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


account_sid = os.getenv("MS_TWILIO_ACCOUNT_SID")
api_sid = os.getenv("MS_TWILIO_API_KEY_SID")
api_secret = os.getenv("MS_TWILIO_API_KEY_SECRET")
my_number = os.getenv("MY_PHONE_NUMBER")
twilio_number = "whatsapp:+493083795321"

# Create a Twilio client
client = Client(api_sid, api_secret, account_sid)

# 1. Create a conversation (no v1 prefix needed)
conversation = client.conversations.conversations.create(friendly_name="My WhatsApp Chat")
print("Conversation created:", conversation.sid)

# 2. Check if participant already exists and add them (no v1 prefix needed)
participants = client.conversations.conversations(conversation.sid).participants.list()

# Check if the participant (your phone number) is already in the conversation
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

# 3. Send a message to the conversation (no v1 prefix needed)
message = client.conversations.conversations(conversation.sid) \
    .messages \
    .create(author=f"whatsapp:{my_number}", body="👋 Hello from Python script!")

print("Message sent:", message.sid)
