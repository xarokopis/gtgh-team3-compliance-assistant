from pathlib import Path
from gtgh_team3_compliance_assistant.embedding.LocalEmbedder import LocalEmbedder
from gtgh_team3_compliance_assistant.model_communication.llm import ChatLLM
from gtgh_team3_compliance_assistant.pipeline.rag_pipeline import RAGPipeline
from gtgh_team3_compliance_assistant.storing.Storage import ChromaVectorStore
from gtgh_team3_compliance_assistant.processing.chunk_storing import ChunkStore
from gtgh_team3_compliance_assistant.processing.text_storing import ExtractedTextStore
from gtgh_team3_compliance_assistant.config import (
    STORAGE_PERSIST_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)


class IngestionService:
    def __init__(self):
        embedding_model = LocalEmbedder(model_name=EMBEDDING_MODEL_NAME)
        vector_store = ChromaVectorStore(
            persist_path=str(STORAGE_PERSIST_PATH),
            collection_name=COLLECTION_NAME,
        )
        llm = ChatLLM()
        self.pipeline = RAGPipeline(
            pdf_path="",
            embedding_model=embedding_model,
            vector_store=vector_store,
            llm=llm,
        )
        self.chunk_store = ChunkStore()
        self.extracted_store = ExtractedTextStore()

    def process_local_pdf(self, pdf_path: str):
        pdf_path = Path(pdf_path)
        document_name = pdf_path.stem

        print(f"Extracting text: {document_name}")
        text = self.pipeline.extractor.extract(str(pdf_path))
        self.extracted_store.save(document_name, text)

        print(f"Chunking: {document_name}")
        raw_chunks = self.pipeline.chunker.chunk(text)
        self.chunk_store.save(document_name, raw_chunks)
        print(f"Saved {len(raw_chunks)} chunks to JSON")

        print(f"Ingesting into Chroma: {document_name}")
        self.pipeline.pdf_path = pdf_path
        self.pipeline.ingest()


if __name__ == "__main__":
    service = IngestionService()
    pdf_dir = Path("data/raw/eurlex")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        print("\n" + "=" * 50)
        try:
            service.process_local_pdf(str(pdf_file))
        except Exception as e:
            print(f"Failed: {pdf_file.name}: {e}")