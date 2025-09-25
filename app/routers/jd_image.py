from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Union
from app.utils.ocr import extract_text_from_image
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# Use a thread pool for parallel OCR (faster if multiple images uploaded)
executor = ThreadPoolExecutor(max_workers=4)


@router.post("/jd-image")
async def analyze_jd_from_images(
    files: Union[UploadFile, List[UploadFile]] = File(...)
):
    try:
        # Normalize to a list
        if isinstance(files, UploadFile):
            files = [files]

        # Read file contents
        file_contents = [await f.read() for f in files]

        # Run OCR in parallel
        results = list(executor.map(extract_text_from_image, file_contents))
        results = [r for r in results if r]  # filter out empty

        if not results:
            raise HTTPException(status_code=400, detail="No text extracted from images")

        combined_jd = "\n".join(results)
        return {"job_description": combined_jd}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
