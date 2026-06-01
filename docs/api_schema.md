# API Schema

第一版前端會先使用 mockData.js。未來 B 的模型 API 建議回傳相同欄位，方便前端直接替換資料來源。

## Response 範例

```json
{
  "is_phishing": true,
  "label": "phishing",
  "risk_level": "high",
  "risk_score": 82,
  "confidence_score": 0.91,
  "indicators": [
    "急迫語氣",
    "要求登入",
    "可疑連結"
  ],
  "manipulation_methods": [
    "製造急迫感",
    "冒充權威"
  ],
  "personal_data_risk": "可能要求輸入帳號、密碼或驗證碼。",
  "payment_risk": "目前未直接要求付款，但可能導向假登入頁。",
  "safe_actions": [
    "不要點擊訊息中的連結",
    "改從官方網站或 App 登入",
    "聯絡官方客服確認"
  ],
  "explanation_for_general_users": "這類訊息會用時間壓力讓人急著操作，因此容易忽略網址與寄件者是否可信。",
  "model_source": "LoRA phishing email model / mock demo",
  "disclaimer": "此結果僅供輔助判斷，重要操作請透過官方管道查證。"
}
```

## 欄位說明

- `is_phishing`：是否偏向 phishing / scam。
- `label`：分類結果，可為 `phishing`、`scam`、`suspicious`、`legitimate`。
- `risk_level`：風險等級，可為 `low`、`medium`、`high`。
- `risk_score`：危險程度分數，0 到 100 的整數。此欄位用於風險進度條與危險程度呈現。
- `confidence_score`：0 到 1 之間的信心分數，表示模型或 prototype 對判斷結果的把握程度。
- `risk_score` 與 `confidence_score` 不能混用；前者代表危險程度，後者代表判斷信心。
- `indicators`：可疑特徵。
- `manipulation_methods`：詐騙或社交工程話術。
- `personal_data_risk`：個資風險說明。
- `payment_risk`：付款風險說明。
- `safe_actions`：安全建議。
- `explanation_for_general_users`：白話說明。
- `model_source`：模型或 mock 來源。
- `disclaimer`：免責聲明。
