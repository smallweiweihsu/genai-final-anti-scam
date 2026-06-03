# 專案接手文件

## 專案基本資訊

- 專案名稱：看懂可疑信件：生成式 AI 輔助一般使用者辨識釣魚郵件的互動介面設計
- GitHub Repo：https://github.com/smallweiweihsu/genai-final-anti-scam
- GitHub Pages：https://smallweiweihsu.github.io/genai-final-anti-scam/
- 目前分支：`main`
- 最新 commit 查詢：`git log -1 --oneline`
- 專案定位：期末專題展示網站、可疑信件 dataset、未來可串接模型 API 的互動式 prototype

## 目前專案狀態

目前專案已完成三個主要部分：

1. Dataset 初版
2. Web 互動展示 prototype
3. GitHub Pages 自動部署

目前線上網站可以正常開啟，部署來源是 repo 內的 `web/` 資料夾。每次 push 到 `main` 且修改 `web/**` 或 `.github/workflows/deploy-pages.yml` 時，GitHub Actions 會自動重新部署。

## 目前 Repo 結構

```text
genai-final-anti-scam/
├── .github/workflows/deploy-pages.yml
├── .gitignore
├── CHATGPT_COMPLETE_PROMPT.md
├── README.md
├── crawler/
│   ├── search_and_collect.py
│   ├── clean_dataset.py
│   └── export_csv.py
├── dataset/
│   ├── README.md
│   ├── text_cases.csv
│   ├── image_cases.csv
│   └── sources.md
├── docs/
│   ├── api_schema.md
│   ├── data_guideline.md
│   ├── dataset_quality_report.md
│   ├── model_notes.md
│   ├── project_plan.md
│   └── handoff.md
├── model/
│   └── README.md
├── presentation/
│   ├── demo_script.md
│   └── report_outline.md
├── scripts/
│   └── build_mock_data.py
└── web/
    ├── index.html
    ├── assets/
    │   ├── index-B3Xw4hRC.js
    │   └── index-BMOoP9BW.css
    ├── .htaccess
    ├── _redirects
    └── web.config
```

## 重要提醒：目前 Web 是已打包靜態版

目前 `web/` 不是完整 React 原始碼專案，而是 menusAi 產生後的打包結果：

- `web/index.html`
- `web/assets/index-B3Xw4hRC.js`
- `web/assets/index-BMOoP9BW.css`

也就是說，目前 repo 裡沒有 `package.json`、`src/`、`vite.config.*` 等可維護的 React source code。若未來要大幅修改 UI，有兩種路線：

1. 繼續直接修改打包後的 HTML / JS / CSS，但維護成本高。
2. 重建一份正式前端 source 專案，例如 `web-src/` 或 `app/`，用 Vite/React 開發後再 build 到 `web/`。

建議後續若時間允許，採用第 2 種方式，避免之後每次都要改 minified bundle。

## Dataset 目前狀態

目前 `dataset/text_cases.csv`：

- 總筆數：146
- phishing：98
- normal：48
- 欄位：
  - `id`
  - `email_subject`
  - `email_content`
  - `sender`
  - `sender_domain`
  - `has_link`
  - `has_attachment`
  - `urgency_level`
  - `suspicious_keywords`
  - `phishing_type`
  - `risk_label`
  - `explanation`
  - `source_url`
  - `source_type`

`phishing_type` 分布：

- `fake_delivery`：14
- `account_lock`：14
- `invoice_attachment`：14
- `fake_prize`：14
- `refund_or_payment`：14
- `qr_phishing`：14
- `document_signing`：14
- `legitimate_it_maintenance`：16
- `legitimate_delivery_notice`：16
- `legitimate_security_notice`：16

目前 `dataset/image_cases.csv`：

- 總筆數：36
- phishing：30
- normal：6
- 欄位：
  - `id`
  - `image_file`
  - `case_title`
  - `image_case_type`
  - `risk_label`
  - `description`
  - `visual_risk_points`
  - `text_in_image`
  - `source_url`
  - `source_type`
  - `license_note`
  - `can_be_public_demo`

注意：目前圖片案例主要是索引與描述，沒有大量圖片檔案上傳。

## 已完成的主要修改

### 1. 專案骨架與文件

