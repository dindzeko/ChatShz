import pdfplumber
import google.generativeai as genai
import re
import json
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

PROMPT_TEMPLATE = """
Analyze this construction document text and extract structured data. Find:
1. Job names (Indonesian terms)
2. Associated coefficients
3. Any additional specifications
4. Page number

Format output as JSON array with keys: job_name, coefficient, page_number, additional_info.

Text content:
{text}
"""

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return [{"page": i+1, "text": page.extract_text()} for i, page in enumerate(pdf.pages)]

def process_page(page):
    try:
        response = model.generate_content(PROMPT_TEMPLATE.format(text=page['text']))
        cleaned_response = re.sub(r'```json|```', '', response.text)
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error processing page {page['page']}: {str(e)}")
        return []
