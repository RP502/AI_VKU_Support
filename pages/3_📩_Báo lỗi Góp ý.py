import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Hàm gửi email
def send_mail(from_name, message, user_email):
    try:
        # Cấu hình SMTP server (thay đổi theo dịch vụ email bạn dùng)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "dinhvietphuong2602@gmail.com"  # Thay bằng email của bạn
        sender_password = "olkp jghh qvfd ysqh"     # Thay bằng mật khẩu ứng dụng
        recipient_email = "phuongdv.21it@gmail.com"  # Email nhận phản hồi

        # Tạo email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = f"Phản hồi từ {from_name}"
        body = f"Tên người gửi: {from_name}\nEmail: {user_email}\n\nNội dung:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        # Kết nối và gửi email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return "SUCCESS"
    except Exception as e:
        return f"FAILED: {e}"

# Giao diện Streamlit
st.set_page_config(page_title="Báo lỗi hoặc góp ý", layout="centered")
st.markdown(
    "<h1 style='color: #df0218;'>📋 Báo lỗi hoặc góp ý</h1>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align: center;">
        <h3 style="color: #374f8a;">Hãy giúp chúng tôi cải thiện sản phẩm bằng những góp ý của bạn!</h3>
        <p style="font-size: 16px;">Chúng tôi trân trọng mọi ý kiến của bạn để sản phẩm ngày càng hoàn thiện hơn.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Nhập nội dung từ người dùng
with st.form("feedback_form"):
    from_name = st.text_input("Tên của bạn", placeholder="Nhập tên của bạn...")
    user_email = st.text_input("Email của bạn", placeholder="Nhập email của bạn...")
    message = st.text_area("Nội dung góp ý / báo lỗi", placeholder="Nhập phản hồi của bạn tại đây...")
    submitted = st.form_submit_button("Gửi")

    # Khi nhấn nút "Gửi"
    if submitted:
        if from_name and user_email and message:
            result = send_mail(from_name, message, user_email)
            if result == "SUCCESS":
                st.success("🎉 Gửi thành công! Cảm ơn bạn đã góp ý.")
            else:
                st.error(f"❌ Gửi không thành công. Lỗi: {result}")
        else:
            st.warning("⚠️ Vui lòng điền đầy đủ thông tin trước khi gửi!")

# Thiết kế giao diện giống React (tùy chỉnh thêm nếu cần)
st.markdown(
    """
    <style>
    *{
        background: #F5F5F7
        }
    .stButton>button {
        background: linear-gradient(to right, #4b7bec, #a29bfe);
        color: white;
        font-size: 18px;
        border-radius: 5px;
        width: 100%;
        height: 50px;
    }
    textarea, input {
        border: 1px solid #dfe6e9;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
        font-size: 16px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
