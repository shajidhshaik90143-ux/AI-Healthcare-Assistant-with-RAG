import streamlit as st
from pathlib import Path

from rag.vector_store import rebuild_vector_database
from rag.vector_store import get_document_count


st.title("📚 Medical Document Manager")

st.markdown(
    "Upload trusted healthcare documents to build "
    "the RAG knowledge base."
)

st.divider()

DOCUMENT_FOLDER = Path(
    "data/medical_documents"
)

DOCUMENT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

uploaded_files = st.file_uploader(
    "Upload Medical PDF Documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    if st.button(
        "📥 Save Uploaded Documents",
        use_container_width=True
    ):

        saved = 0

        for uploaded_file in uploaded_files:

            file_path = (
                DOCUMENT_FOLDER /
                uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            saved += 1

        st.success(
            f"{saved} document(s) saved."
        )

st.divider()

st.subheader("📄 Available Documents")

files = list(
    DOCUMENT_FOLDER.glob("*.pdf")
)

if not files:

    st.info(
        "No PDF documents uploaded yet."
    )

else:

    for file in files:

        st.write(
            f"📄 {file.name}"
        )

st.divider()

st.subheader("🧠 Build RAG Knowledge Base")

if st.button(
    "🔄 Index / Rebuild Knowledge Base",
    use_container_width=True
):

    with st.spinner(
        "Extracting documents and creating embeddings..."
    ):

        try:

            count = rebuild_vector_database()

            st.success(
                f"Knowledge base rebuilt successfully. "
                f"{count} chunks indexed."
            )

        except Exception as error:

            st.error(
                f"Error: {error}"
            )

st.divider()

try:

    count = get_document_count()

    st.metric(
        "Indexed Knowledge Chunks",
        count
    )

except Exception:

    st.metric(
        "Indexed Knowledge Chunks",
        0
    )