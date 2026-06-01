export const mockSamples = [
  {
    "id": "sample-001",
    "dataset_id": "T0017",
    "inputType": "text",
    "phishingType": "fake_delivery",
    "title": "Missed delivery: update shipping details - Case review needed 01",
    "text": "寄件者：Delivery Notification Center <delivery-update.example.invalid>\n主旨：Missed delivery: update shipping details - Case review needed 01\n\nA delivery attempt could not be completed because the shipping address requires confirmation. Please update the delivery preference before the package is returned. Safe sample: link removed. Scenario variation 1: this case is framed for email and mentions action within 2 hours. The lure mentions redelivery, address correction, a customs-like handling fee, or a package being returned.",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "medium",
      "confidence_score": 0.81,
      "indicators": [
        "包含連結或導向外部頁面",
        "帶有時間壓力",
        "missed delivery",
        "redelivery",
        "small fee"
      ],
      "manipulation_methods": [
        "冒充物流通知",
        "小額付款誘導",
        "製造包裹退回壓力"
      ],
      "personal_data_risk": "可能要求姓名、電話、地址、身分資料或其他領取 / 配送資訊。",
      "payment_risk": "可能要求小額手續費、信用卡資料、退款驗證或其他付款資訊。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "假冒物流或配送通知，要求更新地址、重新配送或支付小額費用。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-002",
    "dataset_id": "T0003",
    "inputType": "text",
    "phishingType": "account_lock",
    "title": "最後通知：信箱容量與登入權限即將受限 - Verification window open 10",
    "text": "寄件者：Mail Administrator <mail-quota.example.invalid>\n主旨：最後通知：信箱容量與登入權限即將受限 - Verification window open 10\n\nWe detected a sign-in attempt from a new device. To prevent account suspension, review the activity within 24 hours using the secure verification page. This is a sanitized training sample; the original link has been removed. Scenario variation 10: this case is framed for business mailbox and mentions action this week. The message claims access will be limited unless the recipient confirms identity through a removed verification button.",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "medium",
      "confidence_score": 0.81,
      "indicators": [
        "包含連結或導向外部頁面",
        "帶有時間壓力",
        "account locked",
        "verify",
        "unusual sign-in"
      ],
      "manipulation_methods": [
        "製造帳號停用壓力",
        "冒充安全通知",
        "誘導登入驗證"
      ],
      "personal_data_risk": "可能誘導使用者輸入帳號、密碼、MFA 驗證碼或信箱登入資訊。",
      "payment_risk": "目前付款風險不是主軸，但可能在後續假頁面中要求付款或金融資料。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "利用帳號停用、異常登入或安全驗證製造壓力，誘導使用者交出帳密或驗證碼。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-003",
    "dataset_id": "T0002",
    "inputType": "text",
    "phishingType": "invoice_attachment",
    "title": "Payment confirmation required for overdue invoice - Final reminder 02",
    "text": "寄件者：Vendor Payments <vendor-pay.example.invalid>\n主旨：Payment confirmation required for overdue invoice - Final reminder 02\n\nAn updated billing statement is available. Open the attached document to prevent payment delays. This is a sanitized case with the attachment removed. Scenario variation 2: this case is framed for mobile browser and mentions action within 24 hours. It asks the recipient to open a file instead of viewing the invoice from a known vendor portal.",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "high",
      "confidence_score": 0.8799999999999999,
      "indicators": [
        "要求開啟附件",
        "使用急迫語氣",
        "invoice",
        "attached",
        "payment"
      ],
      "manipulation_methods": [
        "商務流程壓力",
        "附件誘導",
        "偽裝帳務通知"
      ],
      "personal_data_risk": "可能要求帳務、付款、公司或個人識別資料。",
      "payment_risk": "可能利用帳務壓力誘導付款或開啟惡意附件。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要開啟未預期的附件",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "用發票、帳單或付款文件誘導開啟附件，可能導致憑證竊取或惡意程式感染。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-004",
    "dataset_id": "T0005",
    "inputType": "text",
    "phishingType": "fake_prize",
    "title": "You have been selected for a customer bonus - Verification window open 03",
    "text": "寄件者：領獎服務中心 <claim-prize.example.invalid>\n主旨：You have been selected for a customer bonus - Verification window open 03\n\n您已符合抽獎活動資格，請立即填寫個人資料並支付手續費完成領獎。此為安全示範案例。 Scenario variation 3: this case is framed for school mailbox and mentions action before the end of the day. 內容以名額有限、最後通知或領獎期限誘導使用者快速提供資料。",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "high",
      "confidence_score": 0.8700000000000001,
      "indicators": [
        "包含連結或導向外部頁面",
        "使用急迫語氣",
        "winner",
        "claim",
        "processing fee"
      ],
      "manipulation_methods": [
        "中獎誘惑",
        "要求手續費",
        "製造名額或期限壓力"
      ],
      "personal_data_risk": "可能要求姓名、電話、地址、身分資料或其他領取 / 配送資訊。",
      "payment_risk": "可能要求小額手續費、信用卡資料、退款驗證或其他付款資訊。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "以中獎或獎勵為誘因，要求先支付手續費或提供個人與金融資料。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-005",
    "dataset_id": "T0004",
    "inputType": "text",
    "phishingType": "refund_or_payment",
    "title": "退款通知：請更新付款資料 - Security update required 04",
    "text": "寄件者：Refund Support <refund-service.example.invalid>\n主旨：退款通知：請更新付款資料 - Security update required 04\n\nA refund is pending but your payment method must be verified before it can be released. This sample removes the original link and uses a neutral sender. Scenario variation 4: this case is framed for business mailbox and mentions action this week. The message frames card verification as necessary to release a refund or keep a subscription active.",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "medium",
      "confidence_score": 0.81,
      "indicators": [
        "包含連結或導向外部頁面",
        "帶有時間壓力",
        "refund",
        "payment method",
        "card details"
      ],
      "manipulation_methods": [
        "退款誘因",
        "付款資料更新誘導",
        "服務中斷壓力"
      ],
      "personal_data_risk": "可能要求帳務、付款、公司或個人識別資料。",
      "payment_risk": "可能要求小額手續費、信用卡資料、退款驗證或其他付款資訊。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "假冒退款、訂閱或付款失敗通知，誘導更新信用卡或付款資料。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-006",
    "dataset_id": "T0013",
    "inputType": "text",
    "phishingType": "qr_phishing",
    "title": "Mailbox verification by QR code - Verification window open 03",
    "text": "寄件者：身分驗證通知 <qr-auth.example.invalid>\n主旨：Mailbox verification by QR code - Verification window open 03\n\n您的信箱需要重新驗證，請掃描信件中的 QR Code 完成登入。此為教學用安全改寫案例。 Scenario variation 3: this case is framed for school mailbox and mentions action before the end of the day. 信件要求掃描 QR Code 重新驗證，降低使用者檢查網址的機會。",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "high",
      "confidence_score": 0.8700000000000001,
      "indicators": [
        "包含連結或導向外部頁面",
        "使用急迫語氣",
        "QR code",
        "scan",
        "authentication"
      ],
      "manipulation_methods": [
        "QR Code 導流",
        "繞過網址檢查",
        "行動裝置驗證誘導"
      ],
      "personal_data_risk": "可能誘導使用者輸入帳號、密碼、MFA 驗證碼或信箱登入資訊。",
      "payment_risk": "目前付款風險不是主軸，但可能在後續假頁面中要求付款或金融資料。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要掃描信件中的不明 QR Code",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "將惡意連結藏在 QR code 中，繞過一般使用者對網址的檢查。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-007",
    "dataset_id": "T0015",
    "inputType": "text",
    "phishingType": "document_signing",
    "title": "Review and sign pending agreement - Security update required 11",
    "text": "寄件者：Secure Agreement <agreement-flow.example.invalid>\n主旨：Review and sign pending agreement - Security update required 11\n\nYou received a protected agreement. The message urges review through a button that is removed in this dataset. Scenario variation 11: this case is framed for 個人信箱 and mentions action 於今日內. It creates curiosity by claiming the agreement is confidential or time-sensitive.",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "high",
      "confidence_score": 0.94,
      "indicators": [
        "包含連結或導向外部頁面",
        "要求開啟附件",
        "使用急迫語氣",
        "document",
        "signature",
        "secure portal"
      ],
      "manipulation_methods": [
        "偽裝文件簽署",
        "機密文件誘惑",
        "期限壓力"
      ],
      "personal_data_risk": "可能誘導使用者輸入帳號、密碼、MFA 驗證碼或信箱登入資訊。",
      "payment_risk": "目前付款風險不是主軸，但可能在後續假頁面中要求付款或金融資料。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要開啟未預期的附件",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "假冒文件簽署或共享文件通知，誘導登入偽造文件入口。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-008",
    "dataset_id": "T0010",
    "inputType": "text",
    "phishingType": "legitimate_security_notice",
    "title": "Your password was changed successfully - 無需回覆 11",
    "text": "寄件者：IT Service Desk <it.example.edu>\n主旨：Your password was changed successfully - 無需回覆 11\n\nWe noticed a new sign-in and recommend reviewing activity from the official account settings page. No link or attachment is required in this training example. Scenario variation 11: this case is framed for 個人信箱 and mentions action 於今日內. 此通知沒有要求輸入帳密、付款、下載附件或掃描 QR Code。",
    "result": {
      "is_phishing": false,
      "label": "legitimate",
      "risk_level": "low",
      "confidence_score": 0.82,
      "indicators": [
        "official app",
        "no password request",
        "confirmation"
      ],
      "manipulation_methods": [
        "無明顯詐騙話術",
        "建議仍透過官方管道查證"
      ],
      "personal_data_risk": "目前未看到要求輸入帳號、密碼、驗證碼或身分資料的跡象。",
      "payment_risk": "目前沒有付款、退款、信用卡或轉帳要求。",
      "safe_actions": [
        "不要回覆任何帳密",
        "需要確認時自行開啟官方 App 或網站",
        "保留通知但不必透過信件捷徑操作"
      ],
      "explanation_for_general_users": "此案例用於正常信件對照：不要求輸入密碼、付款或下載附件，並建議使用者自行開啟官方管道確認。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-009",
    "dataset_id": "T0006",
    "inputType": "text",
    "phishingType": "legitimate_delivery_notice",
    "title": "Your order has shipped - 資訊通知 10",
    "text": "寄件者：Order Updates <orders.example.com>\n主旨：Your order has shipped - 資訊通知 10\n\nYour order has shipped. You can check delivery status by opening the official shopping app and reviewing your order page. This notice does not ask for payment or personal data. Scenario variation 10: this case is framed for business mailbox and mentions action this week. The safer path is to open the official app or manually type the official website address.",
    "result": {
      "is_phishing": false,
      "label": "legitimate",
      "risk_level": "low",
      "confidence_score": 0.82,
      "indicators": [
        "order shipped",
        "official app",
        "no extra fee"
      ],
      "manipulation_methods": [
        "無明顯詐騙話術",
        "建議仍透過官方管道查證"
      ],
      "personal_data_risk": "目前未看到要求輸入帳號、密碼、驗證碼或身分資料的跡象。",
      "payment_risk": "目前沒有付款、退款、信用卡或轉帳要求。",
      "safe_actions": [
        "不要回覆任何帳密",
        "需要確認時自行開啟官方 App 或網站",
        "保留通知但不必透過信件捷徑操作"
      ],
      "explanation_for_general_users": "此案例用於正常信件對照：不要求輸入密碼、付款或下載附件，並建議使用者自行開啟官方管道確認。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-010",
    "dataset_id": "T0001",
    "inputType": "text",
    "phishingType": "legitimate_it_maintenance",
    "title": "校園 IT 服務維護通知 - Official app notice 15",
    "text": "寄件者：校園 IT 服務 <it.example.edu.tw>\n主旨：校園 IT 服務維護通知 - Official app notice 15\n\n校園系統將於週五晚間進行維護，期間服務可能短暫中斷。本通知不要求點擊連結或輸入帳密。 Scenario variation 15: this case is framed for school mailbox and mentions action before the end of the day. 此通知沒有要求輸入帳密、付款、下載附件或掃描 QR Code。",
    "result": {
      "is_phishing": false,
      "label": "legitimate",
      "risk_level": "low",
      "confidence_score": 0.82,
      "indicators": [
        "maintenance",
        "no action required",
        "no login request"
      ],
      "manipulation_methods": [
        "無明顯詐騙話術",
        "建議仍透過官方管道查證"
      ],
      "personal_data_risk": "目前未看到要求輸入帳號、密碼、驗證碼或身分資料的跡象。",
      "payment_risk": "目前沒有付款、退款、信用卡或轉帳要求。",
      "safe_actions": [
        "不要回覆任何帳密",
        "需要確認時自行開啟官方 App 或網站",
        "保留通知但不必透過信件捷徑操作"
      ],
      "explanation_for_general_users": "此案例用於正常信件對照：不要求輸入密碼、付款或下載附件，並建議使用者自行開啟官方管道確認。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-011",
    "dataset_id": "T0008",
    "inputType": "text",
    "phishingType": "account_lock",
    "title": "帳號安全警示：請立即完成驗證 - Final reminder 09",
    "text": "寄件者：Account Security Center <secure-mail.example.invalid>\n主旨：帳號安全警示：請立即完成驗證 - Final reminder 09\n\n系統偵測到異常登入活動，請於今日內完成帳號驗證，以免服務被暫停。此為安全改寫範例，未保留任何真實連結。 Scenario variation 9: this case is framed for school mailbox and mentions action before the end of the day. 信件暗示若不立即操作，郵件或雲端服務會被限制使用。",
    "result": {
      "is_phishing": true,
      "label": "phishing",
      "risk_level": "high",
      "confidence_score": 0.8700000000000001,
      "indicators": [
        "包含連結或導向外部頁面",
        "使用急迫語氣",
        "account locked",
        "verify",
        "unusual sign-in"
      ],
      "manipulation_methods": [
        "製造帳號停用壓力",
        "冒充安全通知",
        "誘導登入驗證"
      ],
      "personal_data_risk": "可能誘導使用者輸入帳號、密碼、MFA 驗證碼或信箱登入資訊。",
      "payment_risk": "目前付款風險不是主軸，但可能在後續假頁面中要求付款或金融資料。",
      "safe_actions": [
        "不要點擊信件中的連結或按鈕",
        "不要回覆帳號、密碼、驗證碼或信用卡資料",
        "改從官方 App、官方網站或既有客服管道查證"
      ],
      "explanation_for_general_users": "利用帳號停用、異常登入或安全驗證製造壓力，誘導使用者交出帳密或驗證碼。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "sample-012",
    "dataset_id": "T0009",
    "inputType": "text",
    "phishingType": "legitimate_it_maintenance",
    "title": "Email service maintenance window - 無需回覆 11",
    "text": "寄件者：System Notification <system.example.edu>\n主旨：Email service maintenance window - 無需回覆 11\n\nA maintenance window is planned for the learning platform. Please save work before the window begins. This notice contains no login request. Scenario variation 11: this case is framed for 個人信箱 and mentions action 於今日內. 此通知沒有要求輸入帳密、付款、下載附件或掃描 QR Code。",
    "result": {
      "is_phishing": false,
      "label": "legitimate",
      "risk_level": "low",
      "confidence_score": 0.82,
      "indicators": [
        "maintenance",
        "no action required",
        "no login request"
      ],
      "manipulation_methods": [
        "無明顯詐騙話術",
        "建議仍透過官方管道查證"
      ],
      "personal_data_risk": "目前未看到要求輸入帳號、密碼、驗證碼或身分資料的跡象。",
      "payment_risk": "目前沒有付款、退款、信用卡或轉帳要求。",
      "safe_actions": [
        "不要回覆任何帳密",
        "需要確認時自行開啟官方 App 或網站",
        "保留通知但不必透過信件捷徑操作"
      ],
      "explanation_for_general_users": "此案例用於正常信件對照：不要求輸入密碼、付款或下載附件，並建議使用者自行開啟官方管道確認。",
      "model_source": "Rule-based prototype / dataset sample",
      "disclaimer": "目前為 prototype 分析，不代表正式資安判斷。重要操作請透過官方管道查證。"
    }
  },
  {
    "id": "image-demo-001",
    "inputType": "image",
    "phishingType": "image_mock",
    "title": "圖片上傳展示案例",
    "text": "圖片分析目前為展示功能，尚未串接 OCR 或多模態模型。",
    "result": {
      "is_phishing": true,
      "label": "suspicious",
      "risk_level": "medium",
      "confidence_score": 0.68,
      "indicators": [
        "圖片可能包含偽登入頁或付款提示",
        "需進一步 OCR 或多模態模型判讀",
        "來源與網址無法僅靠圖片確認"
      ],
      "manipulation_methods": [
        "冒充官方頁面",
        "製造急迫感",
        "誘導輸入資料"
      ],
      "personal_data_risk": "圖片可能誘導使用者輸入帳號、密碼、驗證碼或聯絡資料。",
      "payment_risk": "若圖片包含付款按鈕、QR Code 或信用卡欄位，需視為中高風險並改由官方管道確認。",
      "safe_actions": [
        "不要掃描不明 QR Code",
        "不要在圖片導向的不明頁面輸入資料",
        "改從官方 App 或網站查證"
      ],
      "explanation_for_general_users": "圖片功能目前只做展示，尚未讀取圖片文字，也沒有真正判斷頁面真假。",
      "model_source": "Image mock prototype",
      "disclaimer": "圖片分析目前為展示功能，尚未串接 OCR 或多模態模型。"
    }
  }
];
