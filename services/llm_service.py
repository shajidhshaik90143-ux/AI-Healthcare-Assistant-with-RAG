from groq import Groq

from utils.config import GROQ_API_KEY, MODEL_NAME
from utils.prompts import SYSTEM_PROMPT
from services.rag_service import build_context


def get_client():

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it to your .env file."
        )

    return Groq(
        api_key=GROQ_API_KEY
    )


def get_healthcare_response(
    question,
    documents,
    conversation_history=None
):

    client = get_client()

    context = build_context(
        documents
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Keep only recent conversation
    if conversation_history:

        recent_messages = conversation_history[-6:]

        for message in recent_messages:

            role = message.get(
                "role"
            )

            content = message.get(
                "content"
            )

            if role in ["user", "assistant"]:

                messages.append({
                    "role": role,
                    "content": content
                })

    user_prompt = f"""
MEDICAL KNOWLEDGE BASE CONTEXT:

{context}

--------------------------------

USER QUESTION:

{question}

--------------------------------

Instructions:

Answer the user's question using the provided
medical knowledge context.

If the context does not contain enough information,
say so clearly.

Do not diagnose the user.

Do not prescribe medication.

At the end, provide a short "Sources" section
listing the document names and page numbers used.
"""

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=1200
    )

    return response.choices[0].message.content