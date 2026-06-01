# Dataset

此資料夾存放「看懂可疑信件」專案的資料集輸出。

## 檔案

- `text_cases.csv`：可疑信件與正常信件文字案例。
- `image_cases.csv`：圖片型 phishing、偽登入頁、偽付款通知、QR code phishing 等圖片案例索引。
- `sources.md`：資料來源、URL、蒐集日期、可信度與備註。

## text_cases.csv 欄位

```text
id,email_subject,email_content,sender,sender_domain,has_link,has_attachment,urgency_level,suspicious_keywords,phishing_type,risk_label,explanation,source_url,source_type
```

## image_cases.csv 欄位

```text
id,image_file,case_title,image_case_type,risk_label,description,visual_risk_points,text_in_image,source_url,source_type,license_note,can_be_public_demo
```

## 重要說明

本資料集採用可信來源導向的安全改寫策略。案例內容不是直接複製真實釣魚信全文，也不保存活的惡意連結、真實個資、真實信用卡、真實驗證碼或可疑附件。

## 重新產生資料

從 repo 根目錄執行：

```bash
python crawler/search_and_collect.py
```

此指令會更新：

- `dataset/text_cases.csv`
- `dataset/image_cases.csv`
- `dataset/sources.md`
