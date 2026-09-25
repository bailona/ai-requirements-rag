from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.retriever import search_requirements

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query, top_k=3):
    results = search_requirements(query, top_k=top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        context_parts.append(
            f"Source: {metadata['source']}\n"
            f"Section: {metadata['section']}\n"
            f"Content:\n{document}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a software requirements assistant specialized in software quality assurance.

Answer the user's question using ONLY the requirements retrieved from the document.

Rules:
- Do not invent requirements or business rules.
- Do not assume information that is not present in the context.
- If the requirements do not provide enough information, explicitly say so.
- Keep the answer clear and concise.
- When useful, mention the requirement section used to support the answer.

Retrieved requirements:

{context}

User question:

{query}
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt,
    )

    return {
        "question": query,
        "answer": response.output_text,
        "sources": [
            {
                "source": metadata["source"],
                "section": metadata["section"],
            }
            for metadata in metadatas
        ],
    }


if __name__ == "__main__":
    query = "How can a user reset their password?"

    result = generate_answer(query)

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['source']} | {source['section']}")
