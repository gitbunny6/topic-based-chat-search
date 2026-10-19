from app.services.parser import parse_whatsapp_chat
from app.services.preprocessor import preprocess_messages
from app.services.chunker import create_chunks


chat_file = "data/_chat.txt"

# Parse
messages = parse_whatsapp_chat(chat_file)

# Clean
cleaned_messages = preprocess_messages(messages)

# Create chunks
chunks = create_chunks(cleaned_messages)

print(f"Cleaned messages: {len(cleaned_messages)}")
print(f"Chunks created: {len(chunks)}")

print("\nFirst 3 chunks:\n")

for i, chunk in enumerate(chunks[:3], start=1):

    print(f"CHUNK {i}")
    print("-" * 50)

    print("Start:", chunk["start_time"])
    print("End:", chunk["end_time"])
    print("Messages:", chunk["message_count"])

    print("\nText:")
    print(chunk["text"])

    print("=" * 60)