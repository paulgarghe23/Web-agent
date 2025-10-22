import re
import logging
import numpy as np
from typing import List, Tuple
from .loader import load_docs
from web_agent.llm.generate import llm_generate, get_embedding

log = logging.getLogger(__name__)

class RAGpipeline:
    def __init__(self) -> None:
        self.docs: List[Tuple[str, str]] = load_docs("data")
        # Pre-compute embeddings for all documents
        self.doc_embeddings: List[List[float]] = []
        for _, text in self.docs:
            self.doc_embeddings.append(get_embedding(text))
        log.info(f"pipeline.__init__: docs={len(self.docs)}")

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def answer(self, question: str) -> str:
        log.info(f"answer: question={question!r}")
        if not question.strip():
            log.info("empty_question")
            return "Ask me something :)"

        # Get embedding for the question
        q_embedding = get_embedding(question)
        
        # Calculate similarity scores using embeddings
        scored = []
        for i, (title, text) in enumerate(self.docs):
            similarity = self._cosine_similarity(q_embedding, self.doc_embeddings[i])
            scored.append((similarity, title, text))
        
        scored.sort(reverse=True)

        best_score, _, _ = scored[0]
        if best_score <= 0.3:  # Threshold for relevance
            return "Based on the context and information I have been provided until now, I don't know."

        # Top-K → contexto para el LLM (R+G real)
        K = 3
        context = "\n\n".join(f"[{t}]\n{tx}" for s, t, tx in scored[:K] if s > 0.3)
        log.info(f"answer: using_context_chars={len(context)} topK={min(K, len(scored))}")
        return llm_generate(context, question)
