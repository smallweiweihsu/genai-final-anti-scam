import { analyzeEmail } from "./analyzer.js";
import { mockSamples } from "./mockData.js";

const sampleSelect = document.querySelector("#sampleSelect");
const messageInput = document.querySelector("#messageInput");
const analyzeButton = document.querySelector("#analyzeButton");
const clearButton = document.querySelector("#clearButton");
const imageInput = document.querySelector("#imageInput");
const imagePreview = document.querySelector("#imagePreview");

const riskTitle = document.querySelector("#riskTitle");
const riskBadge = document.querySelector("#riskBadge");
const phishingStatus = document.querySelector("#phishingStatus");
const confidenceScore = document.querySelector("#confidenceScore");
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

function renderList(element, items) {
  element.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

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

function renderResult(result) {
  riskTitle.textContent = riskTitleText(result);
  riskBadge.textContent = riskLabel(result.risk_level);
  riskBadge.className = `badge ${result.risk_level}`;
  phishingStatus.textContent = result.is_phishing ? "是，建議不要直接操作" : "目前不像";
  confidenceScore.textContent = `${Math.round(result.confidence_score * 100)}%`;
  modelSource.textContent = result.model_source || "Rule-based prototype";
  renderList(indicatorsList, result.indicators);
  renderList(methodsList, result.manipulation_methods);
  renderList(actionsList, result.safe_actions);
  personalRisk.textContent = result.personal_data_risk;
  paymentRisk.textContent = result.payment_risk;
  explanation.textContent = result.explanation_for_general_users;
  disclaimer.textContent = result.disclaimer;
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
  messageInput.value = sample.text;
  renderResult(sample.result);
}

sampleSelect.addEventListener("change", () => {
  loadSample(Number(sampleSelect.value));
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
  sampleSelect.selectedIndex = 0;
  messageInput.focus();
});

imageInput.addEventListener("change", () => {
  const file = imageInput.files?.[0];
  if (!file || !imageSample) return;

  const url = URL.createObjectURL(file);
  imagePreview.innerHTML = "";
  const img = document.createElement("img");
  img.src = url;
  img.alt = "上傳圖片預覽";
  imagePreview.appendChild(img);
  renderResult(imageSample.result);
});

populateSamples();
loadSample(0);
