from datetime import datetime
from uuid import uuid4

from gtgh_team3_compliance_assistant.ingestion.eurlex_client import EurLexClient
from gtgh_team3_compliance_assistant.ingestion.downloader import Downloader
from gtgh_team3_compliance_assistant.ingestion.metadata_storing import MetadataStore
from gtgh_team3_compliance_assistant.processing.text_extractor import TextExtractor
from gtgh_team3_compliance_assistant.processing.eur_chunker import EurChunker
from gtgh_team3_compliance_assistant.processing.chunk_storing import ChunkStore


class IngestionService:
    def __init__(self):
        self.store = MetadataStore()
        self.client = EurLexClient()
        self.downloader = Downloader()
        self.extractor = TextExtractor()
        self.chunker = EurChunker()
        self.chunk_store = ChunkStore()

    async def ingest_eurlex(self):
        docs = self.client.fetch_documents()

        count = 0

        for doc in docs:
            if self.store.exists(doc["url"]):
                continue

            filename = doc["title"].replace(" ", "_") + ".pdf"

            file_path, file_hash = await self.downloader.download(doc["url"],filename)

            text = self.extractor.extract(str(file_path))

            chunks = self.chunker.chunk(text)

            self.chunk_store.save(str(uuid4()), chunks)

            record = {
                "id": str(uuid4()),
                "title": doc["title"],
                "url": doc["url"],
                "local_path": str(file_path),
                "file_hash": file_hash,
                "source": "eurlex",
                "ingested_at": datetime.utcnow().isoformat()
            }

            self.store.add(record)
            count += 1
            

        return count