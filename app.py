import streamlit as st
import pandas as pd
from ocr import process_image
from pathlib import Path


RAW_CSV_PATH = Path("./raw_csv_files/")
CLEANED_CSV_PATH = Path("./cleaned_csv_files/")
UPLOAD_PATH = Path("./uploaded_images/")

required_files = [
    RAW_CSV_PATH / "japanese_raw.csv",
    RAW_CSV_PATH / "romaji_raw.csv",
    RAW_CSV_PATH / "english_raw.csv"
]


def image_processor():
    st.title("Image Uploader")

    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        UPLOAD_PATH.mkdir(exist_ok=True)

        file_path = UPLOAD_PATH / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Uploaded Image", width="stretch")

        if st.button("Process Image"):
            process_image(str(file_path))
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