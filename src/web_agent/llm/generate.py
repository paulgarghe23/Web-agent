from openai import OpenAI
import os

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = OpenAI()
    return _client

def llm_generate(context: str, question: str, model: str = "gpt-4o-mini") -> str:
    """
    Small wrapper that asks the LLM to answer STRICTLY from the provided CV context.
    """
    prompt = (
        "Answer strictly using the provided CV context. "
        "If it's not in the context, say you don't know.\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION: {question}\nANSWER:"
    )
    resp = _get_client().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=350,
    )
    return resp.choices[0].message.content.strip()
