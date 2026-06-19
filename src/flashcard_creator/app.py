import streamlit as st
from flashcard_creator.project_manager import project_sidebar
from flashcard_creator.image_processor import image_processor
from flashcard_creator.flashcard_editor import flashcard_editor
from flashcard_creator.file_browser import project_file_browser


def dashboard():
    paths = project_sidebar()
    project_file_browser()

    if not st.session_state.get("image_processed", False):
        image_processor(paths)
        return
    
    flashcard_editor(paths)


if __name__ == "__main__":
    dashboard()