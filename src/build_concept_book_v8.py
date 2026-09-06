from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUESTIONS_INPUT = ROOT / "data" / "questions" / "questions.json"
DEFAULT_V7_HIGHLIGHTS_INPUT = ROOT / "viewer" / "pdf_highlights_v7.data.js"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "concepts"

# Extensive Catalog of AWS Services with official docs, regex pattern, and description triggers
SERVICE_CATALOG: dict[str, tuple[str, str]] = {
    "Amazon EC2": (
        r"Amazon\s+EC2|\bEC2\b|Elastic\s+Compute\s+Cloud",
        "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html",
    ),
    "Amazon S3": (
        r"Amazon\s+S3|\bS3\b|Simple\s+Storage\s+Service|S3\s+Glacier|S3\s+버킷",
        "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
    ),
    "AWS Lambda": (
        r"AWS\s+Lambda|\bLambda\b|람다",
        "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    ),
    "AWS Organizations": (
        r"AWS\s+Organizations|\bOrganizations\b|조직\s+단위|\bOU\b",
        "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html",
    ),
    "AWS IAM / IAM Identity Center": (
        r"\bIAM\b|IAM\s+Identity\s+Center|Identity\s+Center|\bSSO\b|Single\s+Sign-On",
        "https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html",
    ),
    "AWS Auto Scaling": (
        r"Auto\s+Scaling|자동\s+확장|Auto\s*Scaling\s*그룹",
        "https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html",
    ),
    "Amazon RDS": (
        r"Amazon\s+RDS|\bRDS\b|Relational\s+Database\s+Service",
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html",
    ),
    "Amazon Aurora": (
        r"Amazon\s+Aurora|\bAurora\b|Aurora\s+Global\s+Database|Aurora\s+Serverless",
        "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html",
    ),
    "Application Load Balancer (ALB)": (
        r"Application\s+Load\s+Balancer|\bALB\b|애플리케이션\s+로드\s*밸런서",
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html",
    ),
    "Network Load Balancer (NLB)": (
        r"Network\s+Load\s+Balancer|\bNLB\b|네트워크\s+로드\s*밸런서",
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html",
    ),
    "Gateway Load Balancer (GWLB)": (
        r"Gateway\s+Load\s+Balancer|\bGWLB\b|게이트웨이\s+로드\s*밸런서",
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html",
    ),
    "Elastic Load Balancing (ELB)": (
        r"Elastic\s+Load\s+Balancing|\bELB\b|로드\s*밸런서|Load\s+Balancer",
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html",
    ),
    "Amazon DynamoDB": (
        r"Amazon\s+DynamoDB|\bDynamoDB\b|DynamoDB\s+Global\s+Tables",
        "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html",
    ),
    "Amazon ECS": (
        r"Amazon\s+ECS|\bECS\b|Elastic\s+Container\s+Service",
        "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html",
    ),
    "Amazon Route 53": (
        r"Amazon\s+Route\s*53|Route\s*53|라우트\s*53",
        "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html",
    ),
    "AWS CloudWatch": (
        r"AWS\s+CloudWatch|CloudWatch|CloudWatch\s+Logs|CloudWatch\s+Alarms",
        "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html",
    ),
    "Amazon CloudFront": (
        r"Amazon\s+CloudFront|CloudFront|클라우드프론트",
        "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html",
    ),
    "AWS PrivateLink": (
        r"AWS\s+PrivateLink|PrivateLink|인터페이스\s+VPC\s+엔드포인트|Interface\s+VPC\s+endpoint|VPC\s+엔드포인트|VPC\s+Endpoint",
        "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html",
    ),
    "AWS CloudFormation": (
        r"AWS\s+CloudFormation|CloudFormation|Cloud\s+Formation",
        "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html",
    ),
    "AWS Direct Connect": (
        r"AWS\s+Direct\s+Connect|Direct\s+Connect|\bDX\b",
        "https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html",
    ),
    "Amazon EFS": (
        r"Amazon\s+EFS|\bEFS\b|Elastic\s+File\s+System",
        "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html",
    ),
    "Amazon Kinesis": (
        r"Amazon\s+Kinesis|Kinesis\s+Data\s+Streams|Kinesis\s+Data\s+Firehose|Kinesis\s+Data\s+Analytics",
        "https://docs.aws.amazon.com/streams/latest/dev/introduction.html",
    ),
    "Amazon EventBridge": (
        r"Amazon\s+EventBridge|EventBridge|CloudWatch\s+Events",
        "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html",
    ),
    "Amazon SNS": (
        r"Amazon\s+SNS|\bSNS\b|Simple\s+Notification\s+Service",
        "https://docs.aws.amazon.com/sns/latest/dg/welcome.html",
    ),
    "Amazon API Gateway": (
        r"Amazon\s+API\s+Gateway|API\s+Gateway",
        "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html",
    ),
    "AWS Fargate": (
        r"AWS\s+Fargate|\bFargate\b|파게이트",
        "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html",
    ),
    "Amazon SQS": (
        r"Amazon\s+SQS|\bSQS\b|Simple\s+Queue\s+Service",
        "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html",
    ),
    "Amazon Athena": (
        r"Amazon\s+Athena|\bAthena\b|아테나",
        "https://docs.aws.amazon.com/athena/latest/ug/what-is.html",
    ),
    "AWS KMS": (
        r"AWS\s+KMS|\bKMS\b|Key\s+Management\s+Service|KMS\s+키",
        "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html",
    ),
    "AWS Site-to-Site VPN": (
        r"Site-to-Site\s+VPN|Client\s+VPN|\bVPN\b|VPN\s+연결",
        "https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html",
    ),
    "AWS DMS": (
        r"Database\s+Migration\s+Service|\bDMS\b",
        "https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html",
    ),
    "AWS WAF": (
        r"AWS\s+WAF|\bWAF\b",
        "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html",
    ),
    "AWS DataSync": (
        r"AWS\s+DataSync|DataSync|데이터싱크",
        "https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html",
    ),
    "Amazon FSx": (
        r"Amazon\s+FSx|\bFSx\b|FSx\s+for\s+Windows|FSx\s+for\s+Lustre|FSx\s+for\s+ONTAP",
        "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is-fsx.html",
    ),
    "Amazon EKS": (
        r"Amazon\s+EKS|\bEKS\b|Elastic\s+Kubernetes\s+Service",
        "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html",
    ),
    "AWS Secrets Manager": (
        r"Secrets\s+Manager|시크릿\s+매니저",
        "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html",
    ),
    "AWS Backup": (
        r"AWS\s+Backup|\bBackup\b",
        "https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html",
    ),
    "AWS Control Tower": (
        r"AWS\s+Control\s+Tower|Control\s+Tower|컨트롤\s+타워",
        "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html",
    ),
    "AWS RAM": (
        r"Resource\s+Access\s+Manager|\bRAM\b",
        "https://docs.aws.amazon.com/ram/latest/userguide/what-is.html",
    ),
    "AWS Systems Manager (SSM)": (
        r"Systems\s+Manager|\bSSM\b|Parameter\s+Store|Session\s+Manager|Patch\s+Manager",
        "https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html",
    ),
    "Amazon EBS": (
        r"Amazon\s+EBS|\bEBS\b|Elastic\s+Block\s+Store",
        "https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html",
    ),
    "AWS Elastic Beanstalk": (
        r"Elastic\s+Beanstalk|\bBeanstalk\b",
        "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html",
    ),
    "AWS Transit Gateway": (
        r"Transit\s+Gateway|\bTGW\b|전송\s+게이트웨이",
        "https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html",
    ),
    "AWS Config": (
        r"AWS\s+Config|\bConfig\b",
        "https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html",
    ),
    "AWS CloudTrail": (
        r"AWS\s+CloudTrail|CloudTrail",
        "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html",
    ),
    "Amazon QuickSight": (
        r"Amazon\s+QuickSight|QuickSight|퀵사이트",
        "https://docs.aws.amazon.com/quicksight/latest/user/welcome.html",
    ),
    "Amazon Redshift": (
        r"Amazon\s+Redshift|\bRedshift\b",
        "https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html",
    ),
    "AWS Glue": (
        r"AWS\s+Glue|\bGlue\b|글루",
        "https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html",
    ),
    "AWS Global Accelerator": (
        r"Global\s+Accelerator|글로벌\s+액셀러레이터",
        "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html",
    ),
    "AWS Storage Gateway": (
        r"Storage\s+Gateway|Volume\s+Gateway|File\s+Gateway|Tape\s+Gateway",
        "https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html",
    ),
    "AWS Step Functions": (
        r"AWS\s+Step\s+Functions|Step\s+Functions|스텝\s+방식",
        "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
    ),
    "Amazon ElastiCache": (
        r"Amazon\s+ElastiCache|\bElastiCache\b|\bRedis\b|\bMemcached\b",
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html",
    ),
    "AWS SCT": (
        r"Schema\s+Conversion\s+Tool|\bSCT\b",
        "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html",
    ),
    "Amazon SageMaker": (
        r"Amazon\s+SageMaker|\bSageMaker\b",
        "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html",
    ),
    "Amazon EMR": (
        r"Amazon\s+EMR|\bEMR\b",
        "https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview.html",
    ),
    "AWS Batch": (
        r"AWS\s+Batch|\bBatch\b",
        "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html",
    ),
    "AWS Shield": (
        r"AWS\s+Shield|\bShield\b",
        "https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html",
    ),
    "AWS Inspector": (
        r"AWS\s+Inspector|Amazon\s+Inspector|\bInspector\b",
        "https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html",
    ),
    "Amazon Cognito": (
        r"Amazon\s+Cognito|\bCognito\b|코그니토",
        "https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html",
    ),
    "Amazon OpenSearch": (
        r"Amazon\s+OpenSearch|OpenSearch|Elasticsearch",
        "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html",
    ),
    "AWS Application Migration Service (MGN)": (
        r"Application\s+Migration\s+Service|\bMGN\b",
        "https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html",
    ),
    "AWS GuardDuty": (
        r"AWS\s+GuardDuty|GuardDuty|가드듀티",
        "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html",
    ),
    "AWS Security Hub": (
        r"AWS\s+Security\s+Hub|Security\s+Hub",
        "https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html",
    ),
    "Amazon MSK": (
        r"Amazon\s+MSK|\bMSK\b|Managed\s+Streaming\s+for\s+Apache\s+Kafka",
        "https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html",
    ),
    "AWS Network Firewall": (
        r"Network\s+Firewall|네트워크\s+방화벽",
        "https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html",
    ),
    "AWS Macie": (
        r"Amazon\s+Macie|\bMacie\b",
        "https://docs.aws.amazon.com/macie/latest/userguide/what-is-macie.html",
    ),
    "AWS AppStream 2.0 / Amazon WorkSpaces": (
        r"AppStream|WorkSpaces",
        "https://docs.aws.amazon.com/appstream2/latest/developerguide/what-is-appstream.html",
    ),
    "AWS Transfer Family": (
        r"Transfer\s+Family|AWS\s+Transfer",
        "https://docs.aws.amazon.com/transfer/latest/userguide/what-is-transfer-family.html",
    ),
    "AWS Cost Explorer / Budgets": (
        r"Cost\s+Explorer|AWS\s+Budgets|Savings\s+Plans|비용\s+탐색기",
        "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html",
    ),
}

ANSWER_TRIGGERS: dict[str, str] = {
    "Application Load Balancer (ALB)": "HTTP/HTTPS (Layer 7) 라우팅, 경로/호스트 기반 분산, AWS WAF 연동 및 SSL/TLS 오프로딩 요구 시 정답 검토",
    "Network Load Balancer (NLB)": "초고속 초저지연, 고정 IP(Elastic IP) 필요, TCP/UDP (Layer 4) 트래픽, PrivateLink 엔드포인트 서비스 구성 시 정답 검토",
    "Gateway Load Balancer (GWLB)": "서드파티 가상 네트워크 어플라이언스(방화벽/IDS/IPS)로 트래픽을 투명하게 라우팅 및 검사할 때 정답 검토",
    "Amazon S3": "대규모 정적 데이터/객체 저장, 내구성 99.999999999%, S3 Lifecycle, Cross-Region Replication(CRR) 요건 시 정답 검토",
    "AWS Lambda": "서버리스 이벤트 기반 코드 실행, 인프라 관리 부담 최소화, 밀리초 단위 자동 스케일링 필요 시 정답 검토",
    "AWS PrivateLink": "인터넷을 거치지 않고 VPC 간 또는 AWS 서비스 간 사설 IP(인터페이스 엔드포인트)로 통신 시 정답 검토",
    "AWS Transit Gateway": "수많은 VPC와 온프레미스 네트워크를 중앙 허브로 상호 연결하여 네트워크 토폴로지 단순화 시 정답 검토",
    "AWS Direct Connect": "온프레미스와 AWS 간의 고전용 사설 회선 연결, 안정적인 대역폭 및 높은 보안 요건 시 정답 검토",
    "Amazon Aurora": "PostgreSQL/MySQL 호환 관리형 DB, 최대 15개 Read Replica, Read Replica Auto Scaling, Aurora Global Database 구성 시 정답 검토",
    "Amazon DynamoDB": "밀리초 미만 지연시간의 NoSQL Key-Value 데이터베이스, Global Tables로 다중 리전 활성-활성 구성 시 정답 검토",
    "AWS IAM / IAM Identity Center": "다중 계정 환경에서 중앙 집중식 SSO(단일 로그온) 및 사용자/권한 제어 시 정답 검토",
    "AWS Organizations": "여러 AWS 계정을 중앙 통합 관리, SCP(성분 제어 정책) 적용, 일괄 청구 구성 시 정답 검토",
    "AWS Auto Scaling": "트래픽 변화 및 예측 수요에 따라 EC2/컴퓨팅 용량을 자동으로 증설/감축 시 정답 검토",
    "AWS CloudFormation": "Infrastructure as Code(IaC)로 템플릿 기반 자동 배포 및 스택 관리 시 정답 검토",
    "Amazon CloudFront": "글로벌 엣지 로케이션 기반 정적/동적 콘텐츠 Caching 및 CDN 가속 시 정답 검토",
    "Amazon Route 53": "글로벌 DNS 라우팅, Latency/Failover/Geolocation 라우팅 정책 및 Health Check 요구 시 정답 검토",
    "AWS KMS": "데이터 암호화 키 중앙 관리, Envelope Encryption, FIPS 140-2 컴플라이언스 시 정답 검토",
    "AWS Secrets Manager": "DB 암호, API 키 등 자격 증명의 보안 저장 및 자동 순환(Rotation) 요구 시 정답 검토",
    "AWS Systems Manager (SSM)": "인스턴스 패치 관리, Parameter Store, Bastion 없이 보안 셸 접속(Session Manager) 필요 시 정답 검토",
    "AWS WAF": "L7 웹 애플리케이션 방화벽, SQL Injection, XSS 차단, IP 차단 규칙 설정 시 정답 검토",
    "AWS Backup": "RDS, EBS, EFS, DynamoDB 등의 백업 중앙 관리 및 일정/보존 정책 자동화 요구 시 정답 검토",
    "AWS Control Tower": "가드레일 및 Landing Zone 기반 다중 계정 환경 자동 구축 및 관리 시 정답 검토",
    "Amazon FSx": "Windows File Server(SMB) 또는 Lustre/ONTAP 고성능 파일 시스템 요구 시 정답 검토",
    "AWS DataSync": "온프레미스와 S3/EFS/FSx 간 대용량 데이터 고속 자동 이동 및 동기화 요구 시 정답 검토",
    "AWS DMS": "동종/이종 데이터베이스를 다운타임 최소화하여 AWS로 이관 시 정답 검토",
}


def compact(text: str, limit: int = 160) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def parse_v7_highlights(v7_file_path: Path) -> list[dict[str, Any]]:
    content = v7_file_path.read_text(encoding="utf-8")
    if "DEFAULT_PDF_HIGHLIGHTS_V7 = " in content:
        raw_json = content.split("DEFAULT_PDF_HIGHLIGHTS_V7 = ")[1].rstrip(";\n")
        return json.loads(raw_json)
    return json.loads(content)


def load_questions(questions_path: Path) -> list[dict[str, Any]]:
    return json.loads(questions_path.read_text(encoding="utf-8"))


def build_concept_v8_data(questions: list[dict[str, Any]], v7_highlights: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q_map = {q["qNumber"]: q for q in questions}

    services_data = []

    for service_name, (pattern, docs_url) in SERVICE_CATALOG.items():
        pat = re.compile(pattern, re.IGNORECASE)

        question_hl_qnums = set()
        answer_hl_qnums = set()
        total_hl_qnums = set()

        observed_phrases = Counter()
        condition_examples = []
        answer_examples = []

        q_text_match_qnums = set()
        a_text_match_qnums = set()

        # Iterate over v7 highlights
        for item in v7_highlights:
            q_num = item["qNumber"]
            q_obj = q_map.get(q_num)
            if not q_obj:
                continue

            q_text = str(q_obj.get("question", ""))
            answers = q_obj.get("answers") or [q_obj.get("answer", "")]
            answer_labels = {str(a).strip().upper() for a in answers if a}
            
            correct_choice_texts = [
                str(choice.get("text", ""))
                for choice in q_obj.get("choices", [])
                if str(choice.get("label", "")).upper() in answer_labels
            ]
            a_text = " ".join(correct_choice_texts)

            # Check full text match
            if pat.search(q_text):
                q_text_match_qnums.add(q_num)
            if pat.search(a_text):
                a_text_match_qnums.add(q_num)

            # Check highlight matches
            has_q_hl = False
            has_a_hl = False

            for hl in item.get("highlights", []):
                htext = hl.get("text", "").strip()
                if not htext:
                    continue

                if pat.search(htext):
                    total_hl_qnums.add(q_num)
                    observed_phrases[htext] += 1

                    labels = hl.get("choiceLabels", [])
                    if labels and any(str(l).upper() in answer_labels for l in labels):
                        has_a_hl = True
                    elif labels:
                        pass
                    else:
                        has_q_hl = True

            if has_q_hl:
                question_hl_qnums.add(q_num)
            if has_a_hl:
                answer_hl_qnums.add(q_num)

            # Examples collection
            if has_a_hl or (q_num in a_text_match_qnums and len(answer_examples) < 5):
                if len(answer_examples) < 5 and a_text:
                    answer_examples.append({"qNumber": q_num, "text": compact(a_text)})

            if has_q_hl or (q_num in q_text_match_qnums and len(condition_examples) < 5):
                if len(condition_examples) < 5 and q_text:
                    condition_examples.append({"qNumber": q_num, "text": compact(q_text)})

        total_hl_count = len(total_hl_qnums)
        answer_hl_count = len(answer_hl_qnums)
        question_hl_count = len(question_hl_qnums)

        if total_hl_count == 0 and len(a_text_match_qnums) == 0 and len(q_text_match_qnums) == 0:
            continue

        # Top observed highlight phrases
        top_phrases = [
            {"phrase": phrase, "count": count}
            for phrase, count in observed_phrases.most_common(12)
        ]

        trigger_hint = ANSWER_TRIGGERS.get(service_name, "문제 조건과 최적의 인프라 구성 요건을 만족할 때 정답 검토")

        services_data.append({
            "service": service_name,
            "officialDocs": docs_url,
            "answerTrigger": trigger_hint,
            "answerHighlightCount": answer_hl_count,
            "questionHighlightCount": question_hl_count,
            "totalHighlightCount": total_hl_count,
            "answerTextMatchCount": len(a_text_match_qnums),
            "questionTextMatchCount": len(q_text_match_qnums),
            "answerHighlightQNums": sorted(list(answer_hl_qnums)),
            "questionHighlightQNums": sorted(list(question_hl_qnums)),
            "totalHighlightQNums": sorted(list(total_hl_qnums)),
            "observedPhrases": top_phrases,
            "conditionExamples": condition_examples[:5],
            "answerExamples": answer_examples[:5],
        })

    # Sort by answer highlight count descending, then total highlight count descending, then service name
    services_data.sort(
        key=lambda item: (
            -item["answerHighlightCount"],
            -item["totalHighlightCount"],
            -item["answerTextMatchCount"],
            item["service"],
        )
    )

    return services_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Concept Book v8 based on v7 PDF Highlights")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_INPUT)
    parser.add_argument("--v7-highlights", type=Path, default=DEFAULT_V7_HIGHLIGHTS_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    questions = load_questions(args.questions)
    v7_highlights = parse_v7_highlights(args.v7_highlights)

    services_v8 = build_concept_v8_data(questions, v7_highlights)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "service_candidates_v8.json").write_text(
        json.dumps(services_v8, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    payload = {"services": services_v8}
    (ROOT / "viewer" / "concepts_v8.data.js").write_text(
        "window.CONCEPT_BOOK_V8 = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    print(f"Successfully generated Concept Book v8 data with {len(services_v8)} AWS services!")


if __name__ == "__main__":
    main()
