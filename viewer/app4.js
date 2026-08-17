const state = {
  services: [],
  selected: "",
  query: "",
};

const serviceList = document.getElementById("serviceList");
const serviceTitle = document.getElementById("serviceTitle");
const serviceCount = document.getElementById("serviceCount");
const serviceContent = document.getElementById("serviceContent");
const conceptSearch = document.getElementById("conceptSearch");

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
  if (!query) {
    return state.services;
  }
  return state.services.filter((service) => service.service.toLowerCase().includes(query));
}

function renderServiceList() {
  const services = visibleServices();
  serviceList.innerHTML = services
    .map((service) => {
      const active = service.service === state.selected ? " service-item--active" : "";
      return `<button class="service-item${active}" type="button" data-service="${escapeHtml(service.service)}">
        <span>${escapeHtml(service.service)}</span><small>${service.answerCount}</small>
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

function renderList(items, className = "concept-list") {
  if (!items || items.length === 0) {
    return `<p class="concept-muted">관찰된 항목이 아직 없습니다.</p>`;
  }
  return `<ul class="${className}">${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function renderService() {
  const service = state.services.find((item) => item.service === state.selected);
  if (!service) {
    serviceTitle.textContent = "서비스를 선택하세요";
    serviceCount.textContent = "";
    serviceContent.innerHTML = `<div class="concept-empty">왼쪽에서 서비스를 선택하면 개념과 문제 연결이 표시됩니다.</div>`;
    return;
  }

  serviceTitle.textContent = service.service;
  serviceCount.textContent = `정답 등장 ${service.answerCount}문항`;

  const features = service.observedFeatures ?? [];
  const conditions = service.conditionExamples ?? [];
  const answers = service.answerExamples ?? [];

  serviceContent.innerHTML = `
    <section class="concept-hero">
      <div>
        <span class="concept-kicker">OFFICIAL REFERENCE</span>
        <a href="${escapeHtml(service.officialDocs)}" target="_blank" rel="noreferrer">AWS 공식 문서 열기</a>
      </div>
      <div class="concept-stats">
        <span>문제 ${service.questionCount}</span>
        <span>정답 ${service.answerCount}</span>
      </div>
    </section>

    <section class="concept-grid">
      <article class="concept-panel concept-panel--wide">
        <span class="panel-label">정답지에 이런 표현이 나오면</span>
        <h3>이 서비스/기능을 우선 떠올리세요</h3>
        ${renderList(features.map((feature) => `${escapeHtml(feature.name)} <small>(${feature.evidenceCount}개 관찰)</small>`))}
      </article>
      <article class="concept-panel">
        <span class="panel-label">출제 패턴 힌트</span>
        <h3>보통 이런 경우 정답으로 검토</h3>
        ${renderList((service.answerTriggers ?? []).map((item) => `<strong>${escapeHtml(item.feature)}</strong><br>${escapeHtml(item.condition)}`))}
      </article>
    </section>

    <p class="verification-note">자동 추출 후보입니다. 공식 문서에서 서비스의 실제 동작과 제한사항을 최종 확인하세요.</p>
  `;
}

function init() {
  const data = window.CONCEPT_BOOK;
  if (!data || !Array.isArray(data.services)) {
    serviceContent.innerHTML = `<div class="concept-empty">개념 데이터를 찾지 못했습니다. build_concept_book.py를 먼저 실행하세요.</div>`;
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

init();
