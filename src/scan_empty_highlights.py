import json
import re
from pathlib import Path

questions = json.loads(Path('data/questions/questions.json').read_text(encoding='utf-8'))

ko_stop = {
    '회사','회사는','요구','사항','기능','합니다','있습니다','있어야','있는','위한','대한','솔루션','사용','생성','연결','구성','데이터','서버','문제','정답','운영','지원','수행','계층','기반','작업','활성화','변경','배포','추가','인스턴스','사용하여','배포된','애플리케이션','서비스'
}
common_ex = {'AWS','AMAZON','THE','AND','FOR','WITH','FROM','THAT','THIS','INTO','USING'}
intent_rules = [
    (re.compile(r'(운영\s*오버헤드|관리\s*오버헤드|운영\s*부담)', re.I), [re.compile(x,re.I) for x in [r'AWS\s+Fargate',r'Amazon\s+EKS',r'Amazon\s+Managed\s+Streaming',r'CloudFront',r'자동\s*확장|Auto\s*Scaling']]),
    (re.compile(r'(주문|트래픽|증가|릴리스|확장)', re.I), [re.compile(x,re.I) for x in [r'자동\s*확장|Auto\s*Scaling',r'읽기\s*전용\s*복제본|read-only\s*replica',r'AWS\s+Fargate',r'CloudFront']]),
    (re.compile(r'Kafka|메시지\s*스트림', re.I), [re.compile(r'Amazon\s+Managed\s+Streaming|MSK|Managed\s+Streaming', re.I)]),
    (re.compile(r'(정적\s*콘텐츠|정적\s*파일)', re.I), [re.compile(r'Amazon\s+S3', re.I), re.compile(r'CloudFront', re.I)]),
    (re.compile(r'(PostgreSQL|RDS|데이터베이스)', re.I), [re.compile(x,re.I) for x in [r'읽기\s*전용\s*복제본|read-only\s*replica',r'다중\s*AZ|Multi-?AZ',r'스토리지\s*Auto\s*Scaling']]),
]
cue_patterns = [re.compile(x,re.I) for x in [
    r'운영\s*오버헤드',r'비용\s*효율(?:적)?',r'최저\s*비용',r'비용\s*보고서',r'최소(?:한)?',r'고가용성',r'확장(?:성)?',r'장애\s*조치',r'다중\s*AZ|Multi-?AZ',r'읽기\s*전용\s*복제본|read-only\s*replica',r'정적\s*콘텐츠',r'트래픽|주문\s*증가',r'지연\s*시간',r'컨테이너',r'Kafka|MSK|Managed\s+Streaming',r'PostgreSQL|RDS',r'WorkSpaces|FSx|CloudWatch|EventBridge|Athena|QuickSight',r'Organizations|Savings\s*Plan|Client\s*VPN',r'Amazon\s+S3|CloudFront|Lambda|EKS|Fargate|Auto\s*Scaling'
]]


def normalize_ko_token(word: str) -> str:
    word = word.strip()
    word = re.sub(r'[은는이가을를에의와과로도만께서]', '', word)
    word = re.sub(r'(으로|에서|에게|부터|까지|하며|하고|합니다|입니다)$', '', word)
    return word.strip()


def pick_link_terms(question: str, answers: list[str]) -> list[str]:
    answer_blob = ' '.join(answers)
    q_upper = question.upper()
    service = re.findall(r'\b(?:Amazon|AWS)\s+[A-Za-z0-9@.+-]+(?:\s+[A-Za-z0-9@.+-]+){0,3}\b', answer_blob)
    token = re.findall(r'\b[A-Z][A-Z0-9-]{2,}\b', answer_blob)
    candidates = service + token
    phrase_candidates = []
    word_candidates = []
    terms = []

    punctuation_pattern = r"[()\[\],.:;\"'`]"
    normalized_question = re.sub(r'\s+', ' ', re.sub(punctuation_pattern, ' ', question))
    answer_words = [w.strip() for w in re.sub(punctuation_pattern, ' ', answer_blob).split() if w.strip()]

    for word in answer_words:
        clean = re.sub(r'^[^\w\-가-힣]+|[^\w\-가-힣]+$', '', word)
        norm = normalize_ko_token(clean)
        if len(norm) < 3:
            continue
        if clean in ko_stop or norm in ko_stop:
            continue
        upper = norm.upper()
        if upper in common_ex:
            continue
        if clean in normalized_question or norm in normalized_question:
            word_candidates.append(norm)

    for i in range(len(answer_words) - 1):
        phrase = (answer_words[i] + ' ' + answer_words[i + 1]).strip()
        if len(phrase) >= 4 and phrase in normalized_question:
            phrase_candidates.append(phrase)

    candidates += phrase_candidates + word_candidates
    for term in candidates:
        term = term.strip()
        upper = term.upper()
        if upper in common_ex or len(upper) < 2:
            continue
        if upper not in q_upper and term not in normalized_question:
            continue
        if term not in terms:
            terms.append(term)

    service_first = [t for t in terms if re.match(r'^(AWS|Amazon)\s', t, re.I)]
    two_word = [t for t in terms if ' ' in t and t not in service_first]
    single = [t for t in terms if ' ' not in t and t not in service_first and t not in ko_stop and len(t) >= 3]
    prioritized = service_first + two_word + single
    limited = []
    for term in prioritized:
        if term not in limited:
            limited.append(term)
        if len(limited) >= 4:
            break

    if len(limited) < 2 and len(prioritized) >= 2:
        return prioritized[:2]
    return limited


def extract_intent_links(question: str, answers: list[str]) -> list[str]:
    answer_text = ' '.join(answers)
    found = []
    for qpat, apats in intent_rules:
        if not qpat.search(question):
            continue
        for apat in apats:
            match = apat.search(answer_text)
            if match:
                found.append(match.group(0).strip())
                break

    unique = []
    for term in found:
        if term.lower() not in [x.lower() for x in unique]:
            unique.append(term)
    return unique[:4]


def cue_terms(question: str) -> list[str]:
    out = []
    for pat in cue_patterns:
        for match in pat.findall(question):
            term = match if isinstance(match, str) else next((g for g in match if g), '')
            term = term.strip()
            if term and term.lower() not in [x.lower() for x in out]:
                out.append(term)
    return out[:4]


def generic_terms(question: str) -> list[str]:
    punctuation_pattern = r"[()\[\],.:;\"'`]"
    raw_tokens = [normalize_ko_token(token) for token in re.sub(punctuation_pattern, ' ', question).split() if token.strip()]
    unique = []
    for token in raw_tokens:
        upper = token.upper()
        if len(token) < 3:
            continue
        if token in ko_stop or upper in common_ex:
            continue
        if re.fullmatch(r'[0-9]+', token):
            continue
        if token.lower() not in [x.lower() for x in unique]:
            unique.append(token)
    unique.sort(key=len, reverse=True)
    return unique[:4]


empty = []
for q in questions:
    labels = set(q.get('answers', [])) if q.get('answers') else {q['answer']}
    choices = [c['text'] for c in q['choices'] if c['label'] in labels]
    terms = list(dict.fromkeys(extract_intent_links(q['question'], choices) + pick_link_terms(q['question'], choices)))[:5]
    cues = list(dict.fromkeys(cue_terms(q['question']) + generic_terms(q['question'])))
    if len(terms) == 0 and len(cues) == 0:
        empty.append(q['qNumber'])

print(f'empty_count={len(empty)}')
print('sample=', empty[:50])
