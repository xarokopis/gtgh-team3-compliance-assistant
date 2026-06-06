from gtgh_team3_compliance_assistant.config import EXTRACTED_DIR

class ExtractedTextStore:

    def save(self, document_name: str, text: str):
        file_path = EXTRACTED_DIR / f"{document_name}.txt"

        print(f"Saving extracted text to: {file_path}")

        file_path.write_text(
            text,
            encoding="utf-8",
        )

        return file_path