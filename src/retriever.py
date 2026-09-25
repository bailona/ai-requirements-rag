import chromadb

from src.embeddings import generate_embeddings

CHROMA_PATH = "data/vector_store"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection("requirements")


def search_requirements(query, top_k=3):
    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":
    query = "How can a user reset their password?"

    results = search_requirements(query)

    print(f"Query: {query}")
    print("\nRetrieved chunks:")

    for index, document in enumerate(results["documents"][0], start=1):
        metadata = results["metadatas"][0][index - 1]

        print(f"\n--- Result {index} ---")
        print(f"Source: {metadata['source']}")
        print(f"Section: {metadata['section']}")
        print(document[:500])
