# 資料來源紀錄

蒐集日期：2026-06-01

本資料集採用可信來源導向的安全改寫策略：不重新散布真實釣魚信全文、不保存活的惡意連結、不包含真實個資或真實登入資料。案例內容為依照來源中描述的攻擊型態進行去品牌化、去連結與改寫後的教學 / demo 資料。

## 來源清單

| 資料來源 | URL | 類型 | 是否可信 | HTTP 狀態 | 備註 | 文字案例數 | 圖片案例數 |
| --- | --- | --- | --- | --- | --- | ---: | ---: |
| Microsoft Security - What is a phishing email | https://www.microsoft.com/en-us/security/business/security-101/what-is-phishing-email | security_vendor | 是 | 200 | Common phishing categories: fake invoices, security alerts, delivery, account verification. | 10 | 0 |
| Microsoft Support - A phish story | https://support.microsoft.com/en-US/security/a-phish-story | official_security_education | 是 | 未取得 | User-facing explanation of phishing indicators and safe behavior. | 7 | 0 |
| FTC - Fake shipping notification emails and text messages | https://consumer.ftc.gov/consumer-alerts/2023/12/fake-shipping-notification-emails-and-text-messages-what-you-need-know-holiday-season | government | 是 | 200 | Delivery scam patterns: missed delivery, reschedule links, fake look-alike pages. | 21 | 6 |
| FTC - Fake prize, sweepstakes, and lottery scams | https://consumer.ftc.gov/articles/fake-prize-sweepstakes-and-lottery-scams | government | 是 | 200 | Prize scams ask for fees, personal information, gift cards, or payment apps. | 8 | 0 |
| FTC - The FTC will not demand money, threaten you, or promise you a prize | https://consumer.ftc.gov/consumer-alerts/2023/07/ftc-wont-demand-money-threaten-you-or-promise-you-prize | government | 是 | 200 | Government impersonation red flags and real communication boundaries. | 5 | 0 |
| Kaspersky - Phishing email | https://usa.kaspersky.com/resource-center/preemptive-safety/phishing-email | security_vendor | 是 | 200 | Examples include account security alerts, refund notices, and delivery updates. | 9 | 0 |
| Trend Micro - Scam Emails | https://helpcenter.trendmicro.com/en-us/article/tmka-20565 | security_vendor | 是 | 200 | General scam email signs and response guidance. | 2 | 0 |
| Fortinet FortiGuard Labs - Spoofed invoice used to drop IcedID | https://www.fortinet.com/blog/threat-research/spoofed-invoice-drops-iced-id | security_vendor | 是 | 200 | Invoice lure and attachment-based phishing pattern. | 5 | 0 |
| Cisco Talos - Hook, Line & Sinker | https://blogs.cisco.com/security/talos/hook-line-sinker | security_vendor | 是 | 未取得 | Financial credential phishing with HTML attachments and login pages. | 5 | 6 |
| OpenPhish Knowledge Base | https://www.openphish.com/kb.html | threat_intel | 是 | 200 | Threat intelligence context for phishing URLs and live phishing pages. | 0 | 0 |
| OpenPhish Global Phishing Activity | https://openphish.com/phishing_activity.html | threat_intel | 是 | 200 | Used as source context only; no live malicious URLs are stored in the dataset. | 7 | 6 |
| Cofense - QR code phishing attacks | https://cofense.com/knowledge-center-hub/email-security-resources/stop-qr-code-phishing-attacks | security_vendor | 是 | 200 | QR code phishing and credential-harvesting patterns. | 14 | 6 |
| Docusign - Brand impersonation whitepaper | https://www.docusign.com/sites/default/files/protecting_your_organization_against_docusign_brand_impersonation_whitepaper.pdf | official_security_education | 是 | 200 | Document-signing impersonation and business email lures. | 11 | 6 |
| NKUST Computer and Network Center - phishing mail notice | https://cc.nkust.edu.tw/p/404-1025-99907.php | taiwan_education | 是 | 未取得 | Taiwan university phishing alert about fake mail administration messages. | 8 | 6 |
| Feng Chia University IT - phishing notice | https://its.fcu.edu.tw/en/infosec/phishing-20241219 | taiwan_education | 是 | 未取得 | Taiwan higher-education phishing notice about impersonation and suspicious links. | 9 | 0 |
| NTNU ITC - anti-phishing PDF | https://www.itc.ntnu.edu.tw/wp-content/uploads/2021/07/UP03_antiphishing.pdf | taiwan_education | 是 | 200 | Chinese anti-phishing teaching material with common subject patterns. | 11 | 0 |
| 165 全民防騙網 Q&A - 普發現金詐騙 | https://www.vac.gov.tw/vac_service/pingtung/cp-1616-189456-115.html | taiwan_government | 是 | 未取得 | 165 guidance notes that fake government cash-payment emails and links may steal financial or card data. | 6 | 0 |
| 交通部公路局 - 如何辨識詐騙釣魚簡訊 | https://www.thb.gov.tw/news_content_table.aspx?n=7839&s=259930&sms=13275 | taiwan_government | 是 | 200 | Taiwan government anti-phishing notice about suspicious links and personal/payment information. | 4 | 0 |
| 陽信銀行 - 金融防詐中心 | https://www.sunnybank.com.tw/net/Page/Smenu/387 | bank_official | 是 | 200 | Bank anti-fraud page explaining phishing impersonation and sensitive information risks. | 4 | 0 |

## 使用限制

- 可用於期末專案、模型 prototype、介面展示與教育用途。
- 不應將此資料集視為原始威脅情資或可執法證據。
- 不得加入 API key、真實個資、真實信用卡、真實驗證碼、真實釣魚頁內容或可疑附件。
- 若後續新增外部原文案例，必須先確認授權，授權不明者只記錄來源，不重新散布內容。
