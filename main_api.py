import set_proxy


from fastapi import FastAPI
from pydantic import BaseModel
from agents.data_collector import collect_data
from agents.analyzer import summarize_text, create_vector_index
from agents.knowledge_agent import answer_question

app = FastAPI()

# Store index in memory for now
index_cache = {}

class TopicRequest(BaseModel):
    topic: str

class QuestionRequest(BaseModel):
    topic: str
    question: str


@app.post("/process_topic")
def process_topic(req: TopicRequest):
    """Collect data, summarize it and create index."""
    raw_text = collect_data(req.topic)
    summary = summarize_text(raw_text)
    index = create_vector_index(raw_text)
    index_cache[req.topic] = index  # store for later use
    return {"topic": req.topic, "summary": summary}


@app.post("/ask_question")
def ask_question(req: QuestionRequest):
    """Answer a question about the topic."""
    if req.topic not in index_cache:
        return {"error": "Topic not processed yet. Call /process_topic first."}
    index = index_cache[req.topic]
    answer = answer_question(index, req.question)
    return {"answer": answer}
