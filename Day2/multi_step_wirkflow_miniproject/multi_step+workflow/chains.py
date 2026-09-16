from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

from config import model

from prompts import (
    title_prompt,
    explanation_prompt,
    summary_prompt,
    questions_prompt,
    final_prompt
)


parser = StrOutputParser()


# -----------------------------
# Step 1: Title Chain
# -----------------------------

title_chain = title_prompt | model | parser


# -----------------------------
# Step 2: Explanation Chain
# -----------------------------

explanation_chain = explanation_prompt | model | parser


# -----------------------------
# Step 3: Summary Chain
# -----------------------------

summary_chain = summary_prompt | model | parser


# -----------------------------
# Step 4: Interview Questions
# -----------------------------

questions_chain = questions_prompt | model | parser


def create_workflow(topic):

    # Step 1
    title = title_chain.invoke({
        "topic": topic
    })


    # Step 2
    explanation = explanation_chain.invoke({
        "topic": topic,
        "title": title
    })


    # Step 3 and Step 4 run independently
    parallel_chain = RunnableParallel(
        summary=summary_chain,
        questions=questions_chain
    )


    parallel_result = parallel_chain.invoke({
        "topic": topic,
        "explanation": explanation
    })


    # Final step
    final_chain = final_prompt | model | parser

    result = final_chain.invoke({
        "topic": topic,
        "title": title,
        "explanation": explanation,
        "summary": parallel_result["summary"],
        "questions": parallel_result["questions"]
    })


    return result