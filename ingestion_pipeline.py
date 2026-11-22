import logging
from pathlib import Path

from document_reader import read_document
from text_chunker import chunk_text

logger = logging.getLogger(__name__)


class IngestionPipeline:

    def __init__(self, embedding_generator, vector_store):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def ingest_document(self, document_path):
        path = Path(document_path)

        logger.info(
            "Starting document ingestion: %s",
            path.name
        )

        try:
            # Step 1: Read document
            document_text = read_document(path)

            logger.info(
                "Document reading completed: %s",
                path.name
            )

            # Step 2: Generate chunks
            chunks = chunk_text(document_text)

            if not chunks:
                raise ValueError(
                    "No chunks generated from document."
                )

            logger.info(
                "Chunking completed: %s | Total chunks: %d",
                path.name,
                len(chunks)
            )

            # Step 3: Generate embeddings
            embeddings = self.embedding_generator.generate_embeddings(
                chunks
            )

            logger.info(
                "Embedding generation completed: %s",
                path.name
            )

            # Step 4: Store chunks and embeddings
            self.vector_store.store_chunks(
                chunks=chunks,
                embeddings=embeddings,
                source=path.stem
            )

            logger.info(
                "Document ingestion completed successfully: %s",
                path.name
            )

            print(f"\nDocument ingestion completed: {path.name}")
            print(f"Total chunks generated: {len(chunks)}")

            return len(chunks)

        except Exception:
            logger.exception(
                "Document ingestion failed: %s",
                path.name
            )
            raise
