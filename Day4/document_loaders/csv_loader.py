from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("data.csv")

documents = loader.load()

for doc in documents:
    print(doc.page_content)