import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# -------------------------
# Gemini Configuration
# -------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Configure it in your .env file."
    )

GEMINI_MODEL_NAME = "gemini-3.8-flash"

MAX_RESPONSE_TOKENS = 500
RESPONSE_TEMPERATURE = 0.5


# -------------------------
# User Input Configuration
# -------------------------

MAX_QUESTION_LENGTH = 1000
MIN_QUESTION_LENGTH = 3


# -------------------------
# Document Chunking
# -------------------------

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# -------------------------
# Vector Database
# -------------------------

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "aurora_documents"


# -------------------------
# Retrieval Configuration
# -------------------------

TOP_K_RESULTS = 2


# -------------------------
# RAG System Instruction
# -------------------------

SYSTEM_INSTRUCTION = """
You are a helpful document-based assistant.

Response guidelines:
1. Answer using only the provided document context.
2. Do not invent or assume information.
3. If the context does not contain the answer,
   clearly say that you don't know based on the available documents.
4. Keep responses concise, clear, and natural.
5. Answer the actual question directly.
6. Use simple, human-like language.
7. Use bullet points when they improve readability.
"""


GENERAL_CHAT_SYSTEM_INSTRUCTION = """
You are a helpful, knowledgeable, and conversational AI assistant.

Response guidelines:
1. Answer the user's questions using your general knowledge.
2. Do not invent facts or present uncertain information as certain.
3. If you don't know something, clearly acknowledge it.
4. Keep responses clear, concise, and natural.
5. Answer the actual question directly.
6. Use simple, human-like language.
7. Use bullet points when they improve readability.
"""
