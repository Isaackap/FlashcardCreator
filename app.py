import streamlit as st
import pandas as pd
from ocr import process_crops
from pathlib import Path
from streamlit_cropper import st_cropper
from PIL import Image
from streamlit_file_browser import st_file_browser


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


def image_processor(paths):
    st.title("Image Uploader")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is None:
        return

    img = Image.open(uploaded_file)

    st.image(img, caption="Uploaded Image", width="stretch")

    st.subheader("Select Japanese column")
    japanese_crop = st_cropper(
        img,
        realtime_update=True,
        box_color="#0000FF",
        key="japanese_crop"
    )

    st.subheader("Select English column")
    english_crop = st_cropper(
        img,
        realtime_update=True,
        box_color="#FF0000",
        key="english_crop"
    )

    if st.button("Process Image"):
        uploaded_image_path = paths["uploaded"] / uploaded_file.name
        img.save(uploaded_image_path)
        
        japanese_crop.save(paths["cropped"] / "japanese_crop.png")
        english_crop.save(paths["cropped"] / "english_crop.png")

        process_crops(
            japanese_crop,
            english_crop,
            paths["raw_csv"]
        )

        st.session_state.image_processed = True
        st.success("Image processed successfully!")
        st.rerun()


def dashboard():
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

    st.sidebar.subheader("Project Files")

    with st.sidebar.expander("Browse projects directory"):
        # st.sidebar.write("Path:", PROJECTS_PATH.resolve())
        # st.sidebar.write("Exists:", PROJECTS_PATH.exists())

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

    if "image_processed" not in st.session_state:
        st.session_state.image_processed = False

    if not st.session_state.image_processed:
        image_processor(paths)
        return

    st.title("Flashcard OCR Cleaner")

    japanese_raw_path = paths["raw_csv"] / "japanese_raw.csv"
    english_raw_path = paths["raw_csv"] / "english_raw.csv"

    if not japanese_raw_path.exists() or not english_raw_path.exists():
        st.error("Raw CSV files were not found. Please process an image first.")
        st.session_state.image_processed = False
        st.stop()

    japanese_df = pd.read_csv(japanese_raw_path, header=None, names=["Japanese"])
    english_df = pd.read_csv(english_raw_path, header=None, names=["English"])

    combined_df = pd.DataFrame({
        "Japanese": japanese_df["Japanese"],
        "English": english_df["English"]
    })

    st.subheader("Flashcards")

    edited_df = st.data_editor(
        combined_df,
        num_rows="dynamic",
        width="stretch"
    )

    if st.button("Save edited flashcards"):
        edited_df.to_csv(
            paths["cleaned_csv"] / "flashcards.csv",
            index=False,
            header=False,
            encoding="utf-8-sig")
        
        st.success("Saved cleaned CSV.")

    if st.button("Process another image"):
        st.session_state.image_processed = False
        st.rerun()


if __name__ == "__main__":
    dashboard()