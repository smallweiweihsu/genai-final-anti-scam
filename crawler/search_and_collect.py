"""Collect source-informed phishing email dataset cases.

This project uses trusted public references to build sanitized, paraphrased
cases for education, model prototyping, and UI demos. It does not redistribute
raw malicious emails, live phishing URLs, private data, or copyrighted samples.

Run:
    python crawler/search_and_collect.py
"""

from __future__ import annotations

import json
import random
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "crawler" / "output"
RAW_CASES = OUT_DIR / "raw_cases.json"

TODAY = date.today().isoformat()
RANDOM = random.Random(20260601)


SOURCES = [
    {
        "name": "Microsoft Security - What is a phishing email",
        "url": "https://www.microsoft.com/en-us/security/business/security-101/what-is-phishing-email",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "Common phishing categories: fake invoices, security alerts, delivery, account verification.",
    },
    {
        "name": "Microsoft Support - A phish story",
        "url": "https://support.microsoft.com/en-US/security/a-phish-story",
        "source_type": "official_security_education",
        "trusted": True,
        "notes": "User-facing explanation of phishing indicators and safe behavior.",
    },
    {
        "name": "FTC - Fake shipping notification emails and text messages",
        "url": "https://consumer.ftc.gov/consumer-alerts/2023/12/fake-shipping-notification-emails-and-text-messages-what-you-need-know-holiday-season",
        "source_type": "government",
        "trusted": True,
        "notes": "Delivery scam patterns: missed delivery, reschedule links, fake look-alike pages.",
    },
    {
        "name": "FTC - Fake prize, sweepstakes, and lottery scams",
        "url": "https://consumer.ftc.gov/articles/fake-prize-sweepstakes-and-lottery-scams",
        "source_type": "government",
        "trusted": True,
        "notes": "Prize scams ask for fees, personal information, gift cards, or payment apps.",
    },
    {
        "name": "FTC - The FTC will not demand money, threaten you, or promise you a prize",
        "url": "https://consumer.ftc.gov/consumer-alerts/2023/07/ftc-wont-demand-money-threaten-you-or-promise-you-prize",
        "source_type": "government",
        "trusted": True,
        "notes": "Government impersonation red flags and real communication boundaries.",
    },
    {
        "name": "Kaspersky - Phishing email",
        "url": "https://usa.kaspersky.com/resource-center/preemptive-safety/phishing-email",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "Examples include account security alerts, refund notices, and delivery updates.",
    },
    {
        "name": "Trend Micro - Scam Emails",
        "url": "https://helpcenter.trendmicro.com/en-us/article/tmka-20565",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "General scam email signs and response guidance.",
    },
    {
        "name": "Fortinet FortiGuard Labs - Spoofed invoice used to drop IcedID",
        "url": "https://www.fortinet.com/blog/threat-research/spoofed-invoice-drops-iced-id",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "Invoice lure and attachment-based phishing pattern.",
    },
    {
        "name": "Cisco Talos - Hook, Line & Sinker",
        "url": "https://blogs.cisco.com/security/talos/hook-line-sinker",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "Financial credential phishing with HTML attachments and login pages.",
    },
    {
        "name": "OpenPhish Knowledge Base",
        "url": "https://www.openphish.com/kb.html",
        "source_type": "threat_intel",
        "trusted": True,
        "notes": "Threat intelligence context for phishing URLs and live phishing pages.",
    },
    {
        "name": "OpenPhish Global Phishing Activity",
        "url": "https://openphish.com/phishing_activity.html",
        "source_type": "threat_intel",
        "trusted": True,
        "notes": "Used as source context only; no live malicious URLs are stored in the dataset.",
    },
    {
        "name": "Cofense - QR code phishing attacks",
        "url": "https://cofense.com/knowledge-center-hub/email-security-resources/stop-qr-code-phishing-attacks",
        "source_type": "security_vendor",
        "trusted": True,
        "notes": "QR code phishing and credential-harvesting patterns.",
    },
    {
        "name": "Docusign - Brand impersonation whitepaper",
        "url": "https://www.docusign.com/sites/default/files/protecting_your_organization_against_docusign_brand_impersonation_whitepaper.pdf",
        "source_type": "official_security_education",
        "trusted": True,
        "notes": "Document-signing impersonation and business email lures.",
    },
    {
        "name": "NKUST Computer and Network Center - phishing mail notice",
        "url": "https://cc.nkust.edu.tw/p/404-1025-99907.php",
        "source_type": "taiwan_education",
        "trusted": True,
        "notes": "Taiwan university phishing alert about fake mail administration messages.",
    },
    {
        "name": "Feng Chia University IT - phishing notice",
        "url": "https://its.fcu.edu.tw/en/infosec/phishing-20241219",
        "source_type": "taiwan_education",
        "trusted": True,
        "notes": "Taiwan higher-education phishing notice about impersonation and suspicious links.",
    },
    {
        "name": "NTNU ITC - anti-phishing PDF",
        "url": "https://www.itc.ntnu.edu.tw/wp-content/uploads/2021/07/UP03_antiphishing.pdf",
        "source_type": "taiwan_education",
        "trusted": True,
        "notes": "Chinese anti-phishing teaching material with common subject patterns.",
    },
    {
        "name": "165 全民防騙網 Q&A - 普發現金詐騙",
        "url": "https://www.vac.gov.tw/vac_service/pingtung/cp-1616-189456-115.html",
        "source_type": "taiwan_government",
        "trusted": True,
        "notes": "165 guidance notes that fake government cash-payment emails and links may steal financial or card data.",
    },
    {
        "name": "交通部公路局 - 如何辨識詐騙釣魚簡訊",
        "url": "https://www.thb.gov.tw/news_content_table.aspx?n=7839&s=259930&sms=13275",
        "source_type": "taiwan_government",
        "trusted": True,
        "notes": "Taiwan government anti-phishing notice about suspicious links and personal/payment information.",
    },
    {
        "name": "陽信銀行 - 金融防詐中心",
        "url": "https://www.sunnybank.com.tw/net/Page/Smenu/387",
        "source_type": "bank_official",
        "trusted": True,
        "notes": "Bank anti-fraud page explaining phishing impersonation and sensitive information risks.",
    },
]


