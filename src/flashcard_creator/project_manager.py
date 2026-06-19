from pathlib import Path
import streamlit as st

PROJECTS_PATH = Path("/app/projects/")


def get_project_paths(project_name):
    safe_name = project_name.strip().replace(" ", "_").lower()

    project_path = PROJECTS_PATH / safe_name

    return {
        "project": project_path,
        "raw_csv": project_path / "raw_csv_files",
        "cleaned_csv": project_path / "cleaned_csv_files",
        "uploaded": project_path / "uploaded_images",
        "cropped": project_path / "cropped_images",
    }


def project_sidebar():
    st.sidebar.title("Project Selection")

    project_name = st.sidebar.text_input(
        "Project name",
        placeholder="Enter project name"
    )

    if "active_project" not in st.session_state:
        st.session_state.active_project = None

    if project_name != st.session_state.active_project:
        st.session_state.project_loaded = False
        st.session_state.image_processed = False

    if not project_name.strip():
        st.warning("Please enter a project name.")
        st.stop()

    paths = get_project_paths(project_name)

    if st.sidebar.button("Create / Load Project"):
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)

        st.session_state.project_loaded = True
        st.session_state.active_project = project_name
        st.session_state.image_processed = False
        st.session_state.file_browser_refresh = st.session_state.get("file_browser_refresh", 0) + 1

        st.rerun()

    if not st.session_state.get("project_loaded", False):
        st.info("Create or load a project to continue.")
        st.stop()

    return paths