# 專案規劃

## 專案名稱

看懂可疑信件：生成式 AI 輔助一般使用者辨識釣魚郵件的互動介面設計

## 第一版範圍

- 單頁網站。
- 文字貼上分析為主。
- 圖片上傳先做預覽與 mock 分析。
- 使用 mockData.js 模擬 B 的模型輸出。
- 資料集先建立範例格式，後續擴充到 100 筆與 300 筆。

## 階段規劃

### 第 1 階段：Repo 與格式建立

- 建立資料夾結構。
- 建立 README、docs、CSV 範例與 mockData.js。
- 確認欄位命名與 API response schema。

### 第 2 階段：100 筆文字案例

- 高風險 phishing / scam 約 50 筆。
- 正常 / 低風險約 40 筆。
- 中風險 / 模糊約 10 筆。
- 優先補足台灣常見情境與正常對照組。

### 第 3 階段：300 筆文字案例

- phishing email：70 筆。
- scam SMS / LINE：50 筆。
- fake delivery notification：30 筆。
- fake bank / account verification：30 筆。
- fake government payment / fine notice：30 筆。
- suspicious but ambiguous：30 筆。
- legitimate normal notification：60 筆。
- legitimate IT / school / system notification：30 筆。

### 第 4 階段：網站與展示整合

- C 使用 mockData.js 完成前端展示。
- B 對齊 API schema。
- A 補上 sources.md 與 demo 案例。
- 期末前固定展示版本，避免最後一週大改資料格式。

## 成功標準

- 網站可清楚展示風險分析流程。
- 資料格式一致，組員可共同維護。
- demo 案例不含真實個資與授權風險。
- 模型輸出與前端欄位可順利對接。
