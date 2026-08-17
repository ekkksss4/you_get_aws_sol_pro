const state = { questions: [], index: 0 };

const card = document.getElementById("card");
const statusEl = document.getElementById("status");
const progressEl = document.getElementById("progress");
const qTitleEl = document.getElementById("qTitle");
const qTextEl = document.getElementById("qText");
const choiceListEl = document.getElementById("choiceList");
const answerEl = document.getElementById("answer");
const mappingEl = document.getElementById("mapping");
const jumpInput = document.getElementById("jumpInput");

const stopwords = new Set([
  "회사", "회사는", "사용", "사용하여", "합니다", "있습니다", "있는", "위한", "대한",
  "문제", "요구", "사항", "서비스", "애플리케이션", "데이터", "시스템", "구성", "생성",
  "연결", "활성화", "변경", "배포", "추가", "인스턴스", "제공", "수행", "경우",
]);

const decisionCriteria = [
  /LEAST\s*operational\s*overhead|운영\s*오버헤드가\s*가장\s*낮은|운영\s*부담을\s*줄|관리\s*부담을\s*최소화/i,
  /MOST\s*cost.?effective|비용\s*효율|최저\s*비용|비용을\s*절감/i,
  /MINIMUM\s*downtime|다운타임.*최소화|가동\s*중지\s*시간.*최소|최소한의\s*중단/i,
  /real.?time|실시간|immediately|즉시/i,
  /high\s*availability|고가용성|가용성.*높|장애.*자동/i,
  /fault\s*toleran|disaster\s*recovery|복구력|재해\s*복구/i,
];

const answerJustifiers = [
  { answerPattern: /Fargate|ECS/i, justifyPatterns: [/운영\s*오버헤드|관리\s*부담/i, /운영을.*간소화|자동으로.*관리/i] },
  { answerPattern: /Auto\s*Scaling/i, justifyPatterns: [/트래픽.*변|주문.*증가|부하.*변동|동적.*조정/i, /최대\s*부하|피크\s*시간/i] },
  { answerPattern: /CloudFront/i, justifyPatterns: [/정적\s*콘텐츠|정적\s*파일/i, /전 세계|전세계|전 지역|여러\s*지역|사용자.*멀|지연\s*시간/i] },
  { answerPattern: /Read\s*Replica|읽기\s*전용\s*복제본/i, justifyPatterns: [/읽기\s*부하|읽기.*증가|조회.*증가/i, /자동.*확장|읽기.*확장/i] },
  { answerPattern: /Multi.?AZ|다중\s*AZ/i, justifyPatterns: [/가용\s*영역|AZ.*장애|단일.*리전|지역\s*장애/i, /다운타임\s*최소|고가용성/i] },
  { answerPattern: /Cross.?Region\s*Replication|Global\s*Table/i, justifyPatterns: [/리전.*장애|여러\s*리전|다중\s*리전/i, /재해\s*복구|복제\s*완료/i] },
  { answerPattern: /S3\s*RTC|Replication\s*Time\s*Control/i, justifyPatterns: [/복제.*시간.*보장|복제.*완료.*시간/i, /RTC|S3\s+RTC/i] },
  { answerPattern: /PrivateLink|VPC\s*Endpoint/i, justifyPatterns: [/인터넷.*거치지|사설\s*IP|프라이빗.*접근|VPC.*내부/i] },
  { answerPattern: /Transit\s*Gateway/i, justifyPatterns: [/여러\s*VPC|다중\s*VPC|VPC.*연결/i, /CIDR.*겹|VPC.*간.*통신/i] },
  { answerPattern: /Managed\s*Streaming|MSK/i, justifyPatterns: [/Kafka.*관리|운영\s*부담|브로커.*운영/i, /메시지.*스트림|이벤트.*스트림/i] },
];

function escapeHtml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function parseAnswers(value) {
  if (Array.isArray(value)) return value.map((v) => String(v).trim().toUpperCase()).filter(Boolean);
  return (String(value ?? "").toUpperCase().match(/\b[A-F]\b/g) ?? []);
}

function normalizeQuestions(raw) {
  if (!Array.isArray(raw)) throw new Error("문제 데이터가 배열이 아닙니다.");
  return raw.map((item, index) => {
    const answers = parseAnswers(item.answers ?? item.answer);
    const choices = (item.choices ?? []).map((choice, choiceIndex) => {
      if (typeof choice === "string") {
        const split = choice.split(".");
        return { label: (split[0] ?? String.fromCharCode(65 + choiceIndex)).trim().toUpperCase(), text: split.slice(1).join(".").trim() || choice.trim() };
      }
      return { label: String(choice.label ?? String.fromCharCode(65 + choiceIndex)).trim().toUpperCase(), text: String(choice.text ?? "").trim() };
    });
    if (!item.question || choices.length < 2 || answers.length === 0) throw new Error(`Q${item.qNumber ?? index + 1} 데이터가 부족합니다.`);
    return { qNumber: Number(item.qNumber ?? index + 1), question: String(item.question).trim(), choices, answers, hints: Array.isArray(item.hints) ? item.hints : [] };
  });
}

