import streamlit as st

# Dữ liệu FAQ
data_faqs = [
    [
        "Chatbot hoạt động như thế nào?",
        "Chatbot hoạt động bằng cách từ câu hỏi của người dùng, sử dụng kỹ thuật tìm văn bản liên quan đến câu hỏi trong bộ dữ liệu đã được vector hóa (text similarity) và lưu trữ thông qua vector database. Giúp lấy ra những đoạn văn bản có liên quan sau đó dùng mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời.",
    ],
    [
        "Cách sử dụng chatbot để tra cứu thông tin",
        "Để sử dụng chatbot một cách hiệu quả nhất bạn nên đặt câu hỏi một cách rõ ràng đầy đủ để mô hình có thể đưa ra câu trả lời chính xác. Tuy nhiên, ở một số trường hợp câu trả lời có thể không chính xác nên bạn phải kiểm chứng thông tin hoặc liên hệ hỗ trợ nếu cần thiết nhé.",
    ],
    [
        "Thông tin từ chatbot có đáng tin cậy không?",
        "Vì là một mô hình xác xuất nên thông tin chatbot đưa ra có thể không chính xác ở một số trường hợp, bạn nên kiểm chứng thông tin hoặc liên hệ hỗ trợ nếu cần thiết nhé.",
    ],
    [
        "Tôi có thể liên hệ hỗ trợ như thế nào?",
        "Vào phần Góp ý/báo lỗi hoặc phòng công tác sinh viên của trường theo số điện thoại: 0236 3667 129 và gmail: congtacsinhvien@vku.udn.vn.",
    ],
]

# Streamlit UI Configuration
st.set_page_config(page_title="FAQs", layout="centered")

# Background Gradient
st.markdown(
    """
    <style>
        *{
        background: #F5F5F7
        }
        .faq-title {
            font-size: 2rem;
            font-weight: bold;
          
            text-align: center;
            margin-bottom: 20px;
            background: #374f8a;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .faq-item {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            background-color: white;
        }
        .faq-question {
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
        }
        .faq-answer {
            margin-top: 10px;
            font-size: 1rem;
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# FAQs Section
st.markdown('<div class="faq-container">', unsafe_allow_html=True)

st.markdown('<div class="faq-title">Những câu hỏi thường gặp (FAQs)</div>', unsafe_allow_html=True)

# Loop through FAQs and render them
for question, answer in data_faqs:
    with st.expander(question):
        st.write(answer)

st.markdown("</div>", unsafe_allow_html=True)