已建立基本專案結構：

- `README.md`
- `.gitignore`
- `docs/`
- `dataset/`
- `crawler/`
- `scripts/`
- `model/`
- `presentation/`
- `web/`

也建立了資料規範、模型筆記、API schema、dataset 品質報告與展示腳本等文件。

### 2. Dataset 建立

已完成第一版文字與圖片案例資料：

- `dataset/text_cases.csv`
- `dataset/image_cases.csv`
- `dataset/sources.md`

資料策略：

- 以公開可信來源作為參考。
- 內容以安全改寫、教育展示與模型 prototype 為目的。
- 避免保存真實惡意連結、真實個資、真實附件或授權不明圖片。

### 3. Crawler / Dataset scripts

已建立：

- `crawler/search_and_collect.py`
- `crawler/clean_dataset.py`
- `crawler/export_csv.py`
- `scripts/build_mock_data.py`

其中 `crawler/output/` 會產生本機暫存資料，但已被 `.gitignore` 排除，不會上傳 GitHub。

### 4. Web Demo

目前 web demo 是 menusAi 產出的深色系互動式展示網站，主題為資安 / AI 輔助辨識釣魚信件。

目前功能包含：

- 首頁展示專題定位
- 風險預覽卡
- 可疑信件分析互動區
- 系統流程、介面設計、模型說明、資料集等 SPA 頁面
- 深色 Cyber-Security Prism 風格
- GitHub Pages 可正常部署

目前 web 版本為打包後的靜態 bundle，不是原始 React 專案。

### 5. GitHub Pages 部署

已建立 GitHub Actions workflow：

```text
.github/workflows/deploy-pages.yml
```

部署策略：

- push 到 `main`
- 若修改 `web/**` 或 workflow 檔案
- 自動上傳 `web/` 目錄
- 部署到 GitHub Pages

目前部署網址：

```text
https://smallweiweihsu.github.io/genai-final-anti-scam/
```

### 6. 修正 GitHub Pages 子路徑問題

menusAi 產生的版本原本使用：

```text
/assets/...
```

這會讓 GitHub Pages 在專案頁面中抓錯位置，變成：

```text
https://smallweiweihsu.github.io/assets/...
```

已修正為相對路徑與 repo base path：

```text
./assets/...
/genai-final-anti-scam/...
```

因此目前線上網站可正常開啟。

### 7. 移除 menusAi debug / analytics

已移除 menusAi 注入的追蹤與 debug 內容：

- `web/__manus__/debug-collector.js`
- `web/__manus__/version.json`
- `web/index.html` 中的 `debug-collector.js`
- `web/index.html` 中的 `manus-runtime`
- `web/index.html` 中的 `https://manus-analytics.com/umami`

移除後已驗證：

- 網站仍可正常渲染。
- 線上首頁不再包含 `manus`、`umami`、`analytics`、`debug-collector`。

## 技術決策紀錄

### Web 第一版採靜態部署

決策：使用 GitHub Pages 部署 `web/` 靜態網站。

原因：

- 期末展示需要穩定、快速開啟。
- 不需要後端伺服器即可展示。
- 適合目前 prototype 階段。

### 圖片功能先做 mock

決策：圖片上傳 / 圖片案例目前不串接 OCR 或多模態模型。

原因：

- 目前模型重點是 phishing email / 文字分類。
- 圖片模型或 OCR 會增加技術複雜度。
- 期末展示先用 mock 結果即可說明未來延伸方向。

### `risk_score` 與 `confidence_score` 分開

決策：API schema 與介面中將危險程度與模型信心拆開。

- `risk_score`：0-100，代表危險程度。
- `confidence_score`：0-1，代表模型或 prototype 對判斷結果的信心。

原因：

- 避免出現「低風險 82%」這種容易誤解的呈現。
- 一般使用者更容易理解風險與信心是兩件事。

### Dataset 採安全改寫

決策：不散布真實惡意內容，只保存安全改寫案例與來源紀錄。

原因：

- 避免散布真實釣魚連結。
- 避免真實個資與授權問題。
- 適合作為課堂展示與模型 prototype 資料。

### 不上傳模型檔與敏感檔案

`.gitignore` 已排除：

