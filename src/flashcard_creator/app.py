import streamlit as st
from project_manager import project_sidebar
from image_processor import image_processor
from flashcard_editor import flashcard_editor


def dashboard():
    paths = project_sidebar()

    if not st.session_state.get("image_processed", False):
        image_processor(paths)
        return
    
    flashcard_editor(paths)


if __name__ == "__main__":
    dashboard()