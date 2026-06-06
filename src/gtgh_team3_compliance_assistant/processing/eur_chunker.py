import re


class EurChunker:
    BODY_START_PATTERN = (
        r"\b(?:HAS|HAVE)\s+ADOPTED\s+THIS\s+"
        r"(?:REGULATION|DIRECTIVE|DECISION)\s*:"
    )

    WHEREAS_PATTERN = r"\bWhereas\s*:"

    RECITAL_PATTERN = r"(?m)^\s*\((\d+)\)\s+"

    ARTICLE_PATTERN = r"(?m)^\s*Article\s+(\d+[A-Za-z]?)\s*$"

    def chunk(self, text: str):
        text = text.strip()

        if not text:
            return []

        preamble_text, body_text = self._split_body(text)

        chunks = []

        if preamble_text:
            chunks.extend(self._chunk_recitals(preamble_text))

        article_chunks = self._chunk_articles(body_text)

        if article_chunks:
            chunks.extend(article_chunks)
            return chunks

        return self._fallback_chunk(text)

    def _split_body(self, text: str):
        match = re.search(
            self.BODY_START_PATTERN,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return "", text

        preamble_text = text[: match.start()].strip()
        body_text = text[match.end() :].strip()

        return preamble_text, body_text

    def _chunk_recitals(self, preamble_text: str):
        whereas_match = re.search(
            self.WHEREAS_PATTERN,
            preamble_text,
            flags=re.IGNORECASE,
        )

        if not whereas_match:
            return [
                {
                    "type": "document_intro",
                    "article": None,
                    "article_number": None,
                    "recital_number": None,
                    "title": None,
                    "text": preamble_text,
                }
            ]

        intro_text = preamble_text[: whereas_match.start()].strip()
        recitals_text = preamble_text[whereas_match.end() :].strip()

        chunks = []

        if intro_text:
            chunks.append(
                {
                    "type": "document_intro",
                    "article": None,
                    "article_number": None,
                    "recital_number": None,
                    "title": None,
                    "text": intro_text,
                }
            )

        recital_matches = self._find_recital_matches(recitals_text)

        for i, match in enumerate(recital_matches):
            start = match.start()

            if i + 1 < len(recital_matches):
                end = recital_matches[i + 1].start()
            else:
                end = len(recitals_text)

            recital_number = match.group(1)
            recital_text = recitals_text[start:end].strip()

            chunks.append(
                {
                    "type": "recital",
                    "article": None,
                    "article_number": None,
                    "recital_number": recital_number,
                    "title": None,
                    "text": recital_text,
                }
            )

        return chunks

    def _find_recital_matches(self, recitals_text: str):
        all_matches = list(re.finditer(self.RECITAL_PATTERN, recitals_text))

        recital_matches = []
        expected_number = 1

        for match in all_matches:
            number = int(match.group(1))

            if number == expected_number:
                recital_matches.append(match)
                expected_number += 1

        return recital_matches

    def _chunk_articles(self, body_text: str):
        matches = list(
            re.finditer(
                self.ARTICLE_PATTERN,
                body_text,
                flags=re.IGNORECASE,
            )
        )

        if not matches:
            return []

        chunks = []

        for i, match in enumerate(matches):
            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(body_text)

            article_number = match.group(1)
            article_text = body_text[start:end].strip()
            title = self._get_article_title(article_text)

            chunks.append(
                {
                    "type": "article",
                    "article": f"Article {article_number}",
                    "article_number": article_number,
                    "recital_number": None,
                    "title": title,
                    "text": article_text,
                }
            )

        return chunks

    def _get_article_title(self, article_text: str):
        lines = [line.strip() for line in article_text.splitlines() if line.strip()]

        if len(lines) < 2:
            return None

        title = lines[1]

        if title.startswith(("1.", "2.", "3.", "4.", "5.")):
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