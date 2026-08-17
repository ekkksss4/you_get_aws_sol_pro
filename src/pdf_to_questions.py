from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

Q_SPLIT_RE = re.compile(r"(?m)^\s*Q(\d+)\s*$")
CHOICE_RE = re.compile(r"(?m)^\s*([A-F])\.\s")
ANSWER_LINE_RE = re.compile(r"(?im)^\s*Answer\s*:\s*(.+?)\s*$")
URL_RE = re.compile(r"https?://\S+")
WS_RE = re.compile(r"\s+")


def clean_text(value: str) -> str:
    value = value.replace("\u200b", " ")
    value = value.replace("\xa0", " ")
    value = URL_RE.sub("", value)
    value = WS_RE.sub(" ", value)
    return value.strip()


def strip_tail_metadata(value: str) -> str:
    # Keep only question/choice body and remove explanation/discussion leftovers.
    cut_points = []
    for token in ("Answer:", "설명:", "참고:"):
        idx = value.find(token)
        if idx >= 0:
            cut_points.append(idx)

    if cut_points:
        return value[: min(cut_points)]
    return value


def parse_choices(block: str) -> tuple[str, list[dict[str, str]]]:
    matches = list(CHOICE_RE.finditer(block))
    if len(matches) < 2:
        return clean_text(strip_tail_metadata(block)), []

    question_raw = block[: matches[0].start()]
    choices: list[dict[str, str]] = []

    for i, match in enumerate(matches):
        label = match.group(1).upper()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        chunk = strip_tail_metadata(block[start:end])
        text = clean_text(chunk)
        if text:
            choices.append({"label": label, "text": text})

    return clean_text(strip_tail_metadata(question_raw)), choices


def parse_answer_labels(block: str) -> tuple[list[str], re.Match[str] | None]:
    match = ANSWER_LINE_RE.search(block)
    if not match:
        return [], None

    raw_line = match.group(1).upper()
    labels = re.findall(r"(?<![A-Z])([A-F])(?![A-Z])", raw_line)

    unique_labels: list[str] = []
    for label in labels:
        if label not in unique_labels:
            unique_labels.append(label)

    return unique_labels, match


def build_questions(raw_text: str) -> list[dict[str, Any]]:
    split = Q_SPLIT_RE.split(raw_text)
    if len(split) < 3:
        raise ValueError("질문 구간(Q번호)을 찾지 못했습니다.")

    questions: list[dict[str, Any]] = []

    # split shape: [prefix, qnum1, block1, qnum2, block2, ...]
    for i in range(1, len(split), 2):
        q_number = int(split[i])
        block = split[i + 1]

        answer_labels, answer_match = parse_answer_labels(block)

        body = block[: answer_match.start()] if answer_match else block
        question, choices = parse_choices(body)

        if not question or len(choices) < 2:
            continue

        choice_labels = {c["label"] for c in choices}
        answer_labels = [label for label in answer_labels if label in choice_labels]

        answer = ", ".join(answer_labels)

        question_item: dict[str, Any] = {
            "qNumber": q_number,
            "question": question,
            "choices": choices,
            "answer": answer,
            "answers": answer_labels,
        }
        questions.append(question_item)

    return questions


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def write_json(path: Path, questions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")


def write_js(path: Path, questions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(questions, ensure_ascii=False)
    path.write_text(f"window.DEFAULT_QUESTIONS = {payload};\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Q/A items from exam PDF into viewer JSON format"
    )
    parser.add_argument(
        "--pdf",
        default="data/raw/SAP-C02_V21.95_Examtopics_Kor_문답표기.pdf",
        help="Source PDF path",
    )
    parser.add_argument(
        "--json-out",
        default="data/questions/questions.json",
        help="Output JSON path",
    )
    parser.add_argument(
        "--js-out",
        default="viewer/questions.data.js",
        help="Output JS file for instant viewer load",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일이 없습니다: {pdf_path}")

    text = extract_pdf_text(pdf_path)
    questions = build_questions(text)

    if not questions:
        raise RuntimeError("추출된 문제가 없습니다. PDF 형식을 확인하세요.")

    write_json(Path(args.json_out), questions)
    write_js(Path(args.js_out), questions)

    with_answer = sum(1 for q in questions if q.get("answer"))
    print(f"extracted={len(questions)} with_answer={with_answer}")
    print(f"json={args.json_out}")
    print(f"js={args.js_out}")


if __name__ == "__main__":
    main()
