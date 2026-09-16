from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# 1. Examples
examples = [
    {"input": "2 + 2", "output": "4"},
    {"input": "3 + 3", "output": "6"}
]

# 2. Example format
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Question: {input}\nAnswer: {output}"
)

# 3. Few-shot prompt
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}\nAnswer:",
    input_variables=["input"]
)

# 4. Create final prompt
result = prompt.invoke({"input": "5 + 5"})

print(result)