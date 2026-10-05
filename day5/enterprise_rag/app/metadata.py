def add_metadata(documents):

    for document in documents:

        document.metadata["department"] = "company"
        document.metadata["access"] = "internal"

    return documents