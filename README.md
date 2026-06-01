# 看懂可疑信件：生成式 AI 輔助一般使用者辨識釣魚郵件的互動介面設計

本專案是一個期末專題用的互動式介面與資料集建置專案，目標是協助一般使用者看懂可疑信件，理解釣魚郵件常見特徵、詐騙話術、個資風險與安全處理方式。

第一版以「文字型 phishing / scam email 分析」為主，圖片案例先整理為展示與未來多模態延伸資料。前端 demo 可先讀取 `web/mockData.js`，模型 API 完成後再依照 `docs/api_schema.md` 對接。

## 專案目標

- 建立可供模型與介面展示使用的可疑信件 dataset。
- 協助使用者辨識帳號鎖定、假物流、假銀行、假驗證、假退款、假中獎、假文件簽署等釣魚情境。
- 將模型輸出轉換成一般使用者能理解的繁體中文說明。
- 建立可重跑的資料蒐集、清理與匯出流程。

## Repo 結構

```text
genai-final-anti-scam/
├── README.md
├── .gitignore
├── crawler/
│   ├── search_and_collect.py
│   ├── clean_dataset.py
│   └── export_csv.py
├── docs/
├── web/
├── dataset/
├── model/
└── presentation/
```

## 網站頁面結構

- `web/index.html`：分析 Demo，老師打開後可直接操作。
- `web/workflow.html`：系統流程頁，說明使用者輸入、模型判斷、白話解釋與安全行動。
- `web/interface.html`：介面設計頁，說明如何把模型輸出轉成 tags、checklist 與白話解釋。
- `web/model.html`：模型說明頁，整理任務、API 輸出與評估指標。
- `web/dataset.html`：資料集頁，說明資料數量、來源與安全策略。

網站採白底學術展示風格，使用深綠 / 墨綠作為主色，導覽列、卡片與按鈕都有平滑 hover interaction。

## Dataset

主要輸出位於 `dataset/`：

- `text_cases.csv`：信件文字案例。
- `image_cases.csv`：圖片型 phishing / 偽登入頁 / 偽付款通知等案例索引。
- `sources.md`：資料來源、蒐集日期、可信度與備註。

CSV 採 UTF-8 with BOM，方便 Excel 開啟繁體中文。

## 目前功能

- 從 `dataset/text_cases.csv` 產生可展示的 `web/mockData.js`。
- 提供 10-12 筆代表性範例案例，包含假物流、帳號鎖定、附件發票、中獎、退款、QR phishing、文件簽署與正常通知。
- 使用者可貼上一封信件，透過 rule-based prototype analyzer 取得分析結果。
- 顯示總體風險、是否疑似釣魚、可疑特徵、詐騙話術、個資風險、付款風險、安全行動與白話說明。
- 圖片上傳目前提供預覽與 mock 分析結果。

## Web Demo 介面功能

- 文字 / 圖片雙模式輸入：使用 tab 在「文字信件」與「圖片截圖」之間切換，避免兩種輸入同時攤開。
- 範例案例載入：可使用下拉選單或快速範例按鈕載入 dataset 代表案例。
- 使用者自訂信件分析：可貼上任意 Email 主旨、寄件者與內文進行 prototype 分析。
- Rule-based prototype analyzer：使用關鍵字、急迫語氣、登入要求、付款要求、附件與 QR code 等規則進行展示用判斷。
- 風險分數視覺化：以進度條與高 / 中 / 低風險樣式呈現 `risk_score`。
- 判斷信心顯示：另外呈現 `confidence_score`，避免把模型信心誤解成危險程度。
- 可疑特徵與詐騙話術標籤：用 tag 呈現 indicators 與 manipulation_methods，讓一般使用者更容易掃讀。
- 安全行動 checklist：把 safe_actions 轉成 checklist 樣式，方便展示可執行建議。
- 圖片上傳 mock 展示：可預覽圖片，按下分析圖片後顯示展示用結果。
- 圖片功能目前為 mock 展示，未來可串接 OCR / 多模態模型讀取截圖文字與畫面特徵。

## risk_score 與 confidence_score

- `risk_score`：危險程度分數，0-100 整數，用於風險進度條。
- `confidence_score`：模型或 prototype 對判斷結果的信心，0-1 小數。
- 兩者不能混用；例如「低風險、判斷信心 82%」代表系統有把握這是低風險，不代表危險程度是 82%。

## 展示建議順序

1. 打開分析 Demo，先載入「假物流」或「帳號鎖定」快速範例。
2. 說明風險等級、risk_score 與 confidence_score 的差異。
3. 展示可疑特徵 tags、詐騙話術 tags 與安全行動 checklist。
4. 切到圖片截圖 tab，說明目前為 mock 展示，未來可串接 OCR / 多模態模型。
5. 依序查看系統流程、介面設計、模型說明與資料集頁。

## 如何執行 Web Demo

從 repo 根目錄啟動靜態伺服器：

```bash
python -m http.server 5501 -d web
```

接著開啟：

```text
http://localhost:5501/
```

若要重新從 dataset 產生前端範例資料：

```bash
python scripts/build_mock_data.py
```

此指令會更新：

- `docs/dataset_quality_report.md`
- `web/mockData.js`

## Crawler

重新產生 dataset：

```bash
python crawler/search_and_collect.py
```

流程：

1. `search_and_collect.py`：根據可信來源建立來源導向的安全改寫案例。
2. `clean_dataset.py`：清理欄位、去重複、過濾低品質案例。
3. `export_csv.py`：輸出 `dataset/text_cases.csv`、`dataset/image_cases.csv`、`dataset/sources.md`。

重新產生 dataset 後，請再執行：

```bash
python scripts/build_mock_data.py
```

讓前端展示案例同步更新。

## 目前限制

- `web/analyzer.js` 是 rule-based prototype，不是正式模型。
- 分析結果只供期末展示與介面測試，不代表正式資安判斷。
- 圖片分析目前尚未串接 OCR 或多模態模型，只做預覽與 mock 結果。
- Dataset 是可信來源導向的安全改寫案例，不是原始威脅情資。

## 後續串接模型 API

前端目前的分析入口在 `web/script.js`。之後可將 `analyzeEmail(messageInput.value)` 替換成 API 呼叫，例如：

```js
const response = await fetch("/api/analyze-email", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: messageInput.value })
});
const result = await response.json();
renderResult(result);
```

模型 API 只要回傳符合 `docs/api_schema.md` 的欄位，即可直接沿用目前的結果呈現區。

## 資料安全策略

本專案不直接散布真實釣魚信全文、不保存活的惡意連結、不收集真實個資、不下載可疑附件。資料集內容是依照可信來源描述的攻擊型態進行去品牌化、去連結、去識別化與安全改寫後的教學 / demo 案例。

## 不應上傳

- API key
- `.env`
- 大型模型檔
- `.pkl` / `.pt` / `.safetensors` / `.bin` / `.gguf`
- 大量 raw images
- 授權不明圖片
- 真實個資截圖
- 真實釣魚網站內容
- 可疑附件

## 免責聲明

本專案輸出僅供教學展示、模型 prototype 與輔助判斷，不應作為資安、法律或金融決策的唯一依據。重要操作請透過官方管道查證。
