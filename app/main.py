# # app/main.py
# from fastapi import FastAPI, HTTPException, Query
# from app.services.extractor import extract_text_from_url

# app = FastAPI(title="Text Worker Service")

# @app.get("/health")
# async def health():
#     return {"status": "ok"}

# @app.post("/extract-text")
# async def extract_text(url: str = Query(..., description="URL to extract text from")):
#     try:
#         text = await extract_text_from_url(url)
#         return {"url": url, "extracted_text": text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from app.extractor import extract_text_from_url
from app.services.extractor import extract_text_from_url

app = FastAPI(title="Job Description Extractor")

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
