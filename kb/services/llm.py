from ollama import chat


MODEL_NAME = "llama3.2:3b"


def generate_answer(question, context):

    prompt = f"""
You are a helpful knowledge base assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer cannot be found in the context,
say that the information was not found in the knowledge base.

Do not invent or assume information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]