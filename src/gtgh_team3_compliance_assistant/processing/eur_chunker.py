import re

class EurChunker:
    ARTICLE_PATTERN = r"(Article\s+\d+[A-Za-z]?)"

    def chunk(self, text: str):
        matches = list(re.finditer(self.ARTICLE_PATTERN, text))

        if not matches:
            return self._fallback_chunk(text)

        chunks = []

        for i, match in enumerate(matches):
            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            article_text = text[start:end].strip()

            chunks.append(
                {
                    "article": match.group(),
                    "text": article_text,
                }
            )

        return chunks

    def _fallback_chunk(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 150,
    ):
        chunks = []

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunks.append(
                {
                    "article": None,
                    "text": text[start:end],
                }
            )

            start = end - overlap

        return chunks