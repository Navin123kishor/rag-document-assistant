import logging
from logging_config import configure_logging

from config import (
    MIN_QUESTION_LENGTH,
    MAX_QUESTION_LENGTH
)

from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from LLM_Client import LLMClient

from ingestion_pipeline import IngestionPipeline
from retriever import Retriever
from rag_pipeline import RAGPipeline
from general_chat import GeneralChat


# Configure logging before initializing application components
configure_logging()

logger = logging.getLogger(__name__)


def initialize_application():
    logger.info("Initializing RAG application.")

    embedding_generator = EmbeddingGenerator()
    vector_store = VectorStore()
    llm_client = LLMClient()

    ingestion_pipeline = IngestionPipeline(
        embedding_generator,
        vector_store
    )

    retriever = Retriever(
        embedding_generator,
        vector_store
    )

    rag_pipeline = RAGPipeline(
        retriever,
        llm_client
    )

    general_chat = GeneralChat(llm_client)

    logger.info("RAG application initialized successfully.")

    return (
        ingestion_pipeline,
        rag_pipeline,
        vector_store,
        general_chat
    )


def ingest_document(ingestion_pipeline):
    document_path = input("Enter document path: ").strip()

    if not document_path:
        print("Please provide a document path.")
        logger.warning("Document ingestion cancelled: empty file path.")
        return

    try:
        logger.info("Document ingestion requested.")
        ingestion_pipeline.ingest_document(document_path)

        logger.info("Document ingestion completed successfully.")

    except (FileNotFoundError, ValueError) as e:
        logger.warning("Document ingestion failed: %s", e)
        print(f"Ingestion error: {e}")

    except Exception:
        logger.exception("Unexpected error during document ingestion.")
        print("An unexpected error occurred during ingestion. Check logs for details.")

    print()


def chat_with_documents(rag_pipeline, vector_store):
    if vector_store.count() == 0:
        print("No documents available. Please ingest a document first.\n")
        logger.warning("Document chat requested, but no documents are available.")
        return

    logger.info("Document chat session started.")
    print("\nDocument Chat started! Type 'exit' to return to the menu.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            logger.info("Document chat session ended.")
            print("Returning to main menu.\n")
            break

        if len(question) < MIN_QUESTION_LENGTH:
            print("Please enter a meaningful question.\n")
            logger.warning("Document chat received an input below minimum length.")
            continue

        if len(question) > MAX_QUESTION_LENGTH:
            print(
                f"Question too long! Maximum allowed length is "
                f"{MAX_QUESTION_LENGTH} characters.\n"
            )
            logger.warning("Document chat received an input above maximum length.")
            continue

        try:
            answer = rag_pipeline.generate_answer(question)
            print(f"\nAssistant: {answer}\n")

        except RuntimeError as e:
            logger.error("Document chat generation failed: %s", e)
            print("Unable to generate a response right now. Please try again.\n")

        except Exception:
            logger.exception("Unexpected error during document chat.")
            print("An unexpected error occurred. Check logs for details.\n")


def chat_generally(general_chat):
    logger.info("General chat session started.")
    print("\nGeneral Chat started! Type 'exit' to return to the menu.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            logger.info("General chat session ended.")
            print("Returning to main menu.\n")
            break

        if len(question) < MIN_QUESTION_LENGTH:
            print("Please enter a meaningful question.\n")
            logger.warning("General chat received an input below minimum length.")
            continue

        if len(question) > MAX_QUESTION_LENGTH:
            print(
                f"Question too long! Maximum allowed length is "
                f"{MAX_QUESTION_LENGTH} characters.\n"
            )
            logger.warning("General chat received an input above maximum length.")
            continue

        try:
            answer = general_chat.generate_response(question)
            print(f"\nAssistant: {answer}\n")

        except RuntimeError as e:
            logger.error("General chat generation failed: %s", e)
            print("Unable to generate a response right now. Please try again.\n")

        except Exception:
            logger.exception("Unexpected error during general chat.")
            print("An unexpected error occurred. Check logs for details.\n")


def main():
    logger.info("========== Application startup ==========")

    try:
        (
            ingestion_pipeline,
            rag_pipeline,
            vector_store,
            general_chat
        ) = initialize_application()

    except Exception:
        logger.exception("Application initialization failed.")
        print("Application initialization failed. Check logs for details.")
        return

    try:
        while True:
            print("========== RAG Document Assistant ==========")
            print("1. Ingest a document")
            print("2. Chat with documents")
            print("3. General Chat")
            print("4. Exit")

            choice = input("\nChoose an option: ").strip().lower()

            if choice in ["1", "ingest", "ingest document"]:
                logger.info("Menu option selected: Document ingestion.")
                ingest_document(ingestion_pipeline)

            elif choice in [
                "2",
                "document chat",
                "chat with documents"
            ]:
                logger.info("Menu option selected: Document chat.")
                chat_with_documents(rag_pipeline, vector_store)

            elif choice in [
                "3",
                "general chat",
                "chat generally"
            ]:
                logger.info("Menu option selected: General chat.")
                chat_generally(general_chat)

            elif choice in ["4", "exit", "quit", "bye"]:
                logger.info("Application exit requested.")
                print("Goodbye!")
                break

            else:
                logger.warning("Invalid menu selection received.")
                print(
                    "Invalid choice. Please enter a menu number "
                    "or a valid command.\n"
                )

    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
        print("\nApplication interrupted. Goodbye!")

    except Exception:
        logger.exception("Unexpected application-level error.")
        print("\nAn unexpected error occurred. Check logs for details.")

    finally:
        logger.info("========== Application shutdown ==========")


if __name__ == "__main__":
    main()
