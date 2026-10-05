from llama_index.core import SimpleDirectoryReader
from config import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"

def load_documents():

    documents = SimpleDirectoryReader(
        input_dir=str(DATA_DIR)
    ).load_data()

    return documents