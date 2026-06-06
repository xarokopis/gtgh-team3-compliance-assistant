from pathlib import Path
from uuid import uuid4

from src.gtgh_team3_compliance_assistant.processing.text_extractor2 import TextExtractor
from src.gtgh_team3_compliance_assistant.processing.eur_chunker import EurChunker
from src.gtgh_team3_compliance_assistant.processing.chunk_storing import ChunkStore
from src.gtgh_team3_compliance_assistant.processing.text_storing import ExtractedTextStore

class IngestionService:
    def __init__(self):
        self.extractor = TextExtractor()
        self.chunker = EurChunker()
        self.chunk_store = ChunkStore()
        self.extracted_store = ExtractedTextStore()

    def process_local_pdf(self, pdf_path: str):

        pdf_path = Path(pdf_path)

        document_name = pdf_path.stem

        print(f"Processing: {document_name}")

        text = self.extractor.extract(str(pdf_path))
        #print(f"Text length: {len(text)}")

        print(f"Extracted {len(text)} characters")

        extracted_path = self.extracted_store.save(
            document_name,
            text,
        )

        print(f"Saved extracted text: {extracted_path}")
        print("here?")
        chunks = self.chunker.chunk(text)

        print(f"Created {len(chunks)} chunks")

        self.chunk_store.save(
            document_name,
            chunks,
        )

        print(
            f"Saved chunks: {document_name}.json"
        )

        return {
            "document_name": document_name,
            "extracted_file": str(extracted_path),
            "chunk_count": len(chunks),
        }

if __name__ == "__main__":

    service = IngestionService()
    pdf_dir = Path("data/raw/eurlex")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        print("\n" + "=" * 50)

        try:
            result = service.process_local_pdf(
                str(pdf_file)
            )
            print(result)

        except Exception as e:
            print(
                f"Failed to process {pdf_file.name}: {e}"
            )