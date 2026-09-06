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

function normalized(value) {
  return String(value).toLowerCase().replace(/[^0-9a-z가-힣]+/g, "");
}

function normalizedPositions(value) {
  const normalizedValue = [];
  const positions = [];
  for (let index = 0; index < value.length; index += 1) {
    const character = value[index].toLowerCase();
    if (/^[0-9a-z가-힣]$/.test(character)) {
      normalizedValue.push(character);
      positions.push(index);
    }
  }
  return { value: normalizedValue.join(""), positions };
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

function validHighlights(question, highlights) {
  const searchableText = normalized([question.question, ...question.choices.map((choice) => choice.text)].join(" "));
  return highlights.filter((highlight) => {
    const text = String(highlight.text ?? "").trim();
    return text && normalized(text) && searchableText.includes(normalized(text));
  });
}

function applyHighlightMap(questions, highlightBatches, excluded) {
  const byQuestion = new Map();
  for (const batch of highlightBatches.flat()) {
    if (!batch || excluded.has(Number(batch.qNumber))) continue;
    const qNumber = Number(batch.qNumber);
    if (Number.isFinite(qNumber)) byQuestion.set(qNumber, batch.highlights ?? []);
  }
  return questions.map((question) => ({
    ...question,
    highlights: validHighlights(question, byQuestion.get(question.qNumber) ?? []),
  }));
}

function highlightedChoices(question) {
  const highlightedLabels = new Set(
    question.highlights.flatMap((highlight) => (highlight.choiceLabels ?? []).map((label) => String(label).toUpperCase()))
  );
  if (highlightedLabels.size) return question.choices.filter((choice) => highlightedLabels.has(choice.label));
  return [];
}

function markedText(text, highlights) {
  const source = normalizedPositions(text);
  const ranges = highlights
    .filter((highlight) => highlight.text && normalized(highlight.text))
    .map((highlight) => {
      const needle = normalized(highlight.text);
      const start = source.value.indexOf(needle);
      if (start < 0) return null;
      const end = start + needle.length - 1;
      return {
        start: source.positions[start],
        end: source.positions[end] + 1,
        color: highlight.color,
        opacity: highlight.opacity,
        length: needle.length,
      };
    })
    .filter(Boolean)
    .sort((left, right) => left.start - right.start || right.length - left.length);

  const selected = [];
  for (const range of ranges) {
    if (!selected.some((item) => range.start < item.end && range.end > item.start)) selected.push(range);
  }
  if (!selected.length) return escapeHtml(text);

  let rendered = "";
  let cursor = 0;
  for (const range of selected) {
    rendered += escapeHtml(text.slice(cursor, range.start));
    rendered += `<mark class="pdf-highlight" style="--highlight-color:${range.color};--highlight-opacity:${range.opacity}">${escapeHtml(text.slice(range.start, range.end))}</mark>`;
    cursor = range.end;
  }
  return rendered + escapeHtml(text.slice(cursor));
}

function render() {
  const current = state.questions[state.index];
  if (!current) return;
  const correctChoices = highlightedChoices(current);
  const highlightedAnswers = correctChoices.map((choice) => choice.label);
  qTitleEl.textContent = `Q${current.qNumber}`;
  qTextEl.innerHTML = markedText(current.question, current.highlights);
  choiceListEl.innerHTML = correctChoices.map((choice) => `<li class="correct-choice correct-choice--v6">${markedText(`${choice.label}. ${choice.text}`, current.highlights)}</li>`).join("");
  answerEl.textContent = highlightedAnswers.length
    ? `Answer: ${highlightedAnswers.join(", ")}`
    : "Answer: 텍스트에 칠해진 정답 형광펜이 없습니다.";
  progressEl.textContent = `${state.index + 1} / ${state.questions.length}`;
  statusEl.textContent = current.highlights.length ? `${current.highlights.length}개 텍스트 형광펜 표시` : "텍스트에 칠해진 형광펜이 없는 문제입니다.";
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
    const excluded = new Set((window.DEFAULT_EXCLUDED_QUESTIONS ?? []).map(Number));
    const embeddedQuestions = Array.isArray(window.DEFAULT_QUESTIONS) ? window.DEFAULT_QUESTIONS : null;
    const embeddedHighlights = Array.isArray(window.DEFAULT_PDF_HIGHLIGHTS_V7) ? [window.DEFAULT_PDF_HIGHLIGHTS_V7] : null;
    if (embeddedQuestions && embeddedHighlights) {
      state.questions = applyHighlightMap(normalizeQuestions(embeddedQuestions, excluded), embeddedHighlights, excluded);
      render();
      return;
    }

    const [questions, manifest] = await Promise.all([
      fetch("../data/questions/questions.json").then((response) => response.json()),
      fetch("../data/reclassified_v7/pdf_highlights_manifest.json").then((response) => response.json()),
    ]);
    const batches = await Promise.all(manifest.map((path) => fetch(`../data/reclassified_v7/${path}`).then((response) => response.json())));
    state.questions = applyHighlightMap(normalizeQuestions(questions, excluded), batches, excluded);
    render();
  } catch (error) {
    statusEl.textContent = `데이터 로드 실패: ${error.message}`;
  }
}

loadData();
