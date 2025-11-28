# app/main.py

from src.state import init_session
from src.ui import setup_page, render_sidebar, render_history
from src.chat import handle_user_turn_streaming
# from src.state import init_session


def run_app() -> None:
    setup_page()
    init_session(system_prompt_default="You are a helpful doctor for health-related questions.")
    render_sidebar()
    render_history()
    handle_user_turn_streaming()


if __name__ == "__main__":
    run_app()
