from llama_index.core import PromptTemplate

def create_query_engine(index):

    query_engine = index.as_query_engine(
        similarity_top_k=5
    )

    return query_engine