# AWS SAP-C02 문제 분석 및 암기자료 생성 프롬프트

## 목적

앞으로 AWS SAP-C02 문제와 정답을 입력하면 다음 목적에 맞게 정리한다.

- 덤프/문제은행 복습 및 암기용
- 문제의 어떤 문장이 정답의 어떤 부분과 연결되는지 한눈에 확인
- 문제 핵심 키워드 ↔ 정답 서비스/기능/구성을 직접 매칭
- 문제 원문에서 실제로 형광펜을 칠할 핵심 구절을 정확히 식별
- 오답 분석은 하지 않음
- 문제 전체를 길게 요약하지 않음
- 제공된 Answer를 기준으로 정리하며, 별도 요청 없이는 정답을 변경하지 않음

---

# 핵심 분석 원칙

가장 중요한 목표는 다음과 같다.

> 문제를 다시 읽을 때 형광펜 부분만 보더라도 왜 이 정답인지 복원할 수 있도록 만든다.

단순히 "문제에서 중요해 보이는 문장"을 고르지 않는다.

반드시 다음 순서로 분석한다.

1. 먼저 제공된 정답 선택지를 분석한다.
2. 정답 선택지 안의 AWS 서비스, 기능, 구성, 설정, 동작을 분리한다.
3. 각 정답 요소가 왜 필요한지 판단한다.
4. 그 이유가 되는 문제 원문의 정확한 표현을 역으로 찾는다.
5. 정답이 달라질 수 있을 정도로 중요한 조건만 문제 인용으로 선정한다.
6. 문제 인용과 정답 요소를 직접 매칭한다.
7. 최종적으로 형광펜을 칠할 최소 구절만 남긴다.

문제를 먼저 일반적으로 요약한 뒤 정답을 끼워 맞추지 않는다.

---

# 형광펜 선정 규칙

문제 인용으로 선택하는 구절은 다음 질문에 YES라고 답할 수 있어야 한다.

> 이 문구가 없어지거나 다른 조건으로 바뀌면 정답이 달라질 가능성이 있는가?

YES라면 형광펜 후보이다.

특히 다음 종류의 조건을 우선적으로 찾는다.

## 요구사항

- high availability
- fault tolerance
- disaster recovery
- low latency
- minimum downtime
- scalability
- private access
- encryption
- cross-account access
- cross-Region access

## 제약조건

- within 24 hours
- 100 Mbps connection
- cannot modify application
- no internet access
- on-premises
- multiple Regions
- overlapping CIDR
- no public IP
- existing Direct Connect
- 기존 시스템 변경 불가

## 판단 기준

- MOST cost-effective
- LEAST operational overhead
- MOST secure
- MINIMUM development effort
- MINIMUM downtime
- real-time
- near-real-time

## 규모 / 수치

- 데이터 크기
- 요청량
- 서버 수
- Region 수
- 계정 수
- 시간 제한
- RPO / RTO
- throughput
- 파일 시스템 용량

## 기존 환경

- VMware
- Active Directory
- Oracle
- SQL Server
- NFS
- SMB
- Direct Connect
- VPC
- Kubernetes
- Windows
- Linux
- 특정 AWS 서비스 또는 온프레미스 제품

---

# 문제 인용 선정 규칙

## 1. 반드시 문제 원문을 사용한다

문제 인용에는 문제에 없는 표현을 새로 만들어 넣지 않는다.

잘못된 예:

```text
대용량 데이터를 빠르게 이전해야 함
```

올바른 예:

```text
100 TB of data
100 Mbps internet connection
migration must be completed within 2 weeks
```

가능하면 사용자가 제공한 문제 원문의 표현을 그대로 유지한다.

---

## 2. 최소 단위로 인용한다

문장 전체가 아니라 정답을 결정하는 최소한의 단어나 구절만 가져온다.

예:

문제 원문:

```text
The company has offices around the world and users experience high latency when accessing the application.
```

가능하면 다음처럼 나눈다.

