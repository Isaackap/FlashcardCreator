ARG PYTHON_VERSION=3.12.9
FROM python:${PYTHON_VERSION}-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.7.17 /uv /uvx /bin/

WORKDIR /app

# Install system dependencies:
# - tesseract-ocr: OCR engine
# - tesseract-ocr-jpn: Japanese language data
# - libgl1/libglib2.0-0: needed for OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better Docker caching
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen || uv sync

# Copy project files
COPY . .

# Create app folders if they don't exist
RUN mkdir -p raw_csv_files cleaned_csv_files uploaded_images cropped_images

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]