import streamlit as st
from utils.database import SupabaseClient
from utils.gemini import GeminiProcessor

def main():
    st.title("Document Query Assistant")
    db = SupabaseClient()
    processor = GeminiProcessor()
    
    query = st.text_input("Ask about the document:")
    
    if query:
        try:
            results = db.search(query).data
            if not results:
                st.warning("⚠️ No relevant information found")
            else:
                context = "\n\n".join(
                    [f"Document: {res['document_name']} Page {res['page_number']}:\n{res['content']}" 
                     for res in results]
                )
                
                answer = processor.process_content(
                    f"Answer this question based on context: {query}",
                    context
                )
                
                st.subheader("Answer:")
                st.markdown(f"**{answer}**")
                
                st.subheader("References:")
                for res in results:
                    st.write(f"- {res['document_name']} (Page {res['page_number']})")
        except Exception as e:
            st.error(f"An error occurred while processing your request: {e}")

if __name__ == "__main__":
    main()
