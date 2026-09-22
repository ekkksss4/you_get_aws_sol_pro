from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pymupdf

QUESTION_RE = re.compile(r"(?m)^\s*Q\s*(\d+)\s*$")
CHOICE_RE = re.compile(r"(?m)^\s*([A-F])\.\s*")
ANSWER_RE = re.compile(r"(?im)^\s*Answer\s*:\s*(.+?)\s*$")
URL_RE = re.compile(r"https?://\S+")
Q_MARKER_RE = re.compile(r"^Q\s*(\d+)$", re.IGNORECASE)
CHOICE_MARKER_RE = re.compile(r"^([A-F])(?:\.|．)$")


def clean_text(value: str) -> str:
    value = value.replace("\u200b", " ").replace("\xa0", " ")
    value = URL_RE.sub("", value)
    return re.sub(r"\s+", " ", value).strip()


def normalized(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.lower())


def css_color(color: tuple[float, float, float]) -> str:
        channels = [round(max(0, min(1, channel)) * 255) for channel in color]
        return "#" + "".join(f"{channel:02x}" for channel in channels)


def parse_question(q_number: int, block: str) -> dict[str, Any] | None:
    answer_match = ANSWER_RE.search(block)
    body = block[: answer_match.start()] if answer_match else block
    choice_matches = list(CHOICE_RE.finditer(body))
    if len(choice_matches) < 2:
        return None

    question = clean_text(body[: choice_matches[0].start()])
    choices = []
    for index, match in enumerate(choice_matches):
        end = choice_matches[index + 1].start() if index + 1 < len(choice_matches) else len(body)
        text = clean_text(body[match.end() : end])
        if text:
            choices.append({"label": match.group(1).upper(), "text": text})
    if not question or len(choices) < 2:
        return None
    return {"qNumber": q_number, "question": question, "choices": choices}


def overlap_ratio(left: pymupdf.Rect, right: pymupdf.Rect) -> float:
    intersection = left & right
    if intersection.is_empty or right.get_area() == 0:
        return 0.0
    return intersection.get_area() / right.get_area()


def is_highlight(drawing: dict[str, Any]) -> bool:
    rect = drawing["rect"]
    opacity = drawing.get("fill_opacity", 1)
    return (
        drawing.get("fill") is not None
        and 0 < opacity < 1
        and rect.width >= 8
        and 4 <= rect.height <= 80
    )


def extract_page_highlights(page: pymupdf.Page) -> list[dict[str, Any]]:
    words = [(pymupdf.Rect(word[:4]), word[4]) for word in page.get_text("words")]
    result = []
    for drawing in page.get_drawings():
        if not is_highlight(drawing):
            continue
        rect = drawing["rect"]
        text = " ".join(word for word_rect, word in words if overlap_ratio(rect, word_rect) >= 0.15).strip()
        if text:
            result.append(
                {
                    "y": rect.y0,
                    "text": clean_text(text),
                    "color": css_color(drawing["fill"]),
                    "opacity": round(drawing.get("fill_opacity", 1), 3),
                }
            )
    return sorted(result, key=lambda item: item["y"])


def page_markers(page: pymupdf.Page) -> tuple[list[tuple[float, int]], list[tuple[float, str]]]:
    questions = []
    choices = []
    words = page.get_text("words")
    for index, word in enumerate(words):
        token = word[4].strip()
        q_match = Q_MARKER_RE.fullmatch(token)
        choice_match = CHOICE_MARKER_RE.fullmatch(token)
        if q_match:
            questions.append((word[1], int(q_match.group(1))))
        elif token.upper() == "Q" and index + 1 < len(words):
            next_word = words[index + 1]
            if re.fullmatch(r"\d+", next_word[4].strip()) and abs(next_word[1] - word[1]) <= 24:
                questions.append((word[1], int(next_word[4].strip())))
        elif choice_match:
            choices.append((word[1], choice_match.group(1).upper()))
    return sorted(questions), sorted(choices)


def extract_highlight_answers(pdf_path: Path) -> dict[int, list[dict[str, str]]]:
    document = pymupdf.open(pdf_path)
    answers: dict[int, list[dict[str, str]]] = defaultdict(list)
    current_question: int | None = None
    seen_questions: set[int] = set()

    for page in document:
        question_markers, choice_markers = page_markers(page)
        current_question_y = -1.0
        for highlight in extract_page_highlights(page):
            y = highlight["y"]
            text = highlight["text"]
            while question_markers and question_markers[0][0] <= y:
                current_question_y, current_question = question_markers.pop(0)
                if current_question == 350 and current_question in seen_questions:
                    current_question = 406
                seen_questions.add(current_question)
            if current_question is None:
                continue
            choice_candidates = [
                (choice_y, label)
                for choice_y, label in choice_markers
                if current_question_y < choice_y <= y
            ]
            label = choice_candidates[-1][1] if choice_candidates else ""
            answers[current_question].append({"text": text, "positionLabel": label})

        if question_markers:
            next_question = question_markers[-1][1]
            if next_question == 350 and next_question in seen_questions:
                next_question = 406
            current_question = next_question
            seen_questions.add(current_question)

    document.close()
    return dict(answers)


