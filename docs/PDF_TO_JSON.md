# PDF -> JSON 변환 가이드

목표
- 약 27MB PDF, 약 660문제를 화면에 표시 가능한 JSON으로 정규화

권장 파일 위치
- 원본 PDF: data/raw/
- 변환 JSON: data/questions/questions.json

JSON 구조(배열)
[
  {
    "qNumber": 1,
    "question": "문제 원문",
    "choices": [
      { "label": "A", "text": "선택지 A" },
      { "label": "B", "text": "선택지 B" },
      { "label": "C", "text": "선택지 C" },
      { "label": "D", "text": "선택지 D" }
    ],
    "answer": "C",
    "answers": ["C"],
    "explanation": "선택 사항"
  }
]

복수 정답 예시
{
  "qNumber": 120,
  "question": "...",
  "choices": [
    { "label": "A", "text": "..." },
    { "label": "B", "text": "..." },
    { "label": "C", "text": "..." },
    { "label": "D", "text": "..." }
  ],
  "answer": "A, C",
  "answers": ["A", "C"]
}

필수 규칙
- qNumber, question, choices, answer는 필수
- choices는 최소 2개 이상
- answer/answers 값은 choices.label 내 값만 사용
- 서비스명/기능명은 원문 유지

참고
- Viewer는 위 형식을 기준으로 동작
- 파일 인코딩은 UTF-8 권장

실행 명령
- `C:/Users/ekkks/AppData/Local/Programs/Python/Python312/python.exe src/pdf_to_questions.py`

생성 결과
- `data/questions/questions.json`: 문제/보기/정답 1차 변환 결과
- `viewer/questions.data.js`: 뷰어 자동 로드용 데이터

뷰어 연동 방식
- `viewer/index.html`은 `viewer/questions.data.js`를 먼저 읽고 자동 로드
- 데이터가 없으면 `data/questions/questions.json`을 fetch로 재시도
