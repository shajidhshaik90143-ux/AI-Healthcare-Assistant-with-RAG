def split_text(
    text,
    chunk_size=1000,
    chunk_overlap=150
):

    text = text.replace(
        "\x00",
        " "
    )

    text = " ".join(
        text.split()
    )

    if len(text) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def split_documents(documents):

    chunks = []

    for document in documents:

        text_chunks = split_text(
            document["text"]
        )

        for index, chunk in enumerate(text_chunks):

            chunks.append({
                "text": chunk,
                "page": document["page"],
                "file": document["file"],
                "chunk_id": index
            })

    return chunks