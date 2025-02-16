from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import json

def init_db():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table(supabase: Client):
    return supabase.table('jobs').create([
        {'name': 'id', 'type': 'serial', 'primary_key': True},
        {'name': 'job_name', 'type': 'text'},
        {'name': 'coefficient', 'type': 'float'},
        {'name': 'page_number', 'type': 'int'},
        {'name': 'additional_info', 'type': 'text'},
        {'name': 'created_at', 'type': 'timestamp', 'default': 'now()'}
    ]).execute()

def insert_data(supabase: Client, data):
    return supabase.table('jobs').insert(data).execute()

def query_data(supabase: Client, job_name):
    return supabase.table('jobs').select('*').ilike('job_name', f'%{job_name}%').execute()
