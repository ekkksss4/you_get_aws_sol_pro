const state = { questions: [], index: 0 };

const card = document.getElementById("card");
const statusEl = document.getElementById("status");
const progressEl = document.getElementById("progress");
const qTitleEl = document.getElementById("qTitle");
const qTextEl = document.getElementById("qText");
const choiceListEl = document.getElementById("choiceList");
const answerEl = document.getElementById("answer");
const jumpInput = document.getElementById("jumpInput");

function escapeHtml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function parseAnswers(value) {
  if (Array.isArray(value)) return value.map((item) => String(item).trim().toUpperCase()).filter(Boolean);
  return String(value ?? "").toUpperCase().match(/\b[A-F]\b/g) ?? [];
}

function normalizeQuestions(raw) {
  if (!Array.isArray(raw)) throw new Error("문제 데이터가 배열이 아닙니다.");
  return raw.map((item, index) => ({
    qNumber: Number(item.qNumber ?? index + 1),
    question: String(item.question ?? "").trim(),
    choices: (item.choices ?? []).map((choice, choiceIndex) => ({
      label: String(choice.label ?? String.fromCharCode(65 + choiceIndex)).trim().toUpperCase(),
      text: String(choice.text ?? "").trim(),
    })),
    answers: parseAnswers(item.answers ?? item.answer),
    highlights: [],
  }));
}

function applyHighlightMap(questions, highlightBatches) {
  const byQuestion = new Map();
  for (const batch of highlightBatches.flat()) {
    if (batch && Number.isFinite(Number(batch.qNumber))) byQuestion.set(Number(batch.qNumber), batch.highlights ?? []);
  }
  return questions.map((question) => ({ ...question, highlights: byQuestion.get(question.qNumber) ?? [] }));
}

function markedText(text, highlights) {
  const matches = highlights
    .filter((highlight) => highlight.text)
    .sort((left, right) => right.text.length - left.text.length);
  if (!matches.length) return escapeHtml(text);

  let rendered = escapeHtml(text);
  for (const highlight of matches) {
    const pattern = new RegExp(escapeRegExp(escapeHtml(highlight.text)));
    rendered = rendered.replace(
      pattern,
      `<mark class="pdf-highlight" style="--highlight-color:${highlight.color};--highlight-opacity:${highlight.opacity}">$&</mark>`
    );
  }
  return rendered;
}

function render() {
  const current = state.questions[state.index];
  if (!current) return;
  const correctChoices = current.choices.filter((choice) => current.answers.includes(choice.label));
  qTitleEl.textContent = `Q${current.qNumber}`;
  qTextEl.innerHTML = markedText(current.question, current.highlights);
  choiceListEl.innerHTML = correctChoices.map((choice) => `<li class="correct-choice correct-choice--v6">${markedText(`${choice.label}. ${choice.text}`, current.highlights)}</li>`).join("");
  answerEl.textContent = `Answer: ${current.answers.join(", ")}`;
  progressEl.textContent = `${state.index + 1} / ${state.questions.length}`;
  statusEl.textContent = current.highlights.length ? `${current.highlights.length}개 PDF 형광펜 표시` : "PDF 형광펜이 없는 문제입니다.";
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

async function loadData() {
  try {
    const embeddedQuestions = Array.isArray(window.DEFAULT_QUESTIONS) ? window.DEFAULT_QUESTIONS : null;
    const embeddedHighlights = Array.isArray(window.DEFAULT_PDF_HIGHLIGHTS) ? [window.DEFAULT_PDF_HIGHLIGHTS] : null;
    if (embeddedQuestions && embeddedHighlights) {
      state.questions = applyHighlightMap(normalizeQuestions(embeddedQuestions), embeddedHighlights);
      render();
      return;
    }

    const [questions, manifest] = await Promise.all([
      fetch("../data/questions/questions.json").then((response) => response.json()),
      fetch("../data/reclassified/pdf_highlights_manifest.json").then((response) => response.json()),
    ]);
    const batches = await Promise.all(manifest.map((path) => fetch(`../data/reclassified/${path}`).then((response) => response.json())));
    state.questions = applyHighlightMap(normalizeQuestions(questions), batches);
    render();
  } catch (error) {
    statusEl.textContent = `데이터 로드 실패: ${error.message}`;
  }
}

loadData();