import streamlit as st
from PIL import Image
import base64

# Function to encode image as Base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Hình ảnh không tìm thấy: {image_path}")
        return None

# Path to the robot image
robot_img_path = "images/robot_image.png"
robot_img_base64 = get_base64_image(robot_img_path)

# Streamlit UI Configuration
st.set_page_config(page_title="VKU Chatbot", layout="centered")

if robot_img_base64:  # Only render if the image is successfully loaded
    # Hero Section
    st.markdown(
        f"""
        <style>
        .hero {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 80vh;
            max-height: 600px;
            background: linear-gradient(to right, #ccDbf1, #bfdbfe);
            border-radius: 15px;
            padding: 20px;
            margin: auto;
            width: 90%;
        }}
        .hero-content {{
            text-align: center;
            max-width: 600px;
        }}
        .hero-content img {{
            max-width: 200px;
            height: auto;
            margin: auto;
        }}
        .title-gradient {{
            font-size: 2rem;
            font-weight: bold;
        }}
        .title-gradient .v {{
            color: #df0218; /* Màu đỏ */
        }}
        .title-gradient .k {{
            color: #fed014; /* Màu vàng */
        }}
        .title-gradient .u {{
            color: #374f8a; /* Màu xanh */
        }}
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            font-size: 1rem;
            color: white;
            background-color: #0ea5e9;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            cursor: pointer;
        }}
        .btn:hover {{
            background-color: #fed014;
            color: black;
        }}
        </style>
        <div class="hero">
            <div class="hero-content">
                <img src="data:image/png;base64,{robot_img_base64}" alt="Robot Image"/>
                <h1 class="text-2xl lg:text-5xl font-bold">Xin chào! Mình là</h1>
                <h1 class="title-gradient">
                    <span class="v">V</span>
                    <span class="k">K</span>
                    <span class="u">U</span> Chatbot
                </h1>
                <p class="py-6 font-semibold lg:text-lg text-sm">
                    Giúp bạn giải đáp thắc mắc, tra cứu thông tin một cách nhanh chóng và chính xác nhất!
                </p>
                <a href="Tư_vấn_VKU" class="btn">Bắt đầu ngay</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("Không thể tải hình ảnh. Vui lòng kiểm tra lại đường dẫn hình ảnh.")
