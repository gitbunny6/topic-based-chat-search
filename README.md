# ChatSearch – Topic-Based Chat Search System

An AI-powered semantic search application that helps users find meaningful conversations from their WhatsApp chat history using natural-language queries.

Instead of relying on exact keyword matching, ChatSearch uses sentence embeddings and vector similarity search to retrieve conversations based on their meaning and context.

## Overview

Finding a particular conversation in a large chat history can be difficult when you don't remember the exact words used.

ChatSearch addresses this problem by allowing users to upload exported WhatsApp conversations and search them using topics, ideas, or natural-language queries.

For example, users can search for:

- Internship opportunities
- Project discussions
- Meeting schedules
- Technical conversations
- Previously shared information

The application retrieves conversation segments that are semantically similar to the search query.

## Features

- **WhatsApp Chat Processing:** Parses exported WhatsApp `.txt` conversations.
- **Chat Upload:** Uploads chat exports through the application.
- **Text Preprocessing:** Removes system messages and unnecessary formatting characters.
- **Conversation Chunking:** Groups consecutive messages into searchable segments.
- **Semantic Search:** Retrieves conversations based on meaning rather than exact keyword matches.
- **Sentence Embeddings:** Uses Sentence Transformers to convert text into numerical vectors.
- **Vector Similarity Search:** Uses FAISS for efficient similarity-based retrieval.
- **Search Results:** Displays relevant conversation segments with similarity scores and timestamps.
- **REST API:** Provides backend endpoints using FastAPI.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React.js, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| Numerical Processing | NumPy |
| API Communication | REST APIs |

## System Architecture

```text
              WhatsApp Chat Export
                       |
                       v
                Chat Upload API
                       |
                       v
                Chat Parser
                       |
                       v
                Preprocessing
                       |
                       v
                Text Chunking
                       |
                       v
              Sentence Transformer
                       |
                       v
               Vector Embeddings
                       |
                       v
                 FAISS Index
                       |
                       v
              Semantic Search API
                       |
                       v
                 React Frontend
                       |
                       v
                Search Results
```

## Project Structure

```text
topic-based-chat-search/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── parser.py
│   │   │   ├── preprocessor.py
│   │   │   ├── chunker.py
│   │   │   ├── embedding.py
│   │   │   └── search.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── test_parser.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

*Note: The backend also contains additional test files for preprocessing, chunking, embeddings and search.*

## How It Works

### 1. Chat Parsing

The parser reads exported WhatsApp chat files and extracts message timestamps, sender information and message content.

### 2. Preprocessing

The preprocessing module removes unnecessary formatting characters, media placeholders, empty messages and WhatsApp system messages.

### 3. Chunking

Consecutive messages are grouped into segments of approximately 500 characters to preserve conversational context.

### 4. Embedding Generation

The Sentence Transformer model `all-MiniLM-L6-v2` converts each conversation segment into a 384-dimensional numerical embedding.

### 5. Vector Indexing

FAISS stores the generated embeddings in an `IndexFlatIP` index for inner-product similarity search. Since the embeddings are normalized, this corresponds to cosine similarity.

### 6. Semantic Retrieval

When a user submits a query, ChatSearch generates its embedding and retrieves the most similar conversation segments.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible supported version
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/gitbunny6/topic-based-chat-search.git

cd topic-based-chat-search
```

### 2. Set Up the Backend

```bash
cd backend

python3 -m venv .venv
```

Activate the virtual environment.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 3. Set Up the Frontend

Open another terminal:

```bash
cd topic-based-chat-search/frontend

npm install
npm run dev
```

Open the local Vite URL displayed in your terminal, usually:

`http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running |
| GET | `/health` | Returns API health status |
| POST | `/upload` | Uploads and indexes a WhatsApp chat |
| POST | `/search` | Searches conversations using a query |

### Example Search Request

```json
{
  "query": "internship opportunities",
  "top_k": 5
}
```

## Testing

The backend includes test scripts covering different stages of the processing pipeline:

- `test_parser.py`
- `test_preprocessor.py`
- `test_chunker.py`
- `test_embedding.py`
- `test_chat_embeddings.py`
- `test_search.py`

Run the tests from the backend directory using the appropriate Python test commands.

## Privacy Considerations

WhatsApp exports can contain private conversations and personal information.

- Do not commit personal chat exports to the repository.
- Keep uploaded conversation files out of public version control.
- Use anonymized or sample conversations when demonstrating the application.
- Review deployment and storage practices before processing real user data.

## Future Improvements

- Support additional chat export formats.
- Improve conversation grouping and contextual retrieval.
- Add filters for sender and date range.
- Evaluate retrieval quality using Precision@K and Recall@K.
- Add automated backend and frontend tests.
- Introduce persistent vector storage.
- Deploy the application for public access.

## Author

**Radhika Sharma**

Information Technology Student | Software Developer

- GitHub: https://github.com/gitbunny6
- LinkedIn: https://www.linkedin.com/in/radhika-sharma-91971a290/

---

*Built to explore semantic search, natural-language processing, vector databases and full-stack application development.*
