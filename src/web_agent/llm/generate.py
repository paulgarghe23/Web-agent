from openai import OpenAI
import os
from typing import List
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = OpenAI(api_key=api_key)
    return _client

def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI's text-embedding-3-small model."""
    client = _get_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def llm_generate(context: str, question: str, model: str = "gpt-4o-mini") -> str:
    """
    Small wrapper that asks the LLM to answer STRICTLY from the provided CV context.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are Paul's personal AI agent. "
                "Answer ONLY using the provided CONTEXT about Paul. "
                "If the answer is not in the context, reply something like this, adapted to context, and always in the same language the user asks: "
                "'Based on the context and information I have been provided until now, I don't know.' "
                "Be concise and helpful."
            ),
        },
        {
            "role": "user",
            "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        },
    ]
    resp = _get_client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=450,
    )
    return resp.choices[0].message.content.strip()