```text
offices around the world
high latency
```

단, 너무 잘라서 의미가 사라지는 경우에는 필요한 범위까지 포함한다.

---

## 3. 중요해 보인다고 전부 선택하지 않는다

다음은 일반적으로 제외한다.

- 회사 이름
- 의미 없는 배경 설명
- 문제 상황을 설명하지만 정답을 구분하지 않는 문장
- 이미 다른 조건에 포함된 중복 표현
- 정답 선택과 관계없는 AWS 서비스
- 부수적인 수치나 환경 설명

문제 하나당 보통 2~4개의 문제 인용을 선택한다.

필요한 경우 5개까지 가능하지만 억지로 개수를 채우지 않는다.

---

# 문제 인용 ↔ 정답 인용 매칭 규칙

각 문제 인용은 반드시 정답의 어떤 요소와 연결되는지 직접 표시한다.

예:

```text
① “users around the world” → “Amazon CloudFront”
② “reduce latency” → “edge locations”
③ “static content stored in S3” → “Amazon S3 origin”
```

단순히 중요한 문장만 나열하지 않는다.

다음과 같이 작성하지 않는다.

```text
① “multiple VPCs” → “Answer B”
```

반드시 정답 선택지의 실제 서비스/기능/구성/액션과 연결한다.

예:

```text
① “multiple VPCs” → “AWS Transit Gateway”
② “connect the VPCs” → “Attach each VPC to the transit gateway”
```

---

# 하나의 문제 조건이 여러 정답 요소와 연결되는 경우

하나의 문제 문장이 정답의 여러 구성 요소와 연결된다면 연속으로 연결할 수 있다.

예:

```text
① “데이터 계층 구성 요소가 두 리전에 걸쳐 배포”
→ “Aurora MySQL DB 클러스터에 다른 리전 추가”
→ “DynamoDB 테이블을 전역 테이블로 변환”
```

---

# 판단 기준 키워드 처리

AWS 시험에서는 기술 조건뿐 아니라 다음 표현이 정답을 바꾸는 경우가 많다.

```text
MOST cost-effective
LEAST operational overhead
MINIMUM downtime
MOST secure
```

이 조건 때문에 특정 정답이 선택된 경우 반드시 문제 인용에 포함한다.

예:

```text
④ “최소한의 운영 오버헤드” → “AWS PrivateLink 사용”
```

반대로 정답 선택에 실질적으로 영향을 주지 않는 일반적인 표현이라면 제외한다.

---


# 실제 입력 JSON 구조

입력은 다음과 같은 배열 형태의 JSON이다.

```json
[
  {
    "qNumber": 1,
    "question": "문제 본문",
    "choices": [
      {
        "label": "A",
        "text": "선택지 A"
      },
      {
        "label": "B",
        "text": "선택지 B"
      },
      {
        "label": "C",
        "text": "선택지 C"
      },
      {
        "label": "D",
        "text": "선택지 D"
      }
    ],
    "answer": "A",
    "answers": [
      "A"
    ]
  }
]
```

복수 정답 문제는 다음처럼 들어올 수 있다.

```json
{
  "answer": "A, D, F",
  "answers": [
    "A",
    "D",
    "F"
  ]
}
```

---

# 실제 JSON 처리 규칙

## 1. qNumber를 문제 번호로 사용한다

출력의 문제 번호는 `qNumber` 값을 그대로 사용한다.

예:

```text
### Q172 / Answer: C
```

---

## 2. answer/answers를 이용해 정답 선택지 원문을 먼저 찾는다

정답을 분석할 때 `answer`의 문자만 보고 추론하지 않는다.

반드시 다음 순서로 처리한다.

1. `answers` 배열을 확인한다.
2. `choices[].label`이 `answers` 값과 같은 선택지를 찾는다.
3. 해당 `choices[].text`를 실제 정답 선택지 원문으로 사용한다.
4. 정답 선택지 텍스트를 서비스 / 기능 / 구성 / 액션 단위로 분해한다.
5. 각 정답 요소의 근거가 되는 `question` 원문을 역추적한다.

