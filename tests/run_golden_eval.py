
import json
import re

from pathlib import Path
from app.prompt_builder import build_prompt
from app.llm import generate_explanation


# Load the 10 predefined test cases
BASE_DIR = Path(__file__).resolve().parent.parent
CASES_PATH = BASE_DIR / "tests" / "golden_cases.json"

with open(CASES_PATH, "r", encoding="utf-8") as file:
    golden_cases = json.load(file)


passed = 0
total = len(golden_cases)

print("\n===== EXPLAINBOT GOLDEN EVALUATION =====\n")

for index, case in enumerate(golden_cases, start=1):

    term = case["term"]
    audience = case["audience"]

    print(f"\nTest {index}: {term} ({audience})")

    try:
        prompt = build_prompt(term, audience)
        answer = generate_explanation(prompt)

        # Count sentences
        sentences = [
            s for s in re.split(r'(?<=[.!?])\s+', answer.strip())
            if s
        ]

        # Check answer properties
        length_ok = 1 <= len(sentences) <= 4

        analogy_patterns = [
            r"\blike\b",
            r"\bthink of\b",
            r"\bsimilar to\b",
            r"\bimagine\b"
        ]

        analogy_ok = any(
            re.search(pattern, answer.lower())
            for pattern in analogy_patterns
        )

        test_passed = length_ok and analogy_ok

        print("Answer:", answer)
        print("Sentence count:", len(sentences))
        print("Contains analogy phrase:", analogy_ok)
        print("Sentence limit:", length_ok)
        print("Result:", "PASS" if test_passed else "FAIL")

        if test_passed:
            passed += 1

    except Exception as error:
        print("Result: ERROR")
        print("Reason:", error)


print("\n===== EVALUATION SUMMARY =====")
print(f"Passed: {passed}/{total}")
print(f"Failed: {total - passed}/{total}")

score = (passed / total) * 100 if total else 0

print(f"Golden evaluation score: {score:.1f}%")
