# CAISA Model Switch – Streamlit + Ollama Chat App

This project is a modular **chat application** that connects to a locally running **Ollama** server and allows you to dynamically **switch between installed LLM models**, control temperature, and modify the system prompt in real time.

It is structured for clarity and future expansion on CAISA workflows, patient personas, logging, and evaluation.

---

## Features

- 🔁 Dynamic model switching from installed Ollama models  
- 🎛 Temperature control from the UI  
- 🧠 Editable system prompt (role-based behavior)  
- 💬 Streaming responses with custom chat bubbles  
- 💾 Persistent chat state using `st.session_state`  
- 🧱 Clean modular project structure  
- ⚡ GPU acceleration handled by Ollama automatically  

---

## 📁 Project Structure

```text
caisa_model_switch/
├── src/
│   ├── __init__.py
│   ├── utils.py         # Ollama utilities & model fetching
│   ├── state.py         # Session state management
│   ├── ui.py            # UI, CSS, sidebar, chat rendering
│   └── chat.py          # Streaming chat logic
├── main.py              # Streamlit entry point
├── .env                 # Set OLLAMA_HOST server
├── requirements.txt
└── README.md

