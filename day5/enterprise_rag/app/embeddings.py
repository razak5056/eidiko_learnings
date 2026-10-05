from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_embedding_model():

    return HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )