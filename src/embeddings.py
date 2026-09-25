from openai import OpenAI

from src.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )

    return [item.embedding for item in response.data]


if __name__ == "__main__":
    texts = [
        "The user must provide a registered email address.",
        "The system must allow password reset using email.",
    ]

    embeddings = generate_embeddings(texts)

    print(f"Embeddings generated: {len(embeddings)}")
    print(f"Vector dimensions: {len(embeddings[0])}")
