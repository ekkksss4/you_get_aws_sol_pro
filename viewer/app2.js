const state = {
  questions: [],
  index: 0,
  highlightEnabled: true,
};

const card = document.getElementById("card");
const statusEl = document.getElementById("status");
const progressEl = document.getElementById("progress");
const qTitleEl = document.getElementById("qTitle");
const qTextEl = document.getElementById("qText");
const choiceListEl = document.getElementById("choiceList");
const answerEl = document.getElementById("answer");
const mappingEl = document.getElementById("mapping");

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const jumpInput = document.getElementById("jumpInput");
const jumpBtn = document.getElementById("jumpBtn");
const highlightBtn = document.getElementById("highlightBtn");

const COMMON_TOKEN_EXCLUDES = new Set([
  "AWS",
  "AMAZON",
  "THE",
  "AND",
  "FOR",
  "WITH",
  "FROM",
  "THAT",
  "THIS",
  "INTO",
  "USING",
]);

const KO_STOPWORDS = new Set([
  "회사",
  "회사는",
  "요구",
  "사항",
  "기능",
  "합니다",
  "있습니다",
  "있어야",
  "있는",
  "위한",
  "대한",
  "솔루션",
  "사용",
  "생성",
  "연결",
  "구성",
  "데이터",
  "서버",
  "문제",
  "정답",
  "운영",
  "지원",
  "수행",
  "계층",
  "기반",
  "작업",
  "활성화",
  "변경",
  "배포",
  "추가",
  "인스턴스",
  "사용하여",
  "배포된",
  "애플리케이션",
  "서비스",
]);

const INTENT_RULES = [
  {
    name: "ops_overhead",
    questionPattern: /(운영\s*오버헤드|관리\s*오버헤드|운영\s*부담)/i,
    answerPatterns: [
      /AWS\s+Fargate/i,
      /Amazon\s+EKS/i,
      /Amazon\s+Managed\s+Streaming/i,
      /CloudFront/i,
      /자동\s*확장|Auto\s*Scaling/i,
    ],
  },
  {
    name: "traffic_scale",
    questionPattern: /(주문|트래픽|증가|릴리스|확장)/i,
    answerPatterns: [
      /자동\s*확장|Auto\s*Scaling/i,
      /읽기\s*전용\s*복제본|read-only\s*replica/i,
      /AWS\s+Fargate/i,
      /CloudFront/i,
    ],
  },
  {
    name: "kafka_managed",
    questionPattern: /Kafka|메시지\s*스트림/i,
    answerPatterns: [/Amazon\s+Managed\s+Streaming|MSK|Managed\s+Streaming/i],
  },
  {
    name: "static_content",
    questionPattern: /(정적\s*콘텐츠|정적\s*파일)/i,
    answerPatterns: [/Amazon\s+S3/i, /CloudFront/i],
  },
  {
    name: "db_resilience_scale",
    questionPattern: /(PostgreSQL|RDS|데이터베이스)/i,
    answerPatterns: [
      /읽기\s*전용\s*복제본|read-only\s*replica/i,
      /다중\s*AZ|Multi-?AZ/i,
      /스토리지\s*Auto\s*Scaling/i,
    ],
  },
];

