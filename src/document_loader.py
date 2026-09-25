from pathlib import Path


def load_markdown_documents(directory):
    directory_path = Path(directory)

    documents = []

    for file_path in directory_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


if __name__ == "__main__":
    documents = load_markdown_documents("data/documents")

    print(f"Documents loaded: {len(documents)}")

    for document in documents:
        print(f"Source: {document['source']}")
        print(f"Characters: {len(document['content'])}")
