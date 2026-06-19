import pandas as pd
import streamlit as st


def flashcard_editor(paths):
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