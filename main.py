import streamlit as st
import time
from database import init_db, create_table, insert_data, query_data
from document_processor import extract_text_from_pdf, process_page

def main():
    st.title("📄 Construction Document Assistant")
    
    # Initialize Supabase
    supabase = init_db()
    
    # File upload section
    uploaded_file = st.file_uploader("Upload PDF dokumen pekerjaan", type="pdf")
    
    if uploaded_file:
        st.session_state['processed'] = False
        
        with st.expander("📤 Document Processing Status"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            pages = extract_text_from_pdf(uploaded_file)
            total_pages = len(pages)
            
            all_jobs = []
            for idx, page in enumerate(pages):
                try:
                    jobs = process_page(page)
                    for job in jobs:
                        job['page_number'] = page['page']
                        all_jobs.append(job)
                    
                    progress = (idx + 1) / total_pages
                    progress_bar.progress(progress)
                    status_text.text(f"Memproses halaman {idx+1}/{total_pages}...")
                except Exception as e:
                    st.error(f"Error processing page {page['page']}: {str(e)}")
            
            if all_jobs:
                insert_data(supabase, all_jobs)
                st.session_state['processed'] = True
                processing_time = time.time() - start_time
                st.success(f"✅ Dokumen diproses! {len(all_jobs)} entri tersimpan. Waktu pemrosesan: {processing_time:.2f} detik")

    # Query section
    if st.session_state.get('processed', False):
        st.divider()
        query = st.text_input("🔍 Cari informasi pekerjaan:", placeholder="Contoh: koefisien pemasangan kaca")
        
        if query:
            results = query_data(supabase, query).data
            if results:
                st.subheader("📊 Hasil Pencarian")
                for job in results:
                    with st.expander(f"**{job['job_name']}**"):
                        st.markdown(f"""
                        - **Koefisien**: `{job['coefficient']}`
                        - **Halaman**: {job['page_number']}
                        - **Informasi Tambahan**: {job['additional_info'] or '-'}
                        """)
            else:
                st.warning("❌ Data tidak ditemukan untuk pencarian ini")

if __name__ == "__main__":
    main()
