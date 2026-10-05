from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from config import PROJECT_ROOT

STORAGE_DIR = PROJECT_ROOT / "storage"


def create_index(documents):

    index = VectorStoreIndex.from_documents(
        documents
    )

    index.storage_context.persist(
        persist_dir=str(STORAGE_DIR)
    )

    print("Index created and stored.")

    return index


def load_index():

    storage_context = StorageContext.from_defaults(
        persist_dir=str(STORAGE_DIR)
    )

    index = load_index_from_storage(
        storage_context
    )

    print("Index loaded from storage.")

    return index