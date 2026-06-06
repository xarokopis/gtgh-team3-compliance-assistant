import hashlib
from pathlib import Path
import httpx
from requests import get as get_req

from gtgh_team3_compliance_assistant.config import RAW_DIR, DATA_DIR_PDF

"""
Download a file from EUR-Lex using a CELEX number
and save it as a PDF. The function `download_eurlex_pdf_by_celex` takes a CELEX ID, an optional language code (default is "EN"), and an optional output directory (default is "eu_docs"). It constructs the appropriate URL, makes a GET request to download the PDF, checks the content type, and saves the file locally. The script includes error handling for HTTP requests and ensures that the output directory exists.
file: ex1.py
"""

class Downloader:
    def __init__(self, out_dir):
        self.base_dir = RAW_DIR
        self.out_dir = out_dir

    async def download(self, url: str, filename: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        file_path = self.base_dir / filename
        file_path.write_bytes(response.content)

        file_hash = hashlib.sha256(response.content).hexdigest()

        return file_path, file_hash

    def downloadFromEU(self, celex_id: str, language: str = "EN") -> None:
        Path(self.out_dir).mkdir(parents=True, exist_ok=True)

        url = f"https://eur-lex.europa.eu/legal-content/{language}/TXT/PDF/?uri=CELEX:{celex_id}"

        headers = {
            "User-Agent": "Python EUR-Lex downloader/1.0"
        }

        response = get_req(url, headers=headers, timeout=60)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "pdf" not in content_type.lower():
            print("Warning: response may not be a PDF:", content_type)

        file_path = Path(self.out_dir) / f"{celex_id}_{language}.pdf"
        file_path.write_bytes(response.content)
        return file_path;


# TODO: delete
if __name__ == "__main__":
    list_of_celexs = [
        "32016R0679",  # GDPR Regulation
        "32020R0861",  # ePrivacy Regulation
    ]
    
    downloader = Downloader(DATA_DIR_PDF)
    for celex in list_of_celexs:
        path = downloader.downloadFromEU(celex, language="EN")
        print(f"Downloaded: {path}")