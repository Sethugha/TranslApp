from twilio.rest import Client #update to the latest version
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

# 1. Create a conversation (using the Conversations API v1)
conversation = client.conversations.v1.conversations.create(friendly_name="My WhatsApp Conversation")
print("Conversation created:", conversation.sid)

# 2. Check if the participant already exists
participants = client.conversations.v1.conversations(conversation.sid).participants.list()

# Check if your number is already a participant in the conversation
participant_exists = False
for participant in participants:
    print(f"Checking participant: {participant.messaging_binding_address}")
    if participant.messaging_binding_address == f"whatsapp:{my_number}":
        participant_exists = True
        print("Participant already exists in the conversation.")

# If the participant doesn't exist, add them
if not participant_exists:
    try:
        print(f"Adding participant with address: whatsapp:{my_number} and proxy address: {twilio_number}")
        participant = client.conversations.v1.conversations(conversation.sid) \
            .participants.create(
                messaging_binding_address=f"whatsapp:{my_number}",
                messaging_binding_proxy_address=twilio_number
            )
        print("Participant added:", participant.sid)
    except Exception as e:
        print("Error adding participant:", e)

# 3. Send a message in the conversation
message = client.conversations.v1.conversations(conversation.sid) \
    .messages \
    .create(author=f"whatsapp:{my_number}", body="👋 Hello from the Python script!")

print("Message sent:", message.sid)
