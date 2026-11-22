
# RAG-Based Document Assistant

A Python-based Retrieval-Augmented Generation (RAG) application that allows users to ingest PDF and TXT documents and ask questions about their content using Google's Gemini API.


## Features

- **Document Ingestion:** Read and process PDF and TXT documents.
- **Text Chunking:** Split documents into smaller chunks for efficient retrieval.
- **Local Embeddings:** Generate semantic embeddings using Sentence Transformers (`all-MiniLM-L6-v2`).
- **Vector Storage:** Store document chunks and embeddings persistently using ChromaDB.
- **Semantic Search:** Retrieve relevant document chunks based on user questions.
- **RAG-Based Responses:** Generate context-aware answers using the Gemini API.
- **General Chat:** Ask questions without requiring document ingestion.
- **Logging and Error Handling:** Maintain application logs with rotating file storage and handle common application/API errors.

## Architecture

```text
                User
                 |
                 v
          Application (CLI)
                 |
          +------+------+
          |             |
          v             v
    Document Chat   General Chat
          |             |
          v             v
      Retriever      Gemini API
          |
          v
    Query Embedding
          |
          v
       ChromaDB
          |
          v
   Relevant Chunks
          |
          v
      RAG Pipeline
          |
          v
      Gemini API
          |
          v
       Response


Document Ingestion:

PDF / TXT Document
        |
        v
  Document Reader
        |
        v
   Text Chunker
        |
        v
 Embedding Generator
        |
        v
     ChromaDB
```

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Framework | Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Processing | pypdf |
| Configuration | python-dotenv |
| Logging | Python logging |

## Project Structure

```text
rag-document-assistant/
│
├── documents/
│   ├── aurora.txt
│   └── distributed_systems_intro.pdf
│
├── config.py
├── document_reader.py
├── text_chunker.py
├── embedding_generator.py
├── vector_store.py
├── ingestion_pipeline.py
├── retriever.py
├── rag_pipeline.py
├── general_chat.py
├── LLM_Client.py
├── logging_config.py
├── rag_application_main.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd rag-document-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Gemini API Key

Create a `.env` file in the project root directory:

```dotenv
GEMINI_API_KEY=your_actual_api_key
```

Get your API key from Google AI Studio:

https://aistudio.google.com/apikey


### 5. Run the application

```bash
python rag_application_main.py
```

## Usage

The application provides the following options:

1. **Ingest a document:** Provide the path to a PDF or TXT file.
2. **Chat with documents:** Ask questions based on the ingested documents.
3. **General Chat:** Ask questions using Gemini without document retrieval.
4. **Exit:** Close the application.

Example document path:

```text
documents/distributed_systems_intro.pdf
```

## Current Limitations

- Scanned PDFs requiring OCR are not supported.
- Conversation history is not maintained between questions.
- Document responses use retrieved context and do not yet provide page-level source citations.
- The current application uses a command-line interface.
