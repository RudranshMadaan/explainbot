
from pathlib import Path

# Locate the prompts folder from the project root
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "explain_v1.txt"


def build_prompt(term: str, audience: str) -> str:
    """
    Loads the system prompt and inserts the user's input.
    """

    if not term or not term.strip():
        raise ValueError("Term cannot be empty")

    if audience not in ["eli5", "teenager", "engineer"]:
        raise ValueError("Invalid audience")

    template = PROMPT_PATH.read_text(encoding="utf-8")

    prompt = (
        template
        .replace("{term}", term.strip())
        .replace("{audience}", audience)
    )

    return prompt