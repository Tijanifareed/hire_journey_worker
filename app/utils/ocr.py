
# import pytesseract
# from PIL import Image
# import io
# import re
# import os
# import platform

# # Configure Tesseract path only on Windows (local dev)
# if platform.system() == "Windows":
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# def clean_text(text: str) -> str:
#     """Clean up OCR output."""
#     text = re.sub(r"\s+", " ", text)
#     lines = text.splitlines()
#     cleaned = []
#     blacklist = ["apply now", "sign up", "login", "create account", "subscribe"]
    
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


# # def extract_text_from_image(image_bytes: bytes) -> str:
# #     """Extract job description text from an image using OCR."""
# #     image = Image.open(io.BytesIO(image_bytes))
# #     text = pytesseract.image_to_string(image)
# #     return clean_text(text)

# def extract_text_from_image(image_bytes: bytes) -> str:
#     image = Image.open(io.BytesIO(image_bytes)).convert("L")

#     # Resize if too large
#     max_width = 1000
#     if image.width > max_width:
#         ratio = max_width / image.width
#         image = image.resize((max_width, int(image.height * ratio)))

#     # Binarize (make text pop)
#     image = image.point(lambda x: 0 if x < 180 else 255, "1")

#     # OCR with tuned config
#     config = "--oem 3 --psm 6"
#     text = pytesseract.image_to_string(image, lang="eng", config=config)

#     return clean_text(text)



import pytesseract
from PIL import Image, ImageOps
import io
import re
import platform

# Configure Tesseract path only on Windows (local dev)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def clean_text(text: str) -> str:
    """Clean up OCR output for job descriptions."""
    text = re.sub(r"\s+", " ", text)
    lines = text.splitlines()
    cleaned = []
    blacklist = [
        "apply now",
        "sign up",
        "login",
        "create account",
        "subscribe",
        "visit our website",
        "click here",
        "www.",
        "http",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 20:  # ignore very short lines
            continue
        if any(bad in line.lower() for bad in blacklist):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def preprocess_image(image: Image.Image) -> Image.Image:
    """Prepare image for better OCR."""
    # Convert to grayscale
    image = image.convert("L")

    # Resize if too large (speed boost)
    max_width = 1000
    if image.width > max_width:
        ratio = max_width / image.width
        image = image.resize((max_width, int(image.height * ratio)))

    # Binarize (improve text clarity)
    image = image.point(lambda x: 0 if x < 180 else 255, "1")

    return image


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract job description text from an image using optimized Tesseract OCR."""
    image = Image.open(io.BytesIO(image_bytes))
    image = preprocess_image(image)

    # OCR with tuned config for paragraphs
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(image, lang="eng", config=config)

    return clean_text(text)
