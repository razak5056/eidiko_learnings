from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

# Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# JSON parser
parser = JsonOutputParser()

# Chain
chain = model | parser

# Run
result = chain.invoke("""
Give information about Python.

Return JSON with:
name
type
use
""")

print(result)
print(type(result))