- `.env`
- `.env.*`
- `.pkl`
- `.joblib`
- `.pt`
- `.pth`
- `.bin`
- `.safetensors`
- `.gguf`
- `raw_images/`
- `raw_dataset/`
- `downloads/`
- `crawler/output/`
- `node_modules/`
- `__pycache__/`

已做過機密掃描，目前沒有發現 API key、`.env`、private key、GitHub token、OpenAI key、AWS key、Google API key、Slack token 或 JWT 被上傳。

## 目前待辦事項

### 高優先

1. 建立可維護的前端 source code

目前 `web/` 只有打包後的靜態檔。建議建立：

```text
web-src/
```

或：

```text
app/
```

內容包含：

- `package.json`
- `src/`
- `vite.config.*`
- React components
- Tailwind / CSS source

再將 build 結果輸出到 `web/`。

2. 修正文檔可讀性與編碼狀態

部分 Markdown 文件在終端輸出時出現亂碼或內容可讀性不佳，建議統一重新整理：

- `README.md`
- `docs/api_schema.md`
- `docs/model_notes.md`
- `docs/project_plan.md`

建議全部使用 UTF-8，並重新用繁體中文整理。

3. 檢查 menusAi bundle 內是否仍有不必要的開發資訊

目前已移除 `manus` 追蹤與 debug 腳本，但打包後 JS 仍保留部分 source file path 字串，例如 `/home/ubuntu/...`。這不算機密，但若要更正式，建議重新 build 一版乾淨 bundle。

### 中優先

4. 串接 B 組員模型 API

預計 API response 需符合 `docs/api_schema.md`：

```json
{
  "is_phishing": true,
  "label": "phishing",
  "risk_level": "high",
  "risk_score": 82,
  "confidence_score": 0.91,
  "indicators": [],
  "manipulation_methods": [],
  "personal_data_risk": "",
  "payment_risk": "",
  "safe_actions": [],
  "explanation_for_general_users": "",
  "model_source": "",
  "disclaimer": ""
}
```

接法建議：

- 前端輸入 email text。
- 呼叫 `/api/analyze-email` 或組員提供的 endpoint。
- 若 API 失敗，保留 rule-based / mock fallback。
- UI 明確標示 prototype 或 model API 模式。

5. 補強 dataset 品質

建議補：

- suspicious / medium risk 類別，目前主要是 phishing 與 normal。
- 更多中文案例。
- 更細緻的 sender domain 類型。
- 去重複與長度檢查自動化。

6. 圖片功能規劃

未來可選：

- OCR：先把截圖文字抽出，再送文字分類模型。
- Gemini / 多模態模型：直接分析截圖畫面。
- 自製 demo 圖片：避免授權與真實個資問題。

### 低優先

7. 更新 GitHub Actions Node 版本

GitHub Actions 曾出現 Node 20 deprecation warning，但目前部署成功，不影響網站。

之後可更新 actions 版本或設定 Node 24。

8. 加入自動檢查

可加入：

- secret scan
- CSV schema validation
- Pages link check
- HTML asset path check

## 常用指令

啟動本機靜態網站：

```bash
python -m http.server 5501 -d web
```

開啟：

```text
http://localhost:5501/
```

重新產生 dataset / mock data：

```bash
python scripts/build_mock_data.py
```

重新執行 crawler：

```bash
python crawler/search_and_collect.py
```

檢查 Git 狀態：

```bash
git status --short --branch
```

查看最近 commit：

```bash
git log --oneline -8
```

查看 GitHub Pages workflow：

```bash
gh run list --repo smallweiweihsu/genai-final-anti-scam --limit 5
```

## 交接建議

下一位接手者建議依照以下順序：

1. 先確認線上網站可開啟。
2. 閱讀本文件與 `dataset/README.md`。
3. 檢查 `dataset/text_cases.csv` 與 `dataset/image_cases.csv`。
4. 若只要展示，不要大改 `web/assets/index-B3Xw4hRC.js`。
5. 若要繼續開發 UI，先重建可維護的 React/Vite source 專案。
6. 若要串模型，先對齊 `docs/api_schema.md`，不要讓前端直接依賴模型內部格式。
7. 每次 push 前確認沒有 `.env`、API key、模型檔、raw dataset 或授權不明圖片。
