# tests/test_dump_loader.py
from pathlib import Path
import json
import logging

from web_agent.rag.loader import read_workstories_xlsx, load_docs

log = logging.getLogger("dump")

ART = Path("tests/_artifacts")
ART.mkdir(parents=True, exist_ok=True)

def _save_json(name: str, data):
    p = ART / name
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"guardado: {p.resolve()}  (items={len(data) if hasattr(data,'__len__') else 'n/a'})")

def test_dump_stories_and_docs():
    # 1) STORIES (completas y “visibles”)
    stories = read_workstories_xlsx("data/work_stories.xlsx")
    stories_json = [{"title": t, "text": x} for (t, x) in stories]
    _save_json("stories.json", stories_json)

    # 2) DOCS (completas; acota texto para no hacer archivos gigantes)
    docs = load_docs("data")
    docs_json = [{"title": t, "text": (x if len(x) < 4000 else x[:4000] + " …[truncado]")} for (t, x) in docs]
    _save_json("docs.json", docs_json)

    # 3) Asserts mínimos (para que el test valide “tiene sentido”)
    assert isinstance(stories, list)
    assert isinstance(docs, list)
    assert all(isinstance(t, str) and isinstance(x, str) for t, x in stories)
    assert all(isinstance(t, str) and isinstance(x, str) for t, x in docs)
