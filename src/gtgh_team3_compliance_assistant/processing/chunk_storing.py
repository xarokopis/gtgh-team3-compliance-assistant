import json
from pathlib import Path

from gtgh_team3_compliance_assistant.config import DATA_DIR


CHUNK_DIR = DATA_DIR / "chunks"
CHUNK_DIR.mkdir(parents=True, exist_ok=True)


class ChunkStore:
    def save(self, document_id: str, chunks: list[str]):
        file_path = CHUNK_DIR / f"{document_id}.json"

        data = {
            "document_id": document_id,
            "chunks": [
                {"chunk_id": i, "text": chunk}
                for i, chunk in enumerate(chunks)
            ]
        }

        file_path.write_text(json.dumps(data, indent=2))