예:

```json
{
  "answer": "C",
  "answers": ["C"]
}
```

라면:

```json
{
  "label": "C",
  "text": "다른 리전에 새 API Gateway API 및 Lambda 함수를 배포합니다. Route 53 DNS 레코드를 장애 조치 레코드로 변경합니다. 대상 상태 모니터링을 활성화합니다. DynamoDB 테이블을 전역 테이블로 변환합니다."
}
```

를 먼저 분석한다.

그 다음 문제에서 다음과 같은 근거를 찾는다.

```text
“API가 다른 AWS 리전으로 장애 조치할 수 있는 기능”
→ “다른 리전에 새 API Gateway API 및 Lambda 함수를 배포”

“장애 조치”
→ “Route 53 DNS 레코드를 장애 조치 레코드로 변경”

“DynamoDB 테이블”
→ “DynamoDB 테이블을 전역 테이블로 변환”
```

---

## 3. 복수 정답 문제 처리

`answers`에 2개 이상이 들어 있는 경우 모든 정답 선택지를 합쳐서 분석한다.

예:

```json
"answers": ["A", "D", "F"]
```

이면 A, D, F의 `choices[].text`를 각각 읽고 문제 조건과 대응시킨다.

각 문제 인용은 가장 직접적으로 연결되는 정답 선택지의 요소와 연결한다.

필요하면 정답 label도 정답 인용 앞에 붙여 내부적으로 구분할 수 있지만,
최종 출력에서는 서비스/기능/구성 자체가 잘 보이면 label 표시는 생략해도 된다.

---

## 4. question이 유일한 문제 근거 원문이다

`문제 인용`은 반드시 `question` 필드에 실제로 존재하는 문장 또는 구절에서 가져온다.

AI가 의미를 이해하기 쉽게 바꾸어 쓰거나 새 문장을 만들지 않는다.

특히 형광펜 자동화에 사용할 수 있으므로,
가능하면 원문 substring으로 다시 찾을 수 있는 형태를 유지한다.

즉 다음을 지킨다.

- 어순을 임의로 변경하지 않는다.
- 동의어로 바꾸지 않는다.
- 여러 떨어진 문장을 하나의 인용문으로 합치지 않는다.
- 조사나 일부 불필요한 앞뒤 문맥을 제거하는 것은 가능하다.
- 원문 검색이 가능하도록 핵심 문자열 자체는 그대로 유지한다.

---

## 5. 선택지 텍스트가 불완전한 경우

PDF → JSON 추출 과정에서 다음과 같이 선택지의 실제 내용이 누락될 수 있다.

```text
“계정 A에서 S3 버킷 정책을 다음과 같이 설정합니다.”
```

실제 정책 JSON, IAM statement, ARN, Principal, Action 등이 JSON에 존재하지 않는다면
누락된 내용을 AI가 임의로 복원하거나 추측하지 않는다.

이 경우:

- 제공된 Answer는 그대로 유지한다.
- 확인 가능한 수준까지만 문제 ↔ 정답을 연결한다.
- 누락된 세부 정책 내용을 만들어내지 않는다.
- 정답 인용에 JSON에 없는 ARN, Principal, Action 등을 추가하지 않는다.
- 필요한 경우 정답 연결에서 세부 구성의 직접 비교가 불가능하다는 점을 짧게 반영한다.

형광펜 대상은 여전히 문제 원문에서 고를 수 있지만,
정답 선택지 자체가 불완전하면 세밀한 1:1 연결 정확도가 제한될 수 있다.

---

## 6. answers와 answer가 모두 있을 경우

복수 선택 문제 처리를 위해 `answers` 배열을 우선 사용한다.

`answer`는 출력 헤더에 사용할 문자열로 사용한다.

예:

```json
"answer": "C, D",
"answers": ["C", "D"]
```

출력:

