import re
from typing import List, Tuple
from .loader import load_docs


class RAGpipeline:
    def __init__(self) -> None:
        self.docs: List[Tuple[str, str]] = load_docs("data")

    def answer(self, question: str) -> str:
        q = question.lower()
        words = re.findall(r"\w+", q)
        if not words:
            return "Ask me something :)"
        scored = [(sum(w in text.lower() for w in words), title, text) for title, text in self.docs]
        scored.sort(reverse=True)
        best_score, _, best_text = scored[0]
        return best_text if best_score > 0 else "I don't know yet."
