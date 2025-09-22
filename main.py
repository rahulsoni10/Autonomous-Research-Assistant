import set_proxy

import os

print(os.environ['http_proxy'])

from agents.data_collector import collect_data
from agents.analyzer import summarize_text, create_vector_index
from agents.knowledge_agent import answer_question

topic = input("Enter research topic: ")
raw_text = collect_data(topic)

summary = summarize_text(raw_text)
print("\n---Summary---\n", summary)

index = create_vector_index(raw_text)

while True:
    question = input("\nAsk a question (or 'exit'): ")
    if question.lower() == "exit":
        break
    answer = answer_question(index, question)
    print("\nAnswer:\n", answer)

print("\nGoodbye!")