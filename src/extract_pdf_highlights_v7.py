from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "data" / "raw" / "SAP-C02_V21.95_Examtopics_Kor_정답외우기.pdf"
SOURCE_RECLASSIFIED = ROOT / "data" / "reclassified"
OUTPUT_RECLASSIFIED = ROOT / "data" / "reclassified_v7"
DUPLICATE_PATH = ROOT / "duplicate_question.md"
Q_MARKER_RE = re.compile(r"\bQ\s*(\d+)\b")
CHOICE_MARKER_RE = re.compile(r"([A-F])(?:\.|．)")
DUPLICATE_RE = re.compile(r"^\s*(\d+)\s*번(?:은|과)\s*(\d+)\s*번과\s*같은\s*문제")


def normalized(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.lower())


def excluded_questions() -> set[int]:
    excluded: set[int] = set()
    for line in DUPLICATE_PATH.read_text(encoding="utf-8").splitlines():
        match = DUPLICATE_RE.match(line)
        if match:
            excluded.add(int(match.group(1)))
    return excluded


def overlap_ratio(left: pymupdf.Rect, right: pymupdf.Rect) -> float:
    intersection = left & right
    if intersection.is_empty or right.get_area() == 0:
        return 0.0
    return intersection.get_area() / right.get_area()


def css_color(color: tuple[float, float, float]) -> str:
    channels = [round(max(0, min(1, channel)) * 255) for channel in color]
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def is_highlight(item: dict[str, Any]) -> bool:
    rect = item["rect"]
    opacity = item.get("fill_opacity", 1)
    return (
        item.get("fill") is not None
        and 0 < opacity < 1
        and rect.width >= 8
        and 4 <= rect.height <= 14
    )


def extract_page_highlights(page: pymupdf.Page) -> list[dict[str, Any]]:
    words = [(pymupdf.Rect(word[:4]), word[4]) for word in page.get_text("words")]
    highlights: list[dict[str, Any]] = []

    for drawing in page.get_drawings():
        if not is_highlight(drawing):
            continue
        rect = drawing["rect"]
        matched_words = [word for word_rect, word in words if overlap_ratio(rect, word_rect) >= 0.15]
        text = " ".join(matched_words).strip()
        if not text:
            continue
        highlights.append(
            {
                "y": rect.y0,
                "text": text,
                "color": css_color(drawing["fill"]),
                "opacity": round(drawing["fill_opacity"], 3),
            }
        )
    return sorted(highlights, key=lambda item: item["y"])


def question_text_index() -> dict[int, str]:
    questions = json.loads((ROOT / "data" / "questions" / "questions.json").read_text(encoding="utf-8"))
    indexed: dict[int, str] = {}
    for question in questions:
        parts = [question.get("question", "")]
        parts.extend(choice.get("text", "") for choice in question.get("choices", []))
        indexed[int(question["qNumber"])] = normalized(" ".join(parts))
    return indexed


def source_question(highlight: dict[str, Any], default_question: int, texts: dict[int, str]) -> int:
    needle = normalized(highlight["text"])
    if len(needle) < 8:
        return default_question
    matches = [q_number for q_number, text in texts.items() if needle in text]
    return matches[0] if len(matches) == 1 else default_question


def question_markers(page: pymupdf.Page) -> list[tuple[float, int]]:
    markers = []
    for word in page.get_text("words"):
        match = Q_MARKER_RE.fullmatch(word[4])
        if match:
            markers.append((word[1], int(match.group(1))))
    return sorted(markers)


def choice_markers(page: pymupdf.Page) -> list[tuple[float, str]]:
    markers = []
    for word in page.get_text("words"):
        match = CHOICE_MARKER_RE.fullmatch(word[4])
        if match:
            markers.append((word[1], match.group(1)))
    return sorted(markers)


def highlight_choice_labels(
    y: float,
    question_marker_positions: list[float],
    choices: list[tuple[float, str]],
) -> list[str]:
    last_question_y = max((position for position in question_marker_positions if position <= y), default=None)
    choices_in_question = [
        (position, label)
        for position, label in choices
        if position <= y and (last_question_y is None or position > last_question_y)
    ]
    return [choices_in_question[-1][1]] if choices_in_question else []


