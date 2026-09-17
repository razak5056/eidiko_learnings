from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
LangChain is a framework for building AI applications.
It provides tools for agents, RAG and LLM applications.

RAG retrieves relevant information from a vector database.
The retrieved information is then given to the LLM.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print("----")
    print(chunk)