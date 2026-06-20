import streamlit as st
from streamlit_file_browser import st_file_browser


def project_file_browser(paths):
    st.header("Project Files")

    project_path = paths["project"]

    event = st_file_browser(
        str(project_path),
        key=f"projects_file_browser_{st.session_state.get('active_project')}_{st.session_state.get('file_browser_refresh', 0)}",
        show_preview=True,
        show_download_file=False,
        show_upload_file=False,
        show_delete_file=False,
        show_rename_file=False,
        show_new_folder=False,
        )
    
    if event and event.get("type") == "SELECT_FILE":
        selected_path = project_path / event["target"]["path"]

        if selected_path.is_file():
            st.write(f"Selected file: `{event['target']['name']}`")

            with open(selected_path, "rb") as file:
                st.download_button(
                    label=f"Download {event['target']['name']}",
                    data=file,
                    file_name=event["target"]["name"],
                    mime="application/octet-stream"
                )