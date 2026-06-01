import { mockSamples } from "./mockData.js";

const messageInput = document.querySelector("#messageInput");
const analyzeButton = document.querySelector("#analyzeButton");
const loadScamButton = document.querySelector("#loadScamButton");
const loadNormalButton = document.querySelector("#loadNormalButton");
const imageInput = document.querySelector("#imageInput");
const imagePreview = document.querySelector("#imagePreview");

const riskTitle = document.querySelector("#riskTitle");
const riskBadge = document.querySelector("#riskBadge");
const confidenceScore = document.querySelector("#confidenceScore");
const indicatorsList = document.querySelector("#indicatorsList");
const methodsList = document.querySelector("#methodsList");
const personalRisk = document.querySelector("#personalRisk");
const paymentRisk = document.querySelector("#paymentRisk");
const actionsList = document.querySelector("#actionsList");
const explanation = document.querySelector("#explanation");
const disclaimer = document.querySelector("#disclaimer");

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

function renderResult(result) {
  riskTitle.textContent = result.is_phishing ? "可能有詐騙風險" : "目前風險較低";
  riskBadge.textContent = riskLabel(result.risk_level);
  riskBadge.className = `badge ${result.risk_level}`;
  confidenceScore.textContent = `${Math.round(result.confidence_score * 100)}%`;
  renderList(indicatorsList, result.indicators);
  renderList(methodsList, result.manipulation_methods);
  renderList(actionsList, result.safe_actions);
  personalRisk.textContent = result.personal_data_risk;
  paymentRisk.textContent = result.payment_risk;
  explanation.textContent = result.explanation_for_general_users;
  disclaimer.textContent = result.disclaimer;
}

function chooseTextResult(text) {
  const normalized = text.trim();
  if (!normalized) return null;

  const normalKeywords = ["維護", "官方 App", "公告系統", "無法登入服務"];
  const looksNormal = normalKeywords.some((keyword) => normalized.includes(keyword));

  return looksNormal ? mockSamples[1].result : mockSamples[0].result;
}

analyzeButton.addEventListener("click", () => {
  const result = chooseTextResult(messageInput.value);
  if (!result) {
    messageInput.focus();
    return;
  }
  renderResult(result);
});

loadScamButton.addEventListener("click", () => {
  messageInput.value = mockSamples[0].text;
  renderResult(mockSamples[0].result);
});

loadNormalButton.addEventListener("click", () => {
  messageInput.value = mockSamples[1].text;
  renderResult(mockSamples[1].result);
});

imageInput.addEventListener("change", () => {
  const file = imageInput.files?.[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  imagePreview.innerHTML = "";
  const img = document.createElement("img");
  img.src = url;
  img.alt = "上傳圖片預覽";
  imagePreview.appendChild(img);
  renderResult(mockSamples[2].result);
});

renderResult(mockSamples[0].result);
