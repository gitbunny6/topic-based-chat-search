from app.services.parser import parse_whatsapp_chat


chat_file = "data/_chat.txt"

messages = parse_whatsapp_chat(chat_file)

print(f"Total parsed entries: {len(messages)}")

system_messages = [
    message for message in messages
    if message["type"] == "system"
]

print(f"System messages: {len(system_messages)}")

print("\nSystem messages:\n")

for message in system_messages:
    print("Timestamp:", message["timestamp"])
    print("Message:", message["message"])
    print("-" * 50)