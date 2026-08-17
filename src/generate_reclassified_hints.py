import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECLASSIFIED = ROOT / "data" / "reclassified"

DECISION_PATTERNS = [
    re.compile(r"(?:최저|가장|최소한의|최소)\s*(?:비용|운영\s*오버헤드|개발\s*노력|다운타임|중단|지연)", re.I),
    re.compile(r"(?:고가용성|내결함성|재해\s*복구|실시간|준실시간|확장(?:성|할)|장애\s*조치)", re.I),
    re.compile(r"(?:온프레미스|사설\s*IP|인터넷을\s*통과하지|인터넷\s*접근|여러\s*(?:AWS\s*)?계정|여러\s*리전|다른\s*리전)", re.I),
    re.compile(r"(?:RTO|RPO|\d+\s*(?:분|시간|일|TB|GB|Mbps|Gbps|배))", re.I),
]

SERVICE_PATTERN = re.compile(
    r"(?:Amazon\s+[A-Za-z0-9.-]+|AWS\s+[A-Za-z0-9.-]+|"
    r"(?:Route\s*53|CloudFront|PrivateLink|Transit\s*Gateway|Direct\s*Connect|"
    r"S3|EC2|ECS|EKS|RDS|Aurora|Lambda|DynamoDB|EFS|EBS|VPC|VPN|"
    r"Systems\s*Manager|CloudFormation|CodeDeploy|CodePipeline|"
    r"Auto\s*Scaling|Application\s*Load\s*Balancer|Network\s*Load\s*Balancer|"
    r"Kinesis|EventBridge|SNS|SQS|IAM|Organizations|Config|Rekognition|"
    r"Fargate|Global\s*Table|Multi.?AZ|Read.?Replica|Private\s*Hosted\s*Zone|"
    r"VPC\s*Endpoint|Resolver|Resource\s*Access\s*Manager|RAM))\b",
    re.I,
)

WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9./_-]{2,}|[가-힣]{2,}")
STOPWORDS = {
    "회사", "사용", "사용하여", "위한", "대한", "문제", "요구", "사항", "서비스", "애플리케이션",
    "데이터", "시스템", "구성", "생성", "연결", "경우", "필요", "수행", "있습니다", "해야",
}


def compact(value):
    return re.sub(r"\s+", " ", str(value)).strip()


def sentences(text):
    parts = re.split(r"(?<=[.!?。！？])\s+|(?<=습니다)\s+|(?<=합니다)\s+", text)
    return [compact(part) for part in parts if compact(part)]


def terms(text):
    return {term.lower() for term in WORD_PATTERN.findall(text) if term not in STOPWORDS and len(term) >= 2}


def answer_choices(question):
    labels = {str(label).strip().upper() for label in question.get("answers", [])}
    return [choice for choice in question.get("choices", []) if str(choice.get("label", "")).upper() in labels]


def candidates(question, answer_text):
    source_sentences = sentences(question["question"])
    answer_terms = terms(answer_text)
    answer_services = {match.group(0).strip() for match in SERVICE_PATTERN.finditer(answer_text)}
    scored = []

    for sentence in source_sentences:
        sentence_terms = terms(sentence)
        score = len(answer_terms & sentence_terms) * 2
        if any(service.lower() in sentence.lower() for service in answer_services):
            score += 5
        if any(pattern.search(sentence) for pattern in DECISION_PATTERNS):
            score += 3
        if score:
            scored.append((score, sentence))

    for pattern in DECISION_PATTERNS:
        for match in pattern.finditer(question["question"]):
            scored.append((4, match.group(0)))

    unique = {}
    for score, text in scored:
        unique[text] = max(score, unique.get(text, 0))
    return sorted(unique.items(), key=lambda item: (-item[1], len(item[0])))


def link_text(answer_text, highlight):
    for match in SERVICE_PATTERN.finditer(answer_text):
        return compact(match.group(0))
    for pattern in DECISION_PATTERNS:
        match = pattern.search(answer_text)
        if match:
            return compact(match.group(0))
    return compact(answer_text[:140])


def build_hint(question):
    choices = answer_choices(question)
    scored = []
    for choice in choices:
        answer_text = compact(choice.get("text", ""))
        for text, score in candidates(question, answer_text):
            scored.append((score, text, link_text(answer_text, text)))

    selected = []
    seen = set()
    for score, text, answer_link in sorted(scored, key=lambda item: (-item[0], len(item[1]))):
        if text in seen:
            continue
        seen.add(text)
        selected.append({"text": text, "answerLink": answer_link})
        if len(selected) == 5:
            break

    if len(selected) < 2:
        for sentence in sentences(question["question"]):
            if sentence in seen or len(sentence) < 8:
                continue
            selected.append({"text": sentence, "answerLink": link_text(choices[0].get("text", ""), sentence)})
            if len(selected) == 2:
                break

    return {
        "qNumber": question["qNumber"],
        "answer": question.get("answer", ", ".join(question.get("answers", []))),
        "highlights": selected[:5],
        "memory": "정답 선택지의 서비스와 기능을 먼저 확인한 뒤, 문제 원문에서 해당 선택을 결정하는 조건을 역추적한다.",
    }


def main():
    generated = 0
    hint_files = []
    for questions_path in sorted(RECLASSIFIED.glob("**/questions.json")):
        range_match = re.fullmatch(r"Q(\d+)_(\d+)", questions_path.parent.name)
        if not range_match:
            continue
        start, end = range_match.groups()
        hints_path = questions_path.with_name(f"hints_q{start}_q{end}.json")
        if hints_path.exists():
            hint_files.append(hints_path.relative_to(RECLASSIFIED).as_posix())
            continue
        questions = json.loads(questions_path.read_text(encoding="utf-8"))
        hints = [build_hint(question) for question in questions]
        hints_path.write_text(json.dumps(hints, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated += 1
        hint_files.append(hints_path.relative_to(RECLASSIFIED).as_posix())
        print(hints_path.relative_to(ROOT))
    (RECLASSIFIED / "hints_manifest.json").write_text(
        json.dumps(sorted(hint_files), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated={generated}")


if __name__ == "__main__":
    main()