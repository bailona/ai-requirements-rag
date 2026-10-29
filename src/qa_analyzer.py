
from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.retriever import search_requirements


def analyze_requirement(query, top_k=3):
    """Generate traceable QA test scenarios from requirements retrieved by RAG."""

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
            f"Original requirement:\n{document}"
        )

        sources.append({
            "source": source,
            "section": section,
        })

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a senior QA engineer analyzing software requirements.

Use only the original requirements provided below.
Do not invent business rules or claim that proposed behavior is explicit.

Create traceability IDs for this analysis. These are project-generated
IDs, not official IDs from the source document.

Use:
- LG-01, LG-02... for login requirements.
- PR-01, PR-02... for password reset requirements.
- SEC-01, SEC-02... for security requirements.

TRACEABILITY RULES:
- Assign a stable ID to each distinct requirement.
- Keep each ID consistent throughout the report.
- Preserve the meaning of the original requirement.
- Link each test case to the requirement it actually verifies.
- Do not assign an ID based only on the order in which a requirement
  appears in a retrieved chunk.
- If a test cannot be linked confidently, use "Needs clarification".
- Mark inferred behavior as "Proposed interpretation".

Generate these sections:
1. Requirement traceability table
2. Positive test scenarios
3. Negative test scenarios
4. Edge cases
5. Test data
6. Gherkin scenarios using Given, When, and Then
7. Missing information requiring clarification

For every test case, include:
- Test Case ID (TC-01, TC-02, etc.)
- Requirement ID
- Scenario description
- Preconditions
- Test data
- Execution steps
- Expected result
- Priority (High, Medium, or Low)
- Test type (Positive, Negative, or Edge Case)
- Expected result classification: Explicit requirement or Proposed interpretation

REQUIREMENT GUIDANCE:
- A registered email is required for password reset.
- An invalid email address must be rejected.
- The email field is mandatory.
- A reset link must be sent to the registered email.
- The reset link must allow the user to define a new password.
- The reset link must expire after a defined period.
- Passwords must never be stored in plain text.
- Authentication failures should not expose sensitive information.
- Password reset tokens must be securely generated.

These statements summarize the source requirements. They do not authorize
you to invent additional business rules.

LIMITATIONS:
- Do not invent an exact token expiration duration.
- Do not invent password complexity rules or specific error messages.
- Do not assume single-use tokens or automatic login after reset.
- Do not present inferred expired-link behavior as an explicit requirement.
- Identify security requirements that lack measurable acceptance criteria.
- Do not claim that tests have actually been executed.
- Use practical language suitable for a QA team.

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
