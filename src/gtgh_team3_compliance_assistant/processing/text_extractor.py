import fitz

class TextExtractor:
    def extract(self, file_path: str) -> str:

        doc = fitz.open(file_path)
        pages = []

        try:
            for page in doc:
                text = page.get_text("text")

                if text:
                    pages.append(text)
        finally:
            doc.close()

        full_text = "\n".join(pages)

        return full_text