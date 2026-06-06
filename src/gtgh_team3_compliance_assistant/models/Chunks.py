from pydantic import BaseModel, field_validator

class ChunkInput(BaseModel):
  chunk_id: int
  type: str
  article: str
  article_number: str
  recital_number: int
  title: str
  text: str
  source_file: str
  page: int
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