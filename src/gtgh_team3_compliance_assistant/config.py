from pathlib import Path

# DIRS
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR_PDF = BASE_DIR / "data" / "pdf"

RAW_DIR = DATA_DIR / "raw" / "eurlex"
EXTRACTED_DIR = DATA_DIR / "extracted"

EXTRACTED_DIR.mkdir(parents=True,exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Embedding
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Storage
STORAGE_PERSIST_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "pdf_collection"

PDF_DIR = DATA_DIR_PDF