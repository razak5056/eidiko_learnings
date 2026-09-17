from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")

documents = loader.load()

for doc in documents:
    print(doc.page_content)