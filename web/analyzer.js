const RULES = [
  {
    id: "urgent",
    pattern: /立即|馬上|今日內|限時|逾期|停用|暫停|locked|suspend|urgent|within 24 hours|final reminder/i,
    indicator: "使用急迫或威脅語氣",
    score: 18,
    method: "製造急迫感",
  },
  {
    id: "login",
    pattern: /登入|驗證|確認身分|帳號|密碼|verification|verify|sign in|login|password|MFA|code/i,
    indicator: "要求登入、驗證或提供帳密相關資訊",
    score: 22,
    method: "誘導交出帳號或驗證資訊",
  },
  {
    id: "payment",
    pattern: /付款|繳費|手續費|信用卡|退款|轉帳|罰鍰|payment|refund|card|billing|invoice|fee|overdue/i,
    indicator: "涉及付款、退款、帳單或信用卡資料",
    score: 20,
    method: "付款或退款誘導",
  },
  {
    id: "attachment",
    pattern: /附件|附檔|下載|開啟檔案|attached|attachment|download|document|invoice/i,
    indicator: "要求開啟附件或文件",
    score: 18,
    method: "附件或文件誘導",
  },
  {
    id: "delivery",
    pattern: /包裹|物流|配送|地址|運費|delivery|package|parcel|shipping|redelivery/i,
    indicator: "假物流或配送通知語境",
    score: 14,
    method: "冒充物流通知",
  },
  {
    id: "prize",
    pattern: /中獎|獎品|抽獎|名額|領取|prize|winner|reward|bonus|claim/i,
    indicator: "中獎、獎勵或領取誘因",
    score: 16,
    method: "利益誘惑",
  },
  {
    id: "qr",
    pattern: /QR|QRCode|QR Code|掃描|scan/i,
    indicator: "要求掃描 QR Code",
    score: 18,
    method: "QR Code 導流",
  },
  {
    id: "link",
    pattern: /https?:\/\/|點擊|連結|網址|button|link|click/i,
    indicator: "包含連結、按鈕或外部頁面導向",
    score: 16,
    method: "連結導流",
  },
  {
    id: "official",
    pattern: /官方 App|官方網站|自行開啟|不要求|no action required|official app|manual/i,
    indicator: "提到自行使用官方管道",
    score: -18,
    method: "正常通知特徵",
  },
  {
    id: "no_sensitive",
    pattern: /不要求.*帳密|不要求.*付款|no password|does not ask|no payment/i,
    indicator: "明確說明不要求敏感資料",
    score: -15,
    method: "低風險通知特徵",
  },
];

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function riskLevel(score) {
  if (score >= 55) return "high";
  if (score >= 25) return "medium";
  return "low";
}

function labelFor(level, score) {
  if (level === "high") return "phishing";
  if (level === "medium") return "suspicious";
  return score > 10 ? "suspicious" : "legitimate";
}

function confidence(score) {
  if (score <= 0) return 0.62;
  return Math.min(0.95, 0.58 + score / 100);
}

function personalDataRisk(matches, label) {
  if (label === "legitimate") {
    return "目前未看到明顯要求帳號、密碼、驗證碼或個人資料的跡象。";
  }
  if (matches.has("login") || matches.has("qr")) {
    return "可能誘導輸入帳號、密碼、MFA 驗證碼或其他登入資訊。";
  }
  if (matches.has("delivery") || matches.has("prize")) {
    return "可能進一步要求姓名、電話、地址或身分資料。";
  }
  return "可能要求個人資料、公司資訊或帳務相關資料。";
}

function paymentRisk(matches, label) {
  if (label === "legitimate") {
    return "目前沒有明顯付款、信用卡、退款或轉帳要求。";
  }
  if (matches.has("payment") || matches.has("delivery") || matches.has("prize")) {
    return "可能要求小額付款、信用卡資料、退款驗證或手續費。";
  }
  return "目前付款風險不是最明顯特徵，但後續頁面仍可能要求金融資料。";
}

function safeActions(matches, label) {
  if (label === "legitimate") {
    return ["可保留通知作參考", "如需操作，請自行開啟官方 App 或網站", "不要回覆任何帳密或驗證碼"];
  }
  const actions = ["不要點擊信件中的連結或按鈕", "不要輸入帳號、密碼、驗證碼或信用卡資料", "改從官方 App、官方網站或既有客服管道查證"];
  if (matches.has("attachment")) {
    actions.splice(1, 0, "不要開啟未預期的附件");
  }
  if (matches.has("qr")) {
    actions.splice(1, 0, "不要掃描信件中的不明 QR Code");
  }
  return actions;
}

export function analyzeEmail(text) {
  const input = text.trim();
  if (!input) {
    return null;
  }

  const indicators = [];
  const methods = [];
  const matches = new Set();
  let score = 0;

  for (const rule of RULES) {
    if (rule.pattern.test(input)) {
      score += rule.score;
      matches.add(rule.id);
      indicators.push(rule.indicator);
      methods.push(rule.method);
    }
  }

  score = Math.max(0, score);
  const level = riskLevel(score);
  const label = labelFor(level, score);
  const isPhishing = label === "phishing" || label === "suspicious";
  const cleanIndicators = unique(indicators.length ? indicators : ["未發現明顯高風險特徵"]);
  const cleanMethods = unique(methods.filter((item) => !item.includes("低風險") && !item.includes("正常")));

  return {
    is_phishing: isPhishing,
    label,
    risk_level: level,
    confidence_score: confidence(score),
    indicators: cleanIndicators,
    manipulation_methods: cleanMethods.length ? cleanMethods : ["無明顯詐騙話術"],
    personal_data_risk: personalDataRisk(matches, label),
    payment_risk: paymentRisk(matches, label),
    safe_actions: safeActions(matches, label),
    explanation_for_general_users:
      label === "legitimate"
        ? "這封信目前比較像一般通知，沒有明顯要求你立刻登入、付款或開啟附件。不過只要需要操作帳號或付款，仍建議從官方管道進入。"
        : "這封信同時出現多個可疑訊號，例如時間壓力、登入或付款要求、附件或外部連結。這些特徵常被用來讓使用者在緊張中忽略查證。",
    model_source: "Rule-based prototype analyzer",
    disclaimer: "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。",
  };
}
