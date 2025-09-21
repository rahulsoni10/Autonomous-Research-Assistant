import sys, os
import streamlit as st

# add project root (one directory up) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.data_collector import collect_data
from agents.analyzer import summarize_text, create_vector_index
from agents.knowledge_agent import answer_question

st.title("🌟 AMRA - Text Research Assistant 🌟")

# Initialize session_state for index if not exists
if 'index' not in st.session_state:
    st.session_state['index'] = None

topic = st.text_input("Enter topic to research:")
if st.button("Collect & Summarize"):
    if topic.strip():  # avoid empty topic
        raw_text = collect_data(topic)
        st.success("✅ Data collected!")

        summary = summarize_text(raw_text)
        st.subheader("Summary:")
        st.write(summary)

        st.session_state['index'] = create_vector_index(raw_text)
    else:
        st.warning("⚠️ Please enter a topic first!")

question = st.text_input("Ask a question:")
if st.button("Get Answer"):
    if st.session_state['index'] is not None and question.strip():
        answer = answer_question(st.session_state['index'], question)
        st.subheader("Answer:")
        st.write(answer)
    elif st.session_state['index'] is None:
        st.warning("⚠️ Please collect & summarize first!")
    else:
        st.warning("⚠️ Please enter a question!")
