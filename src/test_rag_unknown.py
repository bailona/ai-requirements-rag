from src.rag_pipeline import generate_answer

query = "What is the exact expiration time of the password reset link?"

result = generate_answer(query)

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"- {source['source']} | {source['section']}")
