
from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.retriever import search_requirements


def analyze_requirement(query, top_k=3):
    """Generate QA test scenarios from requirements retrieved by RAG."""

    results = search_requirements(query, top_k=top_k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "question": query,
            "analysis": "No relevant requirements were found.",
            "sources": [],
        }

    context_parts = []
    sources = []

    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "Unknown source")
        section = metadata.get("section", "Unknown section")

        context_parts.append(
            f"Source: {source}\n"
            f"Section: {section}\n"
            f"Requirement:\n{document}"
        )

        sources.append({
            "source": source,
            "section": section,
        })

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a senior QA engineer analyzing software requirements.

Use only the original requirements provided below.
Do not invent business rules or expected behavior.

Clearly identify information that is missing and requires clarification.

Generate a structured QA analysis containing:
1. Positive test scenarios
2. Negative test scenarios
3. Edge cases
4. Test data
5. Expected results
6. Priority (High, Medium, or Low)
7. Gherkin scenarios using Given, When, and Then
8. Missing information requiring clarification

Every expected result must be supported by the supplied requirements.
Distinguish explicit requirements from proposed tests or assumptions.

Question:
{query}

Original retrieved requirements:
{context}
"""

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt,
    )

    return {
        "question": query,
        "analysis": response.output_text,
        "sources": sources,
    }


if __name__ == "__main__":
    query = "Generate test scenarios for the password reset requirements."
    result = analyze_requirement(query)

    print("\nQUESTION:")
    print(result["question"])

    print("\nQA ANALYSIS:")
    print(result["analysis"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print(f'- {source["source"]} | {source["section"]}')
