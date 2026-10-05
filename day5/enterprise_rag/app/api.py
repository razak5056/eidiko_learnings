from pathlib import Path
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from llama_index.core import Settings
from llama_index.llms.groq import Groq

from chat_engine import create_chat_engine
from config import GROQ_API_KEY
from embeddings import get_embedding_model
from index import STORAGE_DIR, create_index, load_index
from ingestion import load_documents


@asynccontextmanager
async def lifespan(_app):
    _get_index()
    _app.state.index_ready = True
    yield


api = FastAPI(title="Enterprise RAG API", version="1.0.0", lifespan=lifespan)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST"],
    allow_headers=["Content-Type"],
)

_resources_lock = threading.RLock()
_index = None
_chat_engines = {}


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4000)


def _get_index():
    global _index

    with _resources_lock:
        if _index is not None:
            return _index
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is missing. Add it to the project .env file.")

        Settings.llm = Groq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )
        Settings.embed_model = get_embedding_model()

        if (STORAGE_DIR / "docstore.json").exists():
            _index = load_index()
        else:
            documents = load_documents()
            if not documents:
                raise RuntimeError("No documents were found in the project's data folder.")
            _index = create_index(documents)
        return _index


@api.get("/api/health")
def health_check():
    return {"status": "ok", "index_ready": getattr(api.state, "index_ready", False)}


@api.post("/api/chat")
def chat(request: ChatRequest):
    index = _get_index()
    with _resources_lock:
        engine = _chat_engines.get(request.session_id)
        if engine is None:
            engine = create_chat_engine(index)
            _chat_engines[request.session_id] = engine

    response = engine.chat(request.message.strip())
    sources = []
    for source_node in getattr(response, "source_nodes", []):
        metadata = source_node.node.metadata or {}
        source_path = metadata.get("file_name") or metadata.get("file_path") or metadata.get("source")
        if not source_path:
            continue
        label = Path(str(source_path)).name
        page = metadata.get("page_label")
        if page:
            label = f"{label} · page {page}"
        if label not in sources:
            sources.append(label)

    return {"answer": str(response), "sources": sources}


@api.delete("/api/chat/{session_id}")
def reset_chat(session_id: str):
    with _resources_lock:
        _chat_engines.pop(session_id, None)
    return {"status": "reset"}