PHISHING_SCENARIOS = [
    {
        "phishing_type": "account_lock",
        "subjects": [
            "Action required: your account will be locked",
            "Security alert: unusual sign-in detected",
            "Confirm email access before suspension",
            "帳號安全警示：請立即完成驗證",
            "最後通知：信箱容量與登入權限即將受限",
        ],
        "senders": [
            ("Account Security Center", "secure-mail.example.invalid"),
            ("Mail Administrator", "mail-quota.example.invalid"),
            ("Microsoft 365 Support", "microsoft365-alert.example.invalid"),
            ("帳戶安全中心", "account-check.example.invalid"),
        ],
        "bodies": [
            "We detected a sign-in attempt from a new device. To prevent account suspension, review the activity within 24 hours using the secure verification page. This is a sanitized training sample; the original link has been removed.",
            "Your mailbox has exceeded the allowed storage limit. Messages may stop arriving unless you confirm your account ownership today. This demo email intentionally removes all active links.",
            "系統偵測到異常登入活動，請於今日內完成帳號驗證，以免服務被暫停。此為安全改寫範例，未保留任何真實連結。",
        ],
        "keywords": ["account locked", "verify", "unusual sign-in", "suspension", "立即驗證", "帳號停用"],
        "source_index": [0, 1, 5, 13, 15, 18],
    },
    {
        "phishing_type": "fake_delivery",
        "subjects": [
            "Missed delivery: update shipping details",
            "Package on hold pending address confirmation",
            "物流通知：包裹配送失敗需補件",
            "最後提醒：您的包裹將退回寄件人",
        ],
        "senders": [
            ("Delivery Notification Center", "delivery-update.example.invalid"),
            ("Parcel Service", "parcel-alert.example.invalid"),
            ("物流通知中心", "shipping-notice.example.invalid"),
        ],
        "bodies": [
            "A delivery attempt could not be completed because the shipping address requires confirmation. Please update the delivery preference before the package is returned. Safe sample: link removed.",
            "Your package is ready for redelivery, but a small handling fee must be confirmed first. This case is paraphrased from public safety guidance and does not include a real payment URL.",
            "您的包裹因地址資訊不完整暫停配送，請盡快更新收件資料並確認服務費。此案例為教學用改寫內容。",
        ],
        "keywords": ["missed delivery", "redelivery", "small fee", "shipping address", "包裹", "補繳運費"],
        "source_index": [2, 5, 17],
    },
    {
        "phishing_type": "invoice_attachment",
        "subjects": [
            "Invoice attached for immediate review",
            "Payment confirmation required for overdue invoice",
            "Updated billing document available",
            "發票與付款文件待確認",
        ],
        "senders": [
            ("Billing Department", "billing-docs.example.invalid"),
            ("Vendor Payments", "vendor-pay.example.invalid"),
            ("財務文件通知", "invoice-center.example.invalid"),
        ],
        "bodies": [
            "Please review the attached invoice and confirm payment status before the end of the business day. The original attachment pattern is represented here without including any file.",
            "An updated billing statement is available. Open the attached document to prevent payment delays. This is a sanitized case with the attachment removed.",
            "請確認附件中的付款文件，逾期可能影響帳務流程。此範例不包含真實附件。",
        ],
        "keywords": ["invoice", "attached", "payment", "overdue", "附件", "付款文件"],
        "source_index": [7, 8, 12],
    },
    {
        "phishing_type": "fake_prize",
        "subjects": [
            "Congratulations, your prize is waiting",
            "Final notice to claim your reward",
            "You have been selected for a customer bonus",
            "中獎通知：請完成領獎資料確認",
        ],
        "senders": [
            ("Prize Claim Office", "reward-center.example.invalid"),
            ("Customer Bonus Team", "bonus-gift.example.invalid"),
            ("領獎服務中心", "claim-prize.example.invalid"),
        ],
        "bodies": [
            "You have been selected to receive a prize. To release it, complete the claim form and pay a small processing fee. Training sample only; no real claim link is included.",
            "A reward has been reserved under your email address. Submit personal information today to avoid forfeiting the benefit. This message is paraphrased from public scam guidance.",
            "您已符合抽獎活動資格，請立即填寫個人資料並支付手續費完成領獎。此為安全示範案例。",
        ],
        "keywords": ["winner", "claim", "processing fee", "gift card", "中獎", "手續費"],
        "source_index": [3, 4, 16],
    },
    {
        "phishing_type": "refund_or_payment",
        "subjects": [
            "Refund pending: verify payment method",
            "Subscription renewal failed",
            "Confirm card details to receive refund",
            "退款通知：請更新付款資料",
        ],
        "senders": [
            ("Refund Support", "refund-service.example.invalid"),
            ("Subscription Billing", "renewal-billing.example.invalid"),
            ("退款服務中心", "refund-check.example.invalid"),
        ],
        "bodies": [
            "A refund is pending but your payment method must be verified before it can be released. This sample removes the original link and uses a neutral sender.",
            "Your subscription payment failed. Confirm your card details immediately to avoid account interruption. Safe dataset example; no payment page is included.",
            "您的退款申請已受理，請更新付款資料以完成退款流程。此為去品牌化、去連結的教學案例。",
        ],
        "keywords": ["refund", "payment method", "card details", "subscription", "退款", "付款資料"],
        "source_index": [0, 3, 5, 6, 16, 18],
    },
    {
        "phishing_type": "document_signing",
        "subjects": [
            "Document ready for signature",
            "Secure document shared with you",
            "Review and sign pending agreement",
            "文件簽署通知：請開啟安全文件",
        ],
        "senders": [
            ("Document Workflow", "document-sign.example.invalid"),
            ("Secure Agreement", "agreement-flow.example.invalid"),
            ("文件簽署系統", "sign-doc.example.invalid"),
        ],
        "bodies": [
            "A document has been shared with you for signature. Open the secure document portal and sign before it expires. This is a sanitized impersonation pattern.",
            "You received a protected agreement. The message urges review through a button that is removed in this dataset.",
            "您有一份待簽署文件，請於期限內開啟安全文件入口完成確認。此案例不包含真實文件或連結。",
        ],
        "keywords": ["document", "signature", "secure portal", "expires", "簽署", "安全文件"],
        "source_index": [11, 12],
    },
    {
        "phishing_type": "qr_phishing",
        "subjects": [
            "Scan QR code to restore account access",
            "New authentication required",
            "Mailbox verification by QR code",
            "請掃描 QR Code 完成帳號驗證",
        ],
        "senders": [
            ("Authentication Notice", "auth-update.example.invalid"),
            ("Mailbox Verification", "qr-verify.example.invalid"),
            ("身分驗證通知", "qr-auth.example.invalid"),
        ],
        "bodies": [
            "Your account requires re-authentication. Scan the QR code in the message to continue using the service. The QR image is not included in this safe text dataset.",
            "A new security policy requires mobile verification. Scan the displayed code before access expires. This sample describes the tactic without a live code.",
            "您的信箱需要重新驗證，請掃描信件中的 QR Code 完成登入。此為教學用安全改寫案例。",
        ],
        "keywords": ["QR code", "scan", "authentication", "verify", "掃描", "重新驗證"],
        "source_index": [10, 11],
    },
]


