import streamlit as st

from services.llm_service import get_healthcare_response
from services.safety_service import check_emergency
from services.rag_service import search_documents
from database.database import init_database, save_chat

st.set_page_config(
    page_title="AI Healthcare Assistant",
    page_icon="🏥",
    layout="wide"
)

init_database()

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🏥 Healthcare AI")

    st.markdown("""
    ### AI Healthcare Assistant

    A Retrieval-Augmented Generation system that answers healthcare
    information questions using your trusted medical documents.
    """)

    st.divider()

    st.info(
        "⚠️ This application provides general health information "
        "and is not a substitute for professional medical care."
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# HEADER
# -----------------------------
st.title("🏥 AI Healthcare Assistant")
st.caption("Retrieval-Augmented Generation • Medical Information Assistant")

st.divider()

# -----------------------------
# CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"- **{source['file']}** — Page {source['page']}"
                    )

# -----------------------------
# USER INPUT
# -----------------------------
question = st.chat_input(
    "Ask a healthcare information question..."
)

if question:

    # Emergency check
    emergency = check_emergency(question)

    if emergency:
        warning = (
            "🚨 **Potential emergency detected.**\n\n"
            "The information you entered may describe symptoms that "
            "could require urgent medical attention. If you believe "
            "you or someone else is in immediate danger, contact your "
            "local emergency service or seek urgent medical care.\n\n"
            "This application cannot determine whether a medical "
            "emergency is occurring."
        )

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": warning
        })

        save_chat(question, warning)

        st.rerun()

    # Show user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Search knowledge base
    with st.spinner("🔎 Searching medical knowledge base..."):
        documents = search_documents(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("🤖 Generating grounded response..."):

            answer = get_healthcare_response(
                question,
                documents,
                st.session_state.messages
            )

            st.markdown(answer)

            if documents:
                with st.expander("📚 Retrieved Sources"):
                    for doc in documents:
                        st.markdown(
                            f"- **{doc['file']}** — Page {doc['page']}"
                        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": documents
    })

    save_chat(question, answer)