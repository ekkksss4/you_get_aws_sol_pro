from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

DEFAULT_INPUT = Path("data/questions/questions.json")
DEFAULT_OUTPUT_DIR = Path("data/concepts")

# Canonical names are intentionally conservative: only terms visible in the source
# questions/answers are promoted into the generated concept candidates.
SERVICE_CATALOG = {
    "Amazon S3": (r"Amazon\s+S3|\bS3\b", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
    "Amazon EC2": (r"Amazon\s+EC2|\bEC2\b", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"),
    "Amazon EBS": (r"Amazon\s+EBS|\bEBS\b", "https://docs.aws.amazon.com/ebs/latest/userguide/what-is- Amazon-EBS.html".replace(" ", "")),
    "Amazon RDS": (r"Amazon\s+RDS|\bRDS\b", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html"),
    "Amazon Aurora": (r"Amazon\s+Aurora|\bAurora\b", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html"),
    "AWS Lambda": (r"AWS\s+Lambda|\bLambda\b", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"),
    "Amazon ECS": (r"Amazon\s+ECS|Elastic\s+Container\s+Service|\bECS\b", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html"),
    "Amazon EKS": (r"Amazon\s+EKS|Elastic\s+Kubernetes\s+Service|\bEKS\b", "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html"),
    "AWS Fargate": (r"AWS\s+Fargate|\bFargate\b", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html"),
    "Elastic Load Balancing": (r"Elastic\s+Load\s+Balancing|Application\s+Load\s+Balancer|Network\s+Load\s+Balancer|\bALB\b|\bNLB\b", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html"),
    "Amazon CloudFront": (r"Amazon\s+CloudFront|\bCloudFront\b", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html"),
    "Amazon Route 53": (r"Amazon\s+Route\s*53|\bRoute\s*53\b", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html"),
    "AWS PrivateLink": (r"AWS\s+PrivateLink|\bPrivateLink\b|인터페이스\s+VPC\s+엔드포인트", "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html"),
    "AWS Transit Gateway": (r"Transit\s+Gateway|전송\s+게이트웨이", "https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html"),
    "Amazon MSK": (r"Amazon\s+Managed\s+Streaming|Amazon\s+MSK|\bMSK\b", "https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html"),
    "Amazon Kinesis": (r"Amazon\s+Kinesis|Kinesis\s+Data\s+Streams|Kinesis\s+Data\s+Firehose", "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"),
    "Amazon SQS": (r"Amazon\s+SQS|Simple\s+Queue\s+Service|\bSQS\b", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html"),
    "Amazon SNS": (r"Amazon\s+SNS|Simple\s+Notification\s+Service|\bSNS\b", "https://docs.aws.amazon.com/sns/latest/dg/welcome.html"),
    "AWS Step Functions": (r"AWS\s+Step\s+Functions|Step\s+Functions", "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html"),
    "Amazon EventBridge": (r"Amazon\s+EventBridge|EventBridge", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html"),
    "AWS CloudFormation": (r"AWS\s+CloudFormation|CloudFormation|Cloud\s+Formation", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html"),
    "AWS Organizations": (r"AWS\s+Organizations|\bOrganizations\b", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html"),
    "AWS IAM Identity Center": (r"IAM\s+Identity\s+Center|Identity\s+Center", "https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html"),
    "Amazon SageMaker": (r"Amazon\s+SageMaker|\bSageMaker\b", "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html"),
    "AWS Glue": (r"AWS\s+Glue|\bGlue\b", "https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html"),
    "Amazon Athena": (r"Amazon\s+Athena|\bAthena\b", "https://docs.aws.amazon.com/athena/latest/ug/what-is.html"),
    "AWS Transfer Family": (r"AWS\s+Transfer\s+Family|Transfer\s+Family", "https://docs.aws.amazon.com/transfer/latest/userguide/what-is.html"),
}

FEATURE_PATTERNS = {
    "S3 RTC": r"S3\s+RTC|S3\s+복제\s+시간\s+제어",
    "Cross-Region Replication": r"Cross-Region\s+Replication|교차\s+리전\s+복제",
    "DeletionPolicy Retain": r"DeletionPolicy|삭제\s+정책.*Retain|Retain",
    "Aurora Read Replica": r"Aurora\s+복제본|읽기\s+전용\s+복제본|read[- ]only\s+replica",
    "Auto Scaling": r"Auto\s+Scaling|자동\s+확장|자동으로\s+확장",
    "Multi-AZ": r"Multi[- ]?AZ|다중\s+AZ",
    "Global Table": r"Global\s+Table|전역\s+테이블",
    "VPC Endpoint": r"VPC\s+엔드포인트|VPC\s+Endpoint",
    "CloudFront + S3": r"CloudFront.*S3|S3.*CloudFront",
    "Fargate + EKS": r"Fargate.*EKS|EKS.*Fargate",
    "MSK managed Kafka": r"Managed\s+Streaming.*Kafka|Kafka.*Managed\s+Streaming|MSK",
    "Compute Savings Plan": r"Compute\s+Savings\s+Plan",
}

FEATURE_TRIGGERS = {
    "S3 RTC": "복제 완료 시간을 특정 시간 안에 보장하거나 모니터링해야 하는 경우",
    "Cross-Region Replication": "다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우",
    "DeletionPolicy Retain": "CloudFormation 스택 삭제 후에도 RDS/EBS 데이터를 보존해야 하는 경우",
    "Aurora Read Replica": "Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우",
    "Auto Scaling": "트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우",
    "Multi-AZ": "단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우",
    "Global Table": "DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우",
    "VPC Endpoint": "인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우",
    "CloudFront + S3": "정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우",
    "Fargate + EKS": "Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우",
    "MSK managed Kafka": "Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우",
    "Compute Savings Plan": "EC2, Fargate, Lambda 등 컴퓨팅 사용량이 장기간 반복되는 경우",
}


def normalize(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[\[\]{}()\"“”‘’,:;]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact(value: str, limit: int = 180) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."


def question_text(item: dict[str, Any]) -> str:
    return str(item.get("question", ""))


def answer_labels(item: dict[str, Any]) -> set[str]:
    values = item.get("answers") or [item.get("answer", "")]
    return {str(value).strip().upper() for value in values if value}


def correct_text(item: dict[str, Any]) -> str:
    labels = answer_labels(item)
    return " ".join(
        str(choice.get("text", ""))
        for choice in item.get("choices", [])
        if str(choice.get("label", "")).upper() in labels
    )


def extract_matches(text: str, patterns: dict[str, str]) -> list[str]:
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found


def build_dedup_groups(items: list[dict[str, Any]], threshold: float) -> list[list[int]]:
    normalized = [normalize(question_text(item)) for item in items]
    parent = list(range(len(items)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for left in range(len(items)):
        for right in range(left + 1, len(items)):
            if SequenceMatcher(None, normalized[left], normalized[right]).ratio() >= threshold:
                union(left, right)

    groups: dict[int, list[int]] = defaultdict(list)
    for index in range(len(items)):
        groups[find(index)].append(index)
    return [group for group in groups.values() if len(group) > 1]


def build_service_candidates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for service, (pattern, docs_url) in SERVICE_CATALOG.items():
        question_numbers = []
        answer_numbers = []
        features = Counter()
        answer_examples = []
        condition_examples = []

        for item in items:
            q_text = question_text(item)
            a_text = correct_text(item)
            if re.search(pattern, q_text, re.IGNORECASE):
                question_numbers.append(item["qNumber"])
            if re.search(pattern, a_text, re.IGNORECASE):
                answer_numbers.append(item["qNumber"])
                for feature in extract_matches(a_text, FEATURE_PATTERNS):
                    features[feature] += 1
                if len(answer_examples) < 5:
                    answer_examples.append({"qNumber": item["qNumber"], "text": compact(a_text)})
                if len(condition_examples) < 5:
                    condition_examples.append({"qNumber": item["qNumber"], "text": compact(q_text)})

        if question_numbers or answer_numbers:
            candidates.append(
                {
                    "service": service,
                    "officialDocs": docs_url,
                    "questionCount": len(question_numbers),
                    "answerCount": len(answer_numbers),
                    "questionNumbers": question_numbers,
                    "answerNumbers": answer_numbers,
                    "observedFeatures": [
                        {"name": name, "evidenceCount": count}
                        for name, count in features.most_common()
                    ],
                    "answerTriggers": [
                        {"feature": name, "condition": FEATURE_TRIGGERS[name]}
                        for name, _count in features.most_common()
                        if name in FEATURE_TRIGGERS
                    ][:8],
                    "conditionExamples": condition_examples,
                    "answerExamples": answer_examples,
                    "verification": "candidate_extracted_from_question_bank; verify_claims_against_official_docs",
                }
            )
    return sorted(candidates, key=lambda item: (-item["answerCount"], item["service"]))


def build_feature_candidates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for feature, pattern in FEATURE_PATTERNS.items():
        evidence = []
        for item in items:
            text = question_text(item) + " " + correct_text(item)
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append({"qNumber": item["qNumber"], "answer": item.get("answer", ""), "question": compact(question_text(item))})
        if evidence:
            output.append({"feature": feature, "evidenceCount": len(evidence), "evidence": evidence[:12]})
    return sorted(output, key=lambda item: (-item["evidenceCount"], item["feature"]))


def write_markdown(path: Path, service_candidates: list[dict[str, Any]], feature_candidates: list[dict[str, Any]], dedup_groups: list[list[int]], items: list[dict[str, Any]]) -> None:
    number_to_item = {item["qNumber"]: item for item in items}
    lines = [
        "# AWS 개념집 (1차 자동 생성)",
        "",
        "> 이 문서는 문제은행에서 반복 관찰된 서비스/기능/조건을 개념 후보로 정리한 초안입니다. 정답 암기만을 목적으로 하지 않고, 처음 보는 문제의 정답을 추론할 수 있도록 조건과 서비스의 관계를 보여줍니다.",
        "> 모든 항목의 공식 문서 링크를 함께 제공했지만, 덤프의 표현과 정답은 공식 문서 기준으로 별도 검증해야 합니다.",
        "",
        "## 범위와 검증 상태",
        "",
        f"- 입력 문항: {len(items)}개",
        f"- 80% 이상 유사 문항 그룹: {len(dedup_groups)}개",
        f"- 중복 제거 후 참고 문항 수: {len(items) - sum(len(group) - 1 for group in dedup_groups)}개",
        "- 상태: 자동 추출 후보 + 공식 AWS 문서 링크, 내용 검증은 항목별 확인 필요",
        "",
        "## 서비스별 개념 후보",
        "",
    ]

    for candidate in service_candidates:
        lines.extend(
            [
                f"### {candidate['service']}",
                f"공식 문서: {candidate['officialDocs']}",
                "",
                f"- 문제 등장: {candidate['questionCount']}개",
                f"- 정답 선택지 등장: {candidate['answerCount']}개",
            ]
        )
        if candidate["observedFeatures"]:
            lines.append("- 관찰된 기능/조합:")
            for feature in candidate["observedFeatures"][:8]:
                lines.append(f"  - {feature['name']} ({feature['evidenceCount']}개 문항)")
        if candidate.get("answerTriggers"):
            lines.append("- 출제 패턴 기반 연결 후보:")
            for trigger in candidate["answerTriggers"]:
                lines.append(f"  - {trigger['feature']} -> {trigger['condition']}")
        if candidate["conditionExamples"]:
            lines.append("- 문제 조건 예시:")
            for example in candidate["conditionExamples"][:3]:
                lines.append(f"  - Q{example['qNumber']}: {example['text']}")
        if candidate["answerExamples"]:
            lines.append("- 정답 구성 예시:")
            for example in candidate["answerExamples"][:3]:
                lines.append(f"  - Q{example['qNumber']}: {example['text']}")
        lines.extend([f"- 검증 상태: {candidate['verification']}", ""])

    lines.extend(["## 기능/조건 연결 후보", ""])
    for feature in feature_candidates:
        lines.append(f"### {feature['feature']}")
        lines.append(f"- 관찰 문항 수: {feature['evidenceCount']}개")
        for evidence in feature["evidence"][:5]:
            lines.append(f"- Q{evidence['qNumber']} / Answer {evidence['answer']}: {evidence['question']}")
        lines.append("")

    lines.extend(["## 중복 그룹", ""])
    for group in dedup_groups:
        q_numbers = [items[index]["qNumber"] for index in group]
        lines.append("- " + " / ".join(f"Q{q}" for q in q_numbers))
        for q_number in q_numbers:
            lines.append(f"  - Q{q_number}: {compact(number_to_item[q_number]['question'], 120)}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build AWS concept candidates and a dedup report from parsed questions")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dedup-threshold", type=float, default=0.80)
    args = parser.parse_args()

    items = json.loads(args.input.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    service_candidates = build_service_candidates(items)
    feature_candidates = build_feature_candidates(items)
    dedup_groups = build_dedup_groups(items, args.dedup_threshold)
    dedup_report = []
    for group in dedup_groups:
        dedup_report.append({"questions": [items[index]["qNumber"] for index in group], "keepSuggestion": items[group[0]]["qNumber"]})

    (args.output_dir / "service_candidates.json").write_text(json.dumps(service_candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output_dir / "feature_candidates.json").write_text(json.dumps(feature_candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output_dir / "dedup_groups.json").write_text(json.dumps(dedup_report, ensure_ascii=False, indent=2), encoding="utf-8")
    concept_payload = {"services": service_candidates, "features": feature_candidates}
    Path("viewer/concepts.data.js").write_text(
        "window.CONCEPT_BOOK = " + json.dumps(concept_payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    duplicate_numbers = {number for group in dedup_report for number in group["questions"][1:]}
    deduplicated = [item for item in items if item["qNumber"] not in duplicate_numbers]
    (args.output_dir / "questions.deduplicated.json").write_text(
        json.dumps(deduplicated, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (args.output_dir / "VERIFICATION.md").write_text(
        "# 개념집 검증 상태\n\n"
        "- 서비스별 공식 문서 링크는 AWS 공식 documentation URL로 기록했습니다.\n"
        "- 서비스/기능 후보와 문제-정답 연결은 현재 문제 JSON에서 자동 추출했습니다.\n"
        "- 이 실행 환경에서는 공식 문서 본문을 자동 대조하지 않았으므로, 각 개념의 최종 확정 전 링크를 열어 사실을 확인해야 합니다.\n"
        "- 덤프의 Answer는 원문 기준으로 보존했으며, 공식 문서와 다르면 별도 검토 대상으로 남겨야 합니다.\n",
        encoding="utf-8",
    )
    write_markdown(args.output_dir / "AWS_CONCEPT_BOOK.md", service_candidates, feature_candidates, dedup_groups, items)

    print(f"questions={len(items)}")
    print(f"services={len(service_candidates)}")
    print(f"features={len(feature_candidates)}")
    print(f"dedup_groups={len(dedup_groups)}")
    print(f"output={args.output_dir}")


if __name__ == "__main__":
    main()
