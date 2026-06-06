import json
from src.gtgh_team3_compliance_assistant.config import DATA_DIR
CHUNK_DIR = DATA_DIR / "chunks"
CHUNK_DIR.mkdir(parents=True, exist_ok=True)
class ChunkStore:
    def save(self, document_id, chunks):
        file_path = CHUNK_DIR / f"{document_id}.json"

        payload = {
            "document_id": document_id,
            "chunk_count": len(chunks),
            "chunks": [],
        }

        for idx, chunk in enumerate(chunks):
            chunk_text = chunk["text"]

            payload["chunks"].append(
                {
                    "chunk_id": idx,
                    "type": chunk.get("type"),
                    "article": chunk.get("article"),
                    "article_number": chunk.get("article_number"),
                    "recital_number": chunk.get("recital_number"),
                    "title": chunk.get("title"),
                    "text": chunk_text,
                    "char_length": len(chunk_text),
                }
            )

        file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return file_path