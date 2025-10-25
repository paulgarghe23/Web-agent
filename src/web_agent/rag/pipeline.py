import re
import logging
import numpy as np
import json
import os
from pathlib import Path
from typing import List, Tuple
from .loader import load_docs
from web_agent.llm.generate import llm_generate, get_embedding

log = logging.getLogger(__name__)

class RAGpipeline:
    def __init__(self) -> None:
        self.docs: List[Tuple[str, str]] = load_docs("data")
        log.info(f"pipeline.__init__: docs loaded={len(self.docs)}")
        for i, (title, text) in enumerate(self.docs):
            log.info(f"pipeline.__init__: doc[{i}] title='{title}' text_length={len(text)}")
        
        # Try to load cached embeddings first
        self.doc_embeddings: List[List[float]] = self._load_or_compute_embeddings()
        log.info(f"pipeline.__init__: embeddings loaded/computed={len(self.doc_embeddings)}")
    
    def _get_cache_path(self) -> Path:
        """Get the path for the embeddings cache file."""
        return Path("/tmp/embeddings_cache.json")
    
    def _load_embeddings_from_cache(self) -> List[List[float]]:
        """Load embeddings from cache file."""
        cache_path = self._get_cache_path()
        log.info(f"pipeline._load_embeddings_from_cache: checking cache at {cache_path}")
        
        if not cache_path.exists():
            log.info("pipeline._load_embeddings_from_cache: cache file does not exist")
            return []
        
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
            
            log.info(f"pipeline._load_embeddings_from_cache: found {len(cached_data)} cached embeddings")
            log.info(f"pipeline._load_embeddings_from_cache: current docs count: {len(self.docs)}")
            
            # Check if we have the right number of embeddings
            if len(cached_data) == len(self.docs):
                log.info("pipeline._load_embeddings_from_cache: loaded from cache")
                return cached_data
            else:
                log.info(f"pipeline._load_embeddings_from_cache: cache mismatch (cached={len(cached_data)}, docs={len(self.docs)})")
                return []
        except Exception as e:
            log.warning(f"pipeline._load_embeddings_from_cache: failed to load cache: {e}")
            return []
    
    def _save_embeddings_to_cache(self, embeddings: List[List[float]]) -> None:
        """Save embeddings to cache file."""
        cache_path = self._get_cache_path()
        log.info(f"pipeline._save_embeddings_to_cache: saving {len(embeddings)} embeddings to {cache_path}")
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, 'w') as f:
                json.dump(embeddings, f)
            log.info(f"pipeline._save_embeddings_to_cache: saved to cache at {cache_path}")
        except Exception as e:
            log.warning(f"pipeline._save_embeddings_to_cache: failed to save cache: {e}")
    
    def _load_or_compute_embeddings(self) -> List[List[float]]:
        """Load embeddings from cache or compute them if cache doesn't exist."""
        # Try to load from cache first
        cached_embeddings = self._load_embeddings_from_cache()
        if cached_embeddings:
            return cached_embeddings
        
        # If no cache, compute embeddings
        log.info("pipeline._load_or_compute_embeddings: computing embeddings...")
        embeddings = []
        for _, text in self.docs:
            embeddings.append(get_embedding(text))
        
        # Save to cache for next time
        self._save_embeddings_to_cache(embeddings)
        return embeddings

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

        if not scored:
            return "Based on the context and information I have been provided until now, I don't know."
            
        best_score, _, _ = scored[0]
        log.info(f"answer: best_score={best_score:.3f}")
        if best_score <= 0.05:  # Threshold for relevance (lowered for better coverage)
            return "Based on the context and information I have been provided until now, I don't know."

        # Top-K → contexto para el LLM (R+G real)
        K = 3
        context = "\n\n".join(f"[{t}]\n{tx}" for s, t, tx in scored[:K] if s > 0.05)
        log.info(f"answer: using_context_chars={len(context)} topK={min(K, len(scored))}")
        return llm_generate(context, question)
