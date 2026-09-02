from __future__ import annotations

import json
import re
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "data" / "raw" / "SAP-C02_V21.95_Examtopics_Kor_정답외우기.pdf"
RECLASSIFIED = ROOT / "data" / "reclassified"
Q_MARKER_RE = re.compile(r"\bQ\s*(\d+)\b")


def normalized(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.lower())


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


def extract_highlights(max_question: int | None = None) -> dict[int, list[dict[str, Any]]]:
    document = pymupdf.open(SOURCE_PDF)
    current_question: int | None = None
    extracted: dict[int, list[dict[str, Any]]] = defaultdict(list)
    texts = question_text_index()

    for page in document:
        markers = question_markers(page)
        if current_question is None:
            if not markers:
                continue
            current_question = markers[0][1]

        for highlight in extract_page_highlights(page):
            while markers and markers[0][0] <= highlight["y"]:
                current_question = markers.pop(0)[1]
            q_number = source_question(highlight, current_question, texts)
            if max_question is not None and q_number > max_question:
                continue
            entry = {key: value for key, value in highlight.items() if key != "y"}
            if entry not in extracted[q_number]:
                extracted[q_number].append(entry)

        if markers:
            current_question = markers[-1][1]

    return extracted


def write_batches(
    highlights_by_question: dict[int, list[dict[str, Any]]],
    max_question: int | None = None,
) -> tuple[int, int]:
    written = 0
    highlight_count = 0
    manifest: list[str] = []

    for questions_path in sorted(RECLASSIFIED.glob("**/questions.json")):
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
        ]
        output_path = questions_path.with_name(f"pdf_highlights_q{start}_q{end}.json")
        output_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append(output_path.relative_to(RECLASSIFIED).as_posix())
        written += 1
        highlight_count += sum(len(item["highlights"]) for item in batch)

    (RECLASSIFIED / "pdf_highlights_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    embedded = [
        {"qNumber": q_number, "highlights": highlights}
        for q_number, highlights in sorted(highlights_by_question.items())
    ]
    (ROOT / "viewer" / "pdf_highlights.data.js").write_text(
        "window.DEFAULT_PDF_HIGHLIGHTS = "
        + json.dumps(embedded, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    return written, highlight_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract PDF highlights into question batches")
    parser.add_argument("--max-question", type=int, default=None, help="Only generate questions up to this number")
    args = parser.parse_args()
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"PDF 파일이 없습니다: {SOURCE_PDF}")
    highlights_by_question = extract_highlights(args.max_question)
    batches, highlight_count = write_batches(highlights_by_question, args.max_question)
    print(f"questions_with_highlights={len(highlights_by_question)}")
    print(f"highlights={highlight_count}")
    print(f"batches={batches}")


if __name__ == "__main__":
    main()