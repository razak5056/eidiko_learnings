def get_retriever(index):

    retriever = index.as_retriever(
        similarity_top_k=5
    )

    return retriever