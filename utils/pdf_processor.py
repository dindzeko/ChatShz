from PyPDF2 import PdfReader
import streamlit as st

def extract_pdf_content(pdf_path):
    """
    Mengekstrak konten dari file PDF.
    :param pdf_path: Path ke file PDF.
    :return: List of dictionaries berisi nomor halaman dan konten teks.
    """
    try:
        reader = PdfReader(pdf_path)
        
        if len(reader.pages) == 0:
            raise ValueError("File PDF tidak memiliki halaman.")
        
        extracted_content = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text is None or text.strip() == "":
                text = "[Halaman ini tidak memiliki teks yang dapat diekstrak]"
            extracted_content.append({
                "page": i + 1,
                "content": text
            })
        
        return extracted_content
    
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {pdf_path}")
        raise
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca PDF: {e}")
        raise
