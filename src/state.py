# src/state.py

import os

import streamlit as st
from langchain_core.messages import SystemMessage

from src.utils import normalize_base_url


def init_session(system_prompt_default: str) -> None:
    """
    Ensure session state keys exist.
    - messages: chat history as LangChain messages
    - system_prompt: current role/system instruction
    - base_url, selected_model, temperature
    """
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = system_prompt_default

    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=st.session_state.system_prompt)]

    if "base_url" not in st.session_state:
        st.session_state.base_url = normalize_base_url(
            os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        )

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama3"

    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.0


def reset_conversation() -> None:
    """Clear chat history and re-seed with the current system prompt."""
    st.session_state.messages = [SystemMessage(content=st.session_state.system_prompt)]
