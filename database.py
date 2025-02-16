from supabase import create_client, Client
import streamlit as st

# Inisialisasi koneksi ke Supabase menggunakan secrets dari Streamlit
def init_db():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# Membuat tabel 'jobs' di Supabase
def create_table(supabase: Client):
    return supabase.table('jobs').create([
        {'name': 'id', 'type': 'serial', 'primary_key': True},
        {'name': 'job_name', 'type': 'text'},
        {'name': 'coefficient', 'type': 'float'},
        {'name': 'page_number', 'type': 'int'},
        {'name': 'additional_info', 'type': 'text'},
        {'name': 'created_at', 'type': 'timestamp', 'default': 'now()'}
    ]).execute()

# Menyisipkan data ke tabel 'jobs'
def insert_data(supabase: Client, data):
    return supabase.table('jobs').insert(data).execute()

# Mengambil data dari tabel 'jobs' berdasarkan nama pekerjaan (job_name)
def query_data(supabase: Client, job_name):
    return supabase.table('jobs').select('*').ilike('job_name', f'%{job_name}%').execute()
