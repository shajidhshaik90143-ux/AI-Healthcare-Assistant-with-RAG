import streamlit as st

from database.database import (
    get_chat_history,
    delete_chat_history
)


st.title("🕒 Chat History")

history = get_chat_history()

st.write(
    f"Total conversations: **{len(history)}**"
)

st.divider()

if not history:

    st.info(
        "No chat history available."
    )

else:

    for row in history:

        chat_id = row[0]
        question = row[1]
        answer = row[2]
        created_at = row[3]

        with st.expander(
            f"#{chat_id} — {question[:80]}"
        ):

            st.caption(
                f"Created: {created_at}"
            )

            st.markdown(
                "**Question:**"
            )

            st.write(
                question
            )

            st.markdown(
                "**Answer:**"
            )

            st.markdown(
                answer
            )

st.divider()

if history:

    if st.button(
        "🗑️ Delete All History"
    ):

        delete_chat_history()

        st.success(
            "Chat history deleted."
        )

        st.rerun()