def extract_highlights(max_question: int | None = None) -> dict[int, list[dict[str, Any]]]:
    document = pymupdf.open(SOURCE_PDF)
    current_question: int | None = None
    extracted: dict[int, list[dict[str, Any]]] = defaultdict(list)
    texts = question_text_index()
    excluded = excluded_questions()

    for page in document:
        markers = question_markers(page)
        choices = choice_markers(page)
        marker_positions = [position for position, _ in markers]
        if current_question is None:
            if not markers:
                continue
            current_question = markers[0][1]

        for highlight in extract_page_highlights(page):
            while markers and markers[0][0] <= highlight["y"]:
                current_question = markers.pop(0)[1]
            q_number = source_question(highlight, current_question, texts)
            if q_number in excluded or (max_question is not None and q_number > max_question):
                continue

            text = normalized(highlight["text"])
            if not text or text not in texts.get(q_number, ""):
                continue

            entry = {key: value for key, value in highlight.items() if key != "y"}
            labels = highlight_choice_labels(highlight["y"], marker_positions, choices)
            if labels:
                entry["choiceLabels"] = labels
            if entry not in extracted[q_number]:
                extracted[q_number].append(entry)

        if markers:
            current_question = markers[-1][1]

    return extracted


def write_batches(
    highlights_by_question: dict[int, list[dict[str, Any]]],
    excluded: set[int],
    max_question: int | None = None,
) -> tuple[int, int]:
    written = 0
    highlight_count = 0
    manifest: list[str] = []

    for questions_path in sorted(SOURCE_RECLASSIFIED.glob("**/questions.json")):
        range_match = re.fullmatch(r"Q(\d+)_(\d+)", questions_path.parent.name)
        if not range_match:
            continue
        start, end = map(int, range_match.groups())
        if max_question is not None and start > max_question:
            continue
        end = min(end, max_question) if max_question is not None else end
        batch = [
            {"qNumber": q_number, "highlights": highlights_by_question.get(q_number, [])}
            for q_number in range(start, end + 1)
            if q_number not in excluded
        ]
        relative_parent = questions_path.parent.relative_to(SOURCE_RECLASSIFIED)
        output_dir = OUTPUT_RECLASSIFIED / relative_parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"pdf_highlights_q{start}_q{end}.json"
        output_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append(output_path.relative_to(OUTPUT_RECLASSIFIED).as_posix())
        written += 1
        highlight_count += sum(len(item["highlights"]) for item in batch)

    OUTPUT_RECLASSIFIED.mkdir(parents=True, exist_ok=True)
    (OUTPUT_RECLASSIFIED / "pdf_highlights_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    embedded = [
        {"qNumber": q_number, "highlights": highlights}
        for q_number, highlights in sorted(highlights_by_question.items())
        if q_number not in excluded
    ]
    (ROOT / "viewer" / "pdf_highlights_v7.data.js").write_text(
        "window.DEFAULT_EXCLUDED_QUESTIONS = "
        + json.dumps(sorted(excluded), ensure_ascii=False)
        + ";\nwindow.DEFAULT_PDF_HIGHLIGHTS_V7 = "
        + json.dumps(embedded, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    return written, highlight_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text-overlapping PDF highlights for viewer v7")
    parser.add_argument("--max-question", type=int, default=None, help="Only generate questions up to this number")
    args = parser.parse_args()
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"PDF 파일이 없습니다: {SOURCE_PDF}")
    excluded = excluded_questions()
    highlights_by_question = extract_highlights(args.max_question)
    batches, highlight_count = write_batches(highlights_by_question, excluded, args.max_question)
    print(f"excluded_questions={len(excluded)}")
    print(f"questions_with_highlights={len(highlights_by_question)}")
    print(f"highlights={highlight_count}")
    print(f"batches={batches}")


if __name__ == "__main__":
    main()
