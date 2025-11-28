# src/chat.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from src.utils import get_chat_model
from src.ui import render_bubble, render_streaming_bubble


def handle_user_turn_streaming() -> None:
    """
    Read user input, append to history, stream model response in real time,
    then append the final assistant message to history.
    """
    user_text = st.chat_input(placeholder="Ask your question")
    if not user_text:
        return

    text = user_text.strip()
    st.session_state.messages.append(HumanMessage(content=text))
    render_bubble("user", text, "🧑")

    # Prepare model client from current selections
    chat = get_chat_model(
        model_name=st.session_state.selected_model,
        temperature=st.session_state.temperature,
        base_url=st.session_state.base_url,
    )

    # Stream assistant tokens live
    updater = render_streaming_bubble("assistant", "🤖")
    full_text = ""
    try:
        for chunk in chat.stream(st.session_state.messages):
            token = getattr(chunk, "content", None)
            if token:
                full_text += token
                updater(full_text)
    except Exception as e:
        updater(f"**Error:** {e}")
        return

    # Persist the assistant's full response to history
    st.session_state.messages.append(AIMessage(content=full_text))
