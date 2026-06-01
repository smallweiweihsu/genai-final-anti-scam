# 資料蒐集與標註規範

## 核心原則

- 不要只蒐集明顯詐騙案例。
- 正常但看起來有點可疑的通知很重要。
- demo 案例優先自製，使用泛稱，不使用真實品牌 logo。
- 授權不明的來源只記錄，不重新散布原始內容。

## 文字案例比例

第一目標 100 筆：

- 高風險 phishing / scam：約 50 筆。
- 正常 / 低風險：約 40 筆。
- 中風險 / 模糊：約 10 筆。

期末建議 300 筆：

- phishing email：70 筆。
- scam SMS / LINE：50 筆。
- fake delivery notification：30 筆。
- fake bank / account verification：30 筆。
- fake government payment / fine notice：30 筆。
- suspicious but ambiguous：30 筆。
- legitimate normal notification：60 筆。
- legitimate IT / school / system notification：30 筆。

## 圖片案例比例

第一版建議 50 張即可：

- fake government / payment page：10 張。
- fake delivery notification screenshot：10 張。
- fake bank / account verification page：10 張。
- suspicious SMS / LINE screenshot：10 張。
- legitimate website / normal notification screenshot：10 張。

## text_cases.csv 欄位

```text
id,type,language,text,label,risk_level,risk_points,manipulation_methods,personal_data_risk,payment_risk,safe_action,source,license_note,can_be_public_demo
```

## image_cases.csv 欄位

```text
id,image_file,type,label,risk_level,visual_risk_points,text_in_image,personal_data_risk,payment_risk,source,license_note,can_be_public_demo
```

## 標籤值

label：

- phishing
- scam
- suspicious
- legitimate

risk_level：

- low
- medium
- high

type：

- phishing_email
- legitimate_email
- scam_sms
- line_message
- fake_delivery
- fake_bank
- fake_government
- fake_payment
- normal_notification
- school_it_notice
- ambiguous

## 安全限制

- 不打開真實可疑釣魚網站。
- 不點擊登入、付款、驗證、提交表單或下載附件按鈕。
- 不下載可疑附件。
- 不收集真實個資、信用卡、帳密、驗證碼。
- 不把真實品牌 logo 或授權不明圖片放入公開 demo。
