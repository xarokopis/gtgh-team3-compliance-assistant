from pathlib import Path
import fitz

class TextExtractor:
    def extract(self, file_path: str) -> str:
        document = fitz.open(file_path)

        text_parts = []

        try:
            for page in document:
                text_parts.append(page.get_text("text"))

        finally:
            document.close()

        return "\n".join(text_parts)