function normalizeHints(rawHints) {
  if (!Array.isArray(rawHints)) return [];
  return rawHints
    .map((hint) => {
      if (typeof hint === "string") {
        return { text: hint.trim(), importance: "supporting", linkedTo: "" };
      }
      if (!hint || typeof hint !== "object") return null;
      const text = String(hint.text ?? hint.term ?? "").trim();
      if (!text) return null;
      return {
        text,
        importance: String(hint.importance ?? "supporting").trim() || "supporting",
        linkedTo: String(hint.linkedTo ?? hint.service ?? hint.answer ?? "").trim(),
      };
    })
    .filter(Boolean)
    .slice(0, 5);
}

function resolveQuestionHints(currentQuestion, correctChoices) {
  const explicitHints = normalizeHints(currentQuestion.hints ?? []);
  if (explicitHints.length > 0) {
    return explicitHints.map((hint) => hint.text);
  }

  const links = findCoreLinks(currentQuestion.question, correctChoices.map((choice) => choice.text));
  return links.length > 0 ? links.map((link) => link.term).slice(0, 5) : fallbackTerms(currentQuestion.question);
}

function findCoreLinks(question, correctTexts) {
  const answerText = correctTexts.join(" ") + " ";
  const links = [];

  // 1단계: 정답 요소를 찾고, 그것을 정당화하는 문제 조건 찾기
  for (const justifier of answerJustifiers) {
    if (!justifier.answerPattern.test(answerText)) continue;
    const answerService = answerText.match(justifier.answerPattern)[0];

    for (const justifyPattern of justifier.justifyPatterns) {
      const match = question.match(justifyPattern);
      if (match) {
        const term = match[0];
        links.push({
          term,
          service: answerService,
          questionQuote: question.slice(Math.max(0, match.index - 40), Math.min(question.length, match.index + term.length + 60)).trim(),
          answerQuote: answerService,
        });
        break;
      }
    }
  }

  return links.slice(0, 5);
}

function fallbackTerms(question) {
  const patterns = [
    /운영\s*오버헤드|관리\s*부담|운영\s*부담/gi,
    /트래픽\s*(?:증가|급증|변동)|주문(?:이|을)?\s*(?:크게\s*)?증가/gi,
    /정적\s*(?:콘텐츠|파일)/gi,
    /고가용성|장애\s*조치|재해\s*복구/gi,
    /사설\s*(?:IP|접근|연결)|인터넷을\s*거치지/gi,
    /컨테이너|Kubernetes|Kafka|메시지\s*스트림/gi,
    /읽기\s*전용\s*복제본|다중\s*AZ|Multi-?AZ/gi,
    /복제\s*(?:시간|완료)|리전\s*간/gi,
    /비용\s*(?:최적화|효율|절감)|최저\s*비용/gi,
    /Amazon\s+[A-Za-z0-9.-]+|AWS\s+[A-Za-z0-9.-]+/gi,
    /\b(?:S3|EC2|RDS|Aurora|Lambda|EKS|ECS|Fargate|CloudFront|Route\s*53|MSK|VPC)\b/gi,
  ];

  const questionTerms = [];
  for (const pattern of patterns) {
    for (const match of question.match(pattern) ?? []) {
      const term = match.trim();
      if (term.length >= 3 && !questionTerms.some((item) => item.toLowerCase() === term.toLowerCase())) {
        questionTerms.push(term);
      }
    }
  }

  if (questionTerms.length > 0) {
    return questionTerms.slice(0, 5);
  }

  // 최종 폴백: 문제에서 의미 있는 단어
  const questionWords = question.match(/[A-Za-z][A-Za-z0-9+./-]{2,}|[가-힣]{3,}/g) ?? [];
  return questionWords
    .filter((word, index, words) => !stopwords.has(word) && words.indexOf(word) === index)
    .sort((left, right) => right.length - left.length)
    .slice(0, 3);
}

function highlight(text, terms) {
  const unique = Array.from(new Set(terms.filter(Boolean))).sort((a, b) => b.length - a.length);
  if (unique.length === 0) return escapeHtml(text);
  const pattern = new RegExp(unique.map(escapeRegExp).join("|"), "gi");
  let result = "";
  let last = 0;
  for (const match of text.matchAll(pattern)) {
    const start = match.index ?? 0;
    result += escapeHtml(text.slice(last, start));
    result += `<mark class="hl">${escapeHtml(match[0])}</mark>`;
    last = start + match[0].length;
  }
  return result + escapeHtml(text.slice(last));
}

