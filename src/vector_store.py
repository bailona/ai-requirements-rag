import chromadb

from src.chunker import chunk_document
from src.document_loader import load_markdown_documents
from src.embeddings import generate_embeddings

CHROMA_PATH = "data/vector_store"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="requirements")


def index_documents():
    documents = load_markdown_documents("data/documents")

    all_chunks = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

    ids = [chunk["chunk_id"] for chunk in all_chunks]

    existing = collection.get(ids=ids)

    existing_ids = set(existing["ids"])

    chunks_to_index = [
        chunk for chunk in all_chunks
        if chunk["chunk_id"] not in existing_ids
    ]

    if not chunks_to_index:
        print("No new chunks to index.")
        return 0

    texts = [chunk["content"] for chunk in chunks_to_index]

    embeddings = generate_embeddings(texts)

    new_ids = [chunk["chunk_id"] for chunk in chunks_to_index]

    metadatas = [
        {
            "source": chunk["source"],
            "section": chunk["section"],
        }
        for chunk in chunks_to_index
    ]

    collection.upsert(
        ids=new_ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks_to_index)


if __name__ == "__main__":
    total = index_documents()

    print(f"New chunks indexed: {total}")
    print(f"Collection: {collection.name}")
    print(f"Stored documents: {collection.count()}")
