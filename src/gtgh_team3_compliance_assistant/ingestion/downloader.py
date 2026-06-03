import hashlib
from pathlib import Path
import httpx

from gtgh_team3_compliance_assistant.config import RAW_DIR


class Downloader:
    def __init__(self):
        self.base_dir = RAW_DIR

    async def download(self, url: str, filename: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        file_path = self.base_dir / filename
        file_path.write_bytes(response.content)

        file_hash = hashlib.sha256(response.content).hexdigest()

        return file_path, file_hash