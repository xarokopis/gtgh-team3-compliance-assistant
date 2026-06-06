from typing import Any

from pydantic import BaseModel, field_validator, computed_field
from sentence_transformers import SentenceTransformer
from gtgh_team3_compliance_assistant.config import EMBEDDING_MODEL_NAME
import numpy as np

class LocalEmbedder(BaseModel):
  model_name: str
  model: Any = None
  
  model_config = {"arbitrary_types_allowed": True}

  def model_post_init(self, __context: Any):
    self.model = SentenceTransformer(self.model_name)

  def embed(self, text: str) -> np.ndarray:
    return self.model.encode(text)

  def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
    return self.model.encode(texts)