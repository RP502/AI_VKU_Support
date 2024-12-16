import streamlit as st
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import HuggingFaceBgeEmbeddings
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

GOOGLE_API_KEY = st.secrets["GOOGLE_Key_3"]
QDRANT_API_KEY = st.secrets["Qdrant_API_KEY"]
QDRANT_URL = "https://0a664afe-b3d7-45ad-80e3-3af062055000.europe-west3-0.gcp.cloud.qdrant.io:6333"


def configure_gemini():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai.GenerativeModel('gemini-2.0-flash-exp')
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


model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
vectorstore = Qdrant(client=qdrant_client, collection_name="vku_data_all", embeddings=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 30})
gemini_llm = GeminiLLM()


def hybrid_search(question, retriever):
    docs = retriever.get_relevant_documents(question)
    keyword_hits = [doc for doc in docs if question.lower() in doc.page_content.lower()]

    if not keyword_hits:
        return docs
    return keyword_hits


def get_response(question, history):
    docs = hybrid_search(question, retriever)

    if not docs:
        # Trả về thông tin mặc định khi không tìm thấy dữ liệu phù hợp
        response = (
            "Câu hỏi này của bạn sẽ giải đáp được chi tiết hơn để giải đáp được thắc mắc.\n"
            "Bạn có thể tham khảo thông tin tuyển sinh qua các kênh sau đây:\n"
            "- Website: https://tuyensinh.vku.udn.vn/\n"
            "- Facebook: https://www.facebook.com/vku.udn.vn\n"
            "- Group: https://www.facebook.com/groups/vku.tuyensinh/\n"
            "Hoặc liên hệ trực tiếp để được tư vấn\n"
            "0236.6.552.688\n"
            "0236.3.667.113\n"
        )
        return "", response

    context = "\n".join([doc.page_content for doc in docs])

    history_text = "\n".join([f"User: {q}\nAssistant: {a}" for q, a in history])
    prompt = f"""
Bạn là trợ lý hỗ trợ tra cứu thông tin tuyển sinh, thông tin học vụ VKU. Hãy tìm câu trả lời chính xác với câu hỏi của người dùng. 
Hãy nhớ rằng hoãn nghĩa vụ quân sự là đơn xác nhận sinh viên của trường, hãy trả về đường link https://s.net.vn/pv84.
Nếu cần bảng điểm học tập, hãy trả về đường link https://s.net.vn/FHEO.
Nếu cần các mẫu đơn, tài liệu, biểu mẫu của trường hãy trả về đường link: https://portal.vku.udn.vn/tai-nguyen
Hãy kiểm tra lại dữ liệu cho chắc chắn, nếu không có câu trả lời phù hợp hãy trả về các kênh tham khảo sau:
 "- Website: https://tuyensinh.vku.udn.vn/\n"
 "- Facebook: https://www.facebook.com/vku.udn.vn\n"
 "- Group: https://www.facebook.com/groups/vku.tuyensinh/\n"
 "Hoặc liên hệ trực tiếp để được tư vấn\n"
 "0236.6.552.688\n và"
 "0236.3.667.113\n"
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


st.set_page_config(page_title="Trợ lý VKU", layout="centered")
st.title("Hỗ trợ tư vấn")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant",
         "content": "Xin chào! Tôi là trợ lý VKU, giải đáp các thông tin học vụ và thông tin tuyển sinh. Bạn cần hỗ trợ gì hôm nay?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hỏi trợ lý VKU"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    _, response = get_response(prompt,
                               [(m["content"], m["content"]) for m in st.session_state.messages if m["role"] == "user"])
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
