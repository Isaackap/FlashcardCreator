import streamlit as st
import pandas as pd

st.title("Flashcard OCR Cleaner")

japanese_df = pd.read_csv("./raw_csv_files/japanese_raw.csv")
romaji_df = pd.read_csv("./raw_csv_files/romaji_raw.csv")
english_df = pd.read_csv("./raw_csv_files/english_raw.csv")

st.subheader("Japanese")
edited_japanese = st.data_editor(
    japanese_df,
    num_rows="dynamic",
    use_container_width=True
)

st.subheader("Romaji")
edited_romaji = st.data_editor(
    romaji_df,
    num_rows="dynamic",
    use_container_width=True
)

st.subheader("English")
edited_english = st.data_editor(
    english_df,
    num_rows="dynamic",
    use_container_width=True
)

if st.button("Save edited CSVs"):
    edited_japanese.to_csv("./cleaned_csv_files/japanese_cleaned.csv", index=False, encoding="utf-8-sig")
    edited_romaji.to_csv("./cleaned_csv_files/romaji_cleaned.csv", index=False, encoding="utf-8-sig")
    edited_english.to_csv("./cleaned_csv_files/english_cleaned.csv", index=False, encoding="utf-8-sig")
    st.success("Saved cleaned CSVs.")