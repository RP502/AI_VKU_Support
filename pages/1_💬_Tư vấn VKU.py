import streamlit as st
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import HuggingFaceBgeEmbeddings
import google.generativeai as genai

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
            return "Hiện tại tôi không thể kết nối với mô hình. Vui lòng thử lại sau hoặc liên hệ với bộ phận hỗ trợ."
        except Exception as e:
            st.error(f"Lỗi khi tạo phản hồi: {e}")
            return "Đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại."


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
    Bạn là trợ lý hỗ trợ tra cứu thông tin tuyển sinh và học vụ VKU. Hãy cung cấp câu trả lời chính xác và rõ ràng dựa trên câu hỏi của người dùng. Tuân thủ các quy tắc sau:

    1. Nếu người dùng hỏi về:
    - Chỉ tiêu tuyển sinh/ xét tuyển VKU năm 2024: Trả về 1500 chỉ tiêu
    - Ngành/ chuyên ngành đào tạo của trường: Trả về 16 ngành/ chuyên ngành kèm 16 chuyên ngành tương ứng: 
        ### Danh sách ngành/chuyên ngành đào tạo của VKU:
1. **Quản trị kinh doanh**  
   - Mã ĐKXT: 7340101  
   - Chỉ tiêu: 120  

2. **Quản trị kinh doanh - Chuyên ngành Quản trị Logistics và chuỗi cung ứng số**  
   - Mã ĐKXT: 734010EL  
   - Chỉ tiêu: 130  

3. **Quản trị kinh doanh - Chuyên ngành Quản trị dịch vụ du lịch và lữ hành số**  
   - Mã ĐKXT: 7340101ET  
   - Chỉ tiêu: 60  

4. **Quản trị kinh doanh - Chuyên ngành Quản trị tài chính số**  
   - Mã ĐKXT: 7340101EF  
   - Chỉ tiêu: 60  

5. **Quản trị kinh doanh - Chuyên ngành Quản trị dự án Công nghệ thông tin**  
   - Mã ĐKXT: 7340101IM  
   - Chỉ tiêu: 40  

6. **Marketing**  
   - Mã ĐKXT: 7340115  
   - Chỉ tiêu: 40  

7. **Công nghệ kỹ thuật máy tính (kỹ sư)**  
   - Mã ĐKXT: 7480108  
   - Chỉ tiêu: 60  

8. **Công nghệ kỹ thuật máy tính – Chuyên ngành Thiết kế vi mạch bán dẫn (kỹ sư)**  
   - Mã ĐKXT: 7480108IC  
   - Chỉ tiêu: 60  

9. **Công nghệ kỹ thuật máy tính (cử nhân)**  
   - Mã ĐKXT: 7480108B  
   - Chỉ tiêu: 60  

10. **An toàn thông tin (kỹ sư)**  
    - Mã ĐKXT: 740202  
    - Chỉ tiêu: 60  

11. **Công nghệ thông tin (kỹ sư)**  
    - Mã ĐKXT: 7480201  
    - Chỉ tiêu: 320  

12. **Công nghệ thông tin (cử nhân)**  
    - Mã ĐKXT: 7480201B  
    - Chỉ tiêu: 240  

13. **Công nghệ thông tin (cử nhân - Hợp tác doanh nghiệp)**  
    - Mã ĐKXT: 7480201DT  
    - Chỉ tiêu: 120  

14. **Trí tuệ nhân tạo (kỹ sư)**  
    - Mã ĐKXT: 7480107  
    - Chỉ tiêu: 60  

15. **Công nghệ truyền thông (cử nhân)**  
    - Mã ĐKXT: 7320106  
    - Chỉ tiêu: 30  

16. **Công nghệ truyền thông - Chuyên ngành Thiết kế Mỹ thuật số (cử nhân)**  
    - Mã ĐKXT: 7320106DA  
    - Chỉ tiêu: 40  

    - Hoãn nghĩa vụ quân sự: Trả về đường link https://s.net.vn/pv84 kèm giải thích rằng đây là mẫu đơn xác nhận sinh viên của trường.
    - Bảng điểm học tập: Trả về đường link https://s.net.vn/FHEO.
    - Các mẫu đơn, tài liệu, biểu mẫu của trường: Trả về đường link https://portal.vku.udn.vn/tai-nguyen.

    2. Nếu câu hỏi không thuộc các danh mục trên, hãy trả về các kênh tham khảo sau:
    - Website tuyển sinh: https://tuyensinh.vku.udn.vn/
    - Facebook: https://www.facebook.com/vku.udn.vn
    - Group: https://www.facebook.com/groups/vku.tuyensinh/
    - Hoặc đề xuất liên hệ trực tiếp qua số điện thoại:
        + 0236.6.552.688
        + 0236.3.667.113

    3. Khi trả lời:
        Thông tin phải chính xác và cập nhật
        Giọng điệu thân thiện, chuyên nghiệp
        Đưa ra câu hỏi phù hợp để hiểu rõ nhu cầu của người hỏi
        Hướng dẫn cụ thể các bước đăng ký xét tuyển
        Trong trường hợp không thể trả lời hoặc cần thông tin chi tiết hơn:
        Dẫn người dùng đến trang tuyển sinh chính thức: https://tuyensinh.vku.udn.vn
        Đề xuất liên hệ với bộ phận tuyển sinh của trường

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

    with st.spinner("Đang xử lý..."):
        _, response = get_response(prompt,
                                   [(m["content"], m["content"]) for m in st.session_state.messages if
                                    m["role"] == "user"])

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
