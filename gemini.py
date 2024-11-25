import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY ="AIzaSyCA5iz97t1wgvIVi-EWfjmHYlnzR3ykYyo"
# os.environ.get("GOOGLE_Key_2")

class GeminiLLM:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text