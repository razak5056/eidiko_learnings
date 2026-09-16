from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Groq model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key="YOUR_GROQ_API_KEY"
)

# Technical prompt
technical_prompt = PromptTemplate.from_template(
    "Explain {topic} in a technical and detailed way."
)

# Beginner prompt
beginner_prompt = PromptTemplate.from_template(
    "Explain {topic} in very simple beginner-friendly language."
)

# Chains
technical_chain = technical_prompt | model | StrOutputParser()

beginner_chain = beginner_prompt | model | StrOutputParser()


# Router
def route(input_data):
    if input_data["level"] == "technical":
        return technical_chain
    else:
        return beginner_chain


# Dynamic chain
def dynamic_chain(input_data):
    chain = route(input_data)

    return chain.invoke({
        "topic": input_data["topic"]
    })


# Test
result = dynamic_chain({
    "level": "technical",
    "topic": "RAG"
})

print(result)