import { analyzeEmail } from "./analyzer.js";
import { mockSamples } from "./mockData.js";

const modeTabs = document.querySelectorAll(".tab-button");
const modePanels = document.querySelectorAll(".mode-section");
const sampleSelect = document.querySelector("#sampleSelect");
const messageInput = document.querySelector("#messageInput");
const analyzeButton = document.querySelector("#analyzeButton");
const clearButton = document.querySelector("#clearButton");
const imageInput = document.querySelector("#imageInput");
const imagePreview = document.querySelector("#imagePreview");
const analyzeImageButton = document.querySelector("#analyzeImageButton");
const clearImageButton = document.querySelector("#clearImageButton");
const quickButtons = document.querySelectorAll(".quick-button");

const riskTitle = document.querySelector("#riskTitle");
const riskBadge = document.querySelector("#riskBadge");
const riskLevelText = document.querySelector("#riskLevelText");
const phishingStatus = document.querySelector("#phishingStatus");
const confidenceScore = document.querySelector("#confidenceScore");
const riskProgress = document.querySelector("#riskProgress");
const reasonSummary = document.querySelector("#reasonSummary");
const modelSource = document.querySelector("#modelSource");
const indicatorsList = document.querySelector("#indicatorsList");
const methodsList = document.querySelector("#methodsList");
const personalRisk = document.querySelector("#personalRisk");
const paymentRisk = document.querySelector("#paymentRisk");
const actionsList = document.querySelector("#actionsList");
const explanation = document.querySelector("#explanation");
const disclaimer = document.querySelector("#disclaimer");

const textSamples = mockSamples.filter((sample) => sample.inputType === "text");
const imageSample = mockSamples.find((sample) => sample.inputType === "image");

function riskLabel(level) {
  if (level === "high") return "高風險";
  if (level === "medium") return "中風險";
  if (level === "low") return "低風險";
  return "未分析";
}

function riskTitleText(result) {
  if (result.risk_level === "high") return "高度疑似釣魚信件";
  if (result.risk_level === "medium") return "需要進一步查證";
  return "目前風險較低";
}

function reasonText(level) {
  if (level === "high") return "此信件出現多個高風險訊號，建議不要直接操作。";
  if (level === "medium") return "此信件有可疑訊號，建議先查證。";
  return "目前未看到明顯高風險訊號，但仍建議透過官方管道確認。";
}

function renderTags(element, items, className) {
  element.innerHTML = "";
  items.forEach((item) => {
    const span = document.createElement("span");
    span.className = `tag ${className}`;
    span.textContent = item;
    element.appendChild(span);
  });
}

function renderChecklist(element, items) {
  element.innerHTML = "";
  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "check-item";
    row.innerHTML = `<span aria-hidden="true"></span><p></p>`;
    row.querySelector("p").textContent = item;
    element.appendChild(row);
  });
}

function renderResult(result) {
  const percent = Math.round(result.confidence_score * 100);
  riskTitle.textContent = riskTitleText(result);
  riskBadge.textContent = riskLabel(result.risk_level);
  riskBadge.className = `badge ${result.risk_level}`;
  riskLevelText.textContent = riskLabel(result.risk_level);
  phishingStatus.textContent = result.is_phishing ? "疑似釣魚：是" : "疑似釣魚：目前不像";
  confidenceScore.textContent = `${percent}%`;
  riskProgress.style.width = `${percent}%`;
  riskProgress.className = `progress-fill ${result.risk_level}`;
  reasonSummary.textContent = reasonText(result.risk_level);
  modelSource.textContent = result.model_source || "Rule-based prototype";
  renderTags(indicatorsList, result.indicators, "indicator");
  renderTags(methodsList, result.manipulation_methods, "method");
  renderChecklist(actionsList, result.safe_actions);
  personalRisk.textContent = result.personal_data_risk;
  paymentRisk.textContent = result.payment_risk;
  explanation.textContent = result.explanation_for_general_users;
  disclaimer.textContent = result.disclaimer;
}

function switchMode(mode) {
  modeTabs.forEach((tab) => {
    const active = tab.dataset.mode === mode;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", String(active));
  });
  modePanels.forEach((panel) => {
    const active = panel.dataset.panel === mode;
    panel.classList.toggle("active", active);
    panel.hidden = !active;
  });
}

function populateSamples() {
  sampleSelect.innerHTML = "";
  textSamples.forEach((sample, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = `${sample.title}（${sample.phishingType}）`;
    sampleSelect.appendChild(option);
  });
}

function loadSample(index) {
  const sample = textSamples[index];
  if (!sample) return;
  switchMode("text");
  messageInput.value = sample.text;
  sampleSelect.value = String(index);
  renderResult(sample.result);
}

function loadByType(type) {
  const index = textSamples.findIndex((sample) => sample.phishingType === type);
  if (index >= 0) {
    loadSample(index);
  }
}

function clearImage() {
  imageInput.value = "";
  imagePreview.textContent = "尚未選擇圖片";
}

modeTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    switchMode(tab.dataset.mode);
  });
});

sampleSelect.addEventListener("change", () => {
  loadSample(Number(sampleSelect.value));
});

quickButtons.forEach((button) => {
  button.addEventListener("click", () => {
    loadByType(button.dataset.type);
  });
});

analyzeButton.addEventListener("click", () => {
  const result = analyzeEmail(messageInput.value);
  if (!result) {
    messageInput.focus();
    return;
  }
  renderResult(result);
});

clearButton.addEventListener("click", () => {
  messageInput.value = "";
  messageInput.focus();
});

imageInput.addEventListener("change", () => {
  const file = imageInput.files?.[0];
  if (!file) {
    clearImage();
    return;
  }

  const url = URL.createObjectURL(file);
  imagePreview.innerHTML = "";
  const img = document.createElement("img");
  img.src = url;
  img.alt = "上傳圖片預覽";
  imagePreview.appendChild(img);
});

analyzeImageButton.addEventListener("click", () => {
  if (!imageInput.files?.[0]) {
    imageInput.focus();
    return;
  }
  if (imageSample) {
    renderResult(imageSample.result);
  }
});

clearImageButton.addEventListener("click", () => {
  clearImage();
});

populateSamples();
switchMode("text");
loadSample(0);
