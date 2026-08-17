const state = {
  questions: [],
  index: 0,
};

const card = document.getElementById("card");
const statusEl = document.getElementById("status");
const progressEl = document.getElementById("progress");
const qTitleEl = document.getElementById("qTitle");
const clueBoxEl = document.getElementById("clueBox");
const qTextEl = document.getElementById("qText");
const choiceListEl = document.getElementById("choiceList");
const answerEl = document.getElementById("answer");

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const jumpInput = document.getElementById("jumpInput");
const jumpBtn = document.getElementById("jumpBtn");

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
  const uniqueTerms = Array.from(
    new Set((terms ?? []).map((term) => String(term).trim()).filter(Boolean))
  ).sort((a, b) => b.length - a.length);

  if (uniqueTerms.length === 0) {
    return escapeHtml(text);
  }

  const pattern = new RegExp(uniqueTerms.map(escapeRegExp).join("|"), "gi");
  let lastIndex = 0;
  let output = "";

  for (const match of text.matchAll(pattern)) {
    const start = match.index ?? 0;
    output += escapeHtml(text.slice(lastIndex, start));
    output += `<mark class="hl">${escapeHtml(match[0])}</mark>`;
    lastIndex = start + match[0].length;
  }

  output += escapeHtml(text.slice(lastIndex));
  return output;
}

function normalizeQuestions(raw) {
  if (!Array.isArray(raw)) {
    throw new Error("UNIQUE_QUESTIONS는 배열이어야 합니다.");
  }

  return raw.map((item, idx) => {
    if (!item || typeof item !== "object") {
      throw new Error(`${idx + 1}번째 항목이 객체가 아닙니다.`);
    }

    const qNumber = Number(item.qNumber ?? idx + 1);
    const question = String(item.question ?? "").trim();
    const answers = Array.isArray(item.answers)
      ? item.answers.map((value) => String(value).trim().toUpperCase()).filter(Boolean)
      : [];
    const correctChoices = Array.isArray(item.correctChoices)
      ? item.correctChoices.map((choice) => ({
          label: String(choice.label ?? "").trim().toUpperCase(),
          text: String(choice.text ?? "").trim(),
        }))
      : [];
    const uniqueClues = Array.isArray(item.uniqueClues)
      ? item.uniqueClues.map((value) => String(value).trim()).filter(Boolean)
      : [];

    if (!question || correctChoices.length === 0 || uniqueClues.length === 0) {
      throw new Error(`Q${qNumber}: 필수 데이터가 비어 있습니다.`);
    }

    return {
      qNumber,
      question,
      answers,
      answerDisplay: String(item.answer ?? answers.join(", ")).trim(),
      correctChoices,
      uniqueClues,
      primaryClue: String(item.primaryClue ?? uniqueClues[0]).trim(),
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
  qTitleEl.textContent = `Q${current.qNumber}`;
  clueBoxEl.innerHTML = `
    <p class="clue-box__eyebrow">고유 정답 키워드</p>
    <div class="clue-box__badges">
      ${current.uniqueClues.map((clue) => `<span class="clue-badge">${escapeHtml(clue)}</span>`).join("")}
    </div>
  `;
  qTextEl.textContent = current.question;

  choiceListEl.innerHTML = "";
  current.correctChoices.forEach((choice) => {
    const li = document.createElement("li");
    li.classList.add("correct-choice", "correct-choice--v3");
    li.innerHTML = highlightText(`${choice.label}. ${choice.text}`, current.uniqueClues);
    choiceListEl.appendChild(li);
  });

  answerEl.textContent = `Answer: ${current.answerDisplay}`;
  progressEl.textContent = `${state.index + 1} / ${total}`;
  card.classList.remove("hidden");
  setStatus(`고유 정답 키워드 기반 문항 ${total}개 중 ${state.index + 1}번째`);
}

function applyQuestions(questions) {
  state.questions = questions;
  state.index = 0;
  render();
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

  const targetIndex = state.questions.findIndex((question) => question.qNumber === value);
  if (targetIndex < 0) {
    setStatus(`Q${value}는 고유 정답 키워드 대상이 아닙니다.`);
    return;
  }

  state.index = targetIndex;
  render();
}

function autoLoadDefault() {
  try {
    if (!Array.isArray(window.UNIQUE_QUESTIONS) || window.UNIQUE_QUESTIONS.length === 0) {
      throw new Error("고유 정답 키워드 데이터가 없습니다.");
    }

    applyQuestions(normalizeQuestions(window.UNIQUE_QUESTIONS));
  } catch (error) {
    setStatus(`오류: ${error.message}`);
  }
}

prevBtn.addEventListener("click", () => move(-1));
nextBtn.addEventListener("click", () => move(1));
jumpBtn.addEventListener("click", jumpToQuestion);

render();
autoLoadDefault();
