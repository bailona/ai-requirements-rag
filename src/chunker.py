import re


def chunk_document(document):
    content = document["content"]
    source = document["source"]

    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)

    chunks = []

    for index, section in enumerate(sections, start=1):
        section = section.strip()

        if not section:
            continue

        heading_match = re.search(r"^## (.+)$", section, flags=re.MULTILINE)

        if heading_match:
            section_name = heading_match.group(1).strip()
        else:
            section_name = "General"

        chunks.append(
            {
                "chunk_id": f"{source}_{index}",
                "source": source,
                "section": section_name,
                "content": section,
            }
        )

    return chunks


if __name__ == "__main__":
    from document_loader import load_markdown_documents

    documents = load_markdown_documents("data/documents")

    for document in documents:
        chunks = chunk_document(document)

        print(f"Source: {document['source']}")
        print(f"Chunks generated: {len(chunks)}")

        for chunk in chunks:
            print(f"\n--- {chunk['chunk_id']} ---")
            print(f"Section: {chunk['section']}")
            print(chunk["content"][:300])
