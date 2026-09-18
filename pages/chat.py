import streamlit as st

from services.rag_service import search_documents
from services.llm_service import get_healthcare_response
from services.safety_service import check_emergency
from database.database import save_chat


st.title("💬 AI Healthcare Chat")

st.caption(
    "Ask questions about healthcare information "
    "contained in the knowledge base."
)

st.divider()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


question = st.chat_input(
    "Ask a healthcare question..."
)


if question:

    st.session_state.chat_messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    if check_emergency(question):

        answer = """
🚨 **Potential emergency detected**

The symptoms described may require urgent medical attention.

If you believe you or someone else is in immediate danger,
contact your local emergency service or seek urgent medical care.

This application cannot determine whether an emergency
is actually occurring.
"""

        sources = []

    else:

        with st.spinner(
            "Searching medical knowledge..."
        ):

            documents = search_documents(
                question
            )

        with st.spinner(
            "Generating answer..."
        ):

            answer = get_healthcare_response(
                question,
                documents,
                st.session_state.chat_messages
            )

        sources = documents

    with st.chat_message("assistant"):

        st.markdown(answer)

        if sources:

            with st.expander(
                "📚 Sources"
            ):

                for source in sources:

                    st.markdown(
                        f"**{source['file']}** "
                        f"— Page {source['page']}"
                    )

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer
    })

    save_chat(
        question,
        answer
    )