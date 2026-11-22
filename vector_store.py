import chromadb
from config import CHROMA_DB_PATH, COLLECTION_NAME

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def store_chunks(self, chunks, embeddings, source):
        # 1. Retrieve existing chunk IDs for this document
        existing_records = self.collection.get(
            where={"source": source},
            include=["metadatas"]
        )

        existing_ids = set(existing_records["ids"])

        # 2. Generate IDs and metadata for new chunks
        ids = []
        metadatas = []

        for i in range(len(chunks)):
            ids.append(f"{source}_chunk_{i}")

            metadatas.append({
                "source": source,
                "chunk_number": i
            })

        if hasattr(embeddings, "tolist"):
            embeddings = embeddings.tolist()

        # 3. Insert new chunks or update existing chunks
        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        # 4. Identify old chunk IDs that are no longer required
        new_ids = set(ids)
        stale_ids = existing_ids - new_ids

        # 5. Delete outdated chunks
        if stale_ids:
            self.collection.delete(
                ids=list(stale_ids)
            )

        print(f"Successfully stored {len(chunks)} chunks!")

        if stale_ids:
            print(f"Removed {len(stale_ids)} outdated chunks.")

    def search(self, query_embedding, top_k):
        if self.collection.count() == 0:
            return {"documents": [[]], "metadatas": [[]],
                    "distances": [[]], "ids": [[]]}

        if hasattr(query_embedding, "tolist"):
            query_embedding = query_embedding.tolist()

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count())
        )

    def get_all_chunks(self):
        return self.collection.get(
            include=["documents", "metadatas"]
        )

    def count(self):
        return self.collection.count()
