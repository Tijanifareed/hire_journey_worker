
# main.py
from fastapi import File
from app.routers import jd_image
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from app.extractor import extract_text_from_url
from app.services.extractor import extract_text_from_url


app = FastAPI(title="Job Description Extractor")
app.include_router(jd_image.router, prefix="/extract", tags=["JD Image"])




class UrlRequest(BaseModel):
    url: str

@app.post("/extract-text")
async def extract_text(request: UrlRequest):
    try:
        text = extract_text_from_url(request.url)
        if not text:
            raise HTTPException(status_code=404, detail="No job description found")
        return {"job_description": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