function render() {
  const current = state.questions[state.index];
  if (!current) return;
  const correctChoices = current.choices.filter((choice) => current.answers.includes(choice.label));
  const links = findCoreLinks(current.question, correctChoices.map((choice) => choice.text));
  const terms = resolveQuestionHints(current, correctChoices);

  qTitleEl.textContent = `Q${current.qNumber}`;
  qTextEl.innerHTML = highlight(current.question, terms);
  choiceListEl.innerHTML = correctChoices.map((choice) => `<li class="correct-choice correct-choice--v5">${highlight(`${choice.label}. ${choice.text}`, terms)}</li>`).join("");
  answerEl.textContent = `Answer: ${current.answers.join(", ")}`;

  const rows = links.length > 0 ? links : correctChoices.slice(0, 2).map((choice) => ({ questionQuote: current.question.slice(0, 100), answerQuote: choice.text.slice(0, 120) }));
  mappingEl.innerHTML = `<h3>문제 인용 ↔ 정답 인용</h3>${rows.map((row, index) => `<p class="mapping-row">${index + 1}. "${escapeHtml(row.questionQuote)}" <span class="mapping-arrow">→</span> "${escapeHtml(row.answerQuote)}"</p>`).join("")}`;

  progressEl.textContent = `${state.index + 1} / ${state.questions.length}`;
  statusEl.textContent = "문제 핵심 단서와 정답 보기만 표시합니다.";
  card.classList.remove("hidden");
}

function move(delta) {
  state.index = Math.min(state.questions.length - 1, Math.max(0, state.index + delta));
  render();
}

document.getElementById("prevBtn").addEventListener("click", () => move(-1));
document.getElementById("nextBtn").addEventListener("click", () => move(1));
document.getElementById("jumpBtn").addEventListener("click", () => {
  const target = state.questions.findIndex((question) => question.qNumber === Number(jumpInput.value));
  if (target < 0) { statusEl.textContent = `Q${jumpInput.value}를 찾을 수 없습니다.`; return; }
  state.index = target;
  render();
});

// 데이터 로드 함수
function applyHintMap(questions, hintMap) {
  if (!Array.isArray(questions)) return questions;
  const safeHintMap = hintMap && typeof hintMap === "object" ? hintMap : {};

  return questions.map((question) => {
    const qNumber = Number(question.qNumber);
    const batchHint = Array.isArray(safeHintMap)
      ? safeHintMap.find((item) => Number(item?.qNumber) === qNumber)
      : safeHintMap[qNumber];
    const externalHints = batchHint?.highlights ?? batchHint?.hints ?? batchHint ?? [];
    const explicitHints = Array.isArray(question.hints) && question.hints.length > 0 ? question.hints : externalHints;
    return { ...question, hints: normalizeHints(explicitHints) };
  });
}

function loadData() {
  if (window.DEFAULT_QUESTIONS && window.DEFAULT_QUESTIONS.length > 0) {
    try {
      const withHints = applyHintMap(normalizeQuestions(window.DEFAULT_QUESTIONS), window.DEFAULT_HINTS ?? {});
      state.questions = withHints;
      card.classList.remove("hidden");
      render();
      return;
    } catch (error) {
      statusEl.textContent = `오류: ${error.message}`;
      return;
    }
  }

  const loadHintBatch = (path) => fetch(path).then((r) => {
    if (!r.ok) return [];
    return r.json();
  }).catch(() => []);

  Promise.all([
    fetch("../data/questions/questions.json").then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    }),
    fetch("../data/questions/questions.hints.json").then((r) => {
      if (!r.ok) return {};
      return r.json();
    }).catch(() => ({})),
    fetch("../data/reclassified/hints_manifest.json").then((r) => {
      if (!r.ok) return [];
      return r.json();
    }).catch(() => []),
  ])
    .then(([data, hintMap, hintManifest]) => {
      let questions = normalizeQuestions(data);
      questions = applyHintMap(questions, hintMap);
      return Promise.all(hintManifest.map((path) => loadHintBatch(`../data/reclassified/${path}`)))
        .then((hintBatches) => {
          for (const hintBatch of hintBatches) {
            questions = applyHintMap(questions, hintBatch);
          }
          state.questions = questions;
          card.classList.remove("hidden");
          render();
        });
    })
    .catch((err) => {
      statusEl.textContent = `데이터 로드 실패: ${err.message}`;
    });
}

// 페이지 로드 시 데이터 로드
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", loadData);
} else {
  loadData();
}
