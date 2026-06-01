export const mockSamples = [
  {
    id: "demo-001",
    inputType: "text",
    title: "假物流補繳運費通知",
    text: "您的包裹因地址不完整無法配送，請於今日內至物流通知中心補填資料並繳交手續費。點擊連結完成驗證。",
    result: {
      is_phishing: true,
      label: "scam",
      risk_level: "high",
      confidence_score: 0.92,
      indicators: ["急迫語氣", "要求小額付款", "可疑連結", "冒充物流單位"],
      manipulation_methods: ["製造急迫感", "小額付款誘導", "冒充官方通知"],
      personal_data_risk: "可能要求姓名、電話、地址或驗證碼。",
      payment_risk: "可能導向假付款頁並要求輸入信用卡資料。",
      safe_actions: ["不要點擊訊息中的連結", "改至官方物流網站或 App 查詢", "不要輸入信用卡或驗證碼"],
      explanation_for_general_users: "這類訊息常用包裹無法配送來製造焦慮，並用小額費用降低戒心。",
      model_source: "Mock demo / Experiment B compatible format",
      disclaimer: "此結果僅供輔助判斷，重要操作請透過官方管道查證。"
    }
  },
  {
    id: "demo-002",
    inputType: "text",
    title: "正常校園 IT 維護通知",
    text: "校園 IT 服務將於週五 22:00 至 23:00 進行系統維護，期間登入服務可能短暫中斷。若有問題請洽資訊服務窗口。",
    result: {
      is_phishing: false,
      label: "legitimate",
      risk_level: "low",
      confidence_score: 0.84,
      indicators: ["未要求輸入帳密", "未附可疑連結", "未要求付款"],
      manipulation_methods: ["無明顯詐騙話術"],
      personal_data_risk: "目前看不出明顯個資風險。",
      payment_risk: "沒有付款要求。",
      safe_actions: ["可從學校官方公告系統確認", "若不確定，聯絡資訊服務窗口"],
      explanation_for_general_users: "這則訊息雖然提到系統維護與登入服務，但沒有要求你點擊連結或輸入帳密，風險較低。",
      model_source: "Mock demo / Experiment B compatible format",
      disclaimer: "此結果僅供輔助判斷，重要操作請透過官方管道查證。"
    }
  },
  {
    id: "demo-003",
    inputType: "image",
    title: "圖片上傳 mock 分析",
    text: "圖片第一版僅做預覽與 mock 結果，未進行真實 OCR 或多模態判斷。",
    result: {
      is_phishing: true,
      label: "suspicious",
      risk_level: "medium",
      confidence_score: 0.76,
      indicators: ["畫面包含付款提示", "疑似要求輸入資料", "來源需進一步確認"],
      manipulation_methods: ["製造急迫感", "冒充通知頁面"],
      personal_data_risk: "可能要求輸入聯絡資料或帳戶資訊。",
      payment_risk: "若圖片中含付款按鈕，需特別確認來源。",
      safe_actions: ["不要掃描或點擊不明 QR code", "不要在不明頁面輸入資料", "改由官方 App 或網站查詢"],
      explanation_for_general_users: "圖片功能目前是展示用途，實際判斷仍應以官方來源查證為準。",
      model_source: "Mock image demo",
      disclaimer: "此結果僅供輔助判斷，圖片分析目前尚未串接真實模型。"
    }
  }
];
