import streamlit as st
from pathlib import Path
from streamlit_file_browser import st_file_browser
from project_manager import PROJECTS_PATH


def project_file_browser():
    st.sidebar.subheader("Project Files")

    with st.sidebar.expander("Browse projects directory"):
        if PROJECTS_PATH.exists():
            st.sidebar.write("Contents:", [p.name for p in PROJECTS_PATH.iterdir()])

        event = st_file_browser(
            "/app/projects",
            key=f"projects_file_browser_{st.session_state.get('file_browser_refresh', 0)}",
            show_preview=False,
            show_download_file=False,
            show_upload_file=False,
            show_delete_file=False,
            show_rename_file=False,
            show_new_folder=False,
        )

    if event and event.get("type") == "SELECT_FILE":
        selected_path = Path("/app/projects") / event["target"]["path"]

        st.sidebar.caption(f"Selected: {event['target']['name']}")

        with open(selected_path, "rb") as file:
            st.sidebar.download_button(
                label=f"Download {event['target']['name']}",
                data=file,
                file_name=event["target"]["name"],
                mime="application/octet-stream"
            )