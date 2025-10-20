from web_agent.rag.pipeline import RAGpipeline

def test_pipeline_answer():
    pipeline = RAGpipeline()
    answer = pipeline.answer("Tell me what did you do when there was a platform collapse and how did you solve it?")
    assert isinstance(answer, str)
    assert len(answer) > 0