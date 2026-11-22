from config import TOP_K_RESULTS

class Retriever:

    def __init__(self, embedding_generator, vector_store):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def retrieve_chunks(self, question, top_k=TOP_K_RESULTS):

        # Step 1: Generate embedding for the user's question
        question_embedding = (
            self.embedding_generator.generate_embeddings(question)
        )

        # Step 2: Search ChromaDB for relevant chunks
        results = self.vector_store.search(
            query_embedding=question_embedding,
            top_k=top_k
        )

        return results
