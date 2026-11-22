
class RAGPipeline:

    def __init__(self, retriever, llm_client):
        self.retriever = retriever
        self.llm_client = llm_client

    def generate_answer(self, question):

        # Step 1: Retrieve relevant document chunks
        results = self.retriever.retrieve_chunks(question)

        documents = results["documents"][0]

        # Step 2: Handle empty retrieval results
        if not documents:
            return "I don't know based on the available documents."

        # Step 3: Construct context from retrieved chunks
        context = "\n\n".join(documents)

        # Step 4: Construct the prompt
        prompt = f"""
        Document Context:
        {context}

        User Question:
        {question}

        Answer the user's question using only the document context.
        """
        # Step 5: Generate answer using Gemini
        answer = self.llm_client.generate_response(prompt)

        return answer
