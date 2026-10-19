from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import UploadFile, File
import io
import zipfile

from app.services.parser import parse_whatsapp_chat
from app.services.preprocessor import preprocess_messages
from app.services.chunker import create_chunks
from app.services.search import ChatSearchEngine


app = FastAPI(
    title="Topic-Based Chat Search System",
    description="AI-powered semantic search for chat conversations",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request format for the search endpoint
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# Create the search engine when the API starts
search_engine = ChatSearchEngine()


@app.on_event("startup")
def load_chat_index():
    messages = parse_whatsapp_chat("data/_chat.txt")
    cleaned_messages = preprocess_messages(messages)
    chunks = create_chunks(cleaned_messages)

    search_engine.build_index(chunks)


@app.get("/")
def root():
    return {
        "message": "Topic-Based Chat Search API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/search")
def search_chat(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    if not 1 <= request.top_k <= 20:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 20."
        )

    try:
        results = search_engine.search(
            request.query,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "total_results": len(results),
            "results": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Search failed."
        ) from error

@app.post("/upload")

async def upload_chat(file: UploadFile = File(...)):
    import os
    import tempfile
    import zipfile
    from io import BytesIO

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in {".txt", ".zip"}:
        raise HTTPException(
            status_code=400,
            detail="Please upload a WhatsApp .txt or .zip file."
        )

    temp_path = None

    try:
        content = await file.read()

        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        # If a ZIP was uploaded, find the WhatsApp TXT file inside it.
        if extension == ".zip":
            try:
                with zipfile.ZipFile(BytesIO(content)) as archive:
                    txt_files = [
                        name for name in archive.namelist()
                        if name.lower().endswith(".txt")
                        and not name.startswith("__MACOSX/")
                        and not name.split("/")[-1].startswith("._")
                    ]

                    if not txt_files:
                        raise HTTPException(
                            status_code=400,
                            detail="The ZIP contains no WhatsApp .txt file."
                        )

                    # Prefer WhatsApp's usual exported chat filename.
                    chat_files = [
                        name for name in txt_files
                        if name.split("/")[-1].lower() == "_chat.txt"
                    ]

                    selected_file = (
                        chat_files[0] if chat_files else txt_files[0]
                    )
                    content = archive.read(selected_file)

            except zipfile.BadZipFile as error:
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded ZIP file is invalid."
                ) from error

        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="The chat text file inside the upload is empty."
            )

        # Save the TXT content temporarily for the existing parser.
        with tempfile.NamedTemporaryFile(
            suffix=".txt", delete=False
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        messages = parse_whatsapp_chat(temp_path)
        cleaned_messages = preprocess_messages(messages)

        if not cleaned_messages:
            raise HTTPException(
                status_code=400,
                detail="No searchable messages were found in this file."
            )

        chunks = create_chunks(cleaned_messages)

        # Build the search index from the newly uploaded chat.
        search_engine.build_index(chunks)

        return {
            "message": "Chat uploaded and indexed successfully.",
            "filename": filename,
            "messages_processed": len(cleaned_messages),
            "chunks_indexed": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not process this chat file."
        ) from error

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

    