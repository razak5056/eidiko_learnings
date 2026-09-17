from langchain_community.document_loaders import TextLoader
loader = TextLoader.load(
    "/home/bandaru/Desktop/langchain/Day4/document_loaders/sample.txt"
)
documents = loader.load()
print(documents[0].page_content)