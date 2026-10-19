
from app.services.embedding import create_embeddings

texts = [
    "I am looking for an internship.",
    "The summer student program is open.",
    "What should we order for dinner?"
]

embeddings = create_embeddings(texts)

print("Number of messages:", len(texts))
print("Embedding shape:", embeddings.shape)
print("First embedding (first 10 numbers):")
print(embeddings[0][:10])
