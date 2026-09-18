import streamlit as st

from services.rag_service import search_documents
from services.llm_service import get_healthcare_response


st.title("💊 Medicine Information")

st.warning(
    "This feature provides educational information only. "
    "It does not prescribe medicines, doses, or treatment plans."
)

st.divider()

medicine = st.text_input(
    "Enter a medicine name",
    placeholder="Example: Paracetamol"
)

if st.button(
    "🔎 Search Medicine Information",
    use_container_width=True
):

    if not medicine.strip():

        st.warning(
            "Please enter a medicine name."
        )

    else:

        query = f"""
Provide general educational information about:

{medicine}

Explain:
- General purpose
- Common uses
- General precautions
- Common side effects if present in the knowledge base

Do not provide dosage instructions.
Do not prescribe the medicine.
"""

        with st.spinner(
            "Searching medical documents..."
        ):

            documents = search_documents(
                query,
                top_k=5
            )

        with st.spinner(
            "Generating information..."
        ):

            answer = get_healthcare_response(
                query,
                documents
            )

        st.subheader(
            f"📖 Information: {medicine}"
        )

        st.markdown(answer)

        if documents:

            with st.expander(
                "📚 Sources"
            ):

                for document in documents:

                    st.markdown(
                        f"- **{document['file']}** "
                        f"— Page {document['page']}"
                    )