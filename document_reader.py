import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def read_document(document_path):
    path = Path(document_path)

    logger.info("Reading document: %s", path.name)

    try:
        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Not a valid file: {path}"
            )

        extension = path.suffix.lower()

        if extension == ".txt":
            document_text = read_text_file(path)

        elif extension == ".pdf":
            document_text = read_pdf_file(path)

        else:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                "Supported formats: .txt, .pdf"
            )

        if not document_text.strip():
            raise ValueError(
                f"No extractable text found in document: {path.name}"
            )

        logger.info(
            "Document read successfully: %s (%d characters)",
            path.name,
            len(document_text)
        )

        return document_text

    except (FileNotFoundError, ValueError):
        logger.warning(
            "Unable to read document: %s",
            path.name
        )
        raise

    except Exception:
        logger.exception(
            "Unexpected error while reading document: %s",
            path.name
        )
        raise


def read_text_file(path):
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def read_pdf_file(path):
    logger.info("Extracting text from PDF: %s", path.name)

    reader = PdfReader(path)

    if reader.is_encrypted:
        raise ValueError(
            f"PDF is password-protected: {path.name}"
        )

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append(
                f"\n--- Page {page_number} ---\n{page_text}"
            )

    logger.info(
        "PDF extraction completed: %s | Total pages: %d | "
        "Pages containing text: %d",
        path.name,
        len(reader.pages),
        len(pages)
    )

    return "\n".join(pages)