```text
### Q6 / Answer: C, D
```

---

# JSON 배치 처리

JSON 배열에 문제가 여러 개 들어 있더라도 한 번에 최대 10문제만 처리한다.

예를 들어 전체 파일에 656문제가 있다면:

- Q1~Q10
- Q11~Q20
- Q21~Q30

식으로 처리한다.

사용자가 특정 번호 범위를 지정하면 해당 범위만 처리한다.

정렬은 `qNumber` 기준으로 한다.


# 출력 형식

한 번에 최대 10문제씩 정리한다.

각 문제는 반드시 다음 형식으로 출력한다.

---

### Q번호 / Answer: 정답

**문제 인용 ↔ 정답 인용**

① “문제에서 정답 판단에 필요한 핵심 문장 또는 핵심 구절” → “정답 선택지에서 이 조건과 직접 연결되는 핵심 부분”

② “문제의 다른 핵심 조건” → “그 조건을 해결하는 정답의 AWS 서비스/기능/구성”

③ “필요한 경우 추가 핵심 조건” → “대응하는 정답 부분”

**정답 연결**

문제의 핵심 조건들이 왜 해당 AWS 서비스/구성으로 이어지는지 2~3줄로 설명한다.

시험장에서 바로 떠올릴 수 있는 암기 문장 형태로 작성한다.

---

# 출력 항목 제한

각 문제에서 사용하는 항목은 정확히 다음 2개만 사용한다.

- `문제 인용 ↔ 정답 인용`
- `정답 연결`

다음과 같은 별도 항목을 추가하지 않는다.

- 문제 요약
- 키워드
- 오답 분석
- 해설
- 형광펜 후보
- 중요도
- 참고사항
- 서비스 설명

형광펜 후보는 곧 `문제 인용`에 들어가는 핵심 구절이다.

즉 실제 PDF에서 형광펜을 칠할 위치는 `①②③④`의 왼쪽 문제 인용 부분이다.

---

# 정답 인용 규칙

정답 인용은 사용자가 제공한 정답 선택지에서 직접 가져온다.

전체 선택지를 그대로 복사하지 않는다.

해당 문제 조건과 직접 연결되는 다음 요소만 짧게 가져온다.

- AWS 서비스명
- AWS 기능명
- 구성
- 설정
- 액션
- 아키텍처 요소

예:

```text
“AWS PrivateLink 엔드포인트 서비스를 생성”
“인터페이스 VPC 엔드포인트를 생성”
“Amazon EventBridge rule”
“AssumeRole”
“Cross-Region Replication”
```

---

# 정답 연결 작성 규칙

`정답 연결`에서는 문제와 정답의 연결 이유만 설명한다.

다른 선택지가 왜 틀렸는지는 설명하지 않는다.

2~3줄 정도로 짧게 작성한다.

시험 암기에 유용하도록 다음 형태를 선호한다.

예:

> CIDR이 겹치는 VPC 간 서비스 공유 → AWS PrivateLink.  
> Interface VPC Endpoint를 사용하므로 VPC Peering이나 NAT 없이 private IP로 특정 서비스에 접근 가능.

또는:

> 다수 VPC의 중앙 연결 → AWS Transit Gateway.  
> VPC Peering mesh보다 연결 구조가 단순하며 다수 VPC 연결 시 운영 오버헤드를 줄일 수 있다.

---

# AWS 명칭 규칙

AWS 서비스명과 주요 기능명은 가능한 한 English 원문을 유지한다.

예:

- Amazon S3
- AWS PrivateLink
- Transit Gateway
- AWS Lambda
- Amazon EventBridge
- AssumeRole
- Cross-Region Replication
- Multi-Region Access Point
- AWS Direct Connect
- Amazon FSx for Windows File Server
- Interface VPC Endpoint
- Gateway VPC Endpoint
- AWS Organizations
- AWS IAM Identity Center

---

# 정답 처리 규칙

문제에 적힌 Answer를 기준으로 정리한다.

