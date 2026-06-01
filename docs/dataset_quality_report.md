# Dataset Quality Report

產生日期：2026-06-01

## 總覽

- 文字案例總筆數：146
- risk_label 類別數：2
- phishing_type 類別數：10

## risk_label 分布

| risk_label | 筆數 |
| --- | ---: |
| normal | 48 |
| phishing | 98 |

## phishing_type 分布

| phishing_type | 筆數 |
| --- | ---: |
| legitimate_it_maintenance | 16 |
| legitimate_delivery_notice | 16 |
| legitimate_security_notice | 16 |
| invoice_attachment | 14 |
| account_lock | 14 |
| refund_or_payment | 14 |
| fake_prize | 14 |
| qr_phishing | 14 |
| document_signing | 14 |
| fake_delivery | 14 |

## source_type 分布

| source_type | 筆數 |
| --- | ---: |
| security_vendor | 45 |
| government | 34 |
| taiwan_education | 28 |
| official_security_education | 18 |
| taiwan_government | 10 |
| threat_intel | 7 |
| bank_official | 4 |

## 重複檢查

- 重複 email_subject 數量：0
- 重複 email_content 數量：0

## 空欄位檢查

- 未發現必要欄位空值。

## 品質結論

- 已涵蓋 phishing 與 normal 類別，適合第一版互動介面展示。
- 目前沒有直接保存活的惡意連結或真實個資。
- 後續可補強 BEC / CEO fraud、求職詐騙、更多台灣銀行官方防詐來源與實際 demo 圖片素材。
