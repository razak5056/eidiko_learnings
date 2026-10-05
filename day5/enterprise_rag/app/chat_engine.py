def create_chat_engine(index):

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        similarity_top_k=5
    )

    return chat_engine