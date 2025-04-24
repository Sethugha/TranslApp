import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Umgebungsvariablen laden
account_sid = os.getenv('MS_TWILIO_ACCOUNT_SID')
api_key_sid = os.getenv('MS_TWILIO_API_KEY_SID')
api_key_secret = os.getenv('MS_TWILIO_API_KEY_SECRET')

# Twilio Client initialisieren
client = Client(api_key_sid, api_key_secret, account_sid)

conversation_sid = "CH5b24cd3d6f9b46468c02aa18b1bba2a8"
conversation = client.conversations.v1.conversations(conversation_sid).fetch()

print("✅ Conversation geladen:")
print(f"SID: {conversation.sid}")
print(f"Name: {conversation.friendly_name}")

# Beispielnummern
user_number = "whatsapp:+491775252784"
twilio_number = "whatsapp:+493083795321"

# Prüfen ob Teilnehmer schon existiert
participants = client.conversations \
    .v1.conversations(conversation.sid) \
    .participants \
    .list()

already_exists = any(
    p.messaging_binding.get("address") == user_number
    for p in participants if p.messaging_binding
)

if not already_exists:
    participant = client.conversations \
        .v1.conversations(conversation.sid) \
        .participants \
        .create(
            messaging_binding_address=user_number,
            messaging_binding_proxy_address=twilio_number
        )
    print("👥 Teilnehmer hinzugefügt:")
    print(f"Participant SID: {participant.sid}")
else:
    print("⚠️ Teilnehmer existiert bereits – wird nicht erneut hinzugefügt.")

# Nachricht senden
message = client.conversations \
    .v1.conversations(conversation.sid) \
    .messages \
    .create(
        author="ChatBenutzer123",  # Twilio verlangt hier entweder 'identity' oder 'author' (nicht die WhatsApp-Nummer direkt!)
        body="Hallo! Das ist eine WhatsApp-Nachricht 🚀"
    )

print("📨 WhatsApp-Nachricht gesendet.")
