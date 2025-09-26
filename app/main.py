
# main.py
from fastapi import File
from app.routers import jd_image
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from app.extractor import extract_text_from_url
from app.services.extractor import extract_text_from_url
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Job Description Extractor")
app.include_router(jd_image.router, prefix="/extract", tags=["JD Image"])

origins = [
    "http://127.0.0.1:8002",
    "https://hire-journey.onrender.com",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, etc.
    allow_headers=["*"],    # Authorization, Content-Type, etc.
)

@app.get("/")
def root():
    return {"message": "Welcome to HireJourney API 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}



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
    

