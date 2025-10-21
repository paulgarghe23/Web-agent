import pytest
import json
from pathlib import Path
from web_agent.rag.pipeline import RAGpipeline

def test_snowball_question():
    """
    Test simple: pregunta sobre Snowball y verifica que responde algo relevante.
    """
    # Inicializar pipeline
    pipeline = RAGpipeline()
    
    # Guardar documentos en _artifacts (como test_dump_loader)
    artifacts_dir = Path("tests/_artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    docs_data = []
    for title, text in pipeline.docs:
        docs_data.append({
            "title": title,
            "text": text,
            "length": len(text)
        })
    
    docs_file = artifacts_dir / "loaded_docs.json"
    with open(docs_file, 'w', encoding='utf-8') as f:
        json.dump(docs_data, f, ensure_ascii=False, indent=2)
    
    print(f"Documentos guardados en: {docs_file}")
    
    # Pregunta sobre Snowball
    question = "Cuéntame qué hiciste cuando la plataforma Snowball colapsó?"
    
    # Obtener respuesta
    answer = pipeline.answer(question)
    
    # Guardar pregunta y respuesta en _artifacts
    qa_data = {
        "question": question,
        "answer": answer,
        "answer_length": len(answer),
        "snowball_mentioned": "snowball" in answer.lower()
    }
    
    qa_file = artifacts_dir / "snowball_qa.json"
    with open(qa_file, 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, ensure_ascii=False, indent=2)
    
    print(f"Pregunta y respuesta guardadas en: {qa_file}")
    
    # Verificaciones básicas
    assert isinstance(answer, str), "La respuesta debe ser un string"
    assert len(answer) > 0, "La respuesta no puede estar vacía"
    assert "snowball" in answer.lower(), "La respuesta debe mencionar Snowball"
    
    # Verificar que contiene información relevante
    relevant_words = ["plataforma", "colapso", "500m", "200m", "configuraciones"]
    found_words = [word for word in relevant_words if word in answer.lower()]
    assert len(found_words) >= 2, f"La respuesta debe contener al menos 2 palabras relevantes. Encontradas: {found_words}"
    
    print(f"\nPregunta: {question}")
    print(f"Respuesta: {answer}")
    print(f"Palabras relevantes encontradas: {found_words}")