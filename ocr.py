import pytesseract
import pandas as pd
import cv2, os
from pathlib import Path

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

RAW_CSV_PATH = Path("./raw_csv_files/")
# CROPPED_PATH = Path("./cropped_images/")


def ocr_column(image, lang="eng+jpn"):
    text = pytesseract.image_to_string(image, lang=lang)

    return [line.strip() for line in text.splitlines() if line.strip()]


# def crop_columns(image_path):
#     img = cv2.imread(image_path)

#     cropped_images = []
    
#     for i in range(3):
#         x, y, w, h = cv2.selectROI("Select ROI", img, fromCenter=False)
#         if x == 0 and y == 0 and w == 0 and h == 0:
#             break
#         cropped = img[y:y+h, x:x+w]

#         CROPPED_IMAGES_PATH.mkdir(exist_ok=True)

#         cv2.imwrite(CROPPED_IMAGES_PATH / f"cropped_{i}.png", cropped)
#         cropped_images.append(cropped)

#     cv2.destroyAllWindows()

#     return cropped_images


# def process_image(image_path):
#     japanese_img, romaji_img, english_img = crop_columns(image_path)

#     japanese = ocr_column(japanese_img, lang="jpn")
#     romaji = ocr_column(romaji_img, lang="eng")
#     english = ocr_column(english_img, lang="eng")

#     edited_japanese = pd.Series(japanese).map(
#         lambda x: x.strip() if isinstance(x, str) else x
#     )
#     edited_romaji = pd.Series(romaji).map(
#         lambda x: x.strip() if isinstance(x, str) else x
#     )
#     edited_english = pd.Series(english).map(
#         lambda x: x.strip() if isinstance(x, str) else x
#     )

#     RAW_CSV_PATH.mkdir(exist_ok=True)

#     edited_japanese.to_csv(RAW_CSV_PATH / "japanese_raw.csv", index=False, header=False, encoding="utf-8-sig")
#     edited_romaji.to_csv(RAW_CSV_PATH / "romaji_raw.csv", index=False, header=False, encoding="utf-8-sig")
#     edited_english.to_csv(RAW_CSV_PATH / "english_raw.csv", index=False, header=False, encoding="utf-8-sig")


def process_crops(japanese_img, romaji_img, english_img):
    japanese = ocr_column(japanese_img, lang="jpn")
    romaji = ocr_column(romaji_img, lang="eng")
    english = ocr_column(english_img, lang="eng")

    edited_japanese = pd.Series(japanese).map(
        lambda x: x.strip() if isinstance(x, str) else x
    )
    edited_romaji = pd.Series(romaji).map(
        lambda x: x.strip() if isinstance(x, str) else x
    )
    edited_english = pd.Series(english).map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

    RAW_CSV_PATH.mkdir(exist_ok=True)

    edited_japanese.to_csv("./raw_csv_files/japanese_raw.csv", index=False, header=False, encoding="utf-8-sig")
    edited_romaji.to_csv("./raw_csv_files/romaji_raw.csv", index=False, header=False, encoding="utf-8-sig")
    edited_english.to_csv("./raw_csv_files/english_raw.csv", index=False, header=False, encoding="utf-8-sig")


if __name__ == "__main__":
    # process_image()
    pass