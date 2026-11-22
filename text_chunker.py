import re

def chunk_text(text, chunk_size=500, overlap=100):

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # If this is not the final chunk, find a natural boundary
        if end < len(text):

            search_text = text[start:end]

            # Prefer paragraph boundary
            boundary = search_text.rfind("\n\n")

            # Otherwise, prefer sentence boundary
            if boundary == -1:
                sentence_matches = list(
                    re.finditer(r"[.!?]\s+", search_text)
                )

                if sentence_matches:
                    boundary = sentence_matches[-1].end()

            # Otherwise, use word boundary
            if boundary == -1:
                boundary = search_text.rfind(" ")

            if boundary > 0:
                end = start + boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Move forward while maintaining overlap
        if end >= len(text):
            break

        next_start = max(start + 1, end - overlap)

        # Avoid starting in the middle of a word
        while next_start < end and text[next_start].isalnum():
            next_start += 1

        start = next_start

    return chunks
