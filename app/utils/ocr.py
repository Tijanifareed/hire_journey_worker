# import pytesseract
# from PIL import Image
# import io
# import re

# # Tell pytesseract where tesseract.exe is installed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# def clean_text(text: str) -> str:
#     """Clean up OCR output."""
#     # normalize spaces
#     text = re.sub(r"\s+", " ", text)
#     # split into lines and filter out junk
#     lines = text.splitlines()
#     cleaned = []
#     blacklist = ["apply now", "sign up", "login", "create account", "subscribe",]
    
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
#         if len(line) < 15:
#             continue
#         if any(bad in line.lower() for bad in blacklist):
#             continue
#         cleaned.append(line)
#     return "\n".join(cleaned)

# def extract_text_from_image(image_bytes: bytes) -> str:
#     """Extract job description text from an image using OCR."""
#     image = Image.open(io.BytesIO(image_bytes))
#     text = pytesseract.image_to_string(image)
#     return clean_text(text)


import pytesseract
from PIL import Image
import io
import re
import os
import platform

# Configure Tesseract path only on Windows (local dev)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def clean_text(text: str) -> str:
    """Clean up OCR output."""
    text = re.sub(r"\s+", " ", text)
    lines = text.splitlines()
    cleaned = []
    blacklist = ["apply now", "sign up", "login", "create account", "subscribe"]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 15:
            continue
        if any(bad in line.lower() for bad in blacklist):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract job description text from an image using OCR."""
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return clean_text(text)
