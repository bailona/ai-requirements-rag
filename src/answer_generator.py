from openai import OpenAI

from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query, retrieved_documents):
    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are a software requirements assistant.

Answer the user's question using ONLY the information provided in the requirements context below.

If the answer is not explicitly supported by the context, say:
"The requirements do not provide enough information to answer this."

Do not invent requirements, rules, deadlines, technical details, or business logic.

Requirements context:
{context}

User question:
{query}
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt,
    )

    return response.output_text


if __name__ == "__main__":
    query = "How can a user reset their password?"

    documents = [
        """
        The system must allow registered users to request a password reset using their email address.

        The user must provide a registered email address.

        The system must send a password reset link to the registered email.

        The reset link must allow the user to define a new password.

        The system must reject invalid email addresses.

        The email field is mandatory.

        The reset link must expire after a defined period.
        """,
        """
        Passwords must never be stored in plain text.

        Authentication failures should not expose sensitive information.

        Password reset tokens must be securely generated.
        """
    ]

    answer = generate_answer(query, documents)

    print("\nGenerated answer:")
    print(answer)
