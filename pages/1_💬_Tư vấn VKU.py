import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
# from gemini import GeminiLLM
from langchain.embeddings import HuggingFaceBgeEmbeddings
import google.generativeai as genai

GOOGLE_API_KEY = st.secrets["GOOGLE_Key_3"]
# Qdrant API configuration
QDRANT_API_KEY = st.secrets["Qdrant_API_KEY"]
QDRANT_URL = "https://0a664afe-b3d7-45ad-80e3-3af062055000.europe-west3-0.gcp.cloud.qdrant.io:6333"


def configure_gemini():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Failed to configure Gemini LLM: {e}")
        return None

class GeminiLLM:
    def __init__(self):
        self.model = configure_gemini()

    def generate_response(self, prompt):
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                return response.text
            return ""
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return ""

# Set up embeddings
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model_kwargs = {'device': 'cpu'}

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs
)

# Initialize Qdrant client and vectorstore
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

vectorstore = Qdrant(
    client=qdrant_client,
    collection_name="vku_chat_all",
    embeddings=embeddings,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 15})
gemini_llm = GeminiLLM()

# Function to generate response
def get_response(question, history):
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])

    if not context:
        return context, "I couldn't find any relevant context to answer your question."

    history_text = "\n".join([f"User: {q}\nAssistant: {a}" for q, a in history])
    prompt = f"""
You are a conversational assistant. Maintain the flow of conversation and provide accurate, natural responses.

History:
{history_text}

Context:
{context}

Question:
{question}

Answer:
"""
    response = gemini_llm.generate_response(prompt)
    return context, response

# Streamlit UI
st.set_page_config(page_title="Trợ lý VKU", layout="centered")
st.title("Hỗ trợ tư vấn")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": "Xin chào! Tôi là trợ lý VKU. Bạn cần hỗ trợ gì hôm nay?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Hỏi trợ lý VKU"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    _, response = get_response(prompt, [(m["content"], m["content"]) for m in st.session_state.messages if m["role"] == "user"])
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
