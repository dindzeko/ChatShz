import streamlit as st

st.set_page_config(
    page_title="PDF Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

st.markdown("# 📚 PDF Knowledge Assistant")
st.write("Navigate to different pages using the sidebar")

if __name__ == "__main__":
    st.sidebar.success("Select a page above")
