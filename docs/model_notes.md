# 模型筆記

## 目前方向

B 先前已使用 LLaMA-Factory + LoRA 做過 phishing email detection，並使用 Hugging Face dataset `luongnv89/phishing-email` 作為模型方向參考。

本專案第一版以前端展示與資料格式整合為主，模型 API 尚未完成前，網站先使用 `web/mockData.js`。

## 實驗參考

- Experiment C 的 final eval loss 較低，但曾將正常 IT 維護通知誤判為 phishing。
- Experiment B 在測試案例中整體較穩定。
- 第一版 demo 與 API schema 可先以 Experiment B 的輸出形式為參考。

## 對資料的需求

模型需要高風險、低風險與中風險案例都有足夠代表性。尤其要補強：

- 正常 IT / school / system notification。
- 有密碼、帳戶、維護、通知等字眼但實際正常的訊息。
- 模糊、資訊不足、需要提醒但不能直接判定為詐騙的案例。

## 第一版模型輸出目標

模型或 mock response 應提供：

- is_phishing
- label
- risk_level
- confidence_score
- indicators
- manipulation_methods
- personal_data_risk
- payment_risk
- safe_actions
- explanation_for_general_users
- model_source
- disclaimer