function setStatus(message) {
  statusEl.textContent = message;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function splitSentences(text) {
  return text
    .split(/(?<=[.!?])\s+|\n+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function extractQuestionCueTerms(questionText) {
  const cues = [
    /운영\s*오버헤드/gi,
    /비용\s*효율(?:적)?/gi,
    /최저\s*비용/gi,
    /비용\s*보고서/gi,
    /최소(?:한)?/gi,
    /고가용성/gi,
    /확장(?:성)?/gi,
    /장애\s*조치/gi,
    /다중\s*AZ|Multi-?AZ/gi,
    /읽기\s*전용\s*복제본|read-only\s*replica/gi,
    /정적\s*콘텐츠/gi,
    /트래픽|주문\s*증가/gi,
    /지연\s*시간/gi,
    /컨테이너/gi,
    /Kafka|MSK|Managed\s+Streaming/gi,
    /PostgreSQL|RDS/gi,
    /WorkSpaces|FSx|CloudWatch|EventBridge|Athena|QuickSight/gi,
    /Organizations|Savings\s*Plan|Client\s*VPN/gi,
    /Amazon\s+S3|CloudFront|Lambda|EKS|Fargate|Auto\s*Scaling/gi,
  ];

  const terms = [];
  for (const pattern of cues) {
    const matches = questionText.match(pattern) ?? [];
    for (const raw of matches) {
      const t = raw.trim();
      if (t.length >= 2 && !terms.some((x) => x.toLowerCase() === t.toLowerCase())) {
        terms.push(t);
      }
    }
  }

  return terms.slice(0, 4);
}

function extractGenericQuestionTerms(questionText) {
  const rawTokens = questionText
    .replace(/[()\[\],.:;!?"'`]/g, " ")
    .split(/\s+/)
    .map((token) => normalizeKoToken(token))
    .filter(Boolean);

  const unique = [];
  for (const token of rawTokens) {
    const upper = token.toUpperCase();
    if (token.length < 3) {
      continue;
    }
    if (KO_STOPWORDS.has(token) || COMMON_TOKEN_EXCLUDES.has(upper)) {
      continue;
    }
    if (/^[0-9]+$/.test(token)) {
      continue;
    }
    if (!unique.some((v) => v.toLowerCase() === token.toLowerCase())) {
      unique.push(token);
    }
  }

  unique.sort((a, b) => b.length - a.length);
  return unique.slice(0, 4);
}

function normalizeForMatch(text) {
  return String(text)
    .toLowerCase()
    .replace(/[\s.,:;!?"'()\[\]{}]/g, "");
}

function normalizeKoToken(word) {
  return String(word)
    .trim()
    .replace(/[은는이가을를에의와과로도만께서]/g, "")
    .replace(/(으로|에서|에게|부터|까지|하며|하고|합니다|입니다)$/u, "")
    .trim();
}

function highlightText(text, terms) {
  const filtered = Array.from(
    new Set(
      terms
        .map((v) => String(v).trim())
        .filter((v) => v.length >= 2)
    )
  ).sort((a, b) => b.length - a.length);

  if (filtered.length === 0) {
    return escapeHtml(text);
  }

  const pattern = new RegExp(filtered.map(escapeRegExp).join("|"), "gi");
  let last = 0;
  let output = "";

  for (const match of text.matchAll(pattern)) {
    const start = match.index ?? 0;
    output += escapeHtml(text.slice(last, start));
    output += `<mark class="hl">${escapeHtml(match[0])}</mark>`;
    last = start + match[0].length;
  }

  output += escapeHtml(text.slice(last));
  return output;
}

function highlightQuestionBlocks(text, terms) {
  const cleanTerms = terms.filter((v) => v.length >= 2);
  if (cleanTerms.length === 0) {
    return escapeHtml(text);
  }

  const sentenceParts = text.split(/([.!?。]|\n)/g);
  let out = "";

  for (let i = 0; i < sentenceParts.length; i += 2) {
    const body = sentenceParts[i] ?? "";
    const punct = sentenceParts[i + 1] ?? "";
    const sentence = `${body}${punct}`;
    if (!sentence.trim()) {
      continue;
    }

    const hasTerm = cleanTerms.some((term) =>
      sentence.toUpperCase().includes(term.toUpperCase())
    );

    if (hasTerm) {
      out += `<mark class="hl-block">${highlightText(sentence, cleanTerms)}</mark> `;
    } else {
      out += `${escapeHtml(sentence)} `;
    }
  }

  return out.trim();
}

function highlightQuestionByQuotes(text, terms, quotes, cueTerms) {
  const sentences = splitSentences(text);
  const normalizedQuotes = quotes
    .map((q) => normalizeForMatch(q))
    .filter((q) => q.length > 0);

  if (sentences.length === 0) {
    return escapeHtml(text);
  }

  // Fallback: if no intent quotes are available, keep baseline keyword highlights.
  if (normalizedQuotes.length === 0) {
    return highlightQuestionBlocks(text, [...terms, ...cueTerms]);
  }

  let highlightedCount = 0;
  const parts = sentences.map((sentence) => {
    const nSentence = normalizeForMatch(sentence);
    const isCore = normalizedQuotes.some(
      (q) => q.includes(nSentence) || nSentence.includes(q)
    );

    if (isCore) {
      highlightedCount += 1;
      return `<mark class="hl-block">${highlightText(sentence, terms)}</mark>`;
    }

    return escapeHtml(sentence);
  });

  // Fallback: if quote matching is too strict and marks nothing, use baseline mode.
  if (highlightedCount < 2) {
    return highlightQuestionBlocks(text, [...terms, ...cueTerms]);
  }

  return parts.join(" ");
}

function pickLinkTerms(questionText, answerTexts) {
  const answerBlob = answerTexts.join(" ");
  const questionUpper = questionText.toUpperCase();

  const serviceMatches = answerBlob.match(/\b(?:Amazon|AWS)\s+[A-Za-z0-9@.+-]+(?:\s+[A-Za-z0-9@.+-]+){0,3}\b/g) ?? [];
  const tokenMatches = answerBlob.match(/\b[A-Z][A-Z0-9-]{2,}\b/g) ?? [];

  const candidates = [...serviceMatches, ...tokenMatches];
  const phraseCandidates = [];
  const wordCandidates = [];
  const terms = [];

  const normalizedQuestion = questionText
    .replace(/[()\[\],.:;"'`]/g, " ")
    .replace(/\s+/g, " ");

  const answerWords = answerBlob
    .replace(/[()\[\],.:;"'`]/g, " ")
    .split(/\s+/)
    .map((w) => w.trim())
    .filter(Boolean);

  // Add Korean/mixed tokens so non-English clues are also highlightable.
  for (const word of answerWords) {
    const cleanWord = word.replace(/^[^\p{L}\p{N}-]+|[^\p{L}\p{N}-]+$/gu, "");
    const normalizedWord = normalizeKoToken(cleanWord);
    if (normalizedWord.length < 3) {
      continue;
    }
    if (KO_STOPWORDS.has(cleanWord) || KO_STOPWORDS.has(normalizedWord)) {
      continue;
    }
    const upperWord = normalizedWord.toUpperCase();
    if (COMMON_TOKEN_EXCLUDES.has(upperWord)) {
      continue;
    }
    if (normalizedQuestion.includes(cleanWord) || normalizedQuestion.includes(normalizedWord)) {
      wordCandidates.push(normalizedWord);
    }
  }

  // Add two-word phrase candidates (ex: "고정 세션", "Auto Scaling", "User-Agent 헤더")
  for (let i = 0; i < answerWords.length - 1; i += 1) {
    const a = answerWords[i].trim();
    const b = answerWords[i + 1].trim();
    if (!a || !b) {
      continue;
    }
    const phrase = `${a} ${b}`.replace(/\s+/g, " ").trim();
    if (phrase.length < 4) {
      continue;
    }
    if (normalizedQuestion.includes(phrase)) {
      phraseCandidates.push(phrase);
    }
  }

  candidates.push(...phraseCandidates, ...wordCandidates);

  for (const termRaw of candidates) {
    const term = termRaw.trim();
    const upper = term.toUpperCase();

    if (COMMON_TOKEN_EXCLUDES.has(upper)) {
      continue;
    }

    if (upper.length < 2) {
      continue;
    }

    if (!questionUpper.includes(upper) && !normalizedQuestion.includes(term)) {
      continue;
    }

    if (!terms.includes(term)) {
      terms.push(term);
    }
  }

  // Keep 2-4 high-signal links:
  // 1) AWS/Amazon service phrases, 2) matched 2-word phrases, 3) other words.
  const serviceFirst = terms.filter((t) => /^(AWS|Amazon)\s/i.test(t));
  const twoWord = terms.filter((t) => t.includes(" ") && !serviceFirst.includes(t));
  const singleWord = terms.filter(
    (t) =>
      !t.includes(" ") &&
      !serviceFirst.includes(t) &&
      !KO_STOPWORDS.has(t) &&
      t.length >= 3
  );

  const prioritized = [...serviceFirst, ...twoWord, ...singleWord];
  const limited = [];
  for (const term of prioritized) {
    if (!limited.includes(term)) {
      limited.push(term);
    }
    if (limited.length >= 4) {
      break;
    }
  }

  // If too sparse, keep at least 2 clues when possible.
  if (limited.length < 2 && prioritized.length >= 2) {
    return prioritized.slice(0, 2);
  }

  return limited;
}

function findSentenceByPattern(text, pattern) {
  const sentences = splitSentences(text);
  return sentences.find((s) => pattern.test(s)) ?? "";
}

function extractIntentLinks(questionText, correctChoices) {
  const answerText = correctChoices.map((c) => c.text).join(" ");
  const links = [];

  for (const rule of INTENT_RULES) {
    if (!rule.questionPattern.test(questionText)) {
      continue;
    }

    const qQuote = findSentenceByPattern(questionText, rule.questionPattern);
    for (const pattern of rule.answerPatterns) {
      const aQuote = findSentenceByPattern(answerText, pattern);
      if (!aQuote) {
        continue;
      }

      const termMatch = aQuote.match(pattern);
      const term = (termMatch?.[0] ?? "").trim();
      links.push({
        rule: rule.name,
        term,
        qQuote: qQuote || questionText.slice(0, 120),
        aQuote,
      });
      break;
    }
  }

  const unique = [];
  for (const row of links) {
    if (row.term && !unique.some((x) => x.term.toLowerCase() === row.term.toLowerCase())) {
      unique.push(row);
    }
  }

  return unique.slice(0, 4);
}

function extractSnippet(text, term, radius = 40) {
  const lowerText = text.toLowerCase();
  const lowerTerm = term.toLowerCase();
  const idx = lowerText.indexOf(lowerTerm);
  if (idx < 0) {
    return text.slice(0, Math.min(80, text.length)).trim();
  }

  let start = Math.max(0, idx - radius);
  let end = Math.min(text.length, idx + term.length + radius);

  while (start > 0 && text[start] !== " ") {
    start -= 1;
  }
  while (end < text.length && text[end] !== " ") {
    end += 1;
  }

  const slice = text.slice(start, end).replace(/\s+/g, " ").trim();
  return slice;
}

function buildMappings(questionText, correctChoices, terms) {
  const rows = [];
  const selectedTerms = terms.slice(0, 3);

  for (const term of selectedTerms) {
    const answerChoice = correctChoices.find((c) => c.text.toLowerCase().includes(term.toLowerCase()));
    if (!answerChoice) {
      continue;
    }

    const qQuote = extractSnippet(questionText, term, 36);
    const aQuote = extractSnippet(answerChoice.text, term, 36);
    rows.push({ qQuote, aQuote });
  }

  if (rows.length === 0 && correctChoices.length > 0) {
    const fallback = correctChoices[0].text.slice(0, Math.min(90, correctChoices[0].text.length));
    rows.push({
      qQuote: questionText.slice(0, Math.min(90, questionText.length)),
      aQuote: fallback,
    });
  }

  return rows.slice(0, 3);
}

function parseAnswerLabels(answerValue) {
  if (Array.isArray(answerValue)) {
    return answerValue
      .map((v) => String(v).trim().toUpperCase())
      .filter((v) => /^[A-F]$/.test(v));
  }

  const raw = String(answerValue ?? "").toUpperCase();
  const matches = raw.match(/\b[A-F]\b/g);
  return matches ? Array.from(new Set(matches)) : [];
}

function normalizeQuestions(raw) {
  if (!Array.isArray(raw)) {
    throw new Error("루트는 배열이어야 합니다.");
  }

  return raw.map((item, idx) => {
    if (!item || typeof item !== "object") {
      throw new Error(`${idx + 1}번째 항목이 객체가 아닙니다.`);
    }

    const qNumber = Number(item.qNumber ?? idx + 1);
    const question = String(item.question ?? "").trim();
    const answerLabels = parseAnswerLabels(item.answers ?? item.answer ?? "");

    if (!question) {
      throw new Error(`Q${qNumber}: question이 비어 있습니다.`);
    }

    if (!Array.isArray(item.choices) || item.choices.length < 2) {
      throw new Error(`Q${qNumber}: choices는 최소 2개가 필요합니다.`);
    }

    const choices = item.choices.map((choice, cIdx) => {
      if (typeof choice === "string") {
        const parts = choice.split(".");
        if (parts.length >= 2) {
          return {
            label: parts[0].trim(),
            text: parts.slice(1).join(".").trim(),
          };
        }
        return {
          label: String.fromCharCode(65 + cIdx),
          text: choice.trim(),
        };
      }

      return {
        label: String(choice.label ?? String.fromCharCode(65 + cIdx)).trim(),
        text: String(choice.text ?? "").trim(),
      };
    });

    const labels = new Set(choices.map((v) => v.label));
    if (answerLabels.length === 0) {
      throw new Error(`Q${qNumber}: answer가 비어 있습니다.`);
    }

    const invalid = answerLabels.filter((v) => !labels.has(v));
    if (invalid.length > 0) {
      throw new Error(`Q${qNumber}: answer(${invalid.join(", ")})가 choices label과 일치하지 않습니다.`);
    }

    return {
      qNumber,
      question,
      choices,
      answers: answerLabels,
      answerDisplay: answerLabels.join(", "),
      explanation: String(item.explanation ?? "").trim(),
    };
  });
}

function render() {
  const total = state.questions.length;
  if (!total) {
    card.classList.add("hidden");
    progressEl.textContent = "0 / 0";
    return;
  }

  const current = state.questions[state.index];
  const page = state.index + 1;
  const correctLabels = new Set(current.answers);
  const correctChoices = current.choices.filter((choice) => correctLabels.has(choice.label));
  const intentLinks = extractIntentLinks(current.question, correctChoices);
  const intentTerms = intentLinks.map((x) => x.term).filter(Boolean);
  const intentQuestionQuotes = intentLinks.map((x) => x.qQuote).filter(Boolean);
  const overlapTerms = pickLinkTerms(current.question, correctChoices.map((choice) => choice.text));
  const specificCueTerms = extractQuestionCueTerms(current.question);
  const genericCueTerms = extractGenericQuestionTerms(current.question);
  const questionCueTerms = Array.from(new Set([...specificCueTerms, ...genericCueTerms])).slice(0, 5);
  const linkTerms = state.highlightEnabled
    ? Array.from(new Set([...intentTerms, ...overlapTerms])).slice(0, 5)
    : [];

  qTitleEl.textContent = `Q${current.qNumber}`;
  qTextEl.innerHTML = state.highlightEnabled
    ? highlightQuestionByQuotes(current.question, linkTerms, intentQuestionQuotes, questionCueTerms)
    : escapeHtml(current.question);

  choiceListEl.innerHTML = "";
  current.choices.forEach((choice) => {
    const li = document.createElement("li");

    const line = `${choice.label}. ${choice.text}`;
    if (correctLabels.has(choice.label)) {
      li.classList.add("correct-choice");
      li.innerHTML = state.highlightEnabled ? highlightText(line, linkTerms) : escapeHtml(line);
    } else {
      li.textContent = line;
    }

    choiceListEl.appendChild(li);
  });

  answerEl.textContent = `Answer: ${current.answerDisplay}`;

  const mappings = intentLinks.length > 0
    ? intentLinks.slice(0, 3).map((x) => ({ qQuote: x.qQuote, aQuote: x.aQuote }))
    : buildMappings(current.question, correctChoices, linkTerms);
  mappingEl.innerHTML = `
    <h3>문제 인용 ↔ 정답 인용</h3>
    ${mappings
      .map(
        (row, idx) =>
          `<p class="mapping-row">${idx + 1}. "${escapeHtml(row.qQuote)}" <span class="mapping-arrow">→</span> "${escapeHtml(row.aQuote)}"</p>`
      )
      .join("")}
  `;

  progressEl.textContent = `${page} / ${total}`;
  card.classList.remove("hidden");

  const batchStart = Math.floor(state.index / 10) * 10 + 1;
  const batchEnd = Math.min(batchStart + 9, total);
  setStatus(`현재 배치: ${batchStart}~${batchEnd} (최대 10문제 단위)`);
}

function applyQuestions(questions) {
  state.questions = questions;
  state.index = 0;
  render();
}

async function autoLoadDefault() {
  try {
    if (Array.isArray(window.DEFAULT_QUESTIONS) && window.DEFAULT_QUESTIONS.length > 0) {
      applyQuestions(normalizeQuestions(window.DEFAULT_QUESTIONS));
      setStatus("기본 문제 데이터를 불러왔습니다.");
      return;
    }

    const response = await fetch("../data/questions/questions.json");
    if (!response.ok) {
      throw new Error("기본 questions.json을 읽지 못했습니다.");
    }

    const data = await response.json();
    applyQuestions(normalizeQuestions(data));
    setStatus("questions.json을 자동 로드했습니다.");
  } catch (error) {
    setStatus(`데이터를 불러오세요. (${error.message})`);
  }
}

function move(delta) {
  const total = state.questions.length;
  if (!total) {
    return;
  }

  state.index = Math.min(total - 1, Math.max(0, state.index + delta));
  render();
}

function jumpToQuestion() {
  const total = state.questions.length;
  if (!total) {
    return;
  }

  const value = Number(jumpInput.value);
  if (!Number.isFinite(value)) {
    setStatus("이동할 Q번호를 입력하세요.");
    return;
  }

  const targetIndex = state.questions.findIndex((q) => q.qNumber === value);
  if (targetIndex < 0) {
    setStatus(`Q${value}를 찾을 수 없습니다.`);
    return;
  }

  state.index = targetIndex;
  render();
}

prevBtn.addEventListener("click", () => move(-1));
nextBtn.addEventListener("click", () => move(1));
jumpBtn.addEventListener("click", jumpToQuestion);
highlightBtn.addEventListener("click", () => {
  state.highlightEnabled = !state.highlightEnabled;
  highlightBtn.textContent = state.highlightEnabled ? "연결 형광 ON" : "연결 형광 OFF";
  render();
});

render();
autoLoadDefault();
