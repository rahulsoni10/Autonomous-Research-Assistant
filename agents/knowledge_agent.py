def answer_question(index, question: str):
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response)
