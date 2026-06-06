from pypdf import PdfReader

class TextExtractor:
    def extract(self, file_path: str) -> str:
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)