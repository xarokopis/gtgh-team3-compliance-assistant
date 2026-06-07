from pydantic import BaseModel, field_validator
from typing import Optional

class ChunkInput(BaseModel):
  chunk_id: int
  type: Optional[str] = None
  article: Optional[str] = None
  article_number: Optional[str] = None
  recital_number: Optional[int] = None
  title: Optional[str] = None
  text: str
  source_file: str
  page: int = 0
  char_length: int

class AddChunksInput(BaseModel):
  chunks: list[ChunkInput]
  embeddings: list[list[float]]

  @field_validator("embeddings")
  @classmethod
  def embeddings_match_chunks(cls, v, info):
    chunks = info.data.get("chunks", [])
    if(len(v) != len(chunks)):
      raise ValueError(f"Embeddings length ({len(v)}) must match chunks length ({len(chunks)})")
    return v