from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

SOURCE_PATH = Path("data/questions/questions.json")
OUTPUT_JSON_PATH = Path("data/questions/questions.unique.json")
OUTPUT_JS_PATH = Path("viewer/questions.unique.data.js")

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9+./-]*")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "use",
    "using",
    "with",
}
SINGLE_TOKEN_ALLOWLIST = {
    "cloudfront",
    "fargate",
    "privatelink",
    "quicksight",
    "athena",
    "eventbridge",
    "datasync",
    "glue",
    "lambda",
    "msk",
    "outposts",
}


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9가-힣+./-]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def tokenize(value: str) -> list[str]:
    return TOKEN_RE.findall(value)


def generate_candidates(answer_text: str) -> list[str]:
    tokens = tokenize(answer_text)
    candidates: list[str] = []

    for size in range(1, 6):
        for idx in range(0, len(tokens) - size + 1):
            phrase_tokens = tokens[idx : idx + size]
            lower_tokens = [token.lower() for token in phrase_tokens]
            phrase = " ".join(phrase_tokens)

            if size == 1:
                token = phrase_tokens[0]
                lower = token.lower()
                if lower in STOPWORDS:
                    continue
                if len(token) < 5 and lower not in SINGLE_TOKEN_ALLOWLIST and not any(ch.isdigit() for ch in token):
                    continue
                if token.islower() and lower not in SINGLE_TOKEN_ALLOWLIST:
                    continue
            else:
                if lower_tokens[0] in STOPWORDS or lower_tokens[-1] in STOPWORDS:
                    continue
                if all(token.lower() in STOPWORDS for token in phrase_tokens):
                    continue

            if not any(ch.isupper() or ch.isdigit() for ch in phrase):
                continue
            if len(phrase) < 4:
                continue
            if phrase not in candidates:
                candidates.append(phrase)

    return candidates


def score_candidate(candidate: str) -> tuple[int, int, int]:
    words = candidate.split()
    has_aws_prefix = 1 if candidate.startswith(("Amazon ", "AWS ")) else 0
    has_digits = 1 if any(ch.isdigit() for ch in candidate) else 0
    return (has_aws_prefix, len(words), has_digits)


def get_correct_choices(question: dict) -> list[dict]:
    answers = question.get("answers") or [question.get("answer")]
    answer_set = {str(label).strip().upper() for label in answers if label}
    return [choice for choice in question["choices"] if choice["label"].upper() in answer_set]


def main() -> None:
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    documents = []
    for item in source:
        full_text = " ".join(
            [item["question"]] + [choice["text"] for choice in item["choices"]]
        )
        documents.append(normalize_text(full_text))

    unique_questions = []
    for index, item in enumerate(source):
        correct_choices = get_correct_choices(item)
        answer_text = " ".join(choice["text"] for choice in correct_choices)
        candidates = generate_candidates(answer_text)
        valid_candidates = []

        for candidate in candidates:
            normalized_candidate = normalize_text(candidate)
            if not normalized_candidate:
                continue
            containing_docs = [doc_index for doc_index, doc in enumerate(documents) if normalized_candidate in doc]
            if containing_docs == [index]:
                valid_candidates.append(candidate)

        valid_candidates.sort(key=score_candidate, reverse=True)
        unique_clues = valid_candidates[:3]
        if not unique_clues:
            continue

        unique_questions.append(
            {
                "qNumber": item["qNumber"],
                "question": item["question"],
                "answer": item["answer"],
                "answers": item["answers"],
                "correctChoices": correct_choices,
                "primaryClue": unique_clues[0],
                "uniqueClues": unique_clues,
            }
        )

    OUTPUT_JSON_PATH.write_text(
        json.dumps(unique_questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    OUTPUT_JS_PATH.write_text(
        "window.UNIQUE_QUESTIONS = " + json.dumps(unique_questions, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    print(f"unique_questions={len(unique_questions)}")
    q352 = next((item for item in unique_questions if item["qNumber"] == 352), None)
    print(f"q352_clues={q352['uniqueClues'] if q352 else []}")


if __name__ == "__main__":
    main()
