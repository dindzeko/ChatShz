import streamlit as st
import time
from database import init_db, create_table, insert_data, query_data
from document_processor import extract_text_from_pdf, process_page

# Validasi secrets
def check_secrets():
    required_keys = ["SUPABASE_URL", "SUPABASE_KEY", "GEMINI_API_KEY"]
    missing_keys = [key for key in required_keys if key not in st.secrets]
    if missing_keys:
        st.error(f"⚠️ Missing required secrets: {', '.join(missing_keys)}")
        st.stop()

# Fungsi utama
def main():
    # Validasi secrets sebelum mulai
    check_secrets()
    
    # Judul aplikasi
    st.title("📄 Construction Document Assistant")
    
    # Inisialisasi Supabase
    supabase = init_db()
    create_table(supabase)  # Pastikan tabel sudah dibuat
    
    # Bagian upload file
    uploaded_file = st.file_uploader("Upload PDF dokumen pekerjaan", type="pdf")
    
    if uploaded_file:
        st.session_state['processed'] = False
        
        with st.expander("📤 Document Processing Status"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            try:
                pages = extract_text_from_pdf(uploaded_file)
                total_pages = len(pages)
                
                all_jobs = []
                for idx, page in enumerate(pages):
                    try:
                        jobs = process_page(page)
                        for job in jobs:
                            job['page_number'] = page['page']
                            all_jobs.append(job)
                        
                        # Update progress bar
                        progress = (idx + 1) / total_pages
                        progress_bar.progress(progress)
                        status_text.text(f"Memproses halaman {idx+1}/{total_pages}...")
                    except Exception as e:
                        st.error(f"Error processing page {page['page']}: {str(e)}")
                
                # Simpan data ke Supabase jika ada hasil
                if all_jobs:
                    insert_data(supabase, all_jobs)
                    st.session_state['processed'] = True
                    processing_time = time.time() - start_time
                    st.success(f"✅ Dokumen diproses! {len(all_jobs)} entri tersimpan. Waktu pemrosesan: {processing_time:.2f} detik")
                else:
                    st.warning("⚠️ Tidak ada data yang diekstraksi dari dokumen.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memproses dokumen: {str(e)}")
    
    # Bagian pencarian data
    if st.session_state.get('processed', False):
        st.divider()
        query = st.text_input("🔍 Cari informasi pekerjaan:", placeholder="Contoh: koefisien pemasangan kaca")
        
        if query:
            try:
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
                    st.warning("❌ Data tidak ditemukan untuk pencarian ini.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat mencari data: {str(e)}")

# Jalankan aplikasi
if __name__ == "__main__":
    main()
