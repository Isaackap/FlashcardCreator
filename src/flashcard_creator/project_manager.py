from pathlib import Path
import streamlit as st
import shutil
from file_browser import project_file_browser

PROJECTS_PATH = Path("/app/projects/")


def clean_project_name(name):
    return name.strip().replace(" ", "_").lower()


def get_project_paths(project_name):
    safe_name = clean_project_name(project_name)

    project_path = PROJECTS_PATH / safe_name

    return {
        "project": project_path,
        "raw_csv": project_path / "raw_csv_files",
        "cleaned_csv": project_path / "cleaned_csv_files",
        "uploaded": project_path / "uploaded_images",
        "cropped": project_path / "cropped_images",
        "anki": project_path / "anki_exports",
    }


def create_project_folders(paths):
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)


def get_existing_projects():
    PROJECTS_PATH.mkdir(parents=True, exist_ok=True)

    return sorted(
        path.name
        for path in PROJECTS_PATH.iterdir()
        if path.is_dir()
    )


def project_has_raw_csv(paths):
    japanese_raw_path = paths["raw_csv"] / "japanese_raw.csv"
    english_raw_path = paths["raw_csv"] / "english_raw.csv"

    return japanese_raw_path.exists() and english_raw_path.exists()


@st.dialog("Delete project?")
def confirm_delete_project(project_name):
    paths = get_project_paths(project_name)

    st.warning("This will permanently delete the loaded project and all of its files.")
    st.write(f"Project: `{project_name}`")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, delete project", type="primary"):
            if paths["project"].exists():
                shutil.rmtree(paths["project"])

            st.session_state.active_project = None
            st.session_state.project_loaded = False
            st.session_state.image_processed = False
            st.session_state.file_browser = False

            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.rerun()


def toggle_project_folder():
    opening_folder = not st.session_state.file_browser

    st.session_state.file_browser = opening_folder

    if opening_folder:
        st.session_state.file_browser_refresh += 1


def project_sidebar():
    st.sidebar.title("Project Selection")

    if "active_project" not in st.session_state:
        st.session_state.active_project = None

    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False

    if "image_processed" not in st.session_state:
        st.session_state.image_processed = False

    if "file_browser" not in st.session_state:
        st.session_state.file_browser = False

    if "file_browser_refresh" not in st.session_state:
        st.session_state.file_browser_refresh = 0

    st.sidebar.subheader("Create Project")

    new_project_name = st.sidebar.text_input(
        "New project name",
        placeholder="Example: genki1_ch1"
    )

    if st.sidebar.button("Create Project"):
        if not new_project_name.strip():
            st.sidebar.warning("Please enter a project name.")
        else:
            safe_name = clean_project_name(new_project_name)
            paths = get_project_paths(safe_name)

            if paths["project"].exists():
                st.sidebar.warning(f"Project already exists: {safe_name}")
            else:
                create_project_folders(paths)
                st.sidebar.success(f"Created project: {safe_name}")
                st.session_state.file_browser = False
                st.rerun()

    st.sidebar.divider()

    st.sidebar.subheader("Load Project")

    existing_projects = get_existing_projects()

    if not existing_projects:
        st.info("Create a project to continue.")
        st.stop()

    selected_project = st.sidebar.selectbox(
        "Existing projects",
        existing_projects
    )

    if st.sidebar.button("Load Project"):
        paths = get_project_paths(selected_project)

        # protects older projects in case any subfolders are missing.
        create_project_folders(paths)

        st.session_state.active_project = selected_project
        st.session_state.project_loaded = True
        st.session_state.image_processed = project_has_raw_csv(paths)
        st.session_state.file_browser = False

        st.rerun()

    if not st.session_state.project_loaded:
        st.info("Select a project and click Load Project to continue.")
        st.stop()

    paths = get_project_paths(st.session_state.active_project)

    st.sidebar.success(f"Loaded: {st.session_state.active_project}")

    st.sidebar.button(
        "Toggle Project Folder",
        on_click=toggle_project_folder
    )

    if st.session_state.file_browser:
        project_file_browser(paths)

    if st.sidebar.button("Delete Loaded Project", type="secondary"):
        confirm_delete_project(st.session_state.active_project)


    return paths