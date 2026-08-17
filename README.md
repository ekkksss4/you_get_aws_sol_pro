# AWS 자격증 학습 프로젝트

이 저장소는 AWS 자격증 준비를 위한 학습 프로젝트입니다.

## 프로젝트 목표
- 덤프/문제은행 복습 및 암기
- 문제 핵심 키워드와 정답 서비스/구성의 즉시 매칭
- 시험 직전 빠른 회독

## 학습 원칙
- 공식 문서와 합법적인 학습 자료를 우선 사용합니다.
- 문제 전체 장문 요약 없이 핵심 문장만 인용합니다.
- 오답 분석은 하지 않고 정답 연결만 기록합니다.

## 폴더 구조
- `docs/`: 학습 계획, 규칙, 진행 기록
- `data/questions/`: 문제 데이터(JSON)
- `data/concepts/`: 서비스 개념 후보, 기능 연결, 중복 그룹, 개념집
- `viewer/`: 문제/보기 표시 화면
- `src/`: 스크립트 및 도구 코드

## 빠른 시작
1. [docs/FORMAT_RULES.md](docs/FORMAT_RULES.md)에서 출력 규칙을 확인합니다.
2. [docs/PDF_TO_JSON.md](docs/PDF_TO_JSON.md)의 형식으로 문제 JSON을 준비합니다.
3. [viewer/index.html](viewer/index.html)을 열고 JSON 파일을 불러옵니다.
4. 이전/다음/번호 이동으로 문제와 보기를 확인합니다.

## 개념집
- [viewer/index4.html](viewer/index4.html): 서비스 사이드바 + 조건/정답 표현 중심의 화면형 개념집
- [viewer/index5.html](viewer/index5.html): 문제 핵심 형광 + 정답 보기만 표시하는 암기 화면
- [data/concepts/AWS_CONCEPT_BOOK.md](data/concepts/AWS_CONCEPT_BOOK.md): 서비스별 개념 후보와 문제 조건 연결
- [data/concepts/questions.deduplicated.json](data/concepts/questions.deduplicated.json): 80% 이상 유사 문항 그룹에서 대표 문항만 남긴 데이터
- [data/concepts/VERIFICATION.md](data/concepts/VERIFICATION.md): 공식 AWS 문서 검증 상태와 주의사항

개념집 재생성:
`C:/Users/ekkks/AppData/Local/Programs/Python/Python312/python.exe src/build_concept_book.py`

## 현재 포함된 샘플
- [data/questions/questions.sample.json](data/questions/questions.sample.json)
- [data/questions/template.question.json](data/questions/template.question.json)

## 다음 단계(당신이 세부 설명 주면 반영)
- 목표 자격증(예: SAA, DVA, SAP) 확정
- PDF 파싱 결과(JSON) 표준 확정
- 10문제 배치 자동 출력기 추가
