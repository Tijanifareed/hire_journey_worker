# # Use slim Python base image
# FROM python:3.11-slim

# # Install system dependencies (Tesseract OCR + build tools)
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     libtesseract-dev \
#     poppler-utils \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Set work directory
# WORKDIR /app

# # Copy dependencies
# COPY requirements.txt .

# # Install Python deps
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . .

# # Expose FastAPI port
# EXPOSE 8000

# # Run app with uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




# -------- BUILDER STAGE --------
FROM python:3.11-slim AS builder

# Install build dependencies (only used here)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install deps into a temp folder (not system-wide)
RUN pip install --user --no-cache-dir -r requirements.txt


# -------- RUNTIME STAGE --------
FROM python:3.11-slim

# Install runtime dependencies (Tesseract, Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy app source code
COPY . .

# Make sure Python can see installed deps
ENV PATH=/root/.local/bin:$PATH

# Expose FastAPI port
EXPOSE 8000

# Run app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




