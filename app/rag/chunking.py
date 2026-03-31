def split_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    text = text.strip()
    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start += max_chars - overlap

    return chunks
