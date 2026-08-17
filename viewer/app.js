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

const fileInput = document.getElementById("fileInput");
const loadSampleBtn = document.getElementById("loadSampleBtn");
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
  "요구",
  "사항",
  "기능",
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
]);

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

function pickLinkTerms(questionText, answerTexts) {
  const answerBlob = answerTexts.join(" ");
  const questionUpper = questionText.toUpperCase();

  const serviceMatches = answerBlob.match(/\b(?:Amazon|AWS)\s+[A-Za-z0-9@.+-]+(?:\s+[A-Za-z0-9@.+-]+){0,3}\b/g) ?? [];
  const tokenMatches = answerBlob.match(/\b[A-Z][A-Z0-9-]{1,}\b/g) ?? [];

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
    if (cleanWord.length < 2) {
      continue;
    }
    if (KO_STOPWORDS.has(cleanWord)) {
      continue;
    }
    const upperWord = cleanWord.toUpperCase();
    if (COMMON_TOKEN_EXCLUDES.has(upperWord)) {
      continue;
    }
    if (normalizedQuestion.includes(cleanWord)) {
      wordCandidates.push(cleanWord);
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

  // Keep only 2-3 high-signal links:
  // 1) AWS/Amazon service phrases, 2) matched 2-word phrases, 3) other words.
  const serviceFirst = terms.filter((t) => /^(AWS|Amazon)\s/i.test(t));
  const twoWord = terms.filter((t) => t.includes(" ") && !serviceFirst.includes(t));
  const singleWord = terms.filter((t) => !t.includes(" ") && !serviceFirst.includes(t));

  const prioritized = [...serviceFirst, ...twoWord, ...singleWord];
  const limited = [];
  for (const term of prioritized) {
    if (!limited.includes(term)) {
      limited.push(term);
    }
    if (limited.length >= 3) {
      break;
    }
  }

  return limited;
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
  const linkTerms = state.highlightEnabled
    ? pickLinkTerms(current.question, correctChoices.map((choice) => choice.text))
    : [];

  qTitleEl.textContent = `Q${current.qNumber}`;
  qTextEl.innerHTML = state.highlightEnabled
    ? highlightQuestionBlocks(current.question, linkTerms)
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

async function loadSample() {
  try {
    const response = await fetch("../data/questions/questions.sample.json");
    if (!response.ok) {
      throw new Error("샘플 JSON을 읽지 못했습니다.");
    }

    const data = await response.json();
    applyQuestions(normalizeQuestions(data));
    setStatus("샘플 데이터를 불러왔습니다.");
  } catch (error) {
    setStatus(`오류: ${error.message}`);
  }
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

async function handleFile(event) {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }

  try {
    const text = await file.text();
    const data = JSON.parse(text);
    applyQuestions(normalizeQuestions(data));
    setStatus(`${file.name} 파일을 불러왔습니다.`);
  } catch (error) {
    setStatus(`오류: ${error.message}`);
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

fileInput.addEventListener("change", handleFile);
loadSampleBtn.addEventListener("click", loadSample);
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
