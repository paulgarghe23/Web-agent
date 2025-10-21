from pathlib import Path
import json
from web_agent.rag import pipeline as P

ART = Path("tests/_artifacts"); ART.mkdir(parents=True, exist_ok=True)

def test_qa_dump(monkeypatch):
    fake_docs = [
        ("project", "Web-Agent: personal AI agent."),
        ("stack", "Stack: FastAPI, Poetry, LangChain."),
        ("story 1", "S: context T: task A: actions R: results"),
    ]
    monkeypatch.setattr(P, "load_docs", lambda *_: fake_docs)
    rp = P.RAGpipeline()

    qs = ["What’s the stack?", "Tell me about the project", "STAR?"]
    answers = [{ "q": q, "a": rp.answer(q) } for q in qs]

    with (ART / "answers.json").open("w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

    assert any("FastAPI" in x["a"] for x in answers)
    assert any("personal AI agent" in x["a"] for x in answers)
