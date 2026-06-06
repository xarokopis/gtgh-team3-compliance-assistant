import json

from gtgh_team3_compliance_assistant.config import DATA_DIR


CHUNK_DIR = DATA_DIR / "chunks"
CHUNK_DIR.mkdir(parents=True, exist_ok=True)


class ChunkStore:
    def save(self, document_id, chunks):
        file_path = CHUNK_DIR / f"{document_id}.json"

        payload = {
            "document_id": document_id,
            "chunks": [],
        }

        for idx, chunk in enumerate(chunks):
            payload["chunks"].append(
                {
                    "chunk_id": idx,
                    "article": chunk.get("article"),
                    "text": chunk["text"],
                }
            )

        file_path.write_text(
            json.dumps(payload, indent=2)
        )