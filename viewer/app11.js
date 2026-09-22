const state = {
  questions: [],
  index: 0,
  selections: new Map(),
  highlightMode: "none",
};

const card = document.getElementById("card");
const statusEl = document.getElementById("status");
const progressEl = document.getElementById("progress");
const qTitleEl = document.getElementById("qTitle");
const qTextEl = document.getElementById("qText");
const choiceListEl = document.getElementById("choiceList");
const answerEl = document.getElementById("answer");
const jumpInput = document.getElementById("jumpInput");

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

function normalized(value) {
  return String(value).toLowerCase().replace(/[^0-9a-z가-힣]+/g, "");
}

function parseAnswers(value) {
  if (Array.isArray(value)) return value.map((item) => String(item).trim().toUpperCase()).filter(Boolean);
  return String(value ?? "").toUpperCase().match(/\b[A-F]\b/g) ?? [];
}

function normalizeQuestions(raw, excluded) {
  if (!Array.isArray(raw)) throw new Error("문제 데이터가 배열이 아닙니다.");
  return raw
    .map((item, index) => ({
      qNumber: Number(item.qNumber ?? index + 1),
      question: String(item.question ?? "").trim(),
      choices: (item.choices ?? []).map((choice, choiceIndex) => ({
        label: String(choice.label ?? String.fromCharCode(65 + choiceIndex)).trim().toUpperCase(),
        text: String(choice.text ?? "").trim(),
      })),
      answers: parseAnswers(item.answers ?? item.answer),
      highlights: [],
    }))
    .filter((question) => !excluded.has(question.qNumber));
}

function applyHighlights(questions, rawHighlights) {
  const highlightsByQuestion = new Map(
    (rawHighlights ?? []).map((entry) => [Number(entry.qNumber), entry.highlights ?? []])
  );
  return questions.map((question) => ({
    ...question,
    highlights: highlightsByQuestion.get(question.qNumber) ?? [],
  }));
}

function markedText(text, highlights) {
  let rendered = escapeHtml(text);
  for (const highlight of [...highlights].filter((item) => item.text).sort((left, right) => right.text.length - left.text.length)) {
    const pattern = new RegExp(escapeRegExp(escapeHtml(highlight.text)), "g");
    rendered = rendered.replace(
      pattern,
      `<mark class="pdf-highlight" style="--highlight-color:${highlight.color};--highlight-opacity:${highlight.opacity}">$&</mark>`
    );
  }
  return rendered;
}

function currentQuestion() {
  return state.questions[state.index];
}

function selectedLabels() {
  const selected = state.selections.get(state.index);
  return Array.isArray(selected) ? selected : selected ? [selected] : [];
}

function render() {
  const current = currentQuestion();
  if (!current) return;
  const selectedLabelsForQuestion = selectedLabels();
  const isAnswered = selectedLabelsForQuestion.length > 0;
  const hasWrongChoice = selectedLabelsForQuestion.some((label) => !current.answers.includes(label));
  const isComplete = selectedLabelsForQuestion.length === current.answers.length;
  const isCorrect = isComplete && !hasWrongChoice;
  const isMultiAnswer = current.answers.length > 1;

  qTitleEl.textContent = `Q${current.qNumber}`;
  const showQuestionHints = state.highlightMode !== "none";
  const showAnswerHints = state.highlightMode === "question-answer";
  qTextEl.innerHTML = showQuestionHints
    ? markedText(current.question, current.highlights)
    : escapeHtml(current.question);
  choiceListEl.innerHTML = current.choices.map((choice) => {
    const selected = selectedLabelsForQuestion.includes(choice.label);
    const correct = selected && current.answers.includes(choice.label);
    const classNames = ["quiz-choice"];
    if (selected) classNames.push("quiz-choice--selected");
    if (correct) classNames.push("quiz-choice--correct");
    if (selected && !current.answers.includes(choice.label)) classNames.push("quiz-choice--wrong");
    const inputType = isMultiAnswer ? "checkbox" : "radio";
    const choiceText = showAnswerHints && current.answers.includes(choice.label)
      ? markedText(choice.text, current.highlights)
      : escapeHtml(choice.text);
    return `<label class="${classNames.join(" ")}">
      <input type="${inputType}" name="question-${state.index}" value="${escapeHtml(choice.label)}"${selected ? " checked" : ""}>
      <span class="quiz-choice__label">${escapeHtml(choice.label)}.</span>
      <span class="quiz-choice__text">${choiceText}</span>
    </label>`;
  }).join("");

  answerEl.textContent = !isAnswered
    ? "보기를 선택하면 정답 여부를 확인할 수 있습니다."
    : isCorrect
      ? `정답입니다. Answer: ${current.answers.join(", ")}`
      : hasWrongChoice
        ? "선택한 보기 중 오답이 있습니다."
        : isMultiAnswer && !isComplete
          ? "정답을 더 선택하세요."
          : "다시 확인해 보세요.";
  answerEl.className = `answer ${isAnswered ? (isCorrect ? "answer--correct" : "answer--wrong") : ""}`;
  progressEl.textContent = `${state.index + 1} / ${state.questions.length}`;
  statusEl.textContent = isAnswered ? "선택한 보기를 채점했습니다." : "정답을 알고 싶을 때 보기를 선택하세요.";
  card.classList.remove("hidden");
}

