from llama_index.core import Settings

from config import GROQ_API_KEY
from ingestion import load_documents
from embeddings import get_embedding_model
from index import STORAGE_DIR, create_index, load_index
from chat_engine import create_chat_engine

from llama_index.llms.groq import Groq


def main():

    # -------------------------
    # LLM
    # -------------------------

    llm = Groq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0
    )

    # -------------------------
    # Embedding Model
    # -------------------------

    embed_model = get_embedding_model()

    Settings.llm = llm
    Settings.embed_model = embed_model

    # -------------------------
    # Create / Load Index
    # -------------------------

    if (STORAGE_DIR / "docstore.json").exists():

        print("Loading existing index...")

        index = load_index()

    else:

        print("Creating new index...")

        documents = load_documents()

        index = create_index(
            documents
        )

    # -------------------------
    # Chat Engine
    # -------------------------

    chat_engine = create_chat_engine(
        index
    )

    # -------------------------
    # Chat Loop
    # -------------------------

    while True:

        question = input("\nUser: ")

        if question.lower() == "exit":
            break

        response = chat_engine.chat(
            question
        )

        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    main()