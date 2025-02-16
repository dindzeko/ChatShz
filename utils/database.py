from supabase import create_client
import streamlit as st

class SupabaseClient:
    def __init__(self):
        try:
            # Mengambil secrets dari Streamlit Secrets
            self.supabase_url = st.secrets["SUPABASE_URL"]
            self.supabase_key = st.secrets["SUPABASE_KEY"]
            self.client = create_client(self.supabase_url, self.supabase_key)
        except Exception as e:
            st.error(f"Failed to connect to Supabase: {e}")
            raise

    def store_document(self, metadata, content):
        """
        Menyimpan dokumen ke tabel 'documents'.
        :param metadata: Dictionary berisi informasi metadata (name, page).
        :param content: Konten dokumen.
        :return: Hasil eksekusi insert query.
        """
        if not metadata or "name" not in metadata or "page" not in metadata:
            raise ValueError("Metadata must contain 'name' and 'page' keys.")
        if not content:
            raise ValueError("Content cannot be empty.")

        try:
            response = self.client.table("documents").insert({
                "document_name": metadata["name"],
                "page_number": metadata["page"],
                "content": content
            }).execute()
            return response
        except Exception as e:
            st.error(f"Failed to store document: {e}")
            raise

    def search(self, query):
        """
        Mencari dokumen berdasarkan konten menggunakan ILIKE.
        :param query: Kata kunci pencarian.
        :return: Hasil eksekusi query pencarian.
        """
        if not query:
            raise ValueError("Search query cannot be empty.")

        try:
            response = self.client.table("documents").select("*").ilike("content", f"%{query}%").execute()
            return response
        except Exception as e:
            st.error(f"Search failed: {e}")
            raise