NORMAL_SCENARIOS = [
    {
        "phishing_type": "legitimate_security_notice",
        "subjects": [
            "Security notice: review recent account activity",
            "Your password was changed successfully",
            "帳號安全通知：密碼已成功更新",
        ],
        "senders": [
            ("Account Security", "account.example.com"),
            ("IT Service Desk", "it.example.edu"),
            ("帳戶安全中心", "security.example.com"),
        ],
        "bodies": [
            "This is a confirmation that your password was changed. If you did not make this change, visit the official app or type the official website address directly. This message does not request your password.",
            "We noticed a new sign-in and recommend reviewing activity from the official account settings page. No link or attachment is required in this training example.",
            "您的密碼已更新。若非本人操作，請自行開啟官方 App 或網站查看帳號活動。本通知不要求回覆帳密。",
        ],
        "keywords": ["official app", "no password request", "confirmation", "官方 App", "不要求回覆"],
        "source_index": [0, 1, 14, 15],
    },
    {
        "phishing_type": "legitimate_delivery_notice",
        "subjects": [
            "Your order has shipped",
            "Delivery scheduled for tomorrow",
            "訂單已出貨通知",
        ],
        "senders": [
            ("Order Updates", "orders.example.com"),
            ("Customer Service", "service.example-shop.com"),
            ("訂單通知", "orders.example.tw"),
        ],
        "bodies": [
            "Your order has shipped. You can check delivery status by opening the official shopping app and reviewing your order page. This notice does not ask for payment or personal data.",
            "Delivery is scheduled for tomorrow. If you need to change the time, sign in through the official website you normally use.",
            "您的訂單已出貨，請至原購物平台訂單頁查看配送狀態。本通知不要求補繳運費。",
        ],
        "keywords": ["order shipped", "official app", "no extra fee", "訂單", "不要求付款"],
        "source_index": [2],
    },
    {
        "phishing_type": "legitimate_it_maintenance",
        "subjects": [
            "Scheduled maintenance notice",
            "Email service maintenance window",
            "校園 IT 服務維護通知",
        ],
        "senders": [
            ("IT Service Desk", "it.example.edu"),
            ("System Notification", "system.example.edu"),
            ("校園 IT 服務", "it.example.edu.tw"),
        ],
        "bodies": [
            "Email services will undergo scheduled maintenance on Friday from 22:00 to 23:00. No user action is required.",
            "A maintenance window is planned for the learning platform. Please save work before the window begins. This notice contains no login request.",
            "校園系統將於週五晚間進行維護，期間服務可能短暫中斷。本通知不要求點擊連結或輸入帳密。",
        ],
        "keywords": ["maintenance", "no action required", "no login request", "維護", "不要求登入"],
        "source_index": [13, 14, 15],
    },
]


