import pytesseract
from PIL import Image
import pandas as pd
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

DELIMITER = "。"
IMAGE_PATH = "greetings.png"

def ocr_column(image, lang="eng+jpn"):
    text = pytesseract.image_to_string(image, lang=lang)

    return [line.strip() for line in text.splitlines() if line.strip()]


def crop_columns(image_path):
    img = cv2.imread(image_path)

    cropped_images = []
    
    for i in range(3):
        x, y, w, h = cv2.selectROI("Select ROI", img, fromCenter=False)
        if x == 0 and y == 0 and w == 0 and h == 0:
            break
        cropped = img[y:y+h, x:x+w]
        cv2.imwrite(f"./cropped_images/cropped_{i}.png", cropped)
        cropped_images.append(cropped)

    cv2.destroyAllWindows()

    return cropped_images


def build_flashcards():
    japanese_img, romaji_img, english_img = crop_columns(IMAGE_PATH)

    japanese = ocr_column(japanese_img, lang="jpn")
    romaji = ocr_column(romaji_img, lang="eng")
    english = ocr_column(english_img, lang="eng")

    pd.Series(japanese).to_csv("./raw_csv_files/japanese_raw.csv", index=False, encoding="utf-8-sig")
    pd.Series(romaji).to_csv("./raw_csv_files/romaji_raw.csv", index=False, encoding="utf-8-sig")
    pd.Series(english).to_csv("./raw_csv_files/english_raw.csv", index=False, encoding="utf-8-sig")

    print(len(japanese), len(romaji), len(english))

    # max_len = max(len(japanese), len(romaji), len(english))

    # df = pd.DataFrame({
    #     "Japanese": japanese + [""] * (max_len - len(japanese)),
    #     "Romaji": romaji + [""] * (max_len - len(romaji)),
    #     "English": english + [""] * (max_len - len(english))
    # })

    # print(df["Japanese"])
    # print(df["Romaji"])
    # print(df["English"])
    # return df


if __name__ == "__main__":
    build_flashcards()