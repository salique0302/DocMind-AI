import os
from google import genai

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is NOT set")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash"


def generate_answer(query: str, contexts: list[str]) -> str:
    print("🤖 Gemini called with context chunks:", len(contexts))

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say "I don't know based on the given context."

Context:
{chr(10).join(contexts)}

Question:
{query}

Answer:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response or not response.text:
        return "⚠️ Gemini returned an empty response"

    return response.text.strip()
