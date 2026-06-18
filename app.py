import streamlit as st
import pandas as pd
from ocr import process_crops
from pathlib import Path
from streamlit_cropper import st_cropper
from PIL import Image


RAW_CSV_PATH = Path("./raw_csv_files/")
CLEANED_CSV_PATH = Path("./cleaned_csv_files/")
UPLOAD_PATH = Path("./uploaded_images/")
CROPPED_PATH = Path("./cropped_images/")

required_files = [
    RAW_CSV_PATH / "japanese_raw.csv",
    RAW_CSV_PATH / "romaji_raw.csv",
    RAW_CSV_PATH / "english_raw.csv"
]


def image_processor():
    st.title("Image Uploader")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is None:
        return
    
    UPLOAD_PATH.mkdir(exist_ok=True)
    CROPPED_PATH.mkdir(exist_ok=True)

    img = Image.open(uploaded_file)

    uploaded_image_path = UPLOAD_PATH / uploaded_file.name
    img.save(uploaded_image_path)

    st.image(img, caption="Uploaded Image", width="stretch")

    st.subheader("Select Japanese column")
    japanese_crop = st_cropper(
        img,
        realtime_update=True,
        box_color="#0000FF",
        key="japanese_crop"
    )

    st.subheader("Select Romaji column")
    romaji_crop = st_cropper(
        img,
        realtime_update=True,
        box_color="#00FF00",
        key="romaji_crop"
    )

    st.subheader("Select English column")
    english_crop = st_cropper(
        img,
        realtime_update=True,
        box_color="#FF0000",
        key="english_crop"
    )

    if st.button("Process Image"):
        japanese_crop.save(CROPPED_PATH / "japanese_crop.png")
        romaji_crop.save(CROPPED_PATH / "romaji_crop.png")
        english_crop.save(CROPPED_PATH / "english_crop.png")

        process_crops(
            japanese_crop,
            romaji_crop,
            english_crop
        )

        st.session_state.image_processed = True
        st.success("Image processed successfully!")
        st.rerun()


def dashboard():
    if "image_processed" not in st.session_state:
        st.session_state.image_processed = False

    if not st.session_state.image_processed:
        image_processor()
        return

    st.title("Flashcard OCR Cleaner")

    if not all(file.exists() for file in required_files):
        st.error("Raw CSV files were not found. Please process an image first.")
        st.session_state.image_processed = False
        st.stop()

    japanese_df = pd.read_csv(RAW_CSV_PATH / "japanese_raw.csv", header=None, names=["Japanese"])
    romaji_df = pd.read_csv(RAW_CSV_PATH / "romaji_raw.csv", header=None, names=["Romaji"])
    english_df = pd.read_csv(RAW_CSV_PATH / "english_raw.csv", header=None, names=["English"])

    st.subheader("Japanese")
    edited_japanese = st.data_editor(
        japanese_df,
        num_rows="dynamic",
        width="stretch"
    )

    st.subheader("Romaji")
    edited_romaji = st.data_editor(
        romaji_df,
        num_rows="dynamic",
        width="stretch"
    )

    st.subheader("English")
    edited_english = st.data_editor(
        english_df,
        num_rows="dynamic",
        width="stretch"
    )

    if st.button("Save edited CSVs"):
        CLEANED_CSV_PATH.mkdir(exist_ok=True)

        edited_japanese.to_csv(CLEANED_CSV_PATH / "japanese_cleaned.csv", index=False, header=False, encoding="utf-8-sig")
        edited_romaji.to_csv(CLEANED_CSV_PATH / "romaji_cleaned.csv", index=False, header=False, encoding="utf-8-sig")
        edited_english.to_csv(CLEANED_CSV_PATH / "english_cleaned.csv", index=False, header=False, encoding="utf-8-sig")
        st.success("Saved cleaned CSVs.")

    if st.button("Process another image"):
        st.session_state.image_processed = False
        st.rerun()


if __name__ == "__main__":
    dashboard()