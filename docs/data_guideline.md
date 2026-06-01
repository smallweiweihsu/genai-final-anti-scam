# 資料蒐集與標註規範

## 目標

建立可供模型 prototype 與互動介面展示使用的釣魚郵件 / 可疑信件資料集。第一版資料以安全改寫案例為主，不直接散布真實釣魚信全文或活的惡意連結。

## 數量目標

第一版至少：

- phishing / scam email：80 筆以上。
- normal / legitimate email：40 筆以上。
- image cases：30 筆以上。
- 總數超過 150 筆。

目前 crawler 產生的第一版目標為：

- 文字案例 146 筆。
- 圖片案例 36 筆。
- 文字案例中 phishing 98 筆、normal 48 筆。

## text_cases.csv 欄位

```text
id,email_subject,email_content,sender,sender_domain,has_link,has_attachment,urgency_level,suspicious_keywords,phishing_type,risk_label,explanation,source_url,source_type
```

欄位說明：

- `id`：案例 ID。
- `email_subject`：信件主旨。
- `email_content`：信件內容，需為去識別化與安全改寫版本。
- `sender`：寄件者顯示名稱。
- `sender_domain`：寄件者網域，示範案例使用 `example.invalid` 或中性網域。
- `has_link`：是否包含連結誘導。
- `has_attachment`：是否包含附件誘導。
- `urgency_level`：`low`、`medium`、`high`。
- `suspicious_keywords`：可疑關鍵字，以分號分隔。
- `phishing_type`：釣魚類型。
- `risk_label`：`phishing`、`normal` 或 `suspicious`。
- `explanation`：給一般使用者看的白話說明。
- `source_url`：案例參考來源。
- `source_type`：來源類型。

## image_cases.csv 欄位

```text
id,image_file,case_title,image_case_type,risk_label,description,visual_risk_points,text_in_image,source_url,source_type,license_note,can_be_public_demo
```

## 建議類型

文字案例：

- `account_lock`
- `fake_delivery`
- `invoice_attachment`
- `fake_prize`
- `refund_or_payment`
- `document_signing`
- `qr_phishing`
- `legitimate_security_notice`
- `legitimate_delivery_notice`
- `legitimate_it_maintenance`

圖片案例：

- `fake_login_page`
- `fake_payment_notice`
- `fake_delivery_page`
- `qr_phishing`
- `fake_document_portal`
- `legitimate_notice_screenshot`

## 品質要求

- 去重複。
- 避免只有一句話的低品質資料。
- 保留英文與中文案例。
- 正常信件要足夠，避免模型把所有安全通知都判成 phishing。
- 來源授權不明時，只記錄來源，不重新散布原文。

## 安全限制

- 不打開真實可疑釣魚網站。
- 不點擊登入、付款、驗證、提交表單或下載附件按鈕。
- 不下載可疑附件。
- 不收集真實個資、信用卡、帳密、驗證碼。
- 不把真實品牌 logo 或授權不明圖片放入公開 demo。