def extract_viewer_highlights(pdf_path: Path, questions: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    question_texts = {
        question["qNumber"]: normalized(
            " ".join([question["question"], *(choice["text"] for choice in question["choices"])])
        )
        for question in questions
    }
    document = pymupdf.open(pdf_path)
    highlights: dict[int, list[dict[str, Any]]] = defaultdict(list)
    current_question: int | None = None
    seen_questions: set[int] = set()

    for page in document:
        question_markers, _ = page_markers(page)
        for highlight in extract_page_highlights(page):
            while question_markers and question_markers[0][0] <= highlight["y"]:
                current_question = question_markers.pop(0)[1]
                if current_question == 350 and current_question in seen_questions:
                    current_question = 406
                seen_questions.add(current_question)
            if current_question not in question_texts:
                continue
            if normalized(highlight["text"]) not in question_texts[current_question]:
                continue
            entry = {key: highlight[key] for key in ("text", "color", "opacity")}
            if entry not in highlights[current_question]:
                highlights[current_question].append(entry)

        if question_markers:
            current_question = question_markers[-1][1]
            if current_question == 350 and current_question in seen_questions:
                current_question = 406
            seen_questions.add(current_question)

    document.close()
    return dict(highlights)


def write_viewer_highlights(highlights: dict[int, list[dict[str, Any]]], output_path: Path) -> None:
    payload = [
        {"qNumber": q_number, "highlights": items}
        for q_number, items in sorted(highlights.items())
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "window.DEFAULT_PDF_HIGHLIGHTS = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


def extract_questions(pdf_path: Path, highlighted_answers: dict[int, list[dict[str, str]]]) -> list[dict[str, Any]]:
    document = pymupdf.open(pdf_path)
    text = "\n".join(page.get_text("text", sort=True) or "" for page in document)
    document.close()
    matches = list(QUESTION_RE.finditer(text))
    questions = []
    seen_numbers: set[int] = set()
    for index, match in enumerate(matches):
        source_number = int(match.group(1))
        q_number = 406 if source_number == 350 and source_number in seen_numbers else source_number
        seen_numbers.add(source_number)
        if q_number > 529:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        question = parse_question(q_number, text[match.end() : end])
        if not question:
            continue
        labels: list[str] = []
        choice_labels = {choice["label"] for choice in question["choices"]}
        for highlight in highlighted_answers.get(q_number, []):
            highlight_text = normalized(highlight["text"])
            text_matches = [
                choice["label"]
                for choice in question["choices"]
                if len(highlight_text) >= 8 and highlight_text in normalized(choice["text"])
            ]
            label = text_matches[0] if len(text_matches) == 1 else highlight["positionLabel"]
            if label in choice_labels and label not in labels:
                labels.append(label)
        if not labels:
            continue
        question["answer"] = ", ".join(labels)
        question["answers"] = labels
        question["answerSource"] = "pdf_highlight_position"
        questions.append(question)
    return questions


def write_batches(questions: list[dict[str, Any]], batch_dir: Path) -> list[Path]:
    batch_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for start in range(1, 530, 10):
        end = min(start + 9, 529)
        batch = [question for question in questions if start <= question["qNumber"] <= end]
        if not batch:
            continue
        path = batch_dir / f"questions_q{start}_q{end}.json"
        path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Build v11 answers from highlight positions in one PDF")
    parser.add_argument("--pdf", default="data/raw/SAP-C02_V21.95_Examtopics_Kor - 최종정리본★★★★★★★★★★.pdf")
    parser.add_argument("--json-out", default="data/questions/questions_v11.json")
    parser.add_argument("--js-out", default="viewer/questions_v11.data.js")
    parser.add_argument("--batch-dir", default="data/questions/v11_batches")
    parser.add_argument("--highlights-js-out", default="viewer/pdf_highlights.data.js")
    parser.add_argument("--highlights-only", action="store_true")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if args.highlights_only:
        questions = json.loads(Path(args.json_out).read_text(encoding="utf-8"))
        highlights = extract_viewer_highlights(pdf_path, questions)
        write_viewer_highlights(highlights, Path(args.highlights_js_out))
        print(f"questions_with_highlights={len(highlights)}")
        print(f"highlights={sum(len(items) for items in highlights.values())}")
        print(f"js={args.highlights_js_out}")
        return

    highlighted_answers = extract_highlight_answers(pdf_path)
    questions = extract_questions(pdf_path, highlighted_answers)
    if not questions:
        raise RuntimeError("형광펜으로 표시된 문제를 추출하지 못했습니다.")

    batch_paths = write_batches(questions, Path(args.batch_dir))
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = json.dumps(questions, ensure_ascii=False)
    Path(args.js_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.js_out).write_text("window.DEFAULT_QUESTIONS_V11 = " + payload + "\n", encoding="utf-8")
    highlights = extract_viewer_highlights(pdf_path, questions)
    write_viewer_highlights(highlights, Path(args.highlights_js_out))
    print(f"extracted={len(questions)}")
    print(f"highlighted_questions={len(highlighted_answers)}")
    print(f"viewer_highlighted_questions={len(highlights)}")
    print(f"max_question=529")
    print(f"json_batches={len(batch_paths)}")
    print(f"json={args.json_out}")
    print(f"js={args.js_out}")


if __name__ == "__main__":
    main()
