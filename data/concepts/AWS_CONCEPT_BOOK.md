# AWS 개념집 (1차 자동 생성)

> 이 문서는 문제은행에서 반복 관찰된 서비스/기능/조건을 개념 후보로 정리한 초안입니다. 정답 암기만을 목적으로 하지 않고, 처음 보는 문제의 정답을 추론할 수 있도록 조건과 서비스의 관계를 보여줍니다.
> 모든 항목의 공식 문서 링크를 함께 제공했지만, 덤프의 표현과 정답은 공식 문서 기준으로 별도 검증해야 합니다.

## 범위와 검증 상태

- 입력 문항: 643개
- 80% 이상 유사 문항 그룹: 14개
- 중복 제거 후 참고 문항 수: 629개
- 상태: 자동 추출 후보 + 공식 AWS 문서 링크, 내용 검증은 항목별 확인 필요

## 서비스별 개념 후보

### Amazon S3
공식 문서: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

- 문제 등장: 111개
- 정답 선택지 등장: 139개
- 관찰된 기능/조합:
  - CloudFront + S3 (20개 문항)
  - Cross-Region Replication (7개 문항)
  - Auto Scaling (5개 문항)
  - VPC Endpoint (5개 문항)
  - Aurora Read Replica (2개 문항)
  - S3 RTC (1개 문항)
  - Fargate + EKS (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - S3 RTC -> 복제 완료 시간을 특정 시간 안에 보장하거나 모니터링해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q6: 소매 회사는 비즈니스 파트너인 다른 회사에 일련의 데이터 파일을 제공해야 합니다. 이러한 파일은 소매 회사에 속한 계정 A의 Amazon S3 버킷에 저장됩니다. 비즈니스 파트너 회사는 IAM 사용자 중 하나인 User_DataProcessor가 자체 AWS 계정(계정 B)에서 파일에 액세스하기를 원합니다. User...
  - Q10: 소매 회사는 AWS에서 전자 상거래 애플리케이션을 운영하고 있습니다. 애플리케이션은 ALB(Application Load Balancer) 뒤의 Amazon EC2 인스턴스에서 실행됩니다. 이 회사는 Amazon RDS DB 인스턴스를 데이터베이스 백엔드로 사용합니다. Amazon CloudFront 는 ALB를 가...
  - Q14: 한 회사가 Application Load Balancer 뒤에 있는 Auto Scaling 그룹의 여러 Amazon EC2 인스턴스에서 애플리케이션을 실행하고 있습니다. 애플리케이션의 부하는 하루 종일 달라지며 EC2 인스턴스는 정기적으로 확장 및 축소됩니다. EC2 인스턴스의 로그 파일은 15분마다 중앙 Amazo...
- 정답 구성 예시:
  - Q6: 계정 A에서 S3 버킷 정책을 다음과 같이 설정합니다. 계정 B에서 User_DataProcessor의 권한을 다음과 같이 설정합니다.
  - Q10: Amazon S3 버킷을 생성합니다. 정적 웹 페이지를 호스팅하도록 S3 버킷을 구성합니다. 사용자 지정 오류 페이지를 Amazon S3에 업로드합니다. CloudFront 사용자 지정 오류 페이지를 구성하여 사용자 지정 오류 응답을 추가합니다. 공개적으로 액세스할 수 있는 웹 페이지를 가리키도록 DNS 레코드를 수...
  - Q14: 로그 파일을 Amazon S3 에 복사하는 스크립트로 AWS Systems Manager 문서를 생성합니다. Auto Scaling 그룹에서 수명 주기 이벤트를 감지하는 Auto Scaling 수명 주기 후크 및 Amazon EventBridge 규칙을 생성합니다. autoscaling:EC2_INSTANCE_TER...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Lambda
공식 문서: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html

- 문제 등장: 64개
- 정답 선택지 등장: 106개
- 관찰된 기능/조합:
  - Aurora Read Replica (5개 문항)
  - CloudFront + S3 (4개 문항)
  - Auto Scaling (2개 문항)
  - VPC Endpoint (2개 문항)
  - Global Table (1개 문항)
  - Cross-Region Replication (1개 문항)
  - Multi-AZ (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
  - Global Table -> DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
- 문제 조건 예시:
  - Q2: 한 회사에서 REST 기반 API를 통해 여러 고객에게 날씨 데이터를 제공하고 있습니다. API 는 Amazon API Gateway 에서 호스팅되며 각 API 작업에 대해 서로 다른 AWS Lambda 함수와 통합됩니다. 이 회사는 DNS에 Amazon Route 53을 사용하고 weather.example.com...
  - Q5: 회사는 온프레미스에서 호스팅하는 애플리케이션에서 메타데이터를 수집하기 위해 서비스를 사용합니다. TV 및 인터넷 라디오와 같은 소비자 장치는 애플리케이션에 액세스합니다. 많은 구형 장치는 특정 HTTP 헤더를 지원하지 않으며 이러한 헤더가 응답에 있을 때 오류를 표시합니다. 회사는 User-Agent 헤더로 회사에서...
  - Q8: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
- 정답 구성 예시:
  - Q2: 다른 리전에 새 API Gateway API 및 Lambda 함수를 배포합니다. Route 53 DNS 레코드를 장애 조치 레코드로 변경합니다. 대상 상태 모니터링을 활성화합니다. DynamoDB 테이블을 전역 테이블로 변환합니다.
  - Q5: 메타데이터 서비스를 위한 Amazon CloudFront 배포를 생성합니다. Application Load Balancer(ALB)를 생성합니다. 요청을 ALB로 전달하도록 CloudFront 배포를 구성합니다. 각 요청 유형에 대해 올바른 Lambda 함수를 호출하도록 ALB를 구성합니다. User -Agent 헤...
  - Q8: 백업 리전에서 AWS Lambda 함수를 생성하여 읽기 전용 복제본을 승격하고 Auto Scaling 그룹 값을 수정합니다. 웹 애플리케이션을 모니터링하고 상태 확인 상태가 비정상일 때 Lambda 함수에 Amazon Simple Notification Service(Amazon SNS) 알림을 보내는 상태 확인으로...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon EC2
공식 문서: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html

- 문제 등장: 212개
- 정답 선택지 등장: 85개
- 관찰된 기능/조합:
  - Auto Scaling (23개 문항)
  - Aurora Read Replica (6개 문항)
  - Multi-AZ (5개 문항)
  - CloudFront + S3 (1개 문항)
  - Global Table (1개 문항)
  - Cross-Region Replication (1개 문항)
  - VPC Endpoint (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Global Table -> DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
- 문제 조건 예시:
  - Q9: 한 회사가 단일 Amazon EC2 인스턴스에서 중요한 애플리케이션을 호스팅하고 있습니다. 이 애플리케이션은 인 메모리 데이터 스토어를 위해 Redis 단일 노드 클러스터용 Amazon ElastiCache를 사용합니다. 이 애플리케이션은 관계형 데이터베이스에 Amazon RDS for MariaDB DB 인스턴스를...
  - Q13: 회사는 서버에 대한 패치 프로세스를 구현해야 합니다. 온프레미스 서버와 Amazon EC2 인스턴스는 다양한 도구를 사용하여 패치를 수행합니다. 관리에는 모든 서버 및 인스턴스의 패치 상태를 보여주는 단일 보고서가 필요합니다. 이러한 요구 사항을 충족하기 위해 솔루션 설계자는 어떤 조치를 취해야 합니까?
  - Q24: 회사는 고정 포트에서 TCP를 사용하여 액세스할 새로운 서비스를 개발하고 있습니다. 솔루션 설계자는 서비스의 가용성이 높고 가용성 영역 전체에 중복성이 있으며 공개적으로 액세스할 수 있는 DNS 이름 my.service.com을 사용하여 액세스할 수 있는지 확인해야 합니다. 다른 회사에서 허용 목록에 주소를 추가할...
- 정답 구성 예시:
  - Q9: Elastic Load Balancer를 사용하여 여러 EC2 인스턴스에 트래픽을 분산합니다. EC2 인스턴스가 최소 용량이 인스턴스 2개인 Auto Scaling 그룹의 일부인지 확인합니다. 두 가용 영역에 걸쳐 확장되는 다중 AZ 배포를 생성하도록 DB 인스턴스를 수정합니다. Redis 클러스터용 ElastiCa...
  - Q13: AWS Systems Manager를 사용하여 온프레미스 서버 및 EC2 인스턴스에서 패치를 관리합니다. Systems Manager를 사용하여 패치 규정 준수 보고서를 생성합니다.
  - Q24: 서비스에 대한 Amazon EC2 인스턴스를 생성합니다. 각 가용 영역에 대해 하나의 탄력적 IP 주소를 생성합니다. NLB(Network Load Balancer) 를 생성하고 할당된 TCP 포트를 노출합니다. 각 가용 영역의 NLB에 탄력적 IP 주소를 할당합니다. 대상 그룹을 생성하고 EC2 인스턴스를 NLB에...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon Aurora
공식 문서: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html

- 문제 등장: 28개
- 정답 선택지 등장: 45개
- 관찰된 기능/조합:
  - Auto Scaling (12개 문항)
  - Aurora Read Replica (9개 문항)
  - CloudFront + S3 (3개 문항)
  - Multi-AZ (2개 문항)
  - VPC Endpoint (1개 문항)
  - Global Table (1개 문항)
  - Cross-Region Replication (1개 문항)
  - Compute Savings Plan (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
  - Global Table -> DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
  - Compute Savings Plan -> EC2, Fargate, Lambda 등 컴퓨팅 사용량이 장기간 반복되는 경우
- 문제 조건 예시:
  - Q4: 회사는 온프레미스 데이터 센터에서 2계층 웹 기반 애플리케이션을 실행하고 있습니다. 애플리케이션 계층은 상태 저장 애플리케이션을 실행하는 단일 서버로 구성됩니다. 애플리케이션은 별도의 서버에서 실행되는 PostgreSQL 데이터베이스에 연결됩니다. 애플리케이션의 사용자 기반이 크게 성장할 것으로 예상되므로 회사는 애...
  - Q37: 회사는 온프레미스 환경에서 3계층 웹 애플리케이션을 호스팅하고 있습니다. 최근 트래픽 급증으로 인해 가동 중지 시간이 발생하고 재정적으로 상당한 영향을 받았기 때문에 회사 경영진은 애플리케이션을 AWS로 이전하도록 명령했습니다. 애플리케이션은 .NET으로 작성되었으며 MySQL 데이터베이스에 종속됩니다. 솔루션 설계...
  - Q48: 솔루션 설계자는 Amazon API Gateway 지역 엔드포인트와 AWS Lambda 함수를 사용하는 웹 애플리케이션을 개발했습니다. 웹 애플리케이션의 소비자는 모두 애플리케이션이 배포될 AWS 리전에 가깝습니다. Lambda 함수는 Amazon Aurora MySQL 데이터베이스만 쿼리합니다. 솔루션 설계자는 3...
- 정답 구성 예시:
  - Q4: Aurora 복제본에 대해 Aurora Auto Scaling 을 활성화합니다. 라운드 로빈 라우팅 및 고정 세션이 활성화된 Application Load Balancer를 사용하십시오.
  - Q37: AWS CloudFormation 을 사용하여 3개의 가용 영역에 걸쳐 있는 Amazon EC2 Auto Scaling 그룹 앞에 Application Load Balancer(ALB) 가 포함된 스택을 시작합니다. 스택은 삭제 유지 정책을 사용하여 Amazon Aurora MySQL DB 클러스터의 다중 AZ 배포...
  - Q48: RDS Proxy를 사용하여 Aurora 데이터베이스의 리더 엔드포인트에 대한 연결 풀을 설정합니다. 이벤트 핸들러 외부의 Lambda 함수에서 데이터베이스 연결을 여는 코드를 이동합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Elastic Load Balancing
공식 문서: https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html

- 문제 등장: 63개
- 정답 선택지 등장: 45개
- 관찰된 기능/조합:
  - Auto Scaling (22개 문항)
  - Aurora Read Replica (5개 문항)
  - CloudFront + S3 (3개 문항)
  - Multi-AZ (2개 문항)
  - Global Table (1개 문항)
  - Fargate + EKS (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - Global Table -> DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q4: 회사는 온프레미스 데이터 센터에서 2계층 웹 기반 애플리케이션을 실행하고 있습니다. 애플리케이션 계층은 상태 저장 애플리케이션을 실행하는 단일 서버로 구성됩니다. 애플리케이션은 별도의 서버에서 실행되는 PostgreSQL 데이터베이스에 연결됩니다. 애플리케이션의 사용자 기반이 크게 성장할 것으로 예상되므로 회사는 애...
  - Q5: 회사는 온프레미스에서 호스팅하는 애플리케이션에서 메타데이터를 수집하기 위해 서비스를 사용합니다. TV 및 인터넷 라디오와 같은 소비자 장치는 애플리케이션에 액세스합니다. 많은 구형 장치는 특정 HTTP 헤더를 지원하지 않으며 이러한 헤더가 응답에 있을 때 오류를 표시합니다. 회사는 User-Agent 헤더로 회사에서...
  - Q7: 회사는 Amazon EC2 인스턴스에서 기존 웹 애플리케이션을 실행하고 있습니다. 회사는 애플리케이션을 컨테이너에서 실행되는 마이크로서비스로 리팩터링해야 합니다. 애플리케이션의 별도 버전은 생산 및 테스트라는 두 가지 환경에 존재합니다. 애플리케이션에 대한 부하는 가변적이지만 최소 부하와 최대 부하가 알려져 있습니다...
- 정답 구성 예시:
  - Q4: Aurora 복제본에 대해 Aurora Auto Scaling 을 활성화합니다. 라운드 로빈 라우팅 및 고정 세션이 활성화된 Application Load Balancer를 사용하십시오.
  - Q5: 메타데이터 서비스를 위한 Amazon CloudFront 배포를 생성합니다. Application Load Balancer(ALB)를 생성합니다. 요청을 ALB로 전달하도록 CloudFront 배포를 구성합니다. 각 요청 유형에 대해 올바른 Lambda 함수를 호출하도록 ALB를 구성합니다. User -Agent 헤...
  - Q7: 컨테이너 이미지를 Amazon Elastic Container Registry(Amazon ECR) 에 업로드합니다. 예상 로드를 처리하기 위해 Fargate 시작 유형을 사용하여 2개의 자동 확장 Amazon Elastic Container Service(Amazon ECS) 클러스터를 구성합니다. ECR 이미지에...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon RDS
공식 문서: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html

- 문제 등장: 57개
- 정답 선택지 등장: 43개
- 관찰된 기능/조합:
  - Aurora Read Replica (13개 문항)
  - Auto Scaling (4개 문항)
  - DeletionPolicy Retain (2개 문항)
  - Multi-AZ (2개 문항)
  - Cross-Region Replication (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - DeletionPolicy Retain -> CloudFormation 스택 삭제 후에도 RDS/EBS 데이터를 보존해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
- 문제 조건 예시:
  - Q48: 솔루션 설계자는 Amazon API Gateway 지역 엔드포인트와 AWS Lambda 함수를 사용하는 웹 애플리케이션을 개발했습니다. 웹 애플리케이션의 소비자는 모두 애플리케이션이 배포될 AWS 리전에 가깝습니다. Lambda 함수는 Amazon Aurora MySQL 데이터베이스만 쿼리합니다. 솔루션 설계자는 3...
  - Q50: 회사에서 데이터 분석 환경을 온프레미스에서 AWS로 마이그레이션하려고 합니다. 환경은 두 개의 간단한 Node.js 애플리케이션으로 구성됩니다. 애플리케이션 중 하나는 센서 데이터를 수집하여 MySQL 데이터베이스에 로드합니다. 다른 응용 프로그램은 데이터를 보고서로 집계합니다. 집계 작업이 실행될 때 일부 로드 작...
  - Q72: 애플리케이션이 us-east-1 리전에서 Amazon RDS for MySQL 다중 AZ DB 인스턴스를 사용하고 있습니다. 장애 조치 테스트 후 애플리케이션에서 데이터베이스에 대한 연결이 끊어져 연결을 다시 설정할 수 없습니다. 애플리케이션을 다시 시작한 후 애플리케이션이 연결을 다시 설정했습니다. 솔루션 설계자는...
- 정답 구성 예시:
  - Q48: RDS Proxy를 사용하여 Aurora 데이터베이스의 리더 엔드포인트에 대한 연결 풀을 설정합니다. 이벤트 핸들러 외부의 Lambda 함수에서 데이터베이스 연결을 여는 코드를 이동합니다.
  - Q50: Amazon Aurora MySQL 데이터베이스를 설정합니다. AWS Database Migration Service(AWS DMS)를 사용하여 온프레미스 데이터베이스에서 Aurora로 연속 데이터 복제를 수행합니다. Aurora MySQL 데이터베이스용 Aurora 복제본을 생성하고 집계 작업을 이동하여 Auror...
  - Q72: RDS 프록시를 생성합니다. 기존 RDS 엔드포인트를 대상으로 구성합니다. RDS 프록시 엔드포인트를 가리키도록 애플리케이션의 연결 설정을 업데이트합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon Route 53
공식 문서: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html

- 문제 등장: 31개
- 정답 선택지 등장: 38개
- 관찰된 기능/조합:
  - Auto Scaling (10개 문항)
  - Global Table (4개 문항)
  - Aurora Read Replica (4개 문항)
  - CloudFront + S3 (2개 문항)
  - Multi-AZ (1개 문항)
  - Cross-Region Replication (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Global Table -> DynamoDB 데이터를 여러 리전에서 읽고 써야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
- 문제 조건 예시:
  - Q1: 회사는 하이브리드 DNS 솔루션을 설계해야 합니다. 이 솔루션은 VPC 내에 저장된 리소스에 대해 도메인 cloud.example.com에 대해 Amazon Route 53 프라이빗 호스팅 영역을 사용합니다. 회사에는 다음과 같은 DNS 확인 요구 사항이 있습니다. 온프레미스 시스템은 cloud.example.com...
  - Q2: 한 회사에서 REST 기반 API를 통해 여러 고객에게 날씨 데이터를 제공하고 있습니다. API 는 Amazon API Gateway 에서 호스팅되며 각 API 작업에 대해 서로 다른 AWS Lambda 함수와 통합됩니다. 이 회사는 DNS에 Amazon Route 53을 사용하고 weather.example.com...
  - Q8: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
- 정답 구성 예시:
  - Q1: 프라이빗 호스팅 영역을 모든 VPC에 연결합니다. 공유 서비스 VPC에서 Route 53 인바운드 해석기를 생성합니다. 모든 VPC를 전송 게이트웨이에 연결하고 인바운드 해석기를 가리키는 cloud.example.com에 대한 온프레미스 DNS 서버에서 전달 규칙을 생성합니다.
  - Q2: 다른 리전에 새 API Gateway API 및 Lambda 함수를 배포합니다. Route 53 DNS 레코드를 장애 조치 레코드로 변경합니다. 대상 상태 모니터링을 활성화합니다. DynamoDB 테이블을 전역 테이블로 변환합니다.
  - Q8: 백업 리전에서 AWS Lambda 함수를 생성하여 읽기 전용 복제본을 승격하고 Auto Scaling 그룹 값을 수정합니다. 웹 애플리케이션을 모니터링하고 상태 확인 상태가 비정상일 때 Lambda 함수에 Amazon Simple Notification Service(Amazon SNS) 알림을 보내는 상태 확인으로...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon CloudFront
공식 문서: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html

- 문제 등장: 28개
- 정답 선택지 등장: 32개
- 관찰된 기능/조합:
  - CloudFront + S3 (19개 문항)
  - Auto Scaling (5개 문항)
  - Cross-Region Replication (2개 문항)
  - Aurora Read Replica (1개 문항)
  - Fargate + EKS (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Cross-Region Replication -> 다른 AWS 리전에 S3 객체를 자동 복제해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q5: 회사는 온프레미스에서 호스팅하는 애플리케이션에서 메타데이터를 수집하기 위해 서비스를 사용합니다. TV 및 인터넷 라디오와 같은 소비자 장치는 애플리케이션에 액세스합니다. 많은 구형 장치는 특정 HTTP 헤더를 지원하지 않으며 이러한 헤더가 응답에 있을 때 오류를 표시합니다. 회사는 User-Agent 헤더로 회사에서...
  - Q10: 소매 회사는 AWS에서 전자 상거래 애플리케이션을 운영하고 있습니다. 애플리케이션은 ALB(Application Load Balancer) 뒤의 Amazon EC2 인스턴스에서 실행됩니다. 이 회사는 Amazon RDS DB 인스턴스를 데이터베이스 백엔드로 사용합니다. Amazon CloudFront 는 ALB를 가...
  - Q16: 한 회사에서 Amazon EC2 인스턴스를 사용하여 웹 플릿을 배포하여 블로그 사이트를 호스팅했습니다. EC2 인스턴스는 ALB(Application Load Balancer) 뒤에 있으며 Auto Scaling 그룹에서 구성됩니다. 웹 애플리케이션은 모든 블로그 콘텐츠를 Amazon EFS 볼륨에 저장합니다. 이...
- 정답 구성 예시:
  - Q5: 메타데이터 서비스를 위한 Amazon CloudFront 배포를 생성합니다. Application Load Balancer(ALB)를 생성합니다. 요청을 ALB로 전달하도록 CloudFront 배포를 구성합니다. 각 요청 유형에 대해 올바른 Lambda 함수를 호출하도록 ALB를 구성합니다. User -Agent 헤...
  - Q10: Amazon S3 버킷을 생성합니다. 정적 웹 페이지를 호스팅하도록 S3 버킷을 구성합니다. 사용자 지정 오류 페이지를 Amazon S3에 업로드합니다. CloudFront 사용자 지정 오류 페이지를 구성하여 사용자 지정 오류 응답을 추가합니다. 공개적으로 액세스할 수 있는 웹 페이지를 가리키도록 DNS 레코드를 수...
  - Q16: Amazon CloudFront 배포를 구성합니다. 배포를 S3 버킷으로 지정하고 비디오를 EFS에서 Amazon S3로 마이그레이션합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS CloudFormation
공식 문서: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html

- 문제 등장: 26개
- 정답 선택지 등장: 26개
- 관찰된 기능/조합:
  - DeletionPolicy Retain (2개 문항)
  - Auto Scaling (1개 문항)
  - Multi-AZ (1개 문항)
- 출제 패턴 기반 연결 후보:
  - DeletionPolicy Retain -> CloudFormation 스택 삭제 후에도 RDS/EBS 데이터를 보존해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
- 문제 조건 예시:
  - Q30: 회사에는 AWS Organizations 의 조직 구성원인 50개의 AWS 계정이 있습니다. 각 계정에는 여러 VPC가 포함됩니다. 회사는 AWS 운송 게이트웨이(Transit Gateway) 를 사용하여 각 멤버 계정의 VPC 간에 연결을 설정하려고 합니다. 새 멤버 계정이 생성될 때마다 회사는 새 VPC 및 전송...
  - Q37: 회사는 온프레미스 환경에서 3계층 웹 애플리케이션을 호스팅하고 있습니다. 최근 트래픽 급증으로 인해 가동 중지 시간이 발생하고 재정적으로 상당한 영향을 받았기 때문에 회사 경영진은 애플리케이션을 AWS로 이전하도록 명령했습니다. 애플리케이션은 .NET으로 작성되었으며 MySQL 데이터베이스에 종속됩니다. 솔루션 설계...
  - Q38: 회사에서 AWS Organizations 를 사용하여 여러 AWS 계정을 관리하고 있습니다. 보안을 위해 회사는 모든 조직 구성원 계정에서 타사 알림 시스템과 통합할 수 있는 Amazon Simple Notification Service(Amazon SNS) 항목을 생성해야 합니다. 솔루션 설계자는 AWS Cloud...
- 정답 구성 예시:
  - Q30: 마스터 계정에서 AWS Resource Access Manager 를 사용하여 회원 계정과 전송 게이트웨이를 공유합니다. 회원 계정에 새 VPC 및 VPC 전송 게이트웨이 연결을 자동으로 생성하는 마스터 계정에서 AWS CloudFormation 스택 세트를 시작합니다. 전송 게이트웨이 ID를 사용하여 마스터 계정의...
  - Q37: AWS CloudFormation 을 사용하여 3개의 가용 영역에 걸쳐 있는 Amazon EC2 Auto Scaling 그룹 앞에 Application Load Balancer(ALB) 가 포함된 스택을 시작합니다. 스택은 삭제 유지 정책을 사용하여 Amazon Aurora MySQL DB 클러스터의 다중 AZ 배포...
  - Q38: 조직 마스터 계정에서 스택 세트를 생성합니다. 서비스 관리 권한을 사용합니다. 조직에 배포할 배포 옵션을 설정합니다. CloudFormation StackSets 자동 배포를 활성화합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon ECS
공식 문서: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html

- 문제 등장: 25개
- 정답 선택지 등장: 26개
- 관찰된 기능/조합:
  - Auto Scaling (5개 문항)
  - Aurora Read Replica (1개 문항)
  - CloudFront + S3 (1개 문항)
  - Multi-AZ (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
- 문제 조건 예시:
  - Q7: 회사는 Amazon EC2 인스턴스에서 기존 웹 애플리케이션을 실행하고 있습니다. 회사는 애플리케이션을 컨테이너에서 실행되는 마이크로서비스로 리팩터링해야 합니다. 애플리케이션의 별도 버전은 생산 및 테스트라는 두 가지 환경에 존재합니다. 애플리케이션에 대한 부하는 가변적이지만 최소 부하와 최대 부하가 알려져 있습니다...
  - Q63: 비디오 처리 회사에는 Amazon S3 버킷에서 이미지를 다운로드하고, 이미지를 처리하고, 변환된 이미지를 두 번째 S3 버킷에 저장하고, Amazon DynamoDB 테이블에서 이미지에 대한 메타데이터를 업데이트하는 애플리케이션이 있습니다. 애플리케이션은 Node.js로 작성되고 AWS Lambda 함수를 사용하여...
  - Q106: 회사는 회사의 데이터 센터에 있는 VM에 복잡한 종속성이 있는 Java 애플리케이션을 실행합니다. 응용 프로그램이 안정적입니다. 하지만 회사는 기술 스택을 현대화하고자 합니다. 회사는 애플리케이션을 AWS로 마이그레이션하고 서버를 유지 관리하기 위한 관리 오버헤드를 최소화하려고 합니다. 최소한의 코드 변경으로 이러한...
- 정답 구성 예시:
  - Q7: 컨테이너 이미지를 Amazon Elastic Container Registry(Amazon ECR) 에 업로드합니다. 예상 로드를 처리하기 위해 Fargate 시작 유형을 사용하여 2개의 자동 확장 Amazon Elastic Container Service(Amazon ECS) 클러스터를 구성합니다. ECR 이미지에...
  - Q63: 애플리케이션 코드가 포함된 Docker 이미지를 빌드하여 애플리케이션 배포를 수정합니다. 이미지를 Amazon Elastic Container Registry(Amazon ECR)에 게시합니다. 호환 유형이 AWS Fargate인 새 Amazon Elastic Container Service(Amazon ECS) 작...
  - Q106: AWS App2Container 를 사용하여 AWS Fargate 의 Amazon Elastic Container Service(Amazon ECS)로 애플리케이션을 마이그레이션합니다. Amazon Elastic Container Registry(Amazon ECR) 에 컨테이너 이미지를 저장합니다. ECS 작업 실...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon EventBridge
공식 문서: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html

- 문제 등장: 2개
- 정답 선택지 등장: 25개
- 관찰된 기능/조합:
  - Aurora Read Replica (2개 문항)
  - Auto Scaling (1개 문항)
  - S3 RTC (1개 문항)
  - Multi-AZ (1개 문항)
  - Fargate + EKS (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - S3 RTC -> 복제 완료 시간을 특정 시간 안에 보장하거나 모니터링해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
- 문제 조건 예시:
  - Q14: 한 회사가 Application Load Balancer 뒤에 있는 Auto Scaling 그룹의 여러 Amazon EC2 인스턴스에서 애플리케이션을 실행하고 있습니다. 애플리케이션의 부하는 하루 종일 달라지며 EC2 인스턴스는 정기적으로 확장 및 축소됩니다. EC2 인스턴스의 로그 파일은 15분마다 중앙 Amazo...
  - Q54: 회사는 Amazon S3 에서 정적 웹 사이트로 새 애플리케이션을 실행합니다. 이 회사는 프로덕션 AWS 계정에 애플리케이션을 배포했으며 Amazon CloudFront를 사용하여 웹 사이트를 제공합니다. 웹사이트는 Amazon API Gateway REST API 를 호출합니다. AWS Lambda 함수는 각 AP...
  - Q110: 회사에서 AWS WAF 솔루션을 배포하여 여러 AWS 계정에서 AWS WAF 규칙을 관리하려고 합니다. 계정은 AWS Organizations의 서로 다른 OU에서 관리됩니다. 관리자는 필요에 따라 관리형 AWS WAF 규칙 세트에서 계정 또는 OU를 추가하거나 제거할 수 있어야 합니다. 또한 관리자는 모든 계정에서...
- 정답 구성 예시:
  - Q14: 로그 파일을 Amazon S3 에 복사하는 스크립트로 AWS Systems Manager 문서를 생성합니다. Auto Scaling 그룹에서 수명 주기 이벤트를 감지하는 Auto Scaling 수명 주기 후크 및 Amazon EventBridge 규칙을 생성합니다. autoscaling:EC2_INSTANCE_TER...
  - Q54: AWS Compute Optimizer 에 옵트인합니다. ExportLambdaFunctionRecommendations 작업을 호출하는 Lambda 함수를 생성합니다. .csv 파일을 S3 버킷으로 내보냅니다. Amazon EventBridge 규칙을 생성하여 Lambda 함수가 2주마다 실행되도록 예약합니다.
  - Q110: AWS Firewall Manager 를 사용하여 조직의 여러 계정에서 AWS WAF 규칙을 관리합니다. AWS Systems Manager Parameter Store 파라미터를 사용하여 관리할 계정 번호 및 OU를 저장합니다. 필요에 따라 매개변수를 업데이트하여 계정 또는 OU를 추가하거나 제거하십시오. Amaz...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon SNS
공식 문서: https://docs.aws.amazon.com/sns/latest/dg/welcome.html

- 문제 등장: 7개
- 정답 선택지 등장: 22개
- 관찰된 기능/조합:
  - Aurora Read Replica (1개 문항)
  - Auto Scaling (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
- 문제 조건 예시:
  - Q8: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
  - Q66: AWS Organizations 를 사용하는 회사는 개발자가 AWS를 실험할 수 있도록 합니다. 회사에서 배포한 랜딩 존의 일부로 개발자는 회사 이메일 주소를 사용하여 계정을 요청합니다. 회사는 개발자가 비용이 많이 드는 서비스를 시작하거나 불필요하게 서비스를 실행하지 않도록 하기를 원합니다. 회사는 개발자에게 AW...
  - Q88: 회사에서 각 사업부에 대한 내부 클라우드 청구 전략을 변경하려고 합니다. 현재 클라우드 거버넌스팀은 전체 클라우드 지출에 대한 보고서를 각 사업부장과 공유하고 있다. 이 회사는 AWS Organizations 를 사용하여 각 사업부에 대한 별도의 AWS 계정을 관리합니다. 조직의 기존 태깅 표준에는 애플리케이션, 환...
- 정답 구성 예시:
  - Q8: 백업 리전에서 AWS Lambda 함수를 생성하여 읽기 전용 복제본을 승격하고 Auto Scaling 그룹 값을 수정합니다. 웹 애플리케이션을 모니터링하고 상태 확인 상태가 비정상일 때 Lambda 함수에 Amazon Simple Notification Service(Amazon SNS) 알림을 보내는 상태 확인으로...
  - Q66: AWS 예산을 사용하여 계정 생성 프로세스의 일부로 각 개발자 계정에 대한 고정 월 예산을 생성합니다. 고가의 서비스 및 구성 요소에 대한 접근을 거부하는 SCP를 만듭니다. 개발자 계정에 SCP를 적용합니다. 예산 금액에 도달하면 Amazon Simple Notification Service(Amazon SNS)...
  - Q88: 조직의 마스터 계정에서 AWS 예산을 구성하고 애플리케이션, 환경 및 소유자별로 그룹화된 예산 알림을 구성합니다. 각 알림에 대한 Amazon SNS 주제에 각 사업부를 추가합니다. 조직의 마스터 계정에서 비용 탐색기를 사용하여 각 사업부에 대한 월별 보고서를 생성합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon Kinesis
공식 문서: https://docs.aws.amazon.com/streams/latest/dev/introduction.html

- 문제 등장: 5개
- 정답 선택지 등장: 21개
- 관찰된 기능/조합:
  - VPC Endpoint (1개 문항)
  - Auto Scaling (1개 문항)
  - Multi-AZ (1개 문항)
- 출제 패턴 기반 연결 후보:
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
- 문제 조건 예시:
  - Q80: 회사는 AWS에서 IoT 플랫폼을 실행합니다. 다양한 위치에 있는 IoT 센서는 Application Load Balancer 뒤에서 실행되는 Amazon EC2 인스턴스에 있는 회사의 Node.js API 서버로 데이터를 보냅니다. 데이터는 4TB 범용 SSD 볼륨을 사용하는 Amazon RDS MySQL DB 인...
  - Q114: 회사에는 이벤트 지속성을 위해 PostgreSQL 데이터베이스를 사용하는 온프레미스 모니터링 솔루션이 있습니다. 과도한 수집으로 인해 데이터베이스를 확장할 수 없으며 스토리지가 자주 부족합니다. 이 회사는 하이브리드 솔루션을 만들고자 하며 이미 네트워크와 AWS 간에 VPN 연결을 설정했습니다. 솔루션에는 다음 속성...
  - Q115: 팀은 회사 전체에 대한 행동 데이터를 수집하고 라우팅합니다. 이 회사는 퍼블릭 서브넷, 프라이빗 서브넷 및 인터넷 게이트웨이가 있는 다중 AZ VPC 환경을 실행합니다. 각 퍼블릭 서브넷에는 NAT 게이트웨이도 포함되어 있습니다. 대부분의 회사 애플리케이션은 Amazon Kinesis Data Streams에서 읽고...
- 정답 구성 예시:
  - Q80: Amazon Kinesis Data Streams 및 AWS Lambda 를 활용하여 원시 데이터를 수집하고 처리합니다. RDS MySQL DB 인스턴스 대신 Amazon DynamoDB 를 사용하도록 데이터베이스 계층을 재설계합니다.
  - Q114: Amazon Kinesis Data Firehose 를 사용하여 이벤트를 버퍼링하십시오. 이벤트를 처리하고 변환하는 AWS Lambda 함수를 생성합니다. 이벤트를 수신하도록 Amazon Elasticsearch Service(Amazon ES) 를 구성합니다. Amazon ES와 함께 배포된 Kibana 엔드포인트...
  - Q115: Kinesis Data Streams 용 인터페이스 VPC 엔드포인트를 VPC에 추가합니다. VPC 엔드포인트 정책이 애플리케이션의 트래픽을 허용하는지 확인하십시오.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Organizations
공식 문서: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

- 문제 등장: 84개
- 정답 선택지 등장: 18개
- 관찰된 기능/조합:
  - Compute Savings Plan (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Compute Savings Plan -> EC2, Fargate, Lambda 등 컴퓨팅 사용량이 장기간 반복되는 경우
- 문제 조건 예시:
  - Q11: 회사는 많은 AWS 계정을 보유하고 있으며 AWS Organizations 를 사용하여 모든 계정을 관리합니다. 솔루션 설계자는 회사가 여러 계정에서 공통 네트워크를 공유하는 데 사용할 수 있는 솔루션을 구현해야 합니다. 회사의 인프라 팀에는 VPC가 있는 전용 인프라 계정이 있습니다. 인프라 팀은 이 계정을 사용하...
  - Q34: 회사에서 각 엔지니어링 팀을 위해 AWS Organizations 에 OU를 생성했습니다. 각 OU는 여러 AWS 계정을 소유합니다. 조직에는 수백 개의 AWS 계정이 있습니다. 솔루션 설계자는 각 OU가 AWS 계정 전체의 사용 비용 내역을 볼 수 있도록 솔루션을 설계해야 합니다. 어떤 솔루션이 이러한 요구 사항을...
  - Q70: 회사에는 단일 AWS 계정이 있는 환경이 있습니다. 솔루션 아키텍트는 AWS Management Console에 대한 액세스와 관련하여 특히 개선할 수 있는 부분을 추천하기 위해 환경을 검토하고 있습니다. 회사의 IT 지원 작업자는 현재 관리 작업을 위해 콘솔에 액세스하여 직무에 매핑된 명명된 IAM 사용자로 인증합...
- 정답 구성 예시:
  - Q11: AWS Organizations 마스터 계정에서 리소스 공유를 활성화합니다. 인프라 계정의 AWS Resource Access Manager 에서 리소스 공유를 생성합니다. 공유 네트워크를 사용할 특정 AWS Organizations OU 를 선택합니다. 리소스 공유와 연결할 각 서브넷을 선택합니다.
  - Q34: AWS Organizations 마스터 계정에서 AWS 비용 및 사용 보고서(CUR)를 생성합니다. 각 팀이 Amazon QuickSight 대시보드를 통해 CUR을 시각화하도록 허용합니다.
  - Q70: AWS Organizations 에서 조직을 생성합니다. 조직의 모든 기능을 켭니다. 회사의 온프레미스 Active Directory 에 연결할 AD 커넥터를 만들고 구성합니다. IAM Identity Center 를 구성하고 AD Connector를 ID 소스로 설정합니다. 권한 집합을 만들고 회사의 Active...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon SQS
공식 문서: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html

- 문제 등장: 5개
- 정답 선택지 등장: 18개
- 관찰된 기능/조합:
  - Auto Scaling (1개 문항)
  - CloudFront + S3 (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
- 문제 조건 예시:
  - Q18: 회사에는 사용자가 짧은 동영상을 업로드할 수 있는 웹 애플리케이션이 있습니다. 동영상은 Amazon EBS 볼륨에 저장되며 분류를 위해 사용자 정의 인식 소프트웨어로 분석됩니다. 웹사이트에는 특정 달에 피크가 있는 가변 트래픽이 있는 정적 콘텐츠가 포함되어 있습니다. 아키텍처는 웹 애플리케이션용 Auto Scalin...
  - Q42: 솔루션 설계자는 온프레미스 데이터 처리 애플리케이션을 AWS 클라우드로 마이그레이션하는 방법에 대해 회사에 조언해야 합니다. 현재 사용자는 웹 포털을 통해 입력 파일을 업로드합니다. 그런 다음 웹 서버는 업로드된 파일을 NAS에 저장하고 메시지 대기열을 통해 처리 서버에 메시지를 보냅니다. 각 미디어 파일을 처리하는...
  - Q100: 회사가 AWS 클라우드에서 애플리케이션을 실행하고 있습니다. 최근 애플리케이션 메트릭은 일관성 없는 응답 시간과 오류율의 상당한 증가를 보여줍니다. 타사 서비스에 대한 호출로 인해 지연이 발생합니다. 현재 애플리케이션은 AWS Lambda 함수를 직접 호출하여 타사 서비스를 동기식으로 호출합니다. 솔루션 설계자는 타...
- 정답 구성 예시:
  - Q18: Amazon S3 에서 웹 애플리케이션을 호스팅합니다. 업로드된 동영상을 Amazon S3 에 저장합니다. S3 이벤트 알림을 사용하여 이벤트를 SQS 대기열에 게시합니다. 비디오를 분류하기 위해 Amazon Rekognition API를 호출하는 AWS Lambda 함수로 SQS 대기열을 처리합니다.
  - Q42: Amazon SQS 를 사용하여 대기열을 생성합니다. 새 대기열에 게시하도록 기존 웹 서버를 구성합니다. EC2 Auto Scaling 그룹의 Amazon EC2 인스턴스를 사용하여 대기열에서 요청을 가져오고 파일을 처리합니다. SQS 대기열 길이를 기준으로 EC2 인스턴스를 확장합니다. 처리된 파일을 Amazon...
  - Q100: Amazon Simple Queue Service(Amazon SQS) 대기열을 사용하여 이벤트를 저장하고 Lambda 함수를 호출합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Fargate
공식 문서: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html

- 문제 등장: 10개
- 정답 선택지 등장: 17개
- 관찰된 기능/조합:
  - Auto Scaling (3개 문항)
  - CloudFront + S3 (2개 문항)
  - Fargate + EKS (2개 문항)
  - Aurora Read Replica (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q7: 회사는 Amazon EC2 인스턴스에서 기존 웹 애플리케이션을 실행하고 있습니다. 회사는 애플리케이션을 컨테이너에서 실행되는 마이크로서비스로 리팩터링해야 합니다. 애플리케이션의 별도 버전은 생산 및 테스트라는 두 가지 환경에 존재합니다. 애플리케이션에 대한 부하는 가변적이지만 최소 부하와 최대 부하가 알려져 있습니다...
  - Q63: 비디오 처리 회사에는 Amazon S3 버킷에서 이미지를 다운로드하고, 이미지를 처리하고, 변환된 이미지를 두 번째 S3 버킷에 저장하고, Amazon DynamoDB 테이블에서 이미지에 대한 메타데이터를 업데이트하는 애플리케이션이 있습니다. 애플리케이션은 Node.js로 작성되고 AWS Lambda 함수를 사용하여...
  - Q106: 회사는 회사의 데이터 센터에 있는 VM에 복잡한 종속성이 있는 Java 애플리케이션을 실행합니다. 응용 프로그램이 안정적입니다. 하지만 회사는 기술 스택을 현대화하고자 합니다. 회사는 애플리케이션을 AWS로 마이그레이션하고 서버를 유지 관리하기 위한 관리 오버헤드를 최소화하려고 합니다. 최소한의 코드 변경으로 이러한...
- 정답 구성 예시:
  - Q7: 컨테이너 이미지를 Amazon Elastic Container Registry(Amazon ECR) 에 업로드합니다. 예상 로드를 처리하기 위해 Fargate 시작 유형을 사용하여 2개의 자동 확장 Amazon Elastic Container Service(Amazon ECS) 클러스터를 구성합니다. ECR 이미지에...
  - Q63: 애플리케이션 코드가 포함된 Docker 이미지를 빌드하여 애플리케이션 배포를 수정합니다. 이미지를 Amazon Elastic Container Registry(Amazon ECR)에 게시합니다. 호환 유형이 AWS Fargate인 새 Amazon Elastic Container Service(Amazon ECS) 작...
  - Q106: AWS App2Container 를 사용하여 AWS Fargate 의 Amazon Elastic Container Service(Amazon ECS)로 애플리케이션을 마이그레이션합니다. Amazon Elastic Container Registry(Amazon ECR) 에 컨테이너 이미지를 저장합니다. ECS 작업 실...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Transit Gateway
공식 문서: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html

- 문제 등장: 11개
- 정답 선택지 등장: 16개
- 문제 조건 예시:
  - Q1: 회사는 하이브리드 DNS 솔루션을 설계해야 합니다. 이 솔루션은 VPC 내에 저장된 리소스에 대해 도메인 cloud.example.com에 대해 Amazon Route 53 프라이빗 호스팅 영역을 사용합니다. 회사에는 다음과 같은 DNS 확인 요구 사항이 있습니다. 온프레미스 시스템은 cloud.example.com...
  - Q30: 회사에는 AWS Organizations 의 조직 구성원인 50개의 AWS 계정이 있습니다. 각 계정에는 여러 VPC가 포함됩니다. 회사는 AWS 운송 게이트웨이(Transit Gateway) 를 사용하여 각 멤버 계정의 VPC 간에 연결을 설정하려고 합니다. 새 멤버 계정이 생성될 때마다 회사는 새 VPC 및 전송...
  - Q77: Example Corp. 에는 온프레미스 데이터 센터와 Example Corp. AWS 계정에 VPC A 라는 VPC가 있습니다. 온프레미스 네트워크는 AWS Site -To-Site VPN 을 통해 VPC A 에 연결됩니다. 온프레미스 서버는 VPC A 에 적절하게 액세스할 수 있습니다. Example Corp 은...
- 정답 구성 예시:
  - Q1: 프라이빗 호스팅 영역을 모든 VPC에 연결합니다. 공유 서비스 VPC에서 Route 53 인바운드 해석기를 생성합니다. 모든 VPC를 전송 게이트웨이에 연결하고 인바운드 해석기를 가리키는 cloud.example.com에 대한 온프레미스 DNS 서버에서 전달 규칙을 생성합니다.
  - Q30: 마스터 계정에서 AWS Resource Access Manager 를 사용하여 회원 계정과 전송 게이트웨이를 공유합니다. 회원 계정에 새 VPC 및 VPC 전송 게이트웨이 연결을 자동으로 생성하는 마스터 계정에서 AWS CloudFormation 스택 세트를 시작합니다. 전송 게이트웨이 ID를 사용하여 마스터 계정의...
  - Q77: 전송 게이트웨이를 생성합니다. Site-to-Site VPN, VPC A 및 VPC B를 운송 게이트웨이(Transit Gateway)에 연결합니다. 다른 모든 네트워크에 대한 IP 범위 경로를 추가하려면 모든 네트워크에 대한 전송 게이트웨이 경로 테이블을 업데이트하십시오.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS PrivateLink
공식 문서: https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html

- 문제 등장: 6개
- 정답 선택지 등장: 15개
- 관찰된 기능/조합:
  - VPC Endpoint (9개 문항)
  - Auto Scaling (1개 문항)
- 출제 패턴 기반 연결 후보:
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
- 문제 조건 예시:
  - Q12: 회사에서 타사 SaaS(Software-as-a-Service) 애플리케이션을 사용하려고 합니다. 타사 SaaS 애플리케이션은 여러 API 호출을 통해 사용됩니다. 타사 SaaS 애플리케이션도 VPC 내부의 AWS에서 실행됩니다. 회사는 VPC 내부에서 타사 SaaS 애플리케이션을 사용합니다. 회사에는 인터넷을 통과...
  - Q115: 팀은 회사 전체에 대한 행동 데이터를 수집하고 라우팅합니다. 이 회사는 퍼블릭 서브넷, 프라이빗 서브넷 및 인터넷 게이트웨이가 있는 다중 AZ VPC 환경을 실행합니다. 각 퍼블릭 서브넷에는 NAT 게이트웨이도 포함되어 있습니다. 대부분의 회사 애플리케이션은 Amazon Kinesis Data Streams에서 읽고...
  - Q142: 한 회사에서 리전 엔드포인트와 함께 Amazon API Gateway 를 사용하는 API를 개발했습니다. API는 API Gateway 인증 메커니즘을 사용하는 AWS Lambda 함수를 호출합니다. 설계 검토 후 솔루션 설계자는 공용 액세스가 필요하지 않은 API 세트를 식별합니다. 솔루션 설계자는 VPC에서만 A...
- 정답 구성 예시:
  - Q12: AWS PrivateLink 인터페이스 VPC 엔드포인트를 생성합니다. 타사 SaaS 애플리케이션이 제공하는 엔드포인트 서비스에 이 엔드포인트를 연결합니다. 엔드포인트에 대한 접근을 제한하는 보안 그룹을 생성합니다. 보안 그룹을 엔드포인트와 연결합니다.
  - Q115: Kinesis Data Streams 용 인터페이스 VPC 엔드포인트를 VPC에 추가합니다. VPC 엔드포인트 정책이 애플리케이션의 트래픽을 허용하는지 확인하십시오.
  - Q142: API 게이트웨이에서 리전에서 프라이빗으로 API 엔드포인트를 업데이트합니다. VPC 에서 인터페이스 VPC 엔드포인트 생성리소스 정책을 생성하고 API에 연결합니다. VPC 엔드포인트를 사용하여 VPC에서 API를 호출합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon Athena
공식 문서: https://docs.aws.amazon.com/athena/latest/ug/what-is.html

- 문제 등장: 4개
- 정답 선택지 등장: 15개
- 관찰된 기능/조합:
  - CloudFront + S3 (1개 문항)
- 출제 패턴 기반 연결 후보:
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
- 문제 조건 예시:
  - Q46: 한 회사에서 1,000개의 온프레미스 서버를 AWS로 마이그레이션할 계획입니다. 서버는 회사 데이터 센터의 여러 VMware 클러스터에서 실행됩니다. 마이그레이션 계획의 일부로 회사는 CPU 세부 정보, RAM 사용량, 운영 체제 정보 및 실행 중인 프로세스와 같은 서버 메트릭을 수집하려고 합니다. 그런 다음 회사는...
  - Q79: 한 회사가 최근에 다른 여러 회사를 인수했습니다. 각 회사에는 청구 및 보고 방법이 다른 별도의 AWS 계정이 있습니다. 인수 회사는 모든 계정을 AWS Organizations 의 하나의 조직으로 통합했습니다. 그러나 인수 회사는 모든 팀에 대해 의미 있는 그룹을 포함하는 비용 보고서를 생성하는 데 어려움을 겪었습...
  - Q92: 회사가 AWS 클라우드에서 애플리케이션을 실행하고 있습니다. 이 애플리케이션은 Amazon S3 버킷에 대량의 비정형 데이터를 수집하고 저장합니다. S3 버킷에는 수 테라바이트의 데이터가 포함되어 있으며 S3 Standard 스토리지 클래스를 사용합니다. 데이터의 크기는 매일 몇 기가바이트씩 증가합니다. 회사는 데이...
- 정답 구성 예시:
  - Q46: 각 온프레미스 서버에 AWS Application Discovery Agent 를 배포합니다. AWS Migration Hub에서 데이터 탐색을 구성합니다. Amazon Athena 를 사용하여 Amazon S3 의 데이터에 대해 사전 정의된 쿼리를 실행합니다.
  - Q79: 조직에 대한 AWS 비용 및 사용 보고서를 생성합니다. 보고서에서 태그 및 비용 범주를 정의합니다. Amazon Athena 에서 테이블을 생성합니다. Athena 테이블을 기반으로 Amazon QuickSight 데이터 세트를 생성합니다. 재무 팀과 데이터 세트를 공유합니다.
  - Q92: AWS Glue 데이터 카탈로그 및 Amazon Athena 를 사용하여 데이터를 쿼리합니다. S3 수명 주기 정책을 생성하여 1년 이상 된 데이터를 S3 Glacier Deep Archive로 전환합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon EKS
공식 문서: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html

- 문제 등장: 10개
- 정답 선택지 등장: 13개
- 관찰된 기능/조합:
  - Auto Scaling (2개 문항)
  - Aurora Read Replica (2개 문항)
  - Fargate + EKS (2개 문항)
  - Compute Savings Plan (1개 문항)
  - CloudFront + S3 (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - Compute Savings Plan -> EC2, Fargate, Lambda 등 컴퓨팅 사용량이 장기간 반복되는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q95: 한 회사가 AWS 클라우드에서 온프레미스 주문 처리 플랫폼을 리팩토링하고 있습니다. 플랫폼에는 여러 VM에서 호스팅되는 웹 프런트 엔드, 프런트 엔드를 백엔드에 연결하는 RabbitMQ, 컨테이너화된 백엔드 시스템을 실행하여 주문을 처리하는 Kubernetes 클러스터가 포함됩니다. 회사는 응용 프로그램을 크게 변경...
  - Q152: 회사는 AWS에서 이벤트 티켓팅 플랫폼을 실행 중이며 플랫폼의 비용 효율성을 최적화하려고 합니다. 이 플랫폼은 Amazon EC2 와 함께 Amazon Elastic Kubernetes Service(Amazon EKS) 에 배포되며 Amazon RDS for MySQL DB 인스턴스의 지원을 받습니다. 이 회사는...
  - Q175: 회사에는 Amazon Elastic Kubernetes Service(Amazon EKS) 클러스터에서 여러 포드의 ReplicaSet으로 실행되는 애플리케이션이 있습니다. EKS 클러스터에는 여러 가용 영역에 노드가 있습니다. 응용 프로그램은 응용 프로그램의 실행 중인 모든 인스턴스에서 액세스할 수 있어야 하는 많...
- 정답 구성 예시:
  - Q95: 웹 서버 VM의 AMI를 생성합니다. AMI 및 Application Load Balancer를 사용하는 Amazon EC2 Auto Scaling 그룹을 생성합니다. 온프레미스 메시징 대기열을 대체하도록 Amazon MQ 를 설정합니다. 주문 처리 백엔드를 호스팅하도록 Amazon Elastic Kubernetes...
  - Q152: EKS 클러스터의 예상 중간 로드에 대한 Compute Savings Plans 를 구입합니다. 피크 이벤트 날짜를 기준으로 온디맨드 용량 예약으로 클러스터를 확장합니다. 예측된 기본 로드를 충족하기 위해 데이터베이스에 대한 1년 선결제 없음 예약 인스턴스를 구매합니다. 사용량이 많을 때 일시적으로 데이터베이스 읽기...
  - Q175: Amazon Elastic File System(Amazon EFS) 파일 시스템과 EKS 클러스터의 노드를 포함하는 각 서브넷에 대한 탑재 대상을 생성합니다. 파일 시스템을 마운트하도록 ReplicaSet를 구성합니다. 파일 시스템에 파일을 저장하도록 애플리케이션에 지시합니다. 데이터 사본을 백업하고 1년 동안 보...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS IAM Identity Center
공식 문서: https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html

- 문제 등장: 5개
- 정답 선택지 등장: 9개
- 문제 조건 예시:
  - Q21: 회사에서 사용자 인증을 위해 온프레미스 Active Directory 서비스를 사용하고 있습니다. 회사는 동일한 인증 서비스를 사용하여 AWS Organizations 를 사용하는 회사의 AWS 계정에 로그인하려고 합니다. 온프레미스 환경과 회사의 모든 AWS 계정 간에 AWS Site -to-Site VPN 연결이...
  - Q70: 회사에는 단일 AWS 계정이 있는 환경이 있습니다. 솔루션 아키텍트는 AWS Management Console에 대한 액세스와 관련하여 특히 개선할 수 있는 부분을 추천하기 위해 환경을 검토하고 있습니다. 회사의 IT 지원 작업자는 현재 관리 작업을 위해 콘솔에 액세스하여 직무에 매핑된 명명된 IAM 사용자로 인증합...
  - Q118: 회사에서 AWS로 마이그레이션하려고 합니다. 회사는 모든 계정 및 애플리케이션에 대한 접근을 중앙에서 관리하는 다중 계정 구조를 사용하려고 합니다. 회사는 또한 개인 네트워크에서 트래픽을 유지하려고 합니다. 로그인 시 다단계 인증(MFA)이 필요하며 특정 역할이 사용자 그룹에 할당됩니다. 회사는 개발을 위해 별도의...
- 정답 구성 예시:
  - Q21: SAML 2.0 을 사용하여 Active Directory 에 연결하도록 AWS IAM Identity Center(AWS Single Sign-On)를 구성합니다. SCIM(System for Cross -domain Identity Management) v2.0 프로토콜을 사용하여 자동 프로비저닝을 활성화합니다....
  - Q70: AWS Organizations 에서 조직을 생성합니다. 조직의 모든 기능을 켭니다. 회사의 온프레미스 Active Directory 에 연결할 AD 커넥터를 만들고 구성합니다. IAM Identity Center 를 구성하고 AD Connector를 ID 소스로 설정합니다. 권한 집합을 만들고 회사의 Active...
  - Q118: AWS Control Tower 를 사용하여 랜딩 존 환경을 배포합니다. 계정을 등록하고 기존 계정을 AWS Organizations의 결과 조직에 초대합니다. 각 계정에서 전송 게이트웨이 및 전송 게이트웨이 VPC 연결을 생성합니다. 적절한 라우팅 테이블을 구성합니다. AWS IAM Identity Center(A...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Step Functions
공식 문서: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html

- 문제 등장: 1개
- 정답 선택지 등장: 9개
- 관찰된 기능/조합:
  - CloudFront + S3 (3개 문항)
- 출제 패턴 기반 연결 후보:
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
- 문제 조건 예시:
  - Q94: 회사에서 양식 처리 애플리케이션을 AWS로 마이그레이션했습니다. 사용자가 애플리케이션과 상호 작용할 때 웹 애플리케이션을 통해 스캔한 양식을 파일로 업로드합니다. 데이터베이스는 사용자 메타데이터와 Amazon S3 에 저장된 파일에 대한 참조를 저장합니다. 웹 애플리케이션은 Amazon EC2 인스턴스와 Amazon...
  - Q117: 회사가 AWS 클라우드에서 애플리케이션을 실행하고 있습니다. 회사의 보안 팀은 모든 새 IAM 사용자 생성을 승인해야 합니다. 새 IAM 사용자가 생성되면 해당 사용자에 대한 모든 액세스 권한이 자동으로 제거되어야 합니다. 그런 다음 보안 팀은 사용자를 승인하라는 알림을 받아야 합니다. 이 회사는 AWS 계정에 다중...
  - Q138: 생명 과학 회사는 오픈 소스 도구의 조합을 사용하여 데이터 분석 워크플로를 관리하고 온프레미스 데이터 센터의 서버에서 실행되는 Docker 컨테이너를 사용하여 게놈 데이터를 처리합니다. 시퀀싱 데이터가 생성되어 로컬 SAN(Storage Area Network) 에 저장된 다음 데이터가 처리됩니다. 연구 개발 팀은...
- 정답 구성 예시:
  - Q94: AWS Step Functions 및 AWS Lambda를 사용하는 애플리케이션 계층으로 시스템을 확장합니다. 양식이 업로드될 때 Amazon Textract 및 Amazon Comprehend 를 사용하여 양식에서 OCR(광학 문자 인식)을 수행하도록 이 계층을 구성합니다. 출력을 Amazon S3 에 저장합니다....
  - Q117: Amazon EventBridge(Amazon CloudWatch Events) 규칙을 생성합니다. CloudTrail을 통해 AWS API 호출로 설정된 detail-type 값과 CreateUser의 eventName으로 패턴을 정의합니다. AWS Step Functions 상태 시스템을 호출하여 접근을 제거합니...
  - Q138: AWS DataSync 를 사용하여 시퀀싱 데이터를 Amazon S3 로 전송합니다. S3 이벤트를 사용하여 AWS Step Functions 워크플로를 시작하는 AWS Lambda 함수를 트리거합니다. Docker 이미지를 Amazon Elastic Container Registry(Amazon ECR) 에 저장하...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon EBS
공식 문서: https://docs.aws.amazon.com/ebs/latest/userguide/what-is-Amazon-EBS.html

- 문제 등장: 17개
- 정답 선택지 등장: 8개
- 관찰된 기능/조합:
  - DeletionPolicy Retain (2개 문항)
  - Multi-AZ (1개 문항)
- 출제 패턴 기반 연결 후보:
  - DeletionPolicy Retain -> CloudFormation 스택 삭제 후에도 RDS/EBS 데이터를 보존해야 하는 경우
  - Multi-AZ -> 단일 리전 안에서 가용 영역 장애에 대비해야 하는 경우
- 문제 조건 예시:
  - Q89: 회사에서 AWS CloudFormation 을 사용하여 인프라를 배포하고 있습니다. 회사는 프로덕션 CloudFormation 스택이 삭제되면 Amazon RDS 데이터베이스 또는 Amazon EBS 볼륨에 저장된 중요한 데이터도 삭제될 수 있다고 우려하고 있습니다. 회사는 사용자가 이런 방식으로 실수로 데이터를 삭...
  - Q168: 회사는 개발용 AWS 계정이 몇 개 있고 프로덕션 애플리케이션을 AWS로 이동하려고 합니다. 회사는 유휴 상태의 Amazon Elastic Block Store(Amazon EBS) 암호화를 현재 프로덕션 계정과 향후 프로덕션 계정에만 적용해야 합니다. 이 회사는 빌트인 청사진과 가드레일을 포함하는 솔루션이 필요합니...
  - Q320: 한 회사의 규정 준수 감사 결과 AWS 계정에서 생성된 일부 Amazon Elastic Block Store(Amazon EBS) 볼륨이 암호화되지 않은 것으로 나타났습니다. 솔루션 설계자는 저장 중인 모든 새로운 EBS 볼륨을 암호화하는 솔루션을 구현해야 합니다. 최소한의 노력으로 이 요구 사항을 충족할 수 있는...
- 정답 구성 예시:
  - Q89: CloudFormation 템플릿을 수정하여 RDS 및 EBS 리소스에 DeletionPolicy 속성을 추가합니다.
  - Q168: 회사의 마스터 계정에서 새로운 AWS Control Tower 랜딩 존을 생성합니다. 프로덕션 및 개발 OU에 프로덕션 및 개발 계정을 추가합니다. 각기. AWS Organizations 에서 조직에 가입하도록 기존 계정을 초대합니다. 준수를 보장하기 위해 SCP를 생성합니다. 프로덕션 OU에 대한 가드레일을 생성하...
  - Q320: 모든 AWS 리전에서 기본적으로 EBS 암호화를 활성화합니다.
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Glue
공식 문서: https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html

- 문제 등장: 0개
- 정답 선택지 등장: 7개
- 문제 조건 예시:
  - Q92: 회사가 AWS 클라우드에서 애플리케이션을 실행하고 있습니다. 이 애플리케이션은 Amazon S3 버킷에 대량의 비정형 데이터를 수집하고 저장합니다. S3 버킷에는 수 테라바이트의 데이터가 포함되어 있으며 S3 Standard 스토리지 클래스를 사용합니다. 데이터의 크기는 매일 몇 기가바이트씩 증가합니다. 회사는 데이...
  - Q122: 회사에서 다른 공급업체로부터 가전제품을 구입했습니다. 모든 기기에는 IoT 센서가 있습니다. 센서는 정보를 JSON으로 구문 분석하는 레거시 응용 프로그램에 공급업체의 독점 형식으로 상태 정보를 보냅니다. 구문 분석은 간단하지만 각 공급업체마다 고유한 형식이 있습니다. 애플리케이션은 매일 한 번 모든 JSON 레코드...
  - Q147: 금융 서비스 회사는 신용 카드 서비스 파트너로부터 정기적인 데이터 피드를 받습니다. 약 5,000개의 레코드가 15분마다 일반 텍스트로 전송되고 HTTPS를 통해 서버 측 암호화를 통해 Amazon S3 버킷으로 직접 전달됩니다. 이 피드에는 민감한 신용 카드 기본 계정 번호(PAN) 데이터가 포함되어 있습니다. 회...
- 정답 구성 예시:
  - Q92: AWS Glue 데이터 카탈로그 및 Amazon Athena 를 사용하여 데이터를 쿼리합니다. S3 수명 주기 정책을 생성하여 1년 이상 된 데이터를 S3 Glacier Deep Archive로 전환합니다.
  - Q122: IoT 센서를 AWS IoT Core 에 연결합니다. AWS Lambda 함수를 호출하여 정보를 구문 분석하고 .csv 파일을 Amazon에 저장하는 규칙을 설정합니다. S3 AWS Glue 를 사용하여 파일을 분류합니다. 분석을 위해 Amazon Athena 및 Amazon QuickSight를 사용합니다.
  - Q147: 데이터 피드 형식을 기반으로 AWS Glue 크롤러 및 사용자 지정 분류자를 생성하고 일치시킬 테이블 정의를 구축합니다. 파일 전송 시 AWS Lambda 함수를 호출하여 처리 및 변환 요구 사항에 따라 전체 레코드를 변환하는 AWS Glue ETL 작업을 시작합니다. 출력 형식을 JSON으로 정의합니다. 완료되면...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### AWS Transfer Family
공식 문서: https://docs.aws.amazon.com/transfer/latest/userguide/what-is.html

- 문제 등장: 3개
- 정답 선택지 등장: 5개
- 관찰된 기능/조합:
  - VPC Endpoint (1개 문항)
- 출제 패턴 기반 연결 후보:
  - VPC Endpoint -> 인터넷을 거치지 않고 VPC에서 AWS 서비스에 사설로 접근해야 하는 경우
- 문제 조건 예시:
  - Q145: 국제 배송 회사는 AWS에서 배송 관리 시스템을 호스팅합니다. 드라이버는 시스템을 사용하여 배송 확인을 업로드합니다. 확인에는 수령인의 서명 또는 수령인과 함께 패키지 사진이 포함됩니다. 운전자의 핸드헬드 장치는 FTP를 통해 서명과 사진을 단일 Amazon EC2 인스턴스에 업로드합니다. 각 핸드헬드 장치는 로그인...
  - Q290: 회사는 인터넷을 통해 액세스할 수 있는 SFTP 서버를 통해 고객에게 파일을 제공하고 있습니다. SFTP 서버는 탄력적 IP 주소가 연결된 단일 Amazon EC2 인스턴스에서 실행됩니다. 고객은 탄력적 IP 주소를 통해 SFTP 서버에 연결하고 인증을 위해 SSH를 사용합니다. EC2 인스턴스에는 모든 고객 IP...
  - Q292: 회사는 온프레미스 SFTP 사이트를 AWS로 마이그레이션해야 합니다. SFTP 사이트는 현재 Linux VM에서 실행됩니다. 업로드된 파일은 NFS 공유를 통해 다운스트림 애플리케이션에서 사용할 수 있습니다. AWS로 마이그레이션하는 과정에서 솔루션 설계자는 고가용성을 구현해야 합니다. 솔루션은 공급업체가 허용할 수...
- 정답 구성 예시:
  - Q145: AWS Transfer Family 를 사용하여 파일을 Amazon S3 에 배치하는 FTP 서버를 생성합니다. Amazon Simple Notification Service(Amazon SNS) 를 통해 S3 이벤트 알림을 사용하여 AWS Lambda 함수를 호출합니다. 메타데이터를 추가하고 전달 시스템을 업데이트...
  - Q290: EC2 인스턴스에서 탄력적 IP 주소 연결을 해제합니다. SFTP 파일 호스팅에 사용할 Amazon S3 버킷을 생성합니다. AWS Transfer Family 서버를 생성합니다. VPC 에서 호스팅하는 인터넷 연결 엔드포인트로 Transfer Family 서버를 구성합니다. SFTP 탄력적 IP 주소를 새 엔드포인...
  - Q292: AWS Transfer Family 서버를 생성합니다. Transfer Family 서버에 대한 인터넷 연결 VPC 엔드포인트를 구성합니다. 각 서브넷에 탄력적 IP 주소를 지정합니다. 여러 가용 영역에 배포된 Amazon Elastic File System(Amazon EFS) 파일 시스템에 파일을 배치하도록 Tr...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon SageMaker
공식 문서: https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html

- 문제 등장: 5개
- 정답 선택지 등장: 2개
- 문제 조건 예시:
  - Q530: 솔루션 설계자는 회사가 온프레미스에서 호스팅하는 3계층 애플리케이션을 재설계하고 있습니다. 이 응용 프로그램은 사용자 프로필을 기반으로 개인화 된 권장 사항을 제공합니다. 회사에는 이미 AWS 계정이 있으며 애플리케이션을 호스팅하도록 VPC를 구성했습니다. 프런트엔드는 온프레미스 VM에서 실행되는 Java 기반 애플...
  - Q615: 한 회사에 데이터 과학 교육을 위한 온라인 학습 플랫폼이 있습니다. 이 플랫폼은 AWS 클라우드를 사용하여 학생들에게 온디맨드 랩 환경을 제공합니다. 각 학생은 단기간 전용 AWS 계정을 받습니다. 학생들은 단일 Amazon SageMaker 머신 러닝 학습 작업을 실행하고 추론 엔드포인트를 배포하기 위해 ml.p2...
- 정답 구성 예시:
  - Q530: 개인화 모델을 내보냅니다. 모델 아티팩트를 Amazon S3 에 저장합니다. 모델을 Amazon SageMaker에 배포하고 엔드포인트를 생성합니다. AWS Elastic Beanstalk 에서 Java 애플리케이션을 호스팅합니다. AWS Database Migration Service(AWS DMS) 를 사용하여...
  - Q615: 조직의 관리 계정에서 us-east-1 리전에 할당량 요청 템플릿을 생성합니다. 템플릿 연결을 활성화합니다. ml.p2.xlarge 학습 작업 사용을 위해 apsoutheast-2에 SageMaker 할당량을 추가합니다. 원하는 할당량을 1로 설정합니다. ml.p2.xlarge 엔드포인트 사용량을 위해 ap- sou...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

### Amazon MSK
공식 문서: https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html

- 문제 등장: 1개
- 정답 선택지 등장: 1개
- 관찰된 기능/조합:
  - Aurora Read Replica (1개 문항)
  - Auto Scaling (1개 문항)
  - CloudFront + S3 (1개 문항)
  - Fargate + EKS (1개 문항)
  - MSK managed Kafka (1개 문항)
- 출제 패턴 기반 연결 후보:
  - Aurora Read Replica -> Aurora 읽기 부하를 분산하거나 읽기 용량을 자동 확장해야 하는 경우
  - Auto Scaling -> 트래픽이나 작업량이 변하고 수요에 따라 컴퓨팅 용량을 조절해야 하는 경우
  - CloudFront + S3 -> 정적 콘텐츠를 사용자와 가까운 위치에서 전 세계에 제공해야 하는 경우
  - Fargate + EKS -> Kubernetes 컨테이너를 실행하면서 노드 서버 운영 부담을 줄여야 하는 경우
  - MSK managed Kafka -> Kafka 클러스터의 브로커 운영 부담을 AWS 관리형 서비스로 줄여야 하는 경우
- 문제 조건 예시:
  - Q368: 회사에는 퍼블릭 IP를 사용하여 여러 Amazon EC2 인스턴스에 컨테이너화 및 배포된 애플리케이션 서비스가 있습니다. Apache Kafka 클러스터가 EC2 인스턴스에 배포되었습니다. PostgreSQL 데이터베이스가 PostgreSQL용 Amazon RDS 로 마이그레이션되었습니다. 회사는 주력 제품의 새 버...
- 정답 구성 예시:
  - Q368: AWS Fargate를 사용하여 Amazon Elastic Kubernetes Service(Amazon EKS) 에 애플리케이션을 배포하고 Application Load Balancer 뒤에서 자동 확장을 활성화합니다. DB 인스턴스에 대한 추가 읽기 전용 복제본을 생성합니다. Apache Kafka 용 Amazo...
- 검증 상태: candidate_extracted_from_question_bank; verify_claims_against_official_docs

## 기능/조건 연결 후보

### Auto Scaling
- 관찰 문항 수: 89개
- Q4 / Answer C: 회사는 온프레미스 데이터 센터에서 2계층 웹 기반 애플리케이션을 실행하고 있습니다. 애플리케이션 계층은 상태 저장 애플리케이션을 실행하는 단일 서버로 구성됩니다. 애플리케이션은 별도의 서버에서 실행되는 PostgreSQL 데이터베이스에 연결됩니다. 애플리케이션의 사용자 기반이 크게 성장할 것으로 예상되므로 회사는 애...
- Q7 / Answer B: 회사는 Amazon EC2 인스턴스에서 기존 웹 애플리케이션을 실행하고 있습니다. 회사는 애플리케이션을 컨테이너에서 실행되는 마이크로서비스로 리팩터링해야 합니다. 애플리케이션의 별도 버전은 생산 및 테스트라는 두 가지 환경에 존재합니다. 애플리케이션에 대한 부하는 가변적이지만 최소 부하와 최대 부하가 알려져 있습니다...
- Q8 / Answer B: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
- Q9 / Answer A, D, F: 한 회사가 단일 Amazon EC2 인스턴스에서 중요한 애플리케이션을 호스팅하고 있습니다. 이 애플리케이션은 인 메모리 데이터 스토어를 위해 Redis 단일 노드 클러스터용 Amazon ElastiCache를 사용합니다. 이 애플리케이션은 관계형 데이터베이스에 Amazon RDS for MariaDB DB 인스턴스를...
- Q14 / Answer B: 한 회사가 Application Load Balancer 뒤에 있는 Auto Scaling 그룹의 여러 Amazon EC2 인스턴스에서 애플리케이션을 실행하고 있습니다. 애플리케이션의 부하는 하루 종일 달라지며 EC2 인스턴스는 정기적으로 확장 및 축소됩니다. EC2 인스턴스의 로그 파일은 15분마다 중앙 Amazo...

### CloudFront + S3
- 관찰 문항 수: 29개
- Q10 / Answer A, E: 소매 회사는 AWS에서 전자 상거래 애플리케이션을 운영하고 있습니다. 애플리케이션은 ALB(Application Load Balancer) 뒤의 Amazon EC2 인스턴스에서 실행됩니다. 이 회사는 Amazon RDS DB 인스턴스를 데이터베이스 백엔드로 사용합니다. Amazon CloudFront 는 ALB를 가...
- Q16 / Answer C: 한 회사에서 Amazon EC2 인스턴스를 사용하여 웹 플릿을 배포하여 블로그 사이트를 호스팅했습니다. EC2 인스턴스는 ALB(Application Load Balancer) 뒤에 있으며 Auto Scaling 그룹에서 구성됩니다. 웹 애플리케이션은 모든 블로그 콘텐츠를 Amazon EFS 볼륨에 저장합니다. 이...
- Q36 / Answer C: 회사의 솔루션 아키텍트가 AWS에서 실행되는 웹 애플리케이션을 검토하고 있습니다. 애플리케이션은 us-east-1 리전의 Amazon S3 버킷에 있는 정적 자산을 참조합니다. 회사는 여러 AWS 리전에서 복원력이 필요합니다. 회사는 이미 두 번째 리전에 S3 버킷을 생성했습니다. 최소한의 운영 오버헤드로 이러한 요...
- Q54 / Answer B: 회사는 Amazon S3 에서 정적 웹 사이트로 새 애플리케이션을 실행합니다. 이 회사는 프로덕션 AWS 계정에 애플리케이션을 배포했으며 Amazon CloudFront를 사용하여 웹 사이트를 제공합니다. 웹사이트는 Amazon API Gateway REST API 를 호출합니다. AWS Lambda 함수는 각 AP...
- Q81 / Answer A, C: 회사는 사용자가 문서를 업로드하는 전자 문서 관리 시스템을 구축하고 있습니다. 애플리케이션 스택은 완전히 서버리스이며 eu-central-1 리전의 AWS에서 실행됩니다. 이 시스템에는 Amazon S3를 원본으로 사용하여 Amazon CloudFront 배포를 사용하는 웹 애플리케이션이 포함되어 있습니다. 웹 애플...

### VPC Endpoint
- 관찰 문항 수: 25개
- Q12 / Answer A: 회사에서 타사 SaaS(Software-as-a-Service) 애플리케이션을 사용하려고 합니다. 타사 SaaS 애플리케이션은 여러 API 호출을 통해 사용됩니다. 타사 SaaS 애플리케이션도 VPC 내부의 AWS에서 실행됩니다. 회사는 VPC 내부에서 타사 SaaS 애플리케이션을 사용합니다. 회사에는 인터넷을 통과...
- Q40 / Answer C: 회사는 VPC의 AWS에서 이미지 처리 서비스를 호스팅하고 있습니다. VPC 는 두 가용 영역에 걸쳐 확장됩니다. 각 가용 영역에는 퍼블릭 서브넷 1개와 프라이빗 서브넷 1개가 포함됩니다. 이 서비스는 프라이빗 서브넷의 Amazon EC2 인스턴스에서 실행됩니다. 퍼블릭 서브넷의 Application Load Bal...
- Q111 / Answer A: 솔루션 설계자는 회사의 보안 설정 또는 AWS Lambda 함수를 감사하고 있습니다. Lambda 함수는 Amazon Aurora 데이터베이스에서 최신 변경 사항을 검색합니다. Lambda 함수와 데이터베이스는 동일한 VPC에서 실행됩니다. Lambda 환경 변수는 Lambda 함수에 데이터베이스 자격 증명을 제공합...
- Q115 / Answer D: 팀은 회사 전체에 대한 행동 데이터를 수집하고 라우팅합니다. 이 회사는 퍼블릭 서브넷, 프라이빗 서브넷 및 인터넷 게이트웨이가 있는 다중 AZ VPC 환경을 실행합니다. 각 퍼블릭 서브넷에는 NAT 게이트웨이도 포함되어 있습니다. 대부분의 회사 애플리케이션은 Amazon Kinesis Data Streams에서 읽고...
- Q142 / Answer C: 한 회사에서 리전 엔드포인트와 함께 Amazon API Gateway 를 사용하는 API를 개발했습니다. API는 API Gateway 인증 메커니즘을 사용하는 AWS Lambda 함수를 호출합니다. 설계 검토 후 솔루션 설계자는 공용 액세스가 필요하지 않은 API 세트를 식별합니다. 솔루션 설계자는 VPC에서만 A...

### Aurora Read Replica
- 관찰 문항 수: 24개
- Q4 / Answer C: 회사는 온프레미스 데이터 센터에서 2계층 웹 기반 애플리케이션을 실행하고 있습니다. 애플리케이션 계층은 상태 저장 애플리케이션을 실행하는 단일 서버로 구성됩니다. 애플리케이션은 별도의 서버에서 실행되는 PostgreSQL 데이터베이스에 연결됩니다. 애플리케이션의 사용자 기반이 크게 성장할 것으로 예상되므로 회사는 애...
- Q8 / Answer B: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
- Q48 / Answer B, D: 솔루션 설계자는 Amazon API Gateway 지역 엔드포인트와 AWS Lambda 함수를 사용하는 웹 애플리케이션을 개발했습니다. 웹 애플리케이션의 소비자는 모두 애플리케이션이 배포될 AWS 리전에 가깝습니다. Lambda 함수는 Amazon Aurora MySQL 데이터베이스만 쿼리합니다. 솔루션 설계자는 3...
- Q50 / Answer C: 회사에서 데이터 분석 환경을 온프레미스에서 AWS로 마이그레이션하려고 합니다. 환경은 두 개의 간단한 Node.js 애플리케이션으로 구성됩니다. 애플리케이션 중 하나는 센서 데이터를 수집하여 MySQL 데이터베이스에 로드합니다. 다른 응용 프로그램은 데이터를 보고서로 집계합니다. 집계 작업이 실행될 때 일부 로드 작...
- Q76 / Answer D: 소매 회사는 여러 AWS 리전에 걸쳐 AWS에서 전자 상거래 웹 사이트를 호스팅하고 있습니다. 회사는 온라인 구매를 위해 웹 사이트가 항상 작동하기를 원합니다. 웹 사이트는 MySQL DB 인스턴스용 Amazon RDS에 데이터를 저장합니다. 데이터베이스에 가장 높은 가용성을 제공하는 솔루션은 무엇입니까?

### Multi-AZ
- 관찰 문항 수: 14개
- Q8 / Answer B: 회사에는 Application Load Balancer(ALB) 뒤에 있는 Amazon EC2 인스턴스 플릿에서 실행되는 다중 계층 웹 애플리케이션이 있습니다. 인스턴스는 Auto Scaling 그룹에 있습니다. ALB 및 Auto Scaling 그룹은 백업 AWS 리전에서 복제됩니다. Auto Scaling 그룹의...
- Q9 / Answer A, D, F: 한 회사가 단일 Amazon EC2 인스턴스에서 중요한 애플리케이션을 호스팅하고 있습니다. 이 애플리케이션은 인 메모리 데이터 스토어를 위해 Redis 단일 노드 클러스터용 Amazon ElastiCache를 사용합니다. 이 애플리케이션은 관계형 데이터베이스에 Amazon RDS for MariaDB DB 인스턴스를...
- Q37 / Answer B: 회사는 온프레미스 환경에서 3계층 웹 애플리케이션을 호스팅하고 있습니다. 최근 트래픽 급증으로 인해 가동 중지 시간이 발생하고 재정적으로 상당한 영향을 받았기 때문에 회사 경영진은 애플리케이션을 AWS로 이전하도록 명령했습니다. 애플리케이션은 .NET으로 작성되었으며 MySQL 데이터베이스에 종속됩니다. 솔루션 설계...
- Q72 / Answer B: 애플리케이션이 us-east-1 리전에서 Amazon RDS for MySQL 다중 AZ DB 인스턴스를 사용하고 있습니다. 장애 조치 테스트 후 애플리케이션에서 데이터베이스에 대한 연결이 끊어져 연결을 다시 설정할 수 없습니다. 애플리케이션을 다시 시작한 후 애플리케이션이 연결을 다시 설정했습니다. 솔루션 설계자는...
- Q115 / Answer D: 팀은 회사 전체에 대한 행동 데이터를 수집하고 라우팅합니다. 이 회사는 퍼블릭 서브넷, 프라이빗 서브넷 및 인터넷 게이트웨이가 있는 다중 AZ VPC 환경을 실행합니다. 각 퍼블릭 서브넷에는 NAT 게이트웨이도 포함되어 있습니다. 대부분의 회사 애플리케이션은 Amazon Kinesis Data Streams에서 읽고...

### Compute Savings Plan
- 관찰 문항 수: 7개
- Q152 / Answer B: 회사는 AWS에서 이벤트 티켓팅 플랫폼을 실행 중이며 플랫폼의 비용 효율성을 최적화하려고 합니다. 이 플랫폼은 Amazon EC2 와 함께 Amazon Elastic Kubernetes Service(Amazon EKS) 에 배포되며 Amazon RDS for MySQL DB 인스턴스의 지원을 받습니다. 이 회사는...
- Q225 / Answer B: 회사는 AWS에서 많은 워크로드를 실행하고 AWS Organizations 를 사용하여 계정을 관리합니다. 워크로드는 Amazon EC2 에서 호스팅됩니다. AWS 파게이트. 및 AWS 람다. 일부 워크로드에는 예측할 수 없는 수요가 있습니다. 계정은 어떤 달에는 사용량이 많고 다른 달에는 사용량이 적습니다. 이 회...
- Q263 / Answer D: 솔루션 설계자는 EMRFS(EMR 파일 시스템)를 사용하는 Amazon EMR 클러스터의 설계를 검토해야 합니다. 클러스터는 비즈니스 요구에 중요한 작업을 수행합니다. 클러스터는 모든 작업, 기본 및 코어 노드에 대해 항상 Amazon EC2 온디맨드 인스턴스를 실행하고 있습니다. EMR 작업은 매일 아침 오전 1시...
- Q341 / Answer D: 회사는 AWS에서의 애플리케이션 비용을 최적화해야 합니다. 애플리케이션은 AWS Fargate 에서 실행되는 AWS Lambda 함수와 Amazon Elastic Container Service(Amazon ECS) 컨테이너를 사용합니다. 이 애플리케이션은 쓰기 집약적이며 Amazon Aurora MySQL 데이터베...
- Q377 / Answer C: 회사에는 회사의 각 부서에 대한 별도의 AWS 계정을 포함하는 AWS Organizations 에 조직이 있습니다. 다양한 부서의 애플리케이션 팀이 독립적으로 솔루션을 개발하고 배포합니다. 회사는 컴퓨팅 비용을 줄이고 부서 전체에서 비용을 적절하게 관리하기를 원합니다. 또한 회사는 개별 부서의 청구에 대한 가시성을...

### Cross-Region Replication
- 관찰 문항 수: 7개
- Q135 / Answer C: 한 회사가 인기 있는 온라인 게임의 속편을 만들고 있습니다. 전 세계의 많은 사용자가 출시 후 첫 주 이내에 게임을 플레이할 것입니다. 현재 이 게임은 단일 AWS 리전에 배포된 다음 구성 요소로 구성됩니다. • 게임 자산을 저장하는 Amazon S3 버킷 • 플레이어 점수를 저장하는 Amazon DynamoDB 테...
- Q143 / Answer B, D: 날씨 서비스는 eu-west-1 리전의 AWS에서 호스팅되는 웹 애플리케이션의 고해상도 날씨 지도를 제공합니다. 날씨 지도는 자주 업데이트되며 정적 HTML 콘텐츠와 함께 Amazon S3에 저장됩니다. 웹 애플리케이션은 Amazon CloudFront가 전면에 있습니다. 이 회사는 최근 us-east-1 지역의 사...
- Q186 / Answer A, B, E: 솔루션 아키텍트가 Amazon S3 버킷에 객체를 저장하는 애플리케이션을 만들고 있습니다. 솔루션 설계자는 동시에 사용할 두 AWS 리전에 애플리케이션을 배포해야 합니다. 두 S3 버킷의 객체는 서로 동기화된 상태를 유지해야 합니다. 최소한의 운영 오버헤드로 이러한 요구 사항을 충족하는 단계 조합은 무엇입니까? (3...
- Q194 / Answer B: 회사는 AWS에서 애플리케이션을 호스팅합니다. 애플리케이션은 단일 Amazon S3 버킷에 저장된 객체를 읽고 씁니다. 회사는 두 AWS 리전에 애플리케이션을 배포하도록 애플리케이션을 수정해야 합니다. 최소한의 운영 오버헤드로 이러한 요구 사항을 충족하는 솔루션은 무엇입니까?
- Q335 / Answer D, E: 온라인 잡지가 이번 달 최신판을 출시할 예정입니다. 이 버전은 전 세계적으로 최초로 배포될 예정입니다. 이 잡지의 동적 웹 사이트는 현재 웹 계층 앞에 Application Load Balancer, 웹 및 애플리케이션 서버용 Amazon EC2 인스턴스 집합, Amazon Aurora MySQL 을 사용하고 있습니...

### Global Table
- 관찰 문항 수: 6개
- Q2 / Answer C: 한 회사에서 REST 기반 API를 통해 여러 고객에게 날씨 데이터를 제공하고 있습니다. API 는 Amazon API Gateway 에서 호스팅되며 각 API 작업에 대해 서로 다른 AWS Lambda 함수와 통합됩니다. 이 회사는 DNS에 Amazon Route 53을 사용하고 weather.example.com...
- Q160 / Answer A, D: 한 회사에 데이터 계층이 단일 AWS 리전에 배포된 중요한 애플리케이션이 있습니다. 데이터 계층은 Amazon DynamoDB 테이블과 Amazon Aurora MySQL DB 클러스터를 사용합니다. 현재 Aurora MySQL 엔진 버전은 글로벌 데이터베이스를 지원합니다. 애플리케이션 계층은 이미 두 지역에 배포되...
- Q184 / Answer C: 한 환경 기업이 전국 주요 도시에 센서를 배치해 대기질을 측정하고 있다. 센서는 AWS IoT Core에 연결하여 시계열 데이터 판독값을 수집합니다. 회사는 데이터를 Amazon DynamoDB 에 저장합니다. 비즈니스 연속성을 위해 회사는 두 개의 AWS 리전에서 데이터를 수집하고 저장할 수 있어야 합니다. 이러한...
- Q240 / Answer B, C, E: 솔루션 설계자는 웹을 사용하는 3계층 애플리케이션용 솔루션에 대한 참조 아키텍처를 정의해야 합니다. 애플리케이션 및 NoSQL 데이터 계층. 참조 아키텍처는 다음 요구 사항을 충족해야 합니다. • AWS 리전 내 고가용성 • 재해 복구를 위해 1분 안에 다른 AWS 리전으로 장애 조치 가능 • 사용자 경험에 미치는...
- Q312 / Answer C: 한 회사가 Amazon EC2 인스턴스에서 새로운 온라인 게임을 출시하고 있습니다. 게임은 전 세계적으로 이용 가능해야 합니다. 회사는 us-east-1, eu -west-1 및 ap-southeast-1의 3개 AWS 리전에서 게임을 실행할 계획입니다. 게임의 순위표, 플레이어 인벤토리 및 이벤트 상태는 여러 지역...

### Fargate + EKS
- 관찰 문항 수: 3개
- Q152 / Answer B: 회사는 AWS에서 이벤트 티켓팅 플랫폼을 실행 중이며 플랫폼의 비용 효율성을 최적화하려고 합니다. 이 플랫폼은 Amazon EC2 와 함께 Amazon Elastic Kubernetes Service(Amazon EKS) 에 배포되며 Amazon RDS for MySQL DB 인스턴스의 지원을 받습니다. 이 회사는...
- Q368 / Answer D: 회사에는 퍼블릭 IP를 사용하여 여러 Amazon EC2 인스턴스에 컨테이너화 및 배포된 애플리케이션 서비스가 있습니다. Apache Kafka 클러스터가 EC2 인스턴스에 배포되었습니다. PostgreSQL 데이터베이스가 PostgreSQL용 Amazon RDS 로 마이그레이션되었습니다. 회사는 주력 제품의 새 버...
- Q474 / Answer C: 한 소매 회사에서 애플리케이션 아키텍처를 개선하려고 합니다. 회사의 애플리케이션은 새로운 주문을 등록하고 상품 반품을 처리하며 분석을 제공합니다. 애플리케이션은 MySQL 데이터베이스와 Oracle OLAP 분석 데이터베이스에 소매 데이터를 저장합니다. 모든 애플리케이션과 데이터베이스는 Amazon EC2 인스턴스에...

### DeletionPolicy Retain
- 관찰 문항 수: 2개
- Q89 / Answer A: 회사에서 AWS CloudFormation 을 사용하여 인프라를 배포하고 있습니다. 회사는 프로덕션 CloudFormation 스택이 삭제되면 Amazon RDS 데이터베이스 또는 Amazon EBS 볼륨에 저장된 중요한 데이터도 삭제될 수 있다고 우려하고 있습니다. 회사는 사용자가 이런 방식으로 실수로 데이터를 삭...
- Q630 / Answer A: 한 회사가 AWS Cloud Formation 을 사용하여 인프라를 배포하고 있습니다. 이 회사는 프로덕션 Cloud Formation 스택을 삭제할 경우 Amazon RDS 데이터베이스 또는 Amazon EBS 볼륨에 저장된 데이터가 삭제될 수 있다는 점을 우려하고 있습니다. 이러한 방식으로 사용자가 실수로 데이터...

### MSK managed Kafka
- 관찰 문항 수: 2개
- Q368 / Answer D: 회사에는 퍼블릭 IP를 사용하여 여러 Amazon EC2 인스턴스에 컨테이너화 및 배포된 애플리케이션 서비스가 있습니다. Apache Kafka 클러스터가 EC2 인스턴스에 배포되었습니다. PostgreSQL 데이터베이스가 PostgreSQL용 Amazon RDS 로 마이그레이션되었습니다. 회사는 주력 제품의 새 버...
- Q634 / Answer C: 한 회사가 Amazon Managed Streaming for Apache Kafka(Amazon MSK) 클러스터에서 메시지를 소비하는 지연 시간에 민감한 애플리케이션을 운영하고 있습니다. MSK 클러스터는 세 개의 가용 영역에 걸쳐 실행됩니다. 현재 MSK 클러스터는 각 가용 영역에 두 개의 표준 대형 인스턴스를...

### S3 RTC
- 관찰 문항 수: 1개
- Q352 / Answer D: 과학 회사는 Amazon S3 버킷의 텍스트 및 이미지 데이터를 처리해야 합니다. 데이터는 심우주 임무의 시간이 중요한 실시간 단계 동안 여러 레이더 스테이션에서 수집됩니다. 레이더 스테이션은 데이터를 소스 S3 버킷에 업로드합니다. 데이터 앞에는 레이더 스테이션 식별 번호가 붙습니다. 회사는 두 번째 계정에 대상...

## 중복 그룹

- Q10 / Q438
  - Q10: 소매 회사는 AWS에서 전자 상거래 애플리케이션을 운영하고 있습니다. 애플리케이션은 ALB(Application Load Balancer) 뒤의 Amazon EC2 인스턴스에서 실행됩니다. 이 회사는 Amazo...
  - Q438: 한 소매 회사가 AWS에서 전자상거래 애플리케이션을 운영하고 있습니다. 애플리케이션은 ALB(Application Load Balancer) 뒤의 Amazon EC2 인스턴스에서 실행됩니다. 회사는 Amazon...
- Q58 / Q599
  - Q58: 회사에는 회사의 비즈니스에 중요한 모놀리식 애플리케이션이 있습니다. 회사는 Amazon Linux 2를 실행하는 Amazon EC2 인스턴스에서 애플리케이션을 호스팅합니다. 회사의 애플리케이션 팀은 법무 부서로...
  - Q599: 한 회사에 비즈니스에 필수적인 레거시 모놀리식 애플리케이션이 있습니다. 이 회사는 Amazon Linux 2 를 실행하는 Amazon EC2 인스턴스에서 해당 애플리케이션을 호스팅합니다. 회사의 애플리케이션 팀...
- Q60 / Q625
  - Q60: 한 회사에서 AWS CloudFormation 스택에 배포된 AWS Lambda 를 기반으로 애플리케이션을 구축했습니다. 웹 애플리케이션의 마지막 프로덕션 릴리스에서 몇 분 동안 중단되는 문제가 발생했습니다....
  - Q625: 한 회사가 AWS CloudFormation 스택에 배포된 AWS Lambda 기반 애플리케이션을 구축했습니다. 웹 애플리케이션의 마지막 프로덕션 릴리스에서 몇 분 동안 서비스 중단을 초래하는 문제가 발생했습니...
- Q84 / Q85
  - Q84: 회사는 AWS에 클라우드 인프라를 가지고 있습니다. 솔루션 설계자는 인프라를 코드로 정의해야 합니다. 인프라는 현재 하나의 AWS 리전에 배포되어 있습니다. 이 회사의 비즈니스 확장 계획에는 여러 AWS 계정에...
  - Q85: 회사는 AWS에 클라우드 인프라를 가지고 있습니다. 솔루션 설계자는 인프라를 코드로 정의해야 합니다. 인프라는 현재 하나의 AWS 리전에 배포되어 있습니다. 이 회사의 비즈니스 확장 계획에는 여러 AWS 계정에...
- Q89 / Q630
  - Q89: 회사에서 AWS CloudFormation 을 사용하여 인프라를 배포하고 있습니다. 회사는 프로덕션 CloudFormation 스택이 삭제되면 Amazon RDS 데이터베이스 또는 Amazon EBS 볼륨에 저...
  - Q630: 한 회사가 AWS Cloud Formation 을 사용하여 인프라를 배포하고 있습니다. 이 회사는 프로덕션 Cloud Formation 스택을 삭제할 경우 Amazon RDS 데이터베이스 또는 Amazon EB...
- Q187 / Q574
  - Q187: 회사에는 온프레미스 환경에서 실행되는 IoT 플랫폼이 있습니다. 플랫폼은 MQTT 프로토콜을 사용하여 IoT 장치에 연결하는 서버로 구성됩니다. 플랫폼은 적어도 5분마다 한 번씩 장치에서 원격 측정 데이터를 수...
  - Q574: 한 회사에 온프레미스 환경에서 실행되는 IoT 플랫폼이 있습니다. 이 플랫폼은 MQTT 프로토콜을 사용하여 IoT 기기에 연결하는 서버로 구성됩니다. 이 플랫폼은 최소 5분마다 기기에서 원격 측정 데이터를 수집...
- Q209 / Q563
  - Q209: 회사는 AWS 클라우드에서 IoT 애플리케이션을 실행합니다. 이 회사는 미국의 주택에서 데이터를 수집하는 수백만 개의 센서를 보유하고 있습니다. 센서는 MQTT 프로토콜을 사용하여 사용자 지정 MQTT 브로커에...
  - Q563: 한 회사가 AWS 클라우드에서 IoT 애플리케이션을 운영하고 있습니다. 이 회사는 미국 내 가정의 데이터를 수집하는 수백만 개의 센서를 보유하고 있습니다. 이 센서들은 MOTT 프로토콜을 사용하여 사용자 지정...
- Q220 / Q576
  - Q220: 회사에는 대도시 전체의 교통 패턴을 모니터링하는 IoT 센서가 있습니다. 회사는 센서에서 데이터를 읽고 수집하고 데이터 집계를 수행하려고 합니다. 솔루션 설계자는 IoT 디바이스가 Amazon Kinesis D...
  - Q576: 한 회사가 대도시 전역의 교통 패턴을 모니터링하는 IoT 센서를 보유하고 있습니다. 이 회사는 센서에서 데이터를 읽고 수집하여 데이터 집계를 수행하려고 합니다. 솔루션 아키텍트는 IoT 기기가 Amazon Ki...
- Q231 / Q587
  - Q231: 회사에는 밤마다 로컬 드라이브에 200GB 내보내기를 작성하는 온프레미스 Microsoft SQL Server 데이터베이스가 있습니다. 회사는 백업을 Amazon S3 의 보다 강력한 클라우드 스토리지로 이동하...
  - Q587: 한 회사에는 매일 밤 200GB의 데이터를 로컬 드라이브에 내보내는 온프레미스 Microsoft SOL Server 데이터베이스가 있습니다. 이 회사는 백업을 Amazon S3 의 더욱 강력한 클라우드 스토리지...
- Q323 / Q550
  - Q323: 회사에서 환경 데이터를 처리합니다. 이 회사는 도시의 다양한 영역에서 지속적인 데이터 스트림을 제공하기 위해 센서를 설치했습니다. 데이터는 JSON 형식으로 제공됩니다. 회사는 AWS 솔루션을 사용하여 저장을...
  - Q550: 회사에서 환경 데이터를 처리합니다. 도시의 여러 지역에서 연속적인 데이터 스트림을 제공하기 위해 센서를 설정했습니다. 데이터는 JSON 형식으로 제공됩니다. 회사에서는 AWS 솔루션을 사용하여 고정된 스키마 없...
- Q464 / Q541
  - Q464: 회사는 AWS Organizations 를 사용하여 AWS 계정을 관리합니다. 솔루션 설계자는 관리자 역할만 IAM 작업을 사용할 수 있도록 허용되는 솔루션을 설계해야 합니다. 그러나 솔루션 아키텍트는 회사 전...
  - Q541: 회사는 AWS Organizations AWS 계정을 사용합니다. 솔루션 설계자는 관리자 역할만 IAM 작업을 사용할 수 있도록 허용되는 솔루션을 설계해야 합니다. 그러나 아키텍처가 적용된 솔루션은 회사 전체의...
- Q479 / Q545
  - Q479: 회사는 티켓팅 애플리케이션의 신뢰성을 향상시켜야 합니다. 애플리케이션은 Amazon Elastic Container Service(Amazon ECS) 클러스터에서 실행됩니다. 회사는 Amazon CloudFr...
  - Q545: 회사는 신뢰성 있는 티켓팅 애플리케이션을 개선해야 합니다. 애플리케이션은 Amazon Elastic Container Service(Amazon ECS) 클러스터에서 실행됩니다. 이 회사는 Amazon Clou...
- Q498 / Q585
  - Q498: Accompany는 Amazon EC2 및 AWS Lambda 에서 애플리케이션을 실행합니다. 애플리케이션은 Amazon S3에 임시 데이터를 저장합니다. S3 객체는 24시간 후에 삭제됩니다. 회사는 AWS...
  - Q585: 한 회사가 Amazon EC2 와 AWS Lambda 에서 애플리케이션을 실행합니다. 이 애플리케이션은 Amazon S3에 임시 데이터를 저장합니다. S3 객체는 24시간 후 삭제됩니다. 이 회사는 AWS Cl...
- Q507 / Q554
  - Q507: 엔터테인먼트 회사는 Auto Scaling 그룹에 속한 Linux Amazon EC2 인스턴스 집합에서 티켓팅 서비스를 호스팅합니다. 티켓팅 서비스는 가격 파일을 사용합니다. 가격 파일은 S3 Standard...
  - Q554: 한 회사가 Auto Scaling 그룹에 속한 Linux Amazon EC2 인스턴스 플릿에서 티켓팅 서비스를 호스팅하고 있습니다. 티켓팅 서비스는 가격 파일을 사용합니다. 가격 파일은 S3 Standard 스...
