from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR_PDF = BASE_DIR / "data" / "pdf"

RAW_DIR = DATA_DIR / "raw" / "eurlex"
METADATA_DIR = DATA_DIR / "metadata"

EXTRACTED_DIR = DATA_DIR / "extracted"

EXTRACTED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

METADATA_FILE = METADATA_DIR / "documents.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

STORAGE_PERSIST_PATH = BASE_DIR / "db"