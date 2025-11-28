# src/utils.py

import os
from typing import Optional, List
from urllib.parse import urlparse

import requests
import streamlit as st
from langchain_ollama import ChatOllama


def normalize_base_url(url: Optional[str]) -> str:
    """
    Ensure base URL has a scheme and looks like http://host:port.
    Defaults to 127.0.0.1:11434 if none is provided.
    """
    default = "http://127.0.0.1:11434"
    if not url:
        return os.environ.get("OLLAMA_HOST", default)
    u = url.strip()
    if not u:
        return os.environ.get("OLLAMA_HOST", default)
    if not urlparse(u).scheme:
        u = "http://" + u
    return u


@st.cache_data(show_spinner=False)
def fetch_ollama_models(base_url: str) -> List[str]:
    """
    Query Ollama for installed models via /api/tags.
    Returns a list of model names (e.g., 'llama3', 'hermes3:8b').
    Cached for performance; use 'Refresh' button to clear.
    """
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        resp.raise_for_status()
        data = resp.json() or {}
        models = [m.get("name") for m in data.get("models", []) if m.get("name")]
        return sorted(models)  # sorted for stable UI
    except Exception as e:
        st.warning(f"Could not fetch models from Ollama at {base_url}: {e}")
        return []


def get_chat_model(model_name: str, temperature: float, base_url: str) -> ChatOllama:
    """Create a ChatOllama instance pointing at the selected base_url."""
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=base_url,
    )
