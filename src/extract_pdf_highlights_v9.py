from __future__ import annotations

import json
from pathlib import Path

from extract_pdf_highlights_v7 import (
    ROOT,
    SOURCE_PDF,
    SOURCE_RECLASSIFIED,
    DUPLICATE_PATH,
    excluded_questions,
    extract_highlights,
)


OUTPUT_RECLASSIFIED = ROOT / "data" / "reclassified_v9"
EXTRA_EXCLUDED = {85}


def write_outputs(highlights_by_question: dict[int, list[dict]], excluded: set[int]) -> tuple[int, int]:
    manifest: list[str] = []
    batch_count = 0
    highlight_count = 0

    for questions_path in sorted(SOURCE_RECLASSIFIED.glob("**/questions.json")):
        range_name = questions_path.parent.name
        if not range_name.startswith("Q") or "_" not in range_name:
            continue
        start, end = map(int, range_name[1:].split("_"))
        batch = [
            {"qNumber": q_number, "highlights": highlights_by_question.get(q_number, [])}
            for q_number in range(start, end + 1)
            if q_number not in excluded
        ]
        output_dir = OUTPUT_RECLASSIFIED / questions_path.parent.relative_to(SOURCE_RECLASSIFIED)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"pdf_highlights_q{start}_q{end}.json"
        output_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append(output_path.relative_to(OUTPUT_RECLASSIFIED).as_posix())
        batch_count += 1
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
    (ROOT / "viewer" / "pdf_highlights_v9.data.js").write_text(
        "window.DEFAULT_EXCLUDED_QUESTIONS = "
        + json.dumps(sorted(excluded), ensure_ascii=False)
        + ";\nwindow.DEFAULT_PDF_HIGHLIGHTS_V9 = "
        + json.dumps(embedded, ensure_ascii=False)
        + ";\nwindow.DEFAULT_PDF_HIGHLIGHTS_V7 = window.DEFAULT_PDF_HIGHLIGHTS_V9"
        + ";\n",
        encoding="utf-8",
    )
    return batch_count, highlight_count


def main() -> None:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"PDF 파일이 없습니다: {SOURCE_PDF}")
    excluded = excluded_questions() | EXTRA_EXCLUDED
    highlights = extract_highlights()

    highlights = {q_number: items for q_number, items in highlights.items() if q_number not in excluded}
    batches, highlight_count = write_outputs(highlights, excluded)
    print(f"excluded_questions={len(excluded)}")
    print(f"questions_with_highlights={len(highlights)}")
    print(f"highlights={highlight_count}")
    print(f"batches={batches}")
    print(f"duplicate_source={DUPLICATE_PATH.name}")


if __name__ == "__main__":
    main()