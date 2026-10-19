
import faiss
import numpy as np

from app.services.embedding import create_embeddings


class ChatSearchEngine:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build_index(self, chunks: list[dict]):
        """Create a FAISS index from chat chunks."""

        if not chunks:
            raise ValueError("No chat chunks provided.")

        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]
        embeddings = create_embeddings(texts)

        # FAISS expects 32-bit floating-point vectors.
        embeddings = np.asarray(embeddings, dtype=np.float32)

        # Each embedding has 384 dimensions.
        self.index = faiss.IndexFlatIP(embeddings.shape[1])

        # Add all chat vectors to the index.
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Find chat chunks most similar to a query."""

        if self.index is None:
            raise ValueError("Build the search index first.")

        query = query.strip()

        if not query:
            return []

        query_embedding = create_embeddings([query])
        query_embedding = np.asarray(
            query_embedding, dtype=np.float32
        )

        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_embedding, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            result = self.chunks[int(index)].copy()
            result["score"] = float(score)
            results.append(result)

        return results
