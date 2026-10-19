
from app.services.parser import parse_whatsapp_chat
from app.services.preprocessor import preprocess_messages
from app.services.chunker import create_chunks
from app.services.embedding import create_embeddings


# Step 1: Read the WhatsApp chat
messages = parse_whatsapp_chat("data/_chat.txt")

# Step 2: Clean the messages
cleaned_messages = preprocess_messages(messages)

# Step 3: Combine messages into chunks
chunks = create_chunks(cleaned_messages)

# Step 4: Extract the text from each chunk
texts = [chunk["text"] for chunk in chunks]

# Step 5: Generate embeddings
embeddings = create_embeddings(texts)

# Display results
print("Original messages:", len(messages))
print("Cleaned messages:", len(cleaned_messages))
print("Chunks created:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("\nFirst chunk:")
print(texts[0][:300])
