from langchain_core.prompts import ChatPromptTemplate


# Step 1
title_prompt = ChatPromptTemplate.from_template(
    """
Create a short and professional title for this topic:

{topic}
"""
)


# Step 2
explanation_prompt = ChatPromptTemplate.from_template(
    """
Explain the following topic in simple beginner-friendly language.

Topic:
{topic}

Title:
{title}
"""
)


# Step 3
summary_prompt = ChatPromptTemplate.from_template(
    """
Create a short summary of the following topic.

Topic:
{topic}

Explanation:
{explanation}
"""
)


# Step 4
questions_prompt = ChatPromptTemplate.from_template(
    """
Create 5 interview questions about this topic.

Topic:
{topic}

Explanation:
{explanation}
"""
)


# Final step
final_prompt = ChatPromptTemplate.from_template(
    """
Create a final learning report.

Topic:
{topic}

Title:
{title}

Explanation:
{explanation}

Summary:
{summary}

Interview Questions:
{questions}

Format the response clearly using headings.
"""
)