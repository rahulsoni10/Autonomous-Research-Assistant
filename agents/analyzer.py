import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# --- 1. Setup and Configuration ---

# Load environment variables from a .env file
# Create a .env file and add: OPENAI_API_KEY="your-key-here"
load_dotenv()

# Check if the API key is available
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

# Configure LlamaIndex global settings for LLM and embedding models
# This is the modern way to configure models for LlamaIndex
Settings.llm = OpenAI(model="gpt-4", temperature=0.1)
Settings.embed_model = OpenAIEmbedding()


# --- 2. Text Summarization using LangChain ---

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using LangChain Expression Language (LCEL).
    """
    print("--- Summarizing Text ---")
    
    # Define the LLM for LangChain (can be different from LlamaIndex's)
    langchain_llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    # Create a prompt template
    prompt_template = ChatPromptTemplate.from_template(
        "Summarize the following content into three distinct key points. "
        "Be concise and clear:\n\n{input_text}"
    )
    
    # Create a simple chain using LangChain Expression Language (LCEL)
    # This pipes the prompt to the model and then to an output parser.
    chain = prompt_template | langchain_llm | StrOutputParser()
    
    # Invoke the chain with the input text
    summary = chain.invoke({"input_text": text})
    
    return summary


# --- 3. Indexing and Querying using LlamaIndex ---

def create_vector_index(text: str):
    """
    Creates a vector index from the text in-memory and queries it.
    """
    print("\n--- Creating Vector Index ---")
    
    # LlamaIndex works with 'Document' objects.
    # Creating a Document in-memory is more efficient than writing to a file.
    documents = [Document(text=text)]
    
    # Create the index from the documents.
    # It will use the global 'Settings.llm' and 'Settings.embed_model'.
    print("Creating index...")
    index = VectorStoreIndex.from_documents(documents)
    
    # # Create a query engine from the index
    # print("Creating query engine...")
    # query_engine = index.as_query_engine()
    
    # # Query the index
    # print(f"Executing query: '{query}'")
    # response = query_engine.query(query)
    
    # return response

    return index


# # --- 4. Main Execution Block ---

# if __name__ == "__main__":
    
#     # Sample text to work with
#     sample_content = """
#     The James Webb Space Telescope (JWST) is a space telescope designed primarily 
#     to conduct infrared astronomy. As the largest optical telescope in space, its 
#     highly sensitive infrared instruments allow it to observe objects too old, distant, 
#     or faint for the Hubble Space Telescope. This enables investigations in many fields 
#     of astronomy and cosmology, such as observation of the first stars and the formation 
#     of the first galaxies, and detailed atmospheric characterization of potentially 
#     habitable exoplanets. The JWST was launched in December 2021 and began collecting
#     its first scientific data in July 2022.
#     """

#     # --- Task 1: Summarize the content ---
#     summary_result = summarize_text(sample_content)
#     print("\n✅ Summary Result:")
#     print(summary_result)
    
#     print("\n" + "="*50 + "\n")

#     # --- Task 2: Create an index and ask a question ---
#     user_query = "When did the JWST start collecting data?"
#     query_result = create_and_query_index(sample_content, query=user_query)
#     print("\n✅ Query Answer:")
#     print(str(query_result))