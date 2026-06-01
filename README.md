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

## Dataset

主要輸出位於 `dataset/`：

- `text_cases.csv`：信件文字案例。
- `image_cases.csv`：圖片型 phishing / 偽登入頁 / 偽付款通知等案例索引。
- `sources.md`：資料來源、蒐集日期、可信度與備註。

CSV 採 UTF-8 with BOM，方便 Excel 開啟繁體中文。

## Crawler

重新產生 dataset：

```bash
python crawler/search_and_collect.py
```

流程：

1. `search_and_collect.py`：根據可信來源建立來源導向的安全改寫案例。
2. `clean_dataset.py`：清理欄位、去重複、過濾低品質案例。
3. `export_csv.py`：輸出 `dataset/text_cases.csv`、`dataset/image_cases.csv`、`dataset/sources.md`。

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
