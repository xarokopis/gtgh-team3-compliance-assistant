from pathlib import Path
from gtgh_team3_compliance_assistant.processing.text_extractor import TextExtractor
from gtgh_team3_compliance_assistant.processing.eur_chunker import EurChunker
from gtgh_team3_compliance_assistant.models.Chunks import (ChunkInput, AddChunksInput)
from gtgh_team3_compliance_assistant.models.Search import SearchInput


class RAGPipeline:

    def __init__(
        self,
        pdf_path,
        embedding_model,
        vector_store,
        llm=None,
    ):
        self.pdf_path = Path(pdf_path) if pdf_path else None

        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.llm = llm

        self.extractor = TextExtractor()
        self.chunker = EurChunker()

    def ingest(self):

        if self.pdf_path is None:
            raise ValueError(
                "pdf_path is not set"
            )

        print(
            f"\nReading: {self.pdf_path.name}"
        )

        text = self.extractor.extract(
            str(self.pdf_path)
        )

        print(
            f"Extracted {len(text)} characters"
        )

        raw_chunks = self.chunker.chunk(
            text
        )

        print(
            f"Created {len(raw_chunks)} chunks"
        )

        chunk_models = []

        for idx, chunk in enumerate(
            raw_chunks
        ):

            try:

                model = ChunkInput(
                    chunk_id=idx,
                    type=chunk.get("type"),
                    article=chunk.get("article"),
                    article_number=chunk.get(
                        "article_number"
                    ),
                    recital_number=chunk.get(
                        "recital_number"
                    ),
                    title=chunk.get("title"),
                    text=chunk["text"],
                    source_file=self.pdf_path.name,
                    page=0,
                    char_length=len(
                        chunk["text"]
                    ),
                )

                chunk_models.append(
                    model
                )

            except Exception as e:

                print(
                    f"\nChunk failed: {idx}"
                )

                print(chunk)

                raise e

        print(
            f"ChunkInput models created: "
            f"{len(chunk_models)}"
        )

        print(
            "\nFirst chunk:"
        )

        print(
            chunk_models[0].model_dump()
        )

        print(
            "\nCreating embeddings..."
        )

        embeddings = (
            self.embedding_model
            .embed_documents(
                [
                    chunk.text
                    for chunk
                    in chunk_models
                ]
            )
        )

        print(
            f"Embeddings created: "
            f"{len(embeddings)}"
        )

        print(
            "\nCreating AddChunksInput..."
        )

        add_input = AddChunksInput(
            chunks=chunk_models,
            embeddings=embeddings,
        )

        print(
            "AddChunksInput created"
        )

        print(
            "\nSaving to Chroma..."
        )

        self.vector_store.add_chunks(
            add_input
        )

        print(
            "Saved to Chroma"
        )

        print(
            "Collection count:",
            self.vector_store.collection.count()
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        query_embedding = (
            self.embedding_model
            .embed_query(question)
        )

        return self.vector_store.search(
            SearchInput(
                query_embedding=query_embedding,
                top_k=top_k,
            )
        )

    def build_context(
        self,
        results,
    ):

        return "\n\n---\n\n".join(
            [
                result.content
                for result in results
            ]
        )

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ):

        if self.llm is None:
            raise ValueError(
                "No LLM configured"
            )

        results = self.retrieve(question,top_k)

        context = self.build_context(results)

        answer = self.llm.generate(question=question, context=context)

        return {
            "question": question,
            "answer": answer,
            "retrieved_chunks": [
                r.model_dump()
                for r in results
            ],
        }