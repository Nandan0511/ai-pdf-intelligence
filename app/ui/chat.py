import time

import streamlit as st

from core.constants import (
    STREAM_DELAY,
)

from services.llm_service import (
    generate_chat_response,
)


def render_chat_history():

    for message in (
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


def process_query(user_query):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):

        st.markdown(user_query)

    with st.chat_message("assistant"):

        thinking = st.empty()

        thinking.markdown(
            """
            <div class="thinking-box">
                🤖 Thinking...
            </div>
            """,
            unsafe_allow_html=True,
        )

        answer, sources = (
            generate_chat_response(
                user_query,
                st.session_state.messages,
                st.session_state.vectorstore,
            )
        )

        thinking.empty()

        placeholder = st.empty()

        response = ""

        for char in answer:

            response += char

            time.sleep(STREAM_DELAY)

            placeholder.markdown(
                response + "▌"
            )

        placeholder.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )