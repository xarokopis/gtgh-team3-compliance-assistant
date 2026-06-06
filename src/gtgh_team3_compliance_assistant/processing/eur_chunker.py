import re


class EurChunker:
    ARTICLE_PATTERN = r"(?m)^\s*Article\s+(\d+[A-Za-z]?)\s*$"

    def chunk(self, text: str):
        text = self._clean_text(text)

        if not text:
            return []

        article_chunks = self._chunk_articles(text, overlap=50)

        if article_chunks:
            return article_chunks

        return self._fallback_chunk(text)

    def _clean_text(self, text: str):
        text = text.replace("\u00ad", "")  # soft hyphen
        text = text.replace("￾", "")       # weird PDF extraction character
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _normalize_chunk_text(self, text: str):
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _chunk_articles(self, text: str, overlap: int = 50):
        article_matches = list(
            re.finditer(
                self.ARTICLE_PATTERN,
                text,
                flags=re.IGNORECASE,
            )
        )

        if not article_matches:
            return []

        chunks = []

        for i, match in enumerate(article_matches):
            original_start = match.start()

            if i + 1 < len(article_matches):
                original_end = article_matches[i + 1].start()
            else:
                original_end = len(text)

            # Article 1 has no previous article.
            # Every other article starts 50 characters before its heading.
            if i == 0:
                chunk_start = original_start
            else:
                chunk_start = max(0, original_start - overlap)

            article_number = match.group(1)

            # Use the clean article only for title detection.
            # Do NOT use the overlapped text for title detection.
            article_without_overlap = text[original_start:original_end].strip()
            title = self._get_article_title(article_without_overlap)

            # Use overlapped text for the actual chunk.
            chunk_text = text[chunk_start:original_end].strip()
            chunk_text = self._normalize_chunk_text(chunk_text)

            chunks.append(
                {
                    "type": "article",
                    "article": f"Article {article_number}",
                    "article_number": article_number,
                    "recital_number": None,
                    "title": title,
                    "text": chunk_text,
                }
            )

        return chunks

    def _get_article_title(self, article_text: str):
        lines = [line.strip() for line in article_text.splitlines() if line.strip()]

        if len(lines) < 2:
            return None

        title = lines[1]

        if re.match(r"^\d+\.", title):
            return None

        if len(title) > 150:
            return None

        return title

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
            chunk_text = text[start:end].strip()
            chunk_text = self._normalize_chunk_text(chunk_text)

            if chunk_text:
                chunks.append(
                    {
                        "type": "fallback",
                        "article": None,
                        "article_number": None,
                        "recital_number": None,
                        "title": None,
                        "text": chunk_text,
                    }
                )

            start = end - overlap

        return chunks