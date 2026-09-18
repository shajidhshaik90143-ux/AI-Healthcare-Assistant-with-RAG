import streamlit as st

from rag.vector_store import get_document_count
from database.database import get_chat_history


st.title("📊 Healthcare Dashboard")

st.markdown(
    "Monitor your AI Healthcare Assistant."
)

st.divider()

col1, col2, col3 = st.columns(3)

try:
    document_count = get_document_count()
except Exception:
    document_count = 0

try:
    history = get_chat_history()
    question_count = len(history)
except Exception:
    question_count = 0

with col1:
    st.metric(
        "Knowledge Chunks",
        document_count
    )

with col2:
    st.metric(
        "Questions Asked",
        question_count
    )

with col3:
    st.metric(
        "System",
        "RAG Enabled"
    )

st.divider()

st.subheader("🧠 How the system works")

st.markdown("""
1. 📄 Medical PDFs are uploaded.
2. 📝 Text is extracted from the PDFs.
3. ✂️ Text is divided into chunks.
4. 🧠 Embeddings are generated.
5. 🗄️ Chunks are stored in ChromaDB.
6. 🔎 User questions are converted into embeddings.
7. 📚 Relevant medical information is retrieved.
8. 🤖 Groq generates a grounded response.
9. 📖 Source documents are displayed.
""")

st.divider()

st.warning(
    "This dashboard is for an educational AI project. "
    "It does not provide medical diagnosis or treatment."
)