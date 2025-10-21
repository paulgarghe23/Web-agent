import re
import logging
from typing import List, Tuple
from .loader import load_docs
from web_agent.llm.generate import llm_generate

log = logging.getLogger(__name__)

class RAGpipeline:
    def __init__(self) -> None:
        self.docs: List[Tuple[str, str]] = load_docs("data")
        log.info(f"pipeline.__init__: docs={len(self.docs)}")

    def answer(self, question: str) -> str:
        log.info(f"answer: question={question!r}")
        q = question.lower()
        words = re.findall(r"\w+", q)
        if not words:
            return "Ask me something :)"

        # tu retrieval actual (no lo tocamos)
        scored = [(sum(w in text.lower() for w in words), title, text) for title, text in self.docs]
        scored.sort(reverse=True)

        best_score, _, _ = scored[0]
        if best_score <= 0:
            return "I don't know yet."

        # Top-K → contexto para el LLM (R+G real)
        K = 3
        context = "\n\n".join(f"[{t}]\n{tx}" for s, t, tx in scored[:K] if s > 0)
        log.info(f"answer: using_context_chars={len(context)} topK={min(K, len(scored))}")
        return llm_generate(context, question)
