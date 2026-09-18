import streamlit as st

from services.rag_service import search_documents
from services.llm_service import get_healthcare_response
from services.safety_service import check_emergency


st.title("🩺 Symptom Information")

st.warning(
    "This tool provides general educational information. "
    "It does not diagnose diseases."
)

st.divider()

symptoms = st.text_area(
    "Describe your symptoms",
    placeholder=(
        "Example: I have been feeling tired and dizzy "
        "for several days."
    ),
    height=150
)

if st.button(
    "🔎 Get General Information",
    use_container_width=True
):

    if not symptoms.strip():

        st.warning(
            "Please describe your symptoms."
        )

    elif check_emergency(symptoms):

        st.error(
            "🚨 The information entered may describe "
            "a potentially urgent situation. "
            "Please seek appropriate medical attention."
        )

    else:

        with st.spinner(
            "Searching medical knowledge..."
        ):

            documents = search_documents(
                symptoms,
                top_k=5
            )

        with st.spinner(
            "Generating educational information..."
        ):

            answer = get_healthcare_response(
                symptoms,
                documents
            )

        st.subheader(
            "📋 General Information"
        )

        st.markdown(answer)

        if documents:

            st.subheader(
                "📚 Sources"
            )

            for document in documents:

                st.markdown(
                    f"- **{document['file']}** "
                    f"— Page {document['page']}"
                )