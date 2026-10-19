
from app.services.parser import parse_whatsapp_chat
from app.services.preprocessor import preprocess_messages
from app.services.chunker import create_chunks
from app.services.search import ChatSearchEngine


# Load and prepare the WhatsApp chat
messages = parse_whatsapp_chat("data/_chat.txt")
cleaned_messages = preprocess_messages(messages)
chunks = create_chunks(cleaned_messages)

# Build the search engine
search_engine = ChatSearchEngine()
search_engine.build_index(chunks)

print(f"Search index built with {len(chunks)} chunks.")

# Search the chat
query = "internship"
results = search_engine.search(query, top_k=5)

print(f"\nSearch query: {query}")
print(f"Results found: {len(results)}\n")

for i, result in enumerate(results, start=1):
    print(f"RESULT {i}")
    print(f"Similarity score: {result['score']:.4f}")
    print(f"Messages in chunk: {result['message_count']}")
    print(result["text"][:500])
    print("-" * 50)