function selectAnswer(label, checked) {
  const current = currentQuestion();
  if (current.answers.length > 1) {
    const nextSelection = new Set(selectedLabels());
    if (checked) nextSelection.add(label);
    else nextSelection.delete(label);
    state.selections.set(state.index, [...nextSelection]);
  } else {
    state.selections.set(state.index, label);
  }
  render();
}

function move(delta) {
  state.index = Math.min(state.questions.length - 1, Math.max(0, state.index + delta));
  render();
}

document.getElementById("prevBtn").addEventListener("click", () => move(-1));
document.getElementById("nextBtn").addEventListener("click", () => move(1));
choiceListEl.addEventListener("change", (event) => selectAnswer(event.target.value, event.target.checked));

document.getElementById("jumpBtn").addEventListener("click", () => {
  const target = state.questions.findIndex((question) => question.qNumber === Number(jumpInput.value));
  if (target < 0) {
    statusEl.textContent = `Q${jumpInput.value}를 찾을 수 없습니다.`;
    return;
  }
  state.index = target;
  render();
});

const darkModeBtn = document.getElementById("darkModeBtn");
const blueLightBtn = document.getElementById("blueLightBtn");
const blueDeepBtn = document.getElementById("blueDeepBtn");
const skyBtn = document.getElementById("skyBtn");
const questionHintBtn = document.getElementById("questionHintBtn");
const questionAnswerHintBtn = document.getElementById("questionAnswerHintBtn");

function setHighlightMode(mode) {
  state.highlightMode = state.highlightMode === mode ? "none" : mode;
  questionHintBtn.classList.toggle("hint-btn--active", state.highlightMode === "question");
  questionAnswerHintBtn.classList.toggle("hint-btn--active", state.highlightMode === "question-answer");
  render();
}

function setTheme(theme) {
  document.body.classList.remove("dark", "theme-blue-light", "theme-blue-deep", "theme-sky");

  if (theme === "dark") {
    document.body.classList.add("dark");
  } else if (theme === "blue-light") {
    document.body.classList.add("theme-blue-light");
  } else if (theme === "blue-deep") {
    document.body.classList.add("theme-blue-deep");
  } else if (theme === "sky") {
    document.body.classList.add("theme-sky");
  }

  const isDark = document.body.classList.contains("dark");
  darkModeBtn.textContent = isDark ? "라이트모드" : "다크모드";

  [blueLightBtn, blueDeepBtn, skyBtn].forEach((button) => {
    const isActive = button.id === (
      theme === "blue-light" ? "blueLightBtn" :
      theme === "blue-deep" ? "blueDeepBtn" :
      theme === "sky" ? "skyBtn" : ""
    );
    button.classList.toggle("theme-btn--active", isActive);
  });

  localStorage.setItem("theme", theme);
}

function applyDarkMode(enabled) {
  const currentTheme = enabled
    ? "dark"
    : document.body.classList.contains("theme-blue-deep")
      ? "blue-deep"
      : document.body.classList.contains("theme-blue-light")
        ? "blue-light"
        : document.body.classList.contains("theme-sky")
          ? "sky"
          : "blue-light";
  setTheme(enabled ? "dark" : currentTheme);
}

const savedTheme = localStorage.getItem("theme") || "blue-light";
setTheme(savedTheme);

darkModeBtn.addEventListener("click", () => {
  const enabled = !document.body.classList.contains("dark");
  applyDarkMode(enabled);
  localStorage.setItem("darkMode", enabled ? "1" : "0");
});

blueLightBtn.addEventListener("click", () => setTheme("blue-light"));
blueDeepBtn.addEventListener("click", () => setTheme("blue-deep"));
skyBtn.addEventListener("click", () => setTheme("sky"));
questionHintBtn.addEventListener("click", () => setHighlightMode("question"));
questionAnswerHintBtn.addEventListener("click", () => setHighlightMode("question-answer"));

async function loadData() {
  try {
    const embeddedQuestions = Array.isArray(window.DEFAULT_QUESTIONS_V11) ? window.DEFAULT_QUESTIONS_V11 : null;
    const embeddedHighlights = Array.isArray(window.DEFAULT_PDF_HIGHLIGHTS) ? window.DEFAULT_PDF_HIGHLIGHTS : null;
    if (embeddedQuestions && embeddedHighlights) {
      state.questions = applyHighlights(normalizeQuestions(embeddedQuestions, new Set()), embeddedHighlights);
      render();
      return;
    }

    const [questions, highlights] = await Promise.all([
      fetch("../data/questions/questions_v11.json").then((response) => response.json()),
      fetch("../data/reclassified/pdf_highlights_manifest.json")
        .then((response) => response.json())
        .then((manifest) => Promise.all(manifest.map((path) => fetch(`../data/reclassified/${path}`).then((response) => response.json()))))
        .then((batches) => batches.flat()),
    ]);
    state.questions = applyHighlights(normalizeQuestions(questions, new Set()), highlights);
    render();
  } catch (error) {
    statusEl.textContent = `데이터 로드 실패: ${error.message}`;
  }
}

loadData();
