
import os
import re
import wordninja
from dotenv import load_dotenv
from google import genai

# Load API key from the project's .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def validate_explanation(answer: str) -> str:

    if not answer or not answer.strip():
        raise ValueError("The generated explanation is empty")

    answer = answer.strip()

    # Count sentences
    sentences = [
        s for s in re.split(r'(?<=[.!?])\s+', answer)
        if s.strip()
    ]

    if not 2 <= len(sentences) <= 4:
        raise ValueError(
            f"Explanation must contain 2-4 sentences. "
            f"Received: {len(sentences)}"
        )

    # Check for an analogy phrase
    analogy_patterns = [
        r"\blike\b",
        r"\bthink of\b",
        r"\bsimilar to\b",
        r"\bimagine\b"
    ]

    analogy_found = any(
        re.search(pattern, answer.lower())
        for pattern in analogy_patterns
    )

    if not analogy_found:
        raise ValueError("Explanation is missing an analogy")

    # Detect suspiciously joined words
    words = re.findall(r"[a-zA-Z]+", answer)

    for word in words:
        split_words = wordninja.split(word)

        if len(split_words) > 1:
            raise ValueError(
                f"Suspicious word spacing detected: {word}"
            )

    # Return the validated explanation
    return answer


def generate_explanation(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return validate_explanation(response.text)
