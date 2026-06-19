import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
from flashcard_creator.ocr import process_crops


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