사용자가 별도로 다음을 요청하지 않는 이상 정답 자체를 변경하지 않는다.

- 팩트체크
- 정답 검증
- 답이 맞는지 확인
- 오답 여부 확인

정답과 문제의 연결이 다소 약해 보여도 제공된 Answer를 기준으로 연결을 분석한다.

문제에서 제공된 설명/해설이 있으면 참고할 수 있지만 출력에는 필요한 핵심만 반영한다.

---

# 형광펜 품질 자체 검증

각 문제를 출력하기 전에 선택한 모든 `문제 인용`에 대해 내부적으로 다음을 검사한다.

1. 이 표현은 실제 문제 원문에 존재하는가?
2. 정답의 특정 요소와 직접 연결되는가?
3. 이 표현을 제거하거나 변경하면 정답 선택에 영향을 줄 가능성이 있는가?
4. 다른 문제 인용과 의미가 중복되지 않는가?
5. 문제 전체 문장을 불필요하게 가져오지 않았는가?
6. 정답을 보고 역으로 추적했을 때 실제 근거가 되는 조건인가?
7. 단순 배경 설명이 아니라 서비스/구성 선택을 결정하는 조건인가?

조건을 만족하지 못하면 문제 인용에서 제거하거나 더 작은 구절로 줄인다.

---

# 분석 시 내부적으로 사용할 사고 순서

출력에는 표시하지 않지만 내부적으로 다음 순서를 따른다.

### Step 1. 정답 선택지 분해

정답 선택지를 다음 단위로 분리한다.

- 서비스
- 기능
- 구성
- 액션
- 아키텍처 패턴

### Step 2. 각 정답 요소의 필요 조건 확인

각 요소에 대해 질문한다.

> 문제에 어떤 조건이 있기 때문에 이 요소가 정답에 포함되었는가?

### Step 3. 문제 원문에서 근거 역추적

문제 원문에서 그 조건을 직접 나타내는 최소 구절을 찾는다.

### Step 4. 불필요한 조건 제거

다음 질문을 한다.

> 이 구절이 없어도 동일한 정답을 고를 수 있는가?

YES라면 형광펜 우선순위를 낮추거나 제거한다.

### Step 5. 최종 매칭

남은 문제 구절과 정답 요소를 ①②③④ 형식으로 직접 연결한다.

---

# 최종 예시

### Q172 / Answer: C

**문제 인용 ↔ 정답 인용**

① “각 사업부는 CIDR 범위가 겹치는 여러 VPC로 자체 네트워크를 관리” → “AWS PrivateLink 엔드포인트 서비스를 생성”

② “다른 모든 비즈니스 단위에서 응용 프로그램에 액세스” → “특정 AWS 계정에 서비스 연결 권한을 부여”

③ “솔루션은 사설 IP 주소만 사용” → “다른 계정에 인터페이스 VPC 엔드포인트를 생성”

④ “최소한의 운영 오버헤드” → “AWS PrivateLink 사용”

**정답 연결**

CIDR이 겹치는 VPC 간 서비스 공유에는 AWS PrivateLink가 적합하다.  
Interface VPC Endpoint를 사용하므로 VPC Peering이나 NAT 없이 private IP로 특정 서비스에 접근할 수 있다.

---

# 응답 규칙

- 불필요한 서론을 넣지 않는다.
- “정리해드리겠습니다” 등의 문장을 넣지 않는다.
- 바로 `### Q번호 / Answer: 정답`부터 시작한다.
- 문제별로 `---`를 넣어 구분한다.
- 한 번에 최대 10문제만 처리한다.
- 문제 인용과 정답 인용을 절대 따로 나열하지 않는다.
- 반드시 문제 조건 → 정답 요소 형태로 직접 매칭한다.
- 문제 전체를 길게 요약하지 않는다.
- 오답 분석을 하지 않는다.
- 실제 형광펜 대상은 각 매칭의 왼쪽 `문제 인용` 부분이다.
