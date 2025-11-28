# src/ui.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from src.utils import fetch_ollama_models, normalize_base_url
from src.state import reset_conversation


def setup_page() -> None:
    """Configure Streamlit page basics and inject CSS."""
    st.set_page_config(
        page_title="CAISA for CBT Practitioners 🩺",
        page_icon="🩺",
        layout="centered",
    )

    st.markdown(
        """
    <style>
    .chat-row {
        display: flex;
        gap: 12px;
        margin: 14px 0;
        align-items: flex-start;
    }
    .chat-row.right {
        flex-direction: row-reverse;
        justify-content: flex-start;
        margin-left: auto;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #e0e0e0;
        background: #f9f9fb;
        font-size: 20px;
        font-weight: 600;
        color: #3a3a3a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .bubble {
        max-width: 760px;
        padding: 14px 18px;
        border-radius: 16px;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-size: 16px;
        word-break: break-word;
    }
    .bubble.assistant {
        background: linear-gradient(90deg, #f2f4f7 80%, #e9ecef 100%);
        border: 1px solid #e0e0e0;
    }
    .bubble.user {
        background: linear-gradient(90deg, #e8f3ff 80%, #dbefff 100%);
        border: 1px solid #b3d8ff;
    }
    .block-container {
        padding-top: 4rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.header("CAISA for CBT Practitioners 🩺")


def render_bubble(role: str, text: str, avatar: str = ""):
    """Render a single chat bubble."""
    side = "right" if role == "user" else ""
    bubble_cls = "user" if role == "user" else "assistant"
    html = f"""
    <div class="chat-row {side}">
        <div class="avatar">{avatar}</div>
        <div class="bubble {bubble_cls}">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_streaming_bubble(role: str, avatar: str = ""):
    """Return a placeholder you can .markdown() repeatedly during streaming."""
    side = "right" if role == "user" else ""
    bubble_cls = "user" if role == "user" else "assistant"
    container = st.empty()

    def update(text: str):
        html = f"""
        <div class="chat-row {side}">
            <div class="avatar">{avatar}</div>
            <div class="bubble {bubble_cls}">{text}</div>
        </div>
        """
        container.markdown(html, unsafe_allow_html=True)

    return update


def render_sidebar() -> None:
    """Render sidebar controls: base URL, refresh, model dropdown, temperature, system prompt."""
    with st.sidebar:
        st.subheader("Settings")

        # --- Ollama connection ---
        base_url_input = st.text_input(
            "Ollama base URL",
            value=st.session_state.base_url,
            help="Where your Ollama server is listening (e.g., http://127.0.0.1:11434)",
        )
        normalized_base_url = normalize_base_url(base_url_input)

        refresh_models = st.button("🔄 Refresh model list")
        if refresh_models or normalized_base_url != st.session_state.base_url:
            st.session_state.base_url = normalized_base_url
            fetch_ollama_models.clear()  # clear cache

        # --- Model dropdown (fetched from Ollama) ---
        installed_models = fetch_ollama_models(st.session_state.base_url)
        if not installed_models:
            st.info("No models found. Use `ollama pull <model>` to add one.")
        selected_model = st.selectbox(
            "Installed models",
            options=installed_models or [st.session_state.selected_model],
            index=0,
            help="Choose which model to chat with.",
        )
        st.session_state.selected_model = selected_model

        # --- Decoding control ---
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.1
        )
        st.session_state.temperature = temperature

        # --- System prompt (role) ---
        system_prompt = st.text_area(
            "System prompt (role)",
            value=st.session_state.system_prompt,
            help="Sets the assistant's behavior (first system message).",
        )

        col1, col2 = st.columns(2)
        with col1:
            apply_role = st.button("Apply Role")
        with col2:
            clear_clicked = st.button("Clear Chat")

        if apply_role and system_prompt.strip():
            st.session_state.system_prompt = system_prompt.strip()
            reset_conversation()

        if clear_clicked:
            reset_conversation()


def render_history() -> None:
    """Render the chat history (skip the first system message)."""
    for msg in st.session_state.messages[1:]:  # skip system
        if isinstance(msg, HumanMessage):
            render_bubble(role="user", text=msg.content, avatar="🧑")
        elif isinstance(msg, AIMessage):
            render_bubble(role="assistant", text=msg.content, avatar="🤖")
