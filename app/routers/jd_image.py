from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List, Union
from app.utils.ocr import extract_text_from_image
import uuid

router = APIRouter()

# Fake in-memory "queue" storage (reset if server restarts)
jobs = {}


def process_images(job_id: str, files: List[bytes]):
    """Background OCR task for multiple images"""
    try:
        texts = []
        for contents in files:
            text = extract_text_from_image(contents)
            if text:
                texts.append(text)

        if texts:
            jobs[job_id] = {"status": "done", "result": "\n".join(texts)}
        else:
            jobs[job_id] = {"status": "failed", "error": "No text extracted"}
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}
        
        
@router.post("/jd-image")
async def analyze_jd_from_images(
    files: Union[UploadFile, List[UploadFile]] = File(...)
):
    try:
        # Normalize to a list
        if isinstance(files, UploadFile):
            files = [files]

        all_texts = []
        for file in files:
            contents = await file.read()
            jd_text = extract_text_from_image(contents)
            if jd_text:
                all_texts.append(jd_text)

        if not all_texts:
            raise HTTPException(status_code=400, detail="No text extracted from images")

        combined_jd = "\n".join(all_texts)
        return {"job_description": combined_jd}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))             


@router.post("/jd-image-async")
async def analyze_jd_async(
    background_tasks: BackgroundTasks,
    files: Union[UploadFile, List[UploadFile]] = File(...)
):
    # Normalize to list
    if isinstance(files, UploadFile):
        files = [files]

    # Generate ONE job_id for all uploaded files
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}

    # Collect file contents
    file_contents = [await file.read() for file in files]

    # Add background task
    background_tasks.add_task(process_images, job_id, file_contents)

    return {"job_id": job_id}


@router.get("/result/{job_id}")
def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Return job result and delete it immediately
    result = job
    del jobs[job_id]
    return result
