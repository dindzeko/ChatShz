import streamlit as st
from utils.pdf_processor import extract_pdf_content
from utils.gemini import GeminiProcessor
from utils.database import SupabaseClient
import os

def process_pdfs():
    processor = GeminiProcessor()
    db = SupabaseClient()
    pdf_dir = "data"
    
    if not os.path.exists(pdf_dir) or len(os.listdir(pdf_dir)) == 0:
        st.warning("⚠️ Folder 'data/' kosong atau tidak ditemukan.")
        return
    
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            pages = extract_pdf_content(pdf_path)
            
            for page in pages:
                processed_content = processor.process_content(
                    "Extract key information including jobs, coefficients, and technical details:",
                    page["content"]
                )
                db.store_document({
                    "name": filename,
                    "page": page["page"]
                }, processed_content)

def main():
    st.title("PDF Document Processor")
    
    if st.button("Start Processing"):
        with st.spinner("Processing documents..."):
            process_pdfs()
        st.success("✅ Documents processed and stored in database!")

if __name__ == "__main__":
    main()
