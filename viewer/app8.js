const state = {
  services: [],
  selected: "",
  query: "",
  sortBy: "answer", // 'answer' | 'total' | 'name'
};

const serviceList = document.getElementById("serviceList");
const serviceTitle = document.getElementById("serviceTitle");
const serviceCount = document.getElementById("serviceCount");
const serviceContent = document.getElementById("serviceContent");
const conceptSearch = document.getElementById("conceptSearch");
const sortSelect = document.getElementById("sortSelect");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function visibleServices() {
  const query = state.query.trim().toLowerCase();
  let filtered = state.services;

  if (query) {
    filtered = filtered.filter((service) => service.service.toLowerCase().includes(query));
  }

  return filtered.slice().sort((left, right) => {
    if (state.sortBy === "answer") {
      return (
        right.answerHighlightCount - left.answerHighlightCount ||
        right.totalHighlightCount - left.totalHighlightCount ||
        left.service.localeCompare(right.service)
      );
    }
    if (state.sortBy === "total") {
      return (
        right.totalHighlightCount - left.totalHighlightCount ||
        right.answerHighlightCount - left.answerHighlightCount ||
        left.service.localeCompare(right.service)
      );
    }
    return left.service.localeCompare(right.service);
  });
}

function renderServiceList() {
  const services = visibleServices();
  serviceList.innerHTML = services
    .map((service) => {
      const active = service.service === state.selected ? " service-item--active" : "";
      return `<button class="service-item${active}" type="button" data-service="${escapeHtml(service.service)}">
        <span class="service-item-name">${escapeHtml(service.service)}</span>
        <div class="service-item-badges">
          <span class="badge-ans-hl" title="정답 형광펜 등장 문항수">정답 ${service.answerHighlightCount}</span>
          <span class="badge-tot-hl" title="전체 형광펜 등장 문항수">총 ${service.totalHighlightCount}</span>
        </div>
      </button>`;
    })
    .join("");

  serviceList.querySelectorAll("[data-service]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selected = button.dataset.service;
      renderServiceList();
      renderService();
    });
  });
}

function renderService() {
  const service = state.services.find((item) => item.service === state.selected);
  if (!service) {
    serviceTitle.textContent = "서비스를 선택하세요";
    serviceCount.textContent = "";
    serviceContent.innerHTML = `<div class="concept-empty">왼쪽에서 서비스를 선택하면 v7 형광펜 기반 핵심 개념과 문제 연결이 표시됩니다.</div>`;
    return;
  }

  serviceTitle.textContent = service.service;
  serviceCount.textContent = `정답 형광펜 ${service.answerHighlightCount}문항 (총 ${service.totalHighlightCount}문항 관찰)`;

  const phrases = service.observedPhrases ?? [];
  const qNums = service.answerHighlightQNums ?? [];
  const conditionExamples = service.conditionExamples ?? [];
  const answerExamples = service.answerExamples ?? [];

  const phraseHtml = phrases.length
    ? phrases
        .map(
          (p) =>
            `<mark class="phrase-tag" style="--highlight-color:#f4d477;--highlight-opacity:0.6">${escapeHtml(
              p.phrase
            )} <small>(${p.count}회)</small></mark>`
        )
        .join(" ")
    : `<p class="concept-muted">v7 하이라이트 문구가 감지되지 않았거나 전체 텍스트 매칭만 존재합니다.</p>`;

  const qNumBadgesHtml = qNums.length
    ? `<div class="qnum-badge-list">${qNums
        .map((q) => `<span class="qnum-badge">Q${q}</span>`)
        .join("")}</div>`
    : `<p class="concept-muted">정답 선택지 하이라이트 문항이 없습니다.</p>`;

  const renderExamples = (examples, label) => {
    if (!examples || examples.length === 0) {
      return `<p class="concept-muted">${label} 관찰 예시가 없습니다.</p>`;
    }
    return `<div class="example-card-list">
      ${examples
        .map(
          (ex) => `
        <div class="example-card">
          <span class="example-qnum">Q${ex.qNumber}</span>
          <p class="example-text">${escapeHtml(ex.text)}</p>
        </div>
      `
        )
        .join("")}
    </div>`;
  };

  serviceContent.innerHTML = `
    <section class="concept-hero">
      <div>
        <span class="concept-kicker">AWS OFFICIAL DOCUMENTATION</span>
        <a href="${escapeHtml(service.officialDocs)}" target="_blank" rel="noreferrer" class="docs-btn">AWS 공식 문서 바로가기 ↗</a>
      </div>
      <div class="concept-stats">
        <span title="정답 선택지에 형광펜 칠해진 문항 수">정답 HL ${service.answerHighlightCount}</span>
        <span title="문제 본문에 형광펜 칠해진 문항 수">문제 HL ${service.questionHighlightCount}</span>
        <span title="형광펜 칠해진 전체 문항 수">총 HL ${service.totalHighlightCount}</span>
      </div>
    </section>

    <section class="concept-grid v8-grid">
      <article class="concept-panel concept-panel--wide">
        <span class="panel-label">v7 PDF 형광펜 추출 표현</span>
        <h3>시험지에서 실제 칠해진 핵심 키워드/문구 (Highlight Phrase Bank)</h3>
        <div class="phrase-bank-container">
          ${phraseHtml}
        </div>
      </article>

      <article class="concept-panel">
        <span class="panel-label">출제 패턴 & 정답 힌트</span>
        <h3>이럴 때 정답으로 검토하세요</h3>
        <div class="trigger-box">
          <p>${escapeHtml(service.answerTrigger)}</p>
        </div>
      </article>
    </section>

    <section class="concept-panel concept-panel--full margin-top-14">
      <span class="panel-label">정답 출현 문항 리스트</span>
      <h3>정답 선택지에 형광펜이 관찰된 문항 (${qNums.length}개)</h3>
      ${qNumBadgesHtml}
    </section>

    <section class="concept-grid v8-grid margin-top-14">
      <article class="concept-panel">
        <span class="panel-label">실제 출제 조건 예시</span>
        <h3>문제(Question) 조건 문장</h3>
        ${renderExamples(conditionExamples, "문제 조건")}
      </article>

      <article class="concept-panel concept-panel--wide">
        <span class="panel-label">실제 정답 구성 예시</span>
        <h3>정답(Answer) 선택지 문장</h3>
        ${renderExamples(answerExamples, "정답 구성")}
      </article>
    </section>

    <p class="verification-note">v7 PDF 형광펜 추출 결과입니다. 공식 문서에서 서비스의 실제 동작과 제한사항을 최종 확인하세요.</p>
  `;
}

function init() {
  const data = window.CONCEPT_BOOK_V8;
  if (!data || !Array.isArray(data.services)) {
    serviceContent.innerHTML = `<div class="concept-empty">개념 v8 데이터를 찾지 못했습니다. src/build_concept_book_v8.py를 먼저 실행하세요.</div>`;
    return;
  }

  state.services = data.services;
  state.selected = state.services[0]?.service ?? "";
  serviceCount.textContent = `${state.services.length}개 서비스`;
  renderServiceList();
  renderService();
}

conceptSearch.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderServiceList();
});

sortSelect.addEventListener("change", (event) => {
  state.sortBy = event.target.value;
  renderServiceList();
});

init();
