import google.generativeai as genai
import streamlit as st

class GeminiProcessor:
    def __init__(self):
        try:
            # Mengambil API key dari Streamlit Secrets
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"Failed to configure Gemini API: {e}")
            raise

    def process_content(self, prompt, content):
        """
        Memproses konten menggunakan model Gemini.
        :param prompt: Prompt atau instruksi untuk model.
        :param content: Konten yang akan diproses.
        :return: Teks hasil proses dari model.
        """
        if not prompt or not content:
            raise ValueError("Prompt and content cannot be empty.")

        try:
            response = self.model.generate_content(f"{prompt}\n\n{content}")
            return response.text
        except Exception as e:
            st.error(f"Failed to process content with Gemini: {e}")
            raise