IMAGE_SCENARIOS = [
    ("fake_login_page", "偽登入頁面", "A screenshot-like mockup of a branded login page asks for email, password, and MFA code after a warning banner."),
    ("fake_payment_notice", "偽付款通知", "A payment notice mockup asks the recipient to pay a small handling fee to release a delivery or prize."),
    ("fake_delivery_page", "偽物流頁面", "A parcel tracking page mockup shows a failed delivery and a button to update address and payment details."),
    ("qr_phishing", "QR Code 釣魚", "A mail screenshot mockup asks the user to scan a QR code to restore mailbox access."),
    ("fake_document_portal", "偽文件簽署頁", "A document portal mockup asks the recipient to sign in to view a confidential agreement."),
    ("legitimate_notice_screenshot", "正常通知截圖", "A normal notification mockup tells users to open the official app without requesting data or payment."),
]


def fetch_source_metadata(source: dict) -> dict:
    metadata = dict(source)
    metadata["collected_date"] = TODAY
    try:
        request = urllib.request.Request(
            source["url"],
            headers={"User-Agent": "genai-final-anti-scam-dataset-builder/1.0"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read(180_000)
            text = data.decode("utf-8", errors="ignore")
            title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
            metadata["http_status"] = response.status
            metadata["page_title"] = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    except Exception as exc:  # Network may be unavailable in classroom environments.
        metadata["http_status"] = None
        metadata["page_title"] = ""
        metadata["fetch_error"] = str(exc)
    return metadata


def make_text_case(case_id: str, scenario: dict, risk_label: str, language: str, variant: int) -> dict:
    subject = scenario["subjects"][variant % len(scenario["subjects"])]
    sender_name, sender_domain = scenario["senders"][variant % len(scenario["senders"])]
    body = scenario["bodies"][variant % len(scenario["bodies"])]
    source = SOURCES[scenario["source_index"][variant % len(scenario["source_index"])]]
    has_attachment = scenario["phishing_type"] in {"invoice_attachment", "document_signing"} and risk_label != "normal"
    has_link = risk_label != "normal" and scenario["phishing_type"] != "invoice_attachment"
    urgency = "high" if risk_label == "phishing" and variant % 3 != 0 else "medium"
    if risk_label == "normal":
        urgency = "low"

    subject = add_subject_variation(subject, scenario["phishing_type"], risk_label, variant, language)
    body = add_body_variation(body, scenario["phishing_type"], risk_label, variant, language)

    return {
        "id": case_id,
        "email_subject": subject,
        "email_content": body,
        "sender": sender_name,
        "sender_domain": sender_domain,
        "has_link": str(has_link).lower(),
        "has_attachment": str(has_attachment).lower(),
        "urgency_level": urgency,
        "suspicious_keywords": ";".join(scenario["keywords"]),
        "phishing_type": scenario["phishing_type"],
        "risk_label": risk_label,
        "explanation": build_explanation(scenario["phishing_type"], risk_label),
        "source_url": source["url"],
        "source_type": source["source_type"],
        "language": language,
    }


def add_subject_variation(subject: str, phishing_type: str, risk_label: str, variant: int, language: str) -> str:
    if risk_label == "normal":
        suffixes = [
            "Reference only",
            "No action required",
            "Official app notice",
            "資訊通知",
            "無需回覆",
            "官方管道確認",
        ]
    else:
        suffixes = [
            "Case review needed",
            "Final reminder",
            "Verification window open",
            "Security update required",
            "請立即確認",
            "限時處理",
            "重新驗證通知",
        ]
    suffix = suffixes[variant % len(suffixes)]
    return f"{subject} - {suffix} {variant + 1:02d}"


def add_body_variation(body: str, phishing_type: str, risk_label: str, variant: int, language: str) -> str:
    phishing_details = {
        "account_lock": [
            "The message claims access will be limited unless the recipient confirms identity through a removed verification button.",
            "It references a new device, a different city, or mailbox storage pressure to create uncertainty.",
            "信件暗示若不立即操作，郵件或雲端服務會被限制使用。",
        ],
        "fake_delivery": [
            "The lure mentions redelivery, address correction, a customs-like handling fee, or a package being returned.",
            "It encourages the recipient to act before the end of the day instead of checking the official delivery app.",
            "內容以包裹退回、地址錯誤或補繳小額費用製造急迫感。",
        ],
        "invoice_attachment": [
            "The message uses business pressure by referencing an invoice number, late payment, or revised statement.",
            "It asks the recipient to open a file instead of viewing the invoice from a known vendor portal.",
            "信件利用財務流程與附件文件降低收件人的警覺。",
        ],
        "fake_prize": [
            "The message says a reward is reserved but asks for personal details or a fee before release.",
            "It may request gift cards, payment app transfers, or bank information in later steps.",
            "內容以名額有限、最後通知或領獎期限誘導使用者快速提供資料。",
        ],
        "refund_or_payment": [
            "The message frames card verification as necessary to release a refund or keep a subscription active.",
            "It mixes a positive benefit with a penalty, such as losing a refund or service interruption.",
            "信件以退款、續約失敗或付款資料更新引導使用者輸入金融資料。",
        ],
        "document_signing": [
            "The lure imitates a document workflow and asks the user to sign in before seeing the file.",
            "It creates curiosity by claiming the agreement is confidential or time-sensitive.",
            "內容假借合約、簽署或共享文件，誘導開啟偽造入口。",
        ],
        "qr_phishing": [
            "The message moves the risky destination into a QR code so the user cannot easily inspect the URL.",
            "It is designed for mobile scanning and may bypass desktop mail security cues.",
            "信件要求掃描 QR Code 重新驗證，降低使用者檢查網址的機會。",
        ],
    }
    normal_details = [
        "The notice does not ask the recipient to reply with credentials, pay fees, download files, or scan a QR code.",
        "The safer path is to open the official app or manually type the official website address.",
        "此通知沒有要求輸入帳密、付款、下載附件或掃描 QR Code。",
        "若使用者仍不確定，應透過既有官方管道查證，而不是使用信件中的捷徑。",
    ]
    time_windows = ["within 2 hours", "within 24 hours", "before the end of the day", "this week", "於今日內", "於本週內"]
    channels = ["email", "mobile browser", "school mailbox", "business mailbox", "個人信箱", "校園信箱"]
    detail_pool = normal_details if risk_label == "normal" else phishing_details.get(phishing_type, [])
    detail = detail_pool[variant % len(detail_pool)]
    timing = time_windows[variant % len(time_windows)]
    channel = channels[variant % len(channels)]
    return f"{body} Scenario variation {variant + 1}: this case is framed for {channel} and mentions action {timing}. {detail}"


def build_explanation(phishing_type: str, risk_label: str) -> str:
    if risk_label == "normal":
        return "此案例用於正常信件對照：不要求輸入密碼、付款或下載附件，並建議使用者自行開啟官方管道確認。"
    explanations = {
        "account_lock": "利用帳號停用、異常登入或安全驗證製造壓力，誘導使用者交出帳密或驗證碼。",
        "fake_delivery": "假冒物流或配送通知，要求更新地址、重新配送或支付小額費用。",
        "invoice_attachment": "用發票、帳單或付款文件誘導開啟附件，可能導致憑證竊取或惡意程式感染。",
        "fake_prize": "以中獎或獎勵為誘因，要求先支付手續費或提供個人與金融資料。",
        "refund_or_payment": "假冒退款、訂閱或付款失敗通知，誘導更新信用卡或付款資料。",
        "document_signing": "假冒文件簽署或共享文件通知，誘導登入偽造文件入口。",
        "qr_phishing": "將惡意連結藏在 QR code 中，繞過一般使用者對網址的檢查。",
    }
    return explanations.get(phishing_type, "可疑信件案例，需透過官方管道查證。")


def build_text_cases() -> list[dict]:
    cases: list[dict] = []
    counter = 1

    # 98 phishing/scam cases, balanced across seven major patterns.
    for scenario in PHISHING_SCENARIOS:
        for variant in range(14):
            language = "zh-TW" if variant % 4 in {1, 3} else "en"
            cases.append(make_text_case(f"T{counter:04d}", scenario, "phishing", language, variant))
            counter += 1

    # 48 normal cases to keep legitimate examples above 40% of first training use.
    for scenario in NORMAL_SCENARIOS:
        for variant in range(16):
            language = "zh-TW" if variant % 3 == 2 else "en"
            cases.append(make_text_case(f"T{counter:04d}", scenario, "normal", language, variant))
            counter += 1

    RANDOM.shuffle(cases)
    for index, item in enumerate(cases, start=1):
        item["id"] = f"T{index:04d}"
    return cases


def build_image_cases() -> list[dict]:
    image_cases: list[dict] = []
    for index in range(36):
        scenario_type, title, description = IMAGE_SCENARIOS[index % len(IMAGE_SCENARIOS)]
        source = SOURCES[[10, 11, 2, 8, 12, 13][index % 6]]
        risk_label = "normal" if scenario_type == "legitimate_notice_screenshot" else "phishing"
        image_cases.append(
            {
                "id": f"I{index + 1:04d}",
                "image_file": f"curated_images/{scenario_type}_{index + 1:02d}.png",
                "case_title": title,
                "image_case_type": scenario_type,
                "risk_label": risk_label,
                "description": description,
                "visual_risk_points": image_risk_points(scenario_type),
                "text_in_image": image_text(scenario_type),
                "source_url": source["url"],
                "source_type": source["source_type"],
                "license_note": "source-informed sanitized mock image case; no real screenshot redistributed",
                "can_be_public_demo": "true",
            }
        )
    return image_cases


def image_risk_points(scenario_type: str) -> str:
    points = {
        "fake_login_page": "偽登入表單;要求密碼;要求 MFA code;品牌仿冒",
        "fake_payment_notice": "小額付款;限時提示;付款按鈕;假客服資訊",
        "fake_delivery_page": "假物流追蹤;補件要求;地址更新;付款誘導",
        "qr_phishing": "QR code;重新驗證;繞過網址檢查;行動裝置導流",
        "fake_document_portal": "偽文件入口;要求登入;期限壓力;附件或按鈕導流",
        "legitimate_notice_screenshot": "正常通知;無付款要求;無帳密要求;指向官方 App",
    }
    return points[scenario_type]


def image_text(scenario_type: str) -> str:
    text = {
        "fake_login_page": "For your security, sign in again and enter the verification code.",
        "fake_payment_notice": "A small processing fee is required before your refund can be released.",
        "fake_delivery_page": "Delivery failed. Update address and redelivery payment within 24 hours.",
        "qr_phishing": "Scan this QR code to restore mailbox access.",
        "fake_document_portal": "A confidential document is waiting for your signature.",
        "legitimate_notice_screenshot": "Open the official app to review your notification. No action is required here.",
    }
    return text[scenario_type]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_metadata = [fetch_source_metadata(source) for source in SOURCES]
    payload = {
        "generated_at": TODAY,
        "dataset_policy": "sanitized_paraphrased_source_informed_cases",
        "sources": source_metadata,
        "text_cases": build_text_cases(),
        "image_cases": build_image_cases(),
    }
    RAW_CASES.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    from clean_dataset import main as clean_main

    return clean_main()


if __name__ == "__main__":
    sys.exit(main())
