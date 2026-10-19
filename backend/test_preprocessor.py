from app.services.parser import parse_whatsapp_chat
from app.services.preprocessor import preprocess_messages


chat_file = "data/_chat.txt"

# Step 1: Parse the WhatsApp file
messages = parse_whatsapp_chat(chat_file)

# Step 2: Preprocess the messages
cleaned_messages = preprocess_messages(messages)

print(f"Messages before preprocessing: {len(messages)}")
print(f"Messages after preprocessing: {len(cleaned_messages)}")

print("\nFirst 10 cleaned messages:\n")

for message in cleaned_messages[:10]:
    print("Timestamp:", message["timestamp"])
    print("Sender:", message["sender"])
    print("Message:", message["message"])
    print("-" * 50)