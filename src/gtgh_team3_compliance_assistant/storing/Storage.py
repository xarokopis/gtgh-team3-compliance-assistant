import chromadb
from chromadb.config import Settings
from pydantic import BaseModel

from gtgh_team3_compliance_assistant.models.Chunks import AddChunksInput
from gtgh_team3_compliance_assistant.models.Search import SearchInput, SearchResult

class ChromaVectorStore(BaseModel):
    persist_path: str
    collection_name: str

    # Set after init
    client: chromadb.ClientAPI = None
    collection: chromadb.Collection = None

    model_config = { "arbitrary_types_allowed": True }

    def model_post_init(self, __context):
        self.client = chromadb.PersistentClient(
            path=str(self.persist_path),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = (self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"})
        )

    def add_chunks(self, input: AddChunksInput) -> None:
        ids = [f"{chunk.source_file}_{chunk.chunk_id}" for chunk in input.chunks]
        documents = [chunk.text for chunk in input.chunks]

        metadatas = [
            { 
                "source_file": chunk.source_file, 
                "page_number": chunk.page, 
                "chunk_index": chunk.chunk_id,
                "type": chunk.type,
                "article": chunk.article,
                "article_number": chunk.article_number,
                "title": chunk.title,
            } 
            for chunk in input.chunks 
        ]
        
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=input.embeddings,
            metadatas=metadatas
        )

    def search(self, input: SearchInput) -> list[SearchResult]:
        results = self.collection.query(
            query_embeddings=[input.query_embedding],
            n_results=input.top_k,
        )

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        return [
            SearchResult(
                chunk_id=i,
                content=documents[i],
                metadata=metadatas[i],
                distance=distances[i],
            ) for i in range(len(ids))
        ]