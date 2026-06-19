import pytesseract
import pandas as pd
import cv2, os
from pathlib import Path

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_column(image, lang="eng+jpn"):
    text = pytesseract.image_to_string(image, lang=lang)

    return [line.strip() for line in text.splitlines() if line.strip()]


def process_crops(japanese_img, english_img, raw_csv_path):
    japanese = ocr_column(japanese_img, lang="jpn")
    english = ocr_column(english_img, lang="eng")
    
    edited_japanese = pd.Series(japanese).map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

    edited_english = pd.Series(english).map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

    raw_csv_path.mkdir(parents=True, exist_ok=True)

    edited_japanese.to_csv(raw_csv_path / "japanese_raw.csv", index=False, header=False, encoding="utf-8-sig")
    edited_english.to_csv(raw_csv_path / "english_raw.csv", index=False, header=False, encoding="utf-8-sig")


if __name__ == "__main